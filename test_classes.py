#Purpose: Library for representing Shifts, Shifttypes, Days, Weeks in order to generate schedules

from datetime import datetime
from datetime import timedelta
from scipy import stats             #for percentile functions
import random
from numpy.random import choice

class Shift:

    #TODO: Ensure that all shifts abide by a given shift_buffer --> e.g have valid times
    def __init__(self, label, start_time, end_time, is_work, is_shifttype, note = ""):
        self.label = label
        self.start_time = start_time
        self.end_time = end_time
        self.note = note
        self.is_work = is_work
        self.is_shifttype = is_shifttype

    def get_starttime_str(self):
        return self.start_time.strftime('%I:%M%p')

    def get_endtime_str(self):
        return self.end_time.strftime('%I:%M%p')


class ShiftType:

    def __init__(self, label, hrs_req, limit_day, note = ""):
        self.label = label
        self.hrs_req = hrs_req
        self.limit_day = limit_day
        self.note = note
        self.schedule = {}


class Day:

    #sched_shifts = List of Shift objs representing already scheduled things this week
    #day_dt = datetime obj that this Day obj is supposed to represent e.g. 10/20/22
    def __init__(self, label, sched_shifts, unavailability, limit_hrs, shift_buffer):

        self.shifts = {}
        self.shifttypes = {}
        self.shift_hrs = 0
        self.limit_hrs_hit = False
        self.label = label
        self.limit_hrs = limit_hrs
        self.shift_buffer = shift_buffer
        self.unavailable = unavailability

        self.max_possible_work_duration = 0
        self.total_poss_shift_durations = 0
        self.avail_range = {}
        self.nonwork_avail_range = {}
        self.init_avail_range()


        #Populate the shifts now that nonwork_avail_range is also init with avail_range:
        for shift in sched_shifts:
              self.sched_shift(shift)

        self.update_max_poss_duration()

    def init_avail_range(self):
        start_time_str = self.label + " 12:00am"
        time_counter = datetime.strptime(start_time_str, '%m/%d/%y %I:%M%p')
        next_day = datetime.strptime(self.label, '%m/%d/%y') + timedelta(days=1)

        while time_counter < next_day:         #while time_counter hasn't met with or surpassed onto the next day
            if self.intersects_unavailable(time_counter):
                self.nonwork_avail_range[time_counter.strftime('%I:%M%p')] = True

            else:
                self.avail_range[time_counter.strftime('%I:%M%p')] = True

            time_counter = time_counter + timedelta(minutes=self.shift_buffer)       #add buffer minutes to it


    def intersects_unavailable(self, time):
        for tuple in self.unavailable:
            start_time = tuple[0]
            end_time = tuple[1]
            if time >= start_time and time <= end_time:
                return True

        return False


    def sched_shift(self, shift):
        #add shift to the shifts field, assuming all added shifts are already validated --> there will not be another shift with the same start_time
        self.shifts[shift.get_starttime_str()] = shift

        #if the shift is for a shifttype --> look to see if a shiftype key exists already for this Day, yes --> add shift to the list of Shift values, no --> create and add new list of Shift values
        if shift.is_shifttype:
            if shift.label in self.shifttypes:
                shifttype_shifts = self.shifttypes.get(shift.label)
                shifttype_shifts.append(shift)

            else:
                self.shifttypes[shift.label] = [shift]


        #adjust avail_range/nonwork_avail_range to each shift:
        intersects = (shift.is_work is False) and (self.intersects_unavailable(shift.start_time) or self.intersects_unavailable(shift.end_time))

        #assuming Shift will always have exact times according shift_buffer:
        time_counter = shift.start_time

        while time_counter <= shift.end_time:       #deletes all avail times from start_time --> end_time
            time_counter_str = time_counter.strftime('%I:%M%p')

            if time_counter_str in self.avail_range:
                del self.avail_range[time_counter.strftime('%I:%M%p')]

            if intersects and (time_counter_str in self.nonwork_avail_range):
                del self.nonwork_avail_range[time_counter.strftime('%I:%M%p')]

            time_counter = time_counter + timedelta(minutes=self.shift_buffer)

        #update total amount of shift_hrs:
        if shift.is_work:
            duration = shift.end_time - shift.start_time
            duration_whole_hrs = duration.seconds//3600
            duration_min = (duration.seconds//60)%60
            self.shift_hrs = self.shift_hrs + (duration_whole_hrs + (duration_min/60))

        #Check if we already hit the max amount of hrs can work:
        if self.shift_hrs >= self.limit_hrs:
            self.limit_hrs_hit = True

        #Update self.self.max_possible_work_duration and self.total_poss_shift_durations:
        self.update_max_poss_duration()


    #no error handling done --> TODO
    #Issue, now that unavailability and nonwork can intersect --> it overrides the Shift value at the same key (starttime), --> make value = List of Shifts??
    #       --> at this point might as well just not save Unavailability as a Shift obj anymore
    def remove_shift(self, starttime_str):
        #Check if shift even exists;
        if starttime_str in self.shifts:
            del_shift = self.shifts.get(starttime_str)
            del self.shifts[starttime_str]          #take out of shifts{}

            if del_shift.is_shifttype:              #take out of shifttypes{}
                del self.shifttypes[del_shift.label]

            #assuming Shift will always have exact times according shift_buffer:
            intersects = (del_shift.is_work is False) and (self.intersects_unavailable(del_shift.start_time) or self.intersects_unavailable(del_shift.end_time))

            time_counter = del_shift.start_time

            while time_counter <= del_shift.end_time:       #create all consecutive avail times from start_time --> end_time
                if intersects and self.intersects_unavailable(time_counter):
                    self.nonwork_avail_range[time_counter.strftime('%I:%M%p')] = True

                else:
                    self.avail_range[time_counter.strftime('%I:%M%p')] = True

                time_counter = time_counter + timedelta(minutes=self.shift_buffer)

            if del_shift.is_work:
                duration = del_shift.end_time - del_shift.start_time
                duration_whole_hrs = duration.seconds//3600
                duration_min = (duration.seconds//60)%60
                self.shift_hrs = self.shift_hrs - (duration_whole_hrs + (duration_min/60))

            #Check if we need to change limit_hrs_hit
            if self.limit_hrs_hit is True and self.shift_hrs < self.limit_hrs:
                self.limit_hrs_hit = False

            #Update self.self.max_possible_work_duration and self.total_poss_shift_durations:
            self.update_max_poss_duration()

    #Purpose: Works with choose_random_time(), validates whether a given duration from start_time to end_time is avail in self.avail_range
    def is_avail(self, is_work, start_time, end_time):
        time_counter = start_time
        all_times = list(self.avail_range.keys())

        #If shift is non-work --> able to schedule during nonworking hours (includes unavailability times):
        if is_work is False:
            all_times.extend(list(self.nonwork_avail_range.keys()))

        #just check if each time string exists as a key in the avail_range list of keys, if not --> there must be some time thats needed that is unavail
        while time_counter <= end_time:
            if time_counter.strftime('%I:%M%p') not in all_times:
                return False
            time_counter = time_counter + timedelta(minutes=self.shift_buffer)

        return True


    #Purpose: Pick a random available time of day for a Shift given the desired duration (in hrs), and random choosing size (how many random times to generate and chosse from)
    #assume the shift is ONLY for work shifts, this method would only be used for scheduling
    def choose_random_time(self, choosing_size, duration_hrs):
        #avail_range already has every available time --> get them and choose by random:
        avail_hrs = list(self.avail_range.keys())
        choosing_range = []

        #Populate choosing_range with random VALID times until its size == choosing_size:
        while len(choosing_range) < choosing_size and len(avail_hrs) >= 1:
            #still assuming self.label will == format '%m/%d/%y'
            start_time_str = random.choice(avail_hrs)
            start_time = datetime.strptime((self.label + " " + start_time_str), '%m/%d/%y %I:%M%p')
            end_time = start_time + timedelta(hours=duration_hrs)

            #is it valid? yes --> add it to the choosing_range!
            if self.is_avail(True, start_time, end_time):
                choosing_range.append(start_time)

            avail_hrs.remove(start_time_str)

        if len(choosing_range) > 0:
            return random.choice(choosing_range)
        else:
            return None             #whoever calls this method should be error checking for this

    #Purpose:   Find the max duration a work shift can be today --> returns [max duration, sum of durations for today]
    #TODO:  Maybe just make a self.max_duration_possible and self.total_durations --> run this method everytime a Shift is scheduled/removed to update fields --> avoid having to ever traverse from outside the class.
    def update_max_poss_duration(self):
        #Traverse avail_range only since only care for work shifts not non-work
        total_durations = 0
        max_duration = 0

        avail_hrs = list(self.avail_range.keys())

        while len(avail_hrs) >= 1:
            time_counter = datetime.strptime((self.label + " " + avail_hrs[0]), '%m/%d/%y %I:%M%p') + timedelta(minutes=self.shift_buffer)
            avail_hrs.remove(avail_hrs[0])
            current_duration = 0

            #if the expected time exists --> can remove it from the list, increment counters
            while len(avail_hrs) >= 1 and time_counter.strftime('%I:%M%p') in avail_hrs:
                avail_hrs.remove(time_counter.strftime('%I:%M%p'))
                current_duration = current_duration + self.shift_buffer/60  #/60 to convert shift_buffer to hrs
                time_counter = time_counter + timedelta(minutes=self.shift_buffer)

            #
            total_durations = total_durations + current_duration
            if current_duration > max_duration:
                max_duration = current_duration

        #return [max_duration, total_durations]
        self.max_possible_work_duration = max_duration
        self.total_poss_shift_durations = total_durations

    #Purpose:   Returns how many more hrs can be scheduled for work shifts for this Day
    def get_work_shift_hrs_limit(self):
        return abs(self.shift_hrs - self.limit_hrs)




class Week:
    #sched_shifts = dictionary of Shift objects representing already scheduled things this week (keys = datetime label to use for new Day objects, value = List of Shift objects for that Day)
    #unavailability = dictionary : keys = day.label (date str), value = List of tuples (tuples = (start_time, end_time), representing one unavailability of that particular Day
    def __init__(self, sched_shifts, shifttypes_req, unavailability, limit_hrs_day = 24, shift_buffer = 30):
        self.days = {}                              #dictionary of size 7 to represent 7 Days --> keys = Day.label ,  value = Day obj
        self.shifttypes_req = shifttypes_req        #dictionary of all ShiftType objects needed to be scheduled throughout self.days --> keys = ShiftType.label  ,  value = ShiftType obj
        self.total_hrs_req = 0                      # total amount of hrs to schedule through Week.days  --> == sum of hrs_req in Week.shifttypes_req
        self.limit_hrs_day = limit_hrs_day          # max # of that can be worked each day this week --> may change later to be specific to each Day obj, instead of uniformly throughout the Week obj
        self.shift_buffer = shift_buffer
        self.max_hrs_sched_day = 0                  #sum of limit_day field in each Shifttype in shifttypes_req --> tells us how many hours we can schedule each day at max bc == user's specified limit can possibly work on each Shifttype each day


        #Populate Week.days with the given sched_shifts of the week:
#Note to self: Could also just do this from the getgo when parsing input --> pass as parameter already formed in Week constructor
        for daylabel in list(sched_shifts.keys()):
            shifts_day = sched_shifts.get(daylabel)
            unavailable_day = unavailability.get(daylabel)
            self.days[daylabel] = Day(daylabel, shifts_day, unavailable_day, self.limit_hrs_day, self.shift_buffer)

        #calculate total_hrs_req and max_hrs_sched_day
        for shifttype in self.shifttypes_req:
            self.total_hrs_req = self.total_hrs_req + (self.shifttypes_req.get(shifttype)).hrs_req
            self.max_hrs_sched_day = self.max_hrs_sched_day + (self.shifttypes_req.get(shifttype)).limit_day


    #Purpose:   Calculate the available hours we can actually schedule each day ---> for each day == min(day's total shift durations avail, (day's limit_hrs of work - already scheduled work), self.max_hrs_sched_day)
    #           Return actual # of hrs for the week in List AND the distribution of avail hrs for the week --> e.g if total_avail_hrs = 10, and Day 0 accounts for 3 hrs --> total_avail_hrs_distrib[0] = 0.3 (Day 0 accounts for 30% of the total avail hrs for this week)
    def find_total_avail_hrs(self):
        #For each day in days{} --> run find_max_duration_time() and get_work_shift_hrs_limit(), find minimum between those results and self.max_hrs_sched_day:
        total_avail_hrs_week = {}
        total_hrs = 0
        for day_label in self.days:
            current_day = self.days.get(day_label)
            max_hrs_poss_sched = min([current_day.total_poss_shift_durations, current_day.get_work_shift_hrs_limit(), self.max_hrs_sched_day])      #basically == what is the most amount of hrs we can schedule for this day w/o breaking any rules? (limit_day for Shifttypes, limit_day for this Day, actually having availability in the day (e.g. not unavailable for all/most of Day))

            total_avail_hrs_week[day_label] = max_hrs_poss_sched
            total_hrs = total_hrs + max_hrs_poss_sched

        #Calculate and return the distribution:
        total_avail_hrs_distrib = {}                    #keys = Day labels,  values = ratio #

        for day_label in total_avail_hrs_week:
             max_hrs_day = total_avail_hrs_week.get(day_label)
             total_avail_hrs_distrib[day_label] = (max_hrs_day/total_hrs)

        return [total_avail_hrs_distrib, total_avail_hrs_week]


      #Purpose: Find the total avail hrs throughout the week starting from the given day --> distribution over the available days.
    def find_total_avail_hrs_test(self, start_day_label):
        #For each day in days{} --> run find_max_duration_time() and get_work_shift_hrs_limit(), find minimum between those results and self.max_hrs_sched_day:
        total_avail_hrs_week = {}
        total_hrs = 0

        day_labels = list(self.days.keys())
        start_index = day_labels.index(start_day_label)
        daysToDistrib = day_labels[start_index:]

        for day_label in daysToDistrib:
            current_day = self.days.get(day_label)
            max_hrs_poss_sched = min([current_day.total_poss_shift_durations, current_day.get_work_shift_hrs_limit(), self.max_hrs_sched_day])      #basically == what is the most amount of hrs we can schedule for this day w/o breaking any rules? (limit_day for Shifttypes, limit_day for this Day, actually having availability in the day (e.g. not unavailable for all/most of Day))

            total_avail_hrs_week[day_label] = max_hrs_poss_sched
            total_hrs = total_hrs + max_hrs_poss_sched

        #Calculate and return the distribution:
        total_avail_hrs_distrib = {}                    #keys = Day labels,  values = ratio #

        return (total_avail_hrs_week.get(start_day_label)/total_hrs)


    #Purpose:   Calculate and return the distribution of Shifttypes' hrs_req to self.total_hrs_req --> for the total hrs we have to schedule for this week, how much of it is accounted for Shifttype 1, Shifttype 2, etc, returns a tuple of (dictionary: keys = Shifttype.label, value = ratio), and [daily shifttype quotas])
    def get_shifttype_distrib(self, day_hrs_quota):
        shifttype_distrib_hrs_req = {}              #keys = Shifttype labels,  values = ratio #
        shifttype_quotas = {}

        sum = 0
        for shifttype_label in self.shifttypes_req:
            curr_shifttype_hrs_req = (self.shifttypes_req.get(shifttype_label)).hrs_req
            ratio = round((curr_shifttype_hrs_req/self.total_hrs_req), 4)
            quota = ratio*day_hrs_quota
            quota = float((self.shift_buffer*(round(round(quota*60)/self.shift_buffer)))/60)          #rounded as specified in ex to fit a duration in terms of self.shift_buffer

            if ratio > 0:
              shifttype_distrib_hrs_req[shifttype_label] = ratio
              shifttype_quotas[shifttype_label] = quota
              sum = sum + ratio

        #Ensure all ratios sum to 1 bc will need to use for numpy.random.choice with p
        if sum < 1:
          firstElem = list(shifttype_distrib_hrs_req.keys())[0]
          value = shifttype_distrib_hrs_req.get(firstElem)
          shifttype_distrib_hrs_req[firstElem] = value + (1 - sum)
          print("sum < 1: ", sum)
          print("diff: ", (1-sum))

        if sum > 1:
          firstElem = list(shifttype_distrib_hrs_req.keys())[0]
          value = shifttype_distrib_hrs_req.get(firstElem)
          shifttype_distrib_hrs_req[firstElem] = value - (sum-1)

          print("sum > 1: ", sum)
          print("diff: ", (sum-1))



        return (shifttype_quotas, shifttype_distrib_hrs_req)



      #Purpose:  Utilized in every iteration of picking a new Shifttype in schedule(), given the list of Shifttype.hrs_req : Week.hrs_req ratios, re-calculate the ratios to remove the given Shifttype. Used to update the ratios that is used as weights in randomly choosing a Shifttype. shifttypes = list of Shifttypes to include in new ratios

    def updateShifttypeRatios(self, shifttypes):
        ratios = []

        if len(shifttypes) > 0:
          new_week_hrs_req = 0
          for shifttype_label in shifttypes:
            new_week_hrs_req = new_week_hrs_req + self.shifttypes_req.get(shifttype_label).hrs_req

          sum = 0
          for shifttype_label in shifttypes:
              ratio = round((((self.shifttypes_req.get(shifttype_label)).hrs_req)/new_week_hrs_req),4)
              ratios.append(ratio)
              sum = sum + ratio

          #Ensure all ratios sum to 1 bc will need to use for numpy.random.choice with p
          if sum < 1:
            ratios[0] = ratios[0] + (1 - sum)

            print("sum < 1: ", sum)
            print("diff: ", (1-sum))

          elif sum > 1:
            ratios[0] = ratios[0] - (sum-1)

            print("sum > 1: ", sum)
            print("diff: ", (sum - 1))

          else:
            print("sum is 1: ", sum)
        print("updateShifttypeRatios: ", "ratios = ", ratios)
        return ratios




    #Schedule the shifttypes_req into the days
    def schedule(self):
        for day_label in self.days:
            print("\n\nScheduling day: ", day_label)
            print("------------------------------------------------------------------\n")

            current_day = self.days.get(day_label)
            total_avail_hrs_ratio = self.find_total_avail_hrs_test(day_label)
            print("- total_avail_hrs_ratio: ", total_avail_hrs_ratio)

            total_hrs_quota = self.total_hrs_req*total_avail_hrs_ratio  #(total_avail_hrs_distrib.get(day_label))
            print("- Weekly hr goal: ", self.total_hrs_req, " hrs")

            total_hrs_quota = (self.shift_buffer*(round(round(total_hrs_quota*60)/self.shift_buffer)))/60
            print("Quota for the day: ", total_hrs_quota, " hrs")

            sched_hrs_count = 0
            shifttype_distrib = self.get_shifttype_distrib(total_hrs_quota)            #gets the ratios and quotas of each Shifttype that make up the total_hrs_quota
            shifttype_quotas = shifttype_distrib[0]
            shifttype_ratios_dict = shifttype_distrib[1]

            print("- Shifttype hrs_req to Weekly hrs_req ratios: ", shifttype_ratios_dict, "\n")
            shifttypes_today = list(shifttype_ratios_dict.keys())
            print("- Shifttypes: ", shifttypes_today)

            shifttype_ratios = list(shifttype_ratios_dict.values())
            print("- Shifttype ratios: ", shifttype_ratios)

            while current_day.max_possible_work_duration >= (self.shift_buffer/60) and current_day.get_work_shift_hrs_limit() >= (self.shift_buffer/60) and len(shifttypes_today) > 0 and total_hrs_quota > 0:    #TODO: add some margin to the quota so we don't HAVE to meet it everyday
                print("--------------------------------------------")
                print("- Choosing new Shift: ")
                chosen_shifttype_label = choice(shifttypes_today, p = shifttype_ratios)

                print("\tPossible Shifttypes list: ", shifttypes_today)
                print("\tShifttype Ratios list: ", shifttype_ratios)
                print("\tChosen_shifttype: ", chosen_shifttype_label)
                chosen_shifttype = self.shifttypes_req.get(chosen_shifttype_label)
                shifttype_quota = shifttype_quotas.get(chosen_shifttype_label)
                print("\t", chosen_shifttype_label, " Quota for day : ", shifttype_quota, " hrs\n")

                #Calculate duration range:
                print("\tCalculating duration range:")
                if shifttype_quota < (self.shift_buffer/60):        #do not allow min_duration to be 0. periodt
                  min_duration = self.shift_buffer/60
                else:
                  min_duration = shifttype_quota

                max_duration = min([chosen_shifttype.limit_day, chosen_shifttype.hrs_req, current_day.get_work_shift_hrs_limit(), current_day.max_possible_work_duration])        #validated by default
                print("\tmin_duration: ", min_duration, "hrs")
                print("\tmax_duration: ")
                print("\t\t- ", chosen_shifttype_label, " work limit: ", chosen_shifttype.limit_day, "hrs")
                print("\t\t- today's leftover time to work: ", current_day.get_work_shift_hrs_limit(), "hrs")
                print("\t\t- max shift duration: ", current_day.max_possible_work_duration, "hrs")
                print("\t\t- shifttype hrs req left: ", chosen_shifttype.hrs_req)
                print("\t\t == ", max_duration, "hrs")


                #Validate min_duration:
                #if min_duration cannot work --> follow percentile vs. passing rate distribution hard-coded chart:
                if current_day.max_possible_work_duration < min_duration:
                    print("\n\t Today's max shift duration was < min_duration --> gotta figure out if its worth it to still schedule ", chosen_shifttype_label, " today")
                    #calculate percentage that can be fulfilled:
                    ratio = current_day.max_possible_work_duration/min_duration

                    print("\t\t- percentage that can still be fulfilled of the min_duration: ", ratio)
                    #I want to check you further if you don't hit the 0.8 fulfilled
                    if ratio < 0.8:
                        print("\t\t\t Since ratio can't even fulfill 80% of the wanted min_duration --> see if its percentile is good enough for how low its ratio is.")
                        #I want to check you further if you don't suit one of these case:
                        #follow percentile vs. passing rate distribution hard-coded chart:
                        '''
                        90 percentile --> 30% (e.g. as long as max duration fulfills 30% of the calculated min its good)
                        80 percentile --> 40%
                        70 percentile --> 50%
                        60 percentile --> 60%
                        50 percentile --> 70%
                        '''
                        percentile = stats.percentileofscore(list(shifttype_ratios_dict.values()), shifttype_ratios_dict.get(chosen_shifttype_label))

                        print("\t\t\t- percentile = ", percentile)

                        if not((percentile >= 0.9 and ratio >= 0.3) or
                        (percentile >= 0.8 and percentile < 0.9 and ratio >= 0.4) or
                        (percentile >= 0.7 and percentile < 0.8 and ratio >= 0.5) or
                        (percentile >= 0.6 and percentile < 0.7 and ratio >= 0.6) or
                        (percentile >= 0.5 and percentile < 0.6 and ratio >= 0.7)):

                            #Do not take the max duration, just give up this iteration and take this Shifttype out of the shifttypes_today
                            print("\t\t\t- Didn't meet it --> give up this iteration, don't schedule: ", chosen_shifttype_label)
                            shifttypes_today.remove(chosen_shifttype_label)
                            shifttype_ratios = self.updateShifttypeRatios(shifttypes_today)
                            continue

                    #otherwise: take the max we can get:
                    min_duration = current_day.max_possible_work_duration
                    print("\t\t- ratio is good enough, we'll still schedule it. min_duration now = ", min_duration, "\n")

                #Create duration range incrementally, then randomly pick a duration e.g min = 1.5hr, max = 3.5hr       --> duration_range = [1.5hr, 2.0hr, 2.5hr, 3.0hr, 3.5hr)
                duration_range = [min_duration]
                count = min_duration

                while count < max_duration:
                    count = count+(self.shift_buffer/60)
                    duration_range.append(count)

                print("\t- duration range: ", duration_range)
                #pick random duration from duration range:
                chosen_duration = random.choice(duration_range)
                print("\t- chosen duration: ", chosen_duration, "\n")


                #4. Use day.choose_random_time() to pick a valid start time for that Day to have a Shift of chosen duration
                chosen_start_time = current_day.choose_random_time(random.choice([3,4,5,6]), chosen_duration)           #chooses random choosing_size parameter (hard-coded 3 - 6)


                #5. Create the Shift obj for the chosen Shifttype, then use day.sched_shift()
                end_time = chosen_start_time + timedelta(hours=chosen_duration)
                new_shift = Shift(chosen_shifttype_label, chosen_start_time, end_time, True, True, chosen_shifttype.note)
                current_day.sched_shift(new_shift)

                 #6. Update all relevant variables:
                #Add new shift to shifttype.schedule field --> able to find all Shift objects of this Shifttype for all Days this Week:
                if day_label in chosen_shifttype.schedule:
                    chosen_shifttype.schedule.append(new_shift)
                else:
                    chosen_shifttype.schedule[day_label] = [new_shift]

                chosen_shifttype.hrs_req = chosen_shifttype.hrs_req - chosen_duration


                self.total_hrs_req = self.total_hrs_req - chosen_duration
                total_hrs_quota = total_hrs_quota - chosen_duration
                #sched_hrs_count = sched_hrs_count + chosen_duration

                #6. Remove the Shifttype from the list for this Day
                shifttypes_today.remove(chosen_shifttype_label)
                shifttype_ratios = self.updateShifttypeRatios(shifttypes_today)

                print("- Done scheduling: ", chosen_shifttype_label, " :", chosen_start_time, " - ", end_time)
                print("- Total hours scheduled today: ", sched_hrs_count, "hrs")
                print("- Weekly hr goal: ", self.total_hrs_req, "hrs\n")
                print(chosen_shifttype_label, " details:")
                print("\t- Hours left to sched: ", chosen_shifttype.hrs_req)
                print("\t- Schedule for today: ", chosen_shifttype.schedule[day_label], "\n")





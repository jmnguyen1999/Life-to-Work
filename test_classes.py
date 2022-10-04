#Purpose: just to start coding so I finally have some base to work with before fully finalizing logic flow
# --> just coding some of the finalized basics

from datetime import datetime
from datetime import timedelta
import random

'''
#TODO:    What if we want to specify 11:30pm - 02:00am the next day?

#-------------------Testing all other objects:---------------------
#hardcoded sched_shifts:
#Shift("Unavailability", start_time , end_time, False)
unavailable = {
  "09/25/22" : [("12:00am", "03:30am"), ("09:00pm", "11:30pm")],
  "09/26/22" : [("12:00am", "04:30am"), ("09:30pm", "11:30pm")],
  "09/27/22" : [("12:00am", "07:00am"), ("08:00pm", "11:30pm")],
  "09/28/22" : [("12:00am", "03:30am"), ("09:00pm", "11:30pm")],
  "09/29/22" : [("12:00am", "05:00am"), ("08:30pm", "11:30pm")],
  "09/30/22" : [("12:00am", "09:30am"), ("10:00pm", "11:30pm")],
  "10/01/22" : [("12:00am", "03:30am"), ("09:00pm", "11:30pm")],
}

#Shift(label, start_time , end_time, is_work, note)
sched_events = {
  "09/25/22" : [("Work", "04:30am", "08:30am", True, ""), ("Knotts Scary Farm!!", "07:00pm", "11:30pm", False, "Double date scary intestines! :)")],
  "09/26/22" : [("Work", "05:30am", "09:30am", True, "")],
  "09/27/22" : [],
  "09/28/22" : [("Work", "04:30am", "08:30am", True, "")],
  "09/29/22" : [("Work", "10:30am", "02:30pm", True, "")],
  "09/30/22" : [],
  "10/01/22" : [("Work", "06:30am", "10:30am", True, "")]
}

def convert_time(time_str):
  return datetime.strptime(time_str, '%m/%d/%y %I:%M%p')

#initialize sched_shifts:
sched_shifts = {}

#input the unavailability:
for day in list(unavailable.keys()):
  unavail_times = unavailable.get(day)
  shifts_day = []
  for times in unavail_times:
    shifts_day.append(Shift("Unavailability", convert_time((day + " " + times[0])), convert_time((day + " " + times[1])), False))

  sched_shifts[day] = shifts_day

#input the sched_events:
for day in list(sched_events.keys()):
  all_shifts = sched_events.get(day)
  shifts_day = sched_shifts.get(day)
  for shift in all_shifts:
    shifts_day.append(Shift(shift[0], convert_time((day + " " + shift[1])), convert_time((day + " " + shift[2])), shift[3], shift[4]))

  sched_shifts[day] = shifts_day

'''
#print("Here is your pre-filled schedule:\n\n")
#for day in list(sched_shifts.keys()):
#  print("-------------------------- Date: ", day, ": ---------------------------------------\n")
#  shifts_day = sched_shifts.get(day)

#  if len(shifts_day) > 0:
#    for time in shifts_day:
#      print("Label: ", time.label, "\n")
#      print("time: ", time.start_time.strftime('%I:%M%p'), " - ", time.end_time.strftime('%I:%M%p'), "\n")
#      print("is work? ", time.is_work, "\n\n")
#      print("Note: ", time.note, "\n")

#  else:
#      print("Nothing for today!\n")
#  print("\n")
'''


#Create shifttypes_req:
#(self, label, hrs_req, limit_day, note = ""):
shifttypes_req = {
  "Chores/Housework" : ShiftType("Chores/Housework", 7, 3, "- vacuum\n- laundry\n- water week"),
  "Leetcode" : ShiftType("Leetcode", 15, 7),
  "Job Search" : ShiftType("Job search", 8, 4, "-resume touch up\n- applying to jobs\n- follow ups"),
  "Reflections/Goals" : ShiftType("Reflections/Goals", 1, 1)
}


# --> Give to Week obj to create the rest of the actual Day objs needed, + other inputted info about the Week
#self, sched_shifts, shifttypes_req, limit_hrs_day = 24, shift_buffer = 30):
week1 = Week(sched_shifts, shifttypes_req, 4)

print("- total hrs req: ", week1.total_hrs_req)
print("- max hrs can work/day: ", week1.limit_hrs_day)
print("- shift buffer: ", week1.shift_buffer)
print("- all ShiftTypes: ")

for shifttype_label in list(week1.shifttypes_req.keys()):
  shifttype = week1.shifttypes_req.get(shifttype_label)
  print("------Shifttype: ", shifttype_label, " ----")
  print("- Shifttype label: ", shifttype.label, "\n")
  print("\t- hrs req: ", shifttype.hrs_req, "\n")
  print("\t- max hrs to work in a day: ", shifttype.limit_day, "\n")
  print("\t- note: ", shifttype.note, "\n")
  print("\t- schedule: ", shifttype.schedule, "\n\n")

print("- days: ")
for day_label in list(week1.days.keys()):
  print("---- Date: ", day_label, " -----------\n")
  day_obj = week1.days.get(day_label)
  print("Day object:  ", day_obj.label, "\n")
  print("\t- total shift hrs: ", day_obj.shift_hrs, "\n")
  print("\t- max hrs can work: ", day_obj.limit_hrs, "\n")
  print("\t- shift buffer: ", day_obj.shift_buffer, "\n")
  print("\t- hit max hrs of work? ", day_obj.limit_hrs_hit, "\n")
  print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
  print("\t- Shifts today: \n")
  for shift_label in day_obj.shifts:
    shift = day_obj.shifts.get(shift_label)
    print("\t\t- ", shift_label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")



------------------------------------------------------------
#Testing driver code:
sched_shifts = {}

#input for unavailbility + time off/scheduled stuff:
print("Enter all times you want to be unavailable for WORK, enter 'done' when done inputting for each day:\n")
dates = {
  "Sunday 9/25/22" : "09/25/22",
  "Monday 9/26/22" : "09/26/22",
  "Tuesday 9/26/22" : "09/27/22",
  "Wednesday 9/27/22" : "09/28/22",
  "Thursday 9/28/22" : "09/29/22",
  "Friday 9/29/22" : "09/30/22",
  "Saturday 9/30/22" : "09/31/22",
}

for day in list(dates.keys()):

  str = "Do you have unavailability for ", day, ", yes or no?  "
  answer = input(str)

  shifts_day = []

  while answer == "yes":
    print("Please enter all times in the format: 12:30pm")

    start_time_str = input("start time: ")
    end_time_str = input("end_time: ")
    str = "Enter another unavailability for ", day, " yes or no?  "
    answer = input(str)

    start_time = datetime.strptime((dates.get(day) + " " + start_time_str), '%m/%d/%y %I:%M%p')
    end_time = datetime.strptime((dates.get(day) + " " + end_time_str), '%m/%d/%y %I:%M%p')
    shifts_day.append(Shift("Unavailability", start_time , end_time, False))

  sched_shifts[dates.get(day)] = shifts_day

  if len(shifts_day) > 0:
    print("Here is your unavailability for ", day, ": \n")
    counter = 1
    for time in shifts_day:
      print("Unavailability #", counter, ":\n")
      print("Label: ", time.label, "\n")
      print("time: ", time.start_time.strftime('%I:%M%p'), " - ", time.end_time.strftime('%I:%M%p'), "\n")
      print("is work? ", time.is_work, "\n\n")

      counter = counter + 1

  print("\n\n")


print("Here is your full unavailability: \n")

for day in list(sched_shifts.keys()):
  print("Date: ", day, ": \n")
  shifts_day = sched_shifts.get(day)

  if len(shifts_day) > 0:
    for time in shifts_day:
      print("Label: ", time.label, "\n")
      print("time: ", time.start_time.strftime('%I:%M%p'), " - ", time.end_time.strftime('%I:%M%p'), "\n")
      print("is work? ", time.is_work, "\n\n")

  else:
      print("No unavailability given for today!\n")
  print("\n")


#-------doing shifts/other events:
print("Time to do already scheduled work/events!")
for day in list(dates.keys()):

  str = "Do you have anything for ", day, ", yes or no?  "
  answer = input(str)

  shifts_day = dates.get(day)

  print("Please enter all times in the format: 12:30pm")
  while answer == "yes":
    label = input("Label: ")
    start_time_str = input("start time: ")
    end_time_str = input("end_time: ")
    note = input("enter an optional note for it: ")
    is_work_input = input("Is this work to be calculated with other scheduled work? yes or no: ")
    is_work = (is_work_input == "yes")

    str = "Enter another scheduled event for ", day, " yes or no?  "
    answer = input(str)

    start_time = datetime.strptime((dates.get(day) + " " + start_time_str), '%m/%d/%y %I:%M%p')
    end_time = datetime.strptime((dates.get(day) + " " + end_time_str), '%m/%d/%y %I:%M%p')
    shifts_day.append(Shift(label, start_time , end_time, is_work, note))

  sched_shifts[dates.get(day)] = shifts_day

for day in list(sched_shifts.keys()):
  print("Date: ", day, ": \n")
  shifts_day = sched_shifts.get(day)

  if len(shifts_day) > 0:
    for time in shifts_day:
      print("Label: ", time.label, "\n")
      print("time: ", time.start_time.strftime('%I:%M%p'), " - ", time.end_time.strftime('%I:%M%p'), "\n")
      print("is work? ", time.is_work, "\n\n")
      print("Note: ", time.note, "\n")

  else:
      print("Nothing for today!\n")
  print("\n")


----------------------------------------------------------------------------------------------------------------
Example driver code:

   sched_shifts = {}

   input for unavailbility + time off/scheduled stuff:

        for each dayinput:
            #Create Shift objects for each inputted shit/time period
            shifts_day = []
            for each time section given:
                shifts_day.append(Shift(label, starttime, endtime, False, note))

            sched_shifts[dayinput's label] = shifts_day

    input for work shifts:
         #Create Shift objects for each inputted shit/time period
        for each day:
            shifts_day = []
            for each time section given:
                shifts_day.append(Shift(label inputted, starttime, endtime, True))

            sched_shifts[dayinput's label] = shifts_day

    input for shifttypes:
        shifttypes = {}

        for each shifttypes inputted:
            shifttypes[shifttype inputted label] = ShiftType(label, hrs_req, limit_day, note)


    # --> Give to Week obj to create the rest of the actual Day objs needed, + other inputted info about the Week
    week1 = Week(sched_shifts, shifttypes, limit_hrs_day)
'''

#Purpose:       Model a shift to withold a period of time + some additional info, used to be scheduled throughout Day and Week objects (held within some List or Dictionary).
class Shift:

    #TODO: Ensure that all shifts abide by a given shift_buffer --> e.g have valid times
    def __init__(self, label, start_time, end_time, is_work, is_shifttype, note = ""):
        self.label = label                      #string to print when displaying shift == ShiftType.label
        self.start_time = start_time            #datetime obj
        self.end_time = end_time                #datetime obj
        self.note = note                        #string to print when displaying shift == ShiftType.note (just an optional note for user's personal use about what they wanted to do this shift)
        self.is_work = is_work
        self.is_shifttype = is_shifttype        #boolean whether or not Shift is for one of the ShiftTypes program is scheduling --> one of the Shifts that will need to be flexible/referenced again and again for drafts

    def get_starttime_str(self):
        return self.start_time.strftime('%I:%M%p')

    def get_endtime_str(self):
        return self.end_time.strftime('%I:%M%p')

#Purpose:   Model a type of Shift/what kind of work during a shift --> info about required hrs to complete by the end of the week, label, etc
class ShiftType:

    def __init__(self, label, hrs_req, limit_day, note = ""):
        self.label = label              #name of this kind of shift/work     e.g "homework", "chores"
        self.hrs_req = hrs_req          #req. # of hrs to be scheduled for a week(the goal)
        self.limit_day = limit_day      # max # of hrs that can worked/day on this type of work
        self.note = note                #optional note for user's personal use


#Issue: can't save multiple Shift objects in shifts for "Unavailability" key --> yes an unavailability is necessary
#^ issue for "work" too, --> cannot use as keys anymore, maybe no more dictionary
#Solution:      --> only reason i used a dictionary --> can easily find an exact Shift obj to delete later if i needed to, or adjust it. --> create a separate dictionary keys = starting times, value = Shift object
#               --> this way, all shifts are still anonymous, but what makes Shifts unique and will be easy to find is the datetime its scheduled for
#                       --> ShiftType objects also have their own schedule --> can find the start_time and end_times from there if its unknown and you're looking for a specific Shift object that was scheduled for that
#                           --> if this is too much --> can also have a dictionary to tie Worktype labels to their shifts in the Day object? --> don't need a schedule field in the WorkType at all
#                                   e.g keys = "Leetcode", value = Shift[] --> can have multiple shifts of the same WorkType a day if i wanted to
#               --> also won't need unavailable_times for good anymore.

#   - wrong calculation for shift_hrs, forgot to think about is_work field
#Issue #2:      Unavailability shouldn't be counted towards "Shifts" that aren't Work! Unavailability only accounted for work Shifts, but if I'm inputting a random event thats not work --> should be able to input no matter the unavailability
#       --> Shifts are allowed to intersect IFFFFF they are NOT work Shifts
#       --> Shifts trying to be scheduled that == Work cannot intersect ANYTHING, cannot intersect ever
#       --> Shifts trying to be schedule that != Work can intersect Unavailability Shifts and notthinng else
#                   why? --> bc off time events & unavailability are basically the same thing
#                   --> Generally, all Shift objects that is_work = False --> can intersect
#           How to print/display:
#               - show the event for the whole scheduled time no matter what --> whatever Unavailability cuts around it:
#                   e.g. unavail = 09:00pm - 12:00am, event = 11:00 - 12:00am
#                           unavail = 09:00pm - 11:00pm , event = 11:00pm - 12:00am,
#           How to schedule:
#               - if shift.is_work = False:
#                   - additional_avail_times = all unavail times
#                   - shift has valid times if within avail_range and/or unavail_times
#                       --> if uses unavail_times:
#                               - Take out what can from avail_range
#                               - Take out the the times from unavail_times
#                           #Question:  readjust the Unavailability Shifts in shifts? might not be needed --> just leave the shifts intersecting and leave it up to display's problem
#           How to remove from schedule:
#               - if shift.is_work = False:
#                   - give/re-create the avail times for avail_times
#                   - if the times intersect with any of unavailable Shift times --> re-create to make them avail to off work Shifts (but DO NOT re-include in the avail_times, bc its not avail to everyone)
#           Solution:
#               - need an avail_times for on_work and off_work shifts:
#                   --> change avail_times -->
#                   --> create off_work_avail_times     --> avail times specific to events that aren't for work:
#                               --> TODO: for later, maybe change Shift class --> TimePeriod class, then create new Shift class that uses TimePeriod, and create new Event class that uses TimePeriod --> able to specify when things are an actual Shift (always for work), and when an Event (always for non-work)
#Note for self:    do we need "unavailability"/"timeoff" as a Shift obj or can we just include the timeframe in the unavailable? --> i included as a Shift obj originally to also include labels when printing the schedule
class Day:

    #sched_shifts = List of Shift objs representing already scheduled things this week
    #day_dt = datetime obj that this Day obj is supposed to represent e.g. 10/20/22
    def __init__(self, label, sched_shifts, unavailability, limit_hrs, shift_buffer):
                                        #purpose --> easy access to see times of this Day that are occupied with a shift
        self.shifts = {}                #Dictionary of ALL Shift objects that are scheduled for this Day: key = starttime_str (datetime str: %I:%M%p),  value = Shift obj
        self.shifttypes = {}             #dictionary of the Shift objects that represent different WorkTypes --> used for easy access to adjust times during scheduling: key = WorkType.label, value = Shift obj
        self.shift_hrs = 0              # total hrs of WORK scheduled for this Day, e.g. there may be Shift objs this day that are labeled as "Unavailability", which is not a type of work, --> exists only to occupy time period for this Day
        self.limit_hrs_hit = False      # bool, has this Day hit the max # hrs that can be scheduled?
        #self.label = day_dt.strftime('%m/%d/%y')             # string to print date when displaying schedule, may change later into a datetime obj
        self.label = label
        self.limit_hrs = limit_hrs      # max # of hrs that can worked this day
        self.shift_buffer = shift_buffer    # min. amount of time in minutes allowed between consecutive Shifts, e.g. buffer = 30 min, shift 1 = 8:00am --> shift 2 must be >= 8:30am


        self.unavailable = unavailability           #list of tuples, used to JUST save and reference the Day's unavailability for is_work = True Shifts! --> used in scheduling to determine what hrs are available to different Shifts (is_work = True/False)


        self.avail_range = {}
        self.nonwork_avail_range = {}   #same as avail_range, but EXCLUSIVELY avail only to Shifts who's is_work = False --> able to schedule non-work events during unavailability, initialized to all unavailable times

        self.init_avail_range()
        #Populate unavailable:
        #for shift in sched_shifts:
        #    if shift.label == "Unavailability":
        #        self.unavailable.append((shift.start_time, shift.end_time))

        #Initialize nonwork_avail_range now that Day.unavailable is initialized:
        #for tuple in self.unavailable:
        #    start_time = tuple[0]
        #    end_time = tuple[1]

        #     time_counter = start_time
        #    while time_counter <= end_time:
        #        self.nonwork_avail_range[time_counter.strftime('%I:%M%p')] = True
        #        time_counter = time_counter + timedelta(minutes=self.shift_buffer)       #add buffer minutes to it

        #Populate the shifts now that nonwork_avail_range is also init with avail_range:
        for shift in sched_shifts:
              self.sched_shift(shift)


    #Purpose: initializes self.avail_range with all possible times of the day (12am - 12am) using the given shift_buffer:
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
        '''
        unavail = 02:00pm - 04:00pm,  05:00pm - 07:00pm
        event = 04:00pm - 06:00pm

        nonwork: 02:00pm, 02:30pm, 03:00pm, 03:30pm, 04:00pm, 05:00pm, 05:30pm, 06:00pm, 06:30pm, 07:00pm
        avail_range: 04:30pm, ...



        '''

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

    #Purpose: Works with choose_random_time(), validates whether a given duration from start_time to end_time is avail in self.avail_range
    def is_avail(self, is_work, start_time, end_time):
        time_counter = start_time
        all_times = self.avail_range.keys()

        #If shift is non-work --> able to schedule during nonworking hours (includes unavailability times):
        if is_work is False:
            all_times.append(self.nonwork_avail_range.keys())

        #just check if each time string exists as a key in the avail_range list of keys, if not --> there must be some time thats needed that is unavail
        while time_counter <= end_time:
            if time_counter.strftime('%I:%M%p') not in all_times:
                return False
            time_counter = time_counter + timedelta(minutes=self.shift_buffer)

        return True


    #Purpose: Pick a random available time of day for a Shift given the desired duration (in hrs), and random choosing size (how many random times to generate and chosse from)
    def choose_random_time(self, choosing_size, duration_hrs):
        #avail_range already has every available time --> get them and choose by random:
        avail_hrs = list(self.avail_range.keys())
        choosing_range = ()

        #Populate choosing_range with random VALID times until its size == choosing_size:
        while len(choosing_range) < choosing_size:
            #still assuming self.label will == format '%m/%d/%y'
            start_time_str = random.choice(avail_hrs)
            start_time = datetime.strptime((self.label + " " + start_time_str), '%m/%d/%y %I:%M%p')
            end_time = start_time + timedelta(hours=duration_hrs)

            #is it valid? yes --> add it to the choosing_range!
            if self.is_avail(start_time, end_time):
                choosing_range.append(start_time)
                avail_hrs.remove(start_time_str)

        return random.choice(choosing_range)


class Week:
    #sched_shifts = dictionary of Shift objects representing already scheduled things this week (keys = datetime label to use for new Day objects, value = List of Shift objects for that Day)
    #unavailability = dictionary : keys = day.label (date str), value = List of tuples (tuples = (start_time, end_time), representing one unavailability of that particular Day
    def __init__(self, sched_shifts, shifttypes_req, unavailability, limit_hrs_day = 24, shift_buffer = 30):
        self.days = {}                              #dictionary of size 7 to represent 7 Days --> keys = Day.label ,  value = Day obj
        self.shifttypes_req = shifttypes_req        #dictionary of all ShiftType objects needed to be scheduled throughout self.days --> keys = ShiftType.label  ,  value = ShiftType obj
        self.total_hrs_req = 0                      # total amount of hrs to schedule through Week.days  --> == sum of hrs_req in Week.shifttypes_req
        self.limit_hrs_day = limit_hrs_day          # max # of that can be worked each day this week --> may change later to be specific to each Day obj, instead of uniformly throughout the Week obj
        self.shift_buffer = shift_buffer


        #Populate Week.days with the given sched_shifts of the week:
#Note to self: Could also just do this from the getgo when parsing input --> pass as parameter already formed in Week constructor
        for daylabel in list(sched_shifts.keys()):
            shifts_day = sched_shifts.get(daylabel)
            unavailable_day = unavailability.get(daylabel)
            self.days[daylabel] = Day(daylabel, shifts_day, unavailable_day, self.limit_hrs_day, self.shift_buffer)


        #TODO: update total_hrs_req by summing all hrs_req in shifttypes_req





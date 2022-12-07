from test_classes import Shift, ShiftType, Week
from datetime import datetime


#-------------------Testing hardcoded data:---------------------
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
#initialize sched_shifts:
sched_shifts = {}

#input the unavailability:
unavail_parsed = {}

for day in list(unavailable.keys()):
  unavail_times = unavailable.get(day)
  unavail_day = []
  for times in unavail_times:
    unavail_day.append((convert_time((day + " " + times[0])), convert_time((day + " " + times[1]))))
#    shifts_day.append(Shift("Unavailability", convert_time((day + " " + times[0])), convert_time((day + " " + times[1])), False, False))

  unavail_parsed[day] = unavail_day


#input the sched_events:
for day in list(sched_events.keys()):
  all_shifts = sched_events.get(day)
  shifts_day = []
  for shift in all_shifts:
    shifts_day.append(Shift(shift[0], convert_time((day + " " + shift[1])), convert_time((day + " " + shift[2])), shift[3], False, shift[4]))

  sched_shifts[day] = shifts_day


#Create shifttypes_req:
#(self, label, hrs_req, limit_day, note = ""):
shifttypes_req = {
  "Chores/Housework" : ShiftType("Chores/Housework", 7, 3, "- vacuum\n- laundry\n- water week"),
  "Leetcode" : ShiftType("Leetcode", 15, 7),
  "Job Search" : ShiftType("Job search", 8, 4, "-resume touch up\n- applying to jobs\n- follow ups"),
  "Reflections/Goals" : ShiftType("Reflections/Goals", 1, 1)
}

week1 = Week(sched_shifts, shifttypes_req, unavail_parsed, 14)
week1.schedule()
print("done")
'''

# ----------Testing all Days of the week save and displays everything we expect:-------
print("\n\n\n\n#-----------Testing all Days of the week save and displays everything we expect:----------\n\n")
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
  print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")
  print("\t- shifttypes today: \n")
  for shifttype in day_obj.shifttypes:
    print(shifttype, "\n")
    shifts = day_obj.shifttypes.get(shifttype)
    for shift in shifts:
      print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


  print("\t- Shifts today: \n")
  for shift_key in list(day_obj.shifts.keys()):
    shift = day_obj.shifts.get(shift_key)
    print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")





#-----------Playing with functions of Day class with just one Day object:----------
print("\n\n\n\n#-----------Playing with functions of Day class with just one Day object:----------\n\n")
day_obj = week1.days.get("09/25/22")

#Starting data:
print("Day object:  ", day_obj.label, "\n")
print("\t- hrs_limit left: ", day_obj.get_work_shift_hrs_limit())
print("\t- max duration shift: ", day_obj.max_possible_work_duration)
print("\t- total possible durations: ", day_obj.total_poss_shift_durations)
print("\t- total shift hrs: ", day_obj.shift_hrs, "\n")
print("\t- max hrs can work: ", day_obj.limit_hrs, "\n")
print("\t- shift buffer: ", day_obj.shift_buffer, "\n")
print("\t- hit max hrs of work? ", day_obj.limit_hrs_hit, "\n")
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")

#Starting Shifttypes:
print("\t- shifttypes today: \n")
for shifttype in day_obj.shifttypes:
  print(shifttype, "\n")
  shifts = day_obj.shifttypes.get(shifttype)
  for shift in shifts:
    print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")

#Shifts scheduled: (no longer include unavailability!!)
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("key: ", time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


remove_time = datetime.strptime("09/25/22 07:00pm", '%m/%d/%y %I:%M%p')

day_obj.remove_shift(remove_time.strftime("%I:%M%p"))

print("After removing 07:00pm shift:")
print("\t- max duration shift: ", day_obj.max_possible_work_duration)
print("\t- total possible durations: ", day_obj.total_poss_shift_durations)
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")

#Shifts scheduled: (no longer include unavailability!!)
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("key: ", time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")

'''




'''

#-------------------Testing all other objects:---------------------
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
#initialize sched_shifts:
sched_shifts = {}

#input the unavailability:
unavail_parsed = {}

for day in list(unavailable.keys()):
  unavail_times = unavailable.get(day)
  unavail_day = []
  for times in unavail_times:
    unavail_day.append((convert_time((day + " " + times[0])), convert_time((day + " " + times[1]))))
#    shifts_day.append(Shift("Unavailability", convert_time((day + " " + times[0])), convert_time((day + " " + times[1])), False, False))

  unavail_parsed[day] = unavail_day


#input the sched_events:
for day in list(sched_events.keys()):
  all_shifts = sched_events.get(day)
  shifts_day = []
  for shift in all_shifts:
    shifts_day.append(Shift(shift[0], convert_time((day + " " + shift[1])), convert_time((day + " " + shift[2])), shift[3], False, shift[4]))

  sched_shifts[day] = shifts_day


print("Here is your pre-filled schedule:\n\n")
for day in list(sched_shifts.keys()):
  print("-------------------------- Date: ", day, ": ---------------------------------------\n")
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
week1 = Week(sched_shifts, shifttypes_req, unavail_parsed, 4)


# ----------Testing all Days of the week save and displays everything we expect:-------
print("\n\n\n\n#-----------Testing all Days of the week save and displays everything we expect:----------\n\n")
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
  print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")
  print("\t- shifttypes today: \n")
  for shifttype in day_obj.shifttypes:
    print(shifttype, "\n")
    shifts = day_obj.shifttypes.get(shifttype)
    for shift in shifts:
      print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


  print("\t- Shifts today: \n")
  for shift_key in list(day_obj.shifts.keys()):
    shift = day_obj.shifts.get(shift_key)
    print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")





#-----------Playing with functions of Day class with just one Day object:----------
print("\n\n\n\n#-----------Playing with functions of Day class with just one Day object:----------\n\n")
day_obj = week1.days.get("09/25/22")

#Starting data:
print("Day object:  ", day_obj.label, "\n")
print("\t- total shift hrs: ", day_obj.shift_hrs, "\n")
print("\t- max hrs can work: ", day_obj.limit_hrs, "\n")
print("\t- shift buffer: ", day_obj.shift_buffer, "\n")
print("\t- hit max hrs of work? ", day_obj.limit_hrs_hit, "\n")
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")

#Starting Shifttypes:
print("\t- shifttypes today: \n")
for shifttype in day_obj.shifttypes:
  print(shifttype, "\n")
  shifts = day_obj.shifttypes.get(shifttype)
  for shift in shifts:
    print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")

#Shifts scheduled: (no longer include unavailability!!)
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("key: ", time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")



#--------------------Testing removing shifts:------------------------
print("\n\n\n\n#-----------Testing removing shifts:------------------------\n\n")
remove_time = datetime.strptime("09/25/22 07:00pm", '%m/%d/%y %I:%M%p')

day_obj.remove_shift(remove_time.strftime("%I:%M%p"))

#Printing output:
print("\n\nremoved 07:00pm shift:  \n\n")
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


#-------------------Testing is_avail with different expected outputs-------------------
print("\n\n\n\n#-----------Testing is_avail with different expected outputs----------\n\n")
start = datetime.strptime("09/25/22 05:00pm", '%m/%d/%y %I:%M%p')
end = datetime.strptime("09/25/22 10:00pm", '%m/%d/%y %I:%M%p')

print("is_avail: 05:00pm - 10:00pm", day_obj.is_avail(False, start, end))
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
max_duration_result = day_obj.find_max_duration_time()
print("max shift duration possible: ", max_duration_result[0])
print("total possible shift hrs: ", max_duration_result[1])

#Testing scheduling this time:
print("Schedluing shift: \"Fun time with Henry\"")
day_obj.sched_shift(Shift("Fun time with Henry", start, end, False, False))

#Printing output:
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


#-------------Testing adding to the Day.shifttypes field using is_avail-------
print("\n\n\n\n#-----------Testing adding to the Day.shifttypes field using is_avail----------\n\n")
print("\n\n Adding a shifttype:")
start = datetime.strptime("09/25/22 12:00pm", '%m/%d/%y %I:%M%p')
end = datetime.strptime("09/25/22 03:00pm", '%m/%d/%y %I:%M%p')

#is it avail?
print("is_avail for shifttype: 12:00pm - 03:00pm", day_obj.is_avail(True, start, end))
max_duration_result = day_obj.find_max_duration_time()
print("max shift duration possible: ", max_duration_result[0])
print("total possible shift hrs: ", max_duration_result[1])

#Testing scheduling this time:
print("Schedluing shift: \"Chores/Housework\"")

#Schedule the shift for this time
day_obj.sched_shift(Shift("Chores/Housework", start, end, False, True))

#Printing output:
max_duration_result = day_obj.find_max_duration_time()
print("max shift duration possible: ", max_duration_result[0])
print("total possible shift hrs: ", max_duration_result[1])
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")

#Printing Day.shifttypes:
for shifttype in day_obj.shifttypes:
  print(shifttype, "\n")
  shifttype_shifts = day_obj.shifttypes.get(shifttype)

  for shift in shifttype_shifts:
    print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


#------------Testing removing the newly adding shifts---------------------
print("\n\n\n\n------------Testing removing the newly adding shifts---------------------\n\n")

remove_time = datetime.strptime("09/25/22 04:30AM", '%m/%d/%y %I:%M%p')
day_obj.remove_shift(remove_time.strftime("%I:%M%p"))
print("removed work: 04:30am - 08:30am\n\n")

#Priting output:
max_duration_result = day_obj.find_max_duration_time()
print("max shift duration possible: ", max_duration_result[0])
print("total possible shift hrs: ", max_duration_result[1])
print("\t- total shift hrs: ", day_obj.shift_hrs, "\n")
print("\t- max hrs can work: ", day_obj.limit_hrs, "\n")
print("\t- shift buffer: ", day_obj.shift_buffer, "\n")
print("\t- hit max hrs of work? ", day_obj.limit_hrs_hit, "\n")
print("\t- avail range: ", list(day_obj.avail_range.keys()), "\n")
print("\t- nonwork avail range: ", list(day_obj.nonwork_avail_range.keys()), "\n")
print("\t- Shifts today: \n")
for time_str in list(day_obj.shifts.keys()):
  shift = day_obj.shifts.get(time_str)
  print("\t\t- ", shift.label, ":  ", shift.start_time.strftime('%I:%M%p'), " - ", shift.end_time.strftime('%I:%M%p'), "\n")


#------------------Testing choosing a random avail time given duration-------------
print("choosing random time of 3.5 hrs: ", (day_obj.choose_random_time(10, 3.5)).strftime('%I:%M%p'), "\n")
'''


'''
#--------------------Testing inputting random data----------------------
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
  '''






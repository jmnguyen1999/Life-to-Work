# Life-to-Work
Personal project of mine! Scheduler for all my work to essentially "assign" me "work" shifts to keep me productive and on top of all adult things!
<br><br>**Link not yet public:** http://lifetowork-jmnguyen1999.pythonanywhere.com/

## Things done so far: 
- [x] Create user models and webpages to do some base login/logout functionalities
- [x] Create web UI as a way to test random notification scheduling
- [x] Able to send unique, multiple notifications at scheduled times, specifying a specific email or phone.
- [x] Database tied together to keep track of scheduled Notification objects. 
- [x] Create and fine tune testing a Scheduler library to represent objects needed to create a schedule of a week: e.g. Week, Day, Shift, Shifttype
- [x] All helper methods needed to generate a scheduled are tested and functioning properly --> e.g. A shift can be scheduled and removed, Time periods are represented correctly to know when is unavailable/available, how to pick a random duration of the Day given the desired duration of the Shift, etc
- [x] Create schedule() in Week class to generate a schedule using its fields that meets all the rules:
   - [x] No work hour limits are broken --> Weekly limits, Daily limits, and Shifttype specific limits.
   - [x] All Shifts scheduled abide by all availabilities/unavailabilities.
- [ ] Fine tune schedule() in Week class to meet designed algorithm:
   - [x] Choose Shifttypes according to weight
   - [x] Create the quotas for each Shifttype first, this way we can just choose it and not have to calculate it atm with the wrong ratios. Ratios are only there to put a weight towards picking it, the quotas are only tied to the original ratios.

## Things still to do: 
### In General:
- [ ] Create some base UI to actually start seeing all my functionality and generated schedules --> research into easy peasy calendar UIs for CSS?
- [ ] Also create some base UI to start inputting random data --> start testing with actual data!!
- [ ] Big task... start organizing/designing the database to correspond to all these new models in Scheduler library
- [ ] Still need some sort of profile settings --> profile webpages for inputting user data --> for personal info to send emails and text + preferences of scheduling, etc so so so much more..
   - [ ] ^ Also means re-organizing the database to tie in all of that 

### With the Scheduler Library:
- [ ] Choose duration from validated duration range ACCORDING to weight
- [ ] Make some margin of error so don’t haveee to meet total hrs quota each day, just a target
- [ ] Also allow random way for total hrs to go overr the quota as well
- [ ] Change the complicated while loop statement into some helper method
- [ ] When scheduling a chosen duration, create a catch statement in case the algorithm messed up and there was no valid duration for that day, e.g. it returns null bc → error for sure
- [ ] Include way for scheduler to just not schedule anything on some days → allow random days off. B/c the way it works now → tries to balance everything as its number 1 priority. --> Try to by default, schedule less stuff on the weekend, no one wants to work on the weekend come on. Could just schedule the weekdays first, and then Sunday and Saturday b/c it's more likely to have most things scheduled
- [ ] When choosing the max duration, if min == shifttype.hrs_req we should just pick that as the duration and not even do the duration range. Why? B/c that means that we have everything we need to finish off that Shifttype, so lets just do it. → else leads to us choosing smaller and smaller shifts for it for no reason.


## Random Ideas for now:
- Instead of using ratios of what can be fulfilled of the min_duration, maybe also put in terms of shift_buffers? Bc 1.5hr / 2 hrs is 0.75, but the shift buffer is 30 min so, its really not bad at all, but 0.75 is a bad ratio…
- Ask user for an average shift duration? Might help to make shifts more reasonable for what type of work it is → bc issue: most Days choose a shift for every Shifttype bc the min = ratio of the total… → can use the average shift duration to give weights to the calculated durations, closest durations to the average get the most weight
  - Could also pre-process the shifttype choice range first for each day depending on their ratios, e.g. if ⅖ shifttypes cover 70% of total → just choose good shifts from those 2
- Some kind of evaluation method to determine if the scheduled Shifts of the day make sense with the ratios of the shifftypes after we met the total_hrs quota, bc just bc we meet that quota doesn’t mean the Shifts are great.

#imports
import csv
from itertools import product, combinations

class Subject:
    def __init__(self):
        self.term_options = []

    def add_term_option(self, start_date, end_date, day_of_the_week,type_arg):
        term_option = {
            'start_date': start_date,
            'end_date': end_date,
            'day_of_the_week': day_of_the_week,
            'type': type_arg,
            'length': end_date-start_date
        }
        self.term_options.append(term_option)

    def choose_term(self, index):
        if index < len(self.term_options):
            return self.term_options[index]
        else:
            return None
names=[]
for i in range(0,10000):
    names.append(i)

class ClassSchedule:
    def __init__(self,name):
        self.subjects = {}
        self.name = name

    def calculate_hours(self):
        count=0
        for s in self.subjects.values():
            for to in s.term_options:
                count+=to['length']
        return count
    def get_gaps_with_limit(self, ignore_upper_limit):
        time_data = []
        for predmet in self.subjects.values():
            for option in predmet.term_options:
                time_data.append([option["start_date"], option["end_date"], option["day_of_the_week"]])

        # Step 1: Group by day
        grouped_by_day = {}
        for start, end, day in time_data:
            if day not in grouped_by_day:
                grouped_by_day[day] = []
            grouped_by_day[day].append((start, end))

        total_gaps = 0
        quarter_hour_gaps_count = 0  # Counter for gaps of 0.25
        # Step 2 & 3: Sort and calculate gaps
        for day, slots in grouped_by_day.items():
            slots.sort()  # Sort by start time
            for i in range(len(slots)-1):
                gap = slots[i+1][0] - slots[i][1]
                if gap > 0 and gap <= ignore_upper_limit:
                    total_gaps += gap
                    if gap == 0.25:
                        quarter_hour_gaps_count += 1

        return total_gaps, quarter_hour_gaps_count
    def add_subject(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects[subject_name] = Subject()
    def has_subject(self, subject_name):
        """Check if the subject already exists in the schedule."""
        return subject_name in self.subjects

    def get_subject(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects[subject_name] = Subject()
        return self.subjects[subject_name]
    def save_to_csv(self):
        with open(f"f{self.name}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            for subject_name, subject in self.subjects.items():
                for term_option in subject.term_options:
                    writer.writerow(['Subject Name', 'Day of the Week', 'Type', 'Start Time', 'End Time'])
                    for subject_name, subject in self.subjects.items():
                        for term_option in subject.term_options:
                            writer.writerow([
                                subject_name,
                                term_option['day_of_the_week'],
                                term_option['type'],
                                term_option['start_date'],  # Assuming these keys exist
                                term_option['end_date']
                            ])

    def load_from_csv(self,name):
        with open(name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                subject_name = row['Subject Name']
                if subject_name not in self.subjects:
                    self.add_subject(subject_name)
                # Assuming add_term_option method exists and can handle these parameters
                self.subjects[subject_name].add_term_option(

                    float(row['Start Time']),  # Assuming the add_term_option method is updated to handle these
                    float(row['End Time']),
                    row['Day of the Week'],
                    row['Type']
                )
    def print_schedule(self):
        print("----------------------------------------------------------------------")
        # Helper function to convert decimal hours to HH:MM format
        def decimal_to_time(decimal_time):
            hours = int(decimal_time)
            minutes = int((decimal_time - hours) * 60)
            return f"{hours:02d}:{minutes:02d}"

        # Dictionary to hold the schedule for each day
        weekly_schedule = {'po': [], 'ut': [], 'st': [], 'ct': [], 'pa': []}

        # Iterate through each subject and its term options
        for subject_name, subject in self.subjects.items():
            for term_option in subject.term_options:
                # Append the term option to the appropriate day in the weekly schedule
                if term_option['day_of_the_week'] in weekly_schedule:
                    weekly_schedule[term_option['day_of_the_week']].append(
                        (decimal_to_time(term_option['start_date']), subject_name, decimal_to_time(term_option['end_date']))
                    )

        # Sort and print the schedule for each day
        for day, schedule in weekly_schedule.items():
            # Sort the schedule by start time
            schedule.sort(key=lambda x: x[0])
            
            print(f"Day: {day}")
            # Use join to print all subjects for the day on the same line, with formatted times
            schedule_str = ' | '.join(f"{start_time} {name} {end_time}" for start_time, name, end_time in schedule)
            print(schedule_str)
            print()  # Blank line for better readability
        print("----------------------------------------------------------------------")
def check_intervals_for_overlap_with_days(time_data):
    # Step 1: Group intervals by day
    intervals_by_day = {}
    for start, end, day in time_data:
        if day not in intervals_by_day:
            intervals_by_day[day] = []
        intervals_by_day[day].append((start, end))
    
    # Step 2: Check for overlaps within each day
    for day, intervals in intervals_by_day.items():
        # Sort intervals by start time
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        
        # Check for overlaps
        for i in range(len(sorted_intervals) - 1):
            if sorted_intervals[i][1] > sorted_intervals[i + 1][0]:
                
                #print(f"Overlap found on {day}: {sorted_intervals[i]} and {sorted_intervals[i + 1]}")
                return False  # Overlap found
    
    # No overlaps found
    return True
def create_predmet(schedule,print_b=False):
    start_date=float(input("Pridej zacatek: "))
    end_date=float(input("Pridej konec: "))
    day_of_week=input("Den v tydnu: ")
    type_argument=input("Typ: ")
    name=input("Nazev predmetu: ")

    predmet=schedule.get_subject(name)
    predmet.add_term_option(start_date,end_date,day_of_week,type_argument)

    if(print_b):
        print(schedule.get_subject(name).term_options)

def load_from_csv_and_create_schedules(filename):
    subjects = {}
    # Load CSV and organize data
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            subject_name = row['Subject Name']
            if subject_name not in subjects:
                subjects[subject_name] = {'pr': [], 'cv': []}
            subjects[subject_name][row['Type']].append(row)

    # Generate all `pr` types for each schedule
    pr_types = {subject: options for subject, options in subjects.items() if options['pr']}

    # Generate combinations of `cv` types for each subject
    cv_combinations = {subject: [combo for r in range(1, len(options['cv']) + 1)
                                 for combo in combinations(options['cv'], r)]
                       for subject, options in subjects.items() if options['cv']}

    # Generate all possible schedules combining `cv` type combinations across subjects
    all_combinations = list(product(*cv_combinations.values()))

    schedules = []
    for combination in all_combinations:
        schedule = ClassSchedule(str(names[0]))
        names.pop(0)
        # Add all `pr` types to the schedule
        for subject, options in pr_types.items():
            for option in options['pr']:
                if not schedule.has_subject(subject):  # Assuming has_subject checks if the subject exists
                    schedule.add_subject(subject)  # Assuming add_subject creates a new subject in the schedule
                 # Corrected call to add_term_option with dictionary values accessed by keys
                schedule.get_subject(subject).add_term_option(float(option["Start Time"]), float(option["End Time"]), option["Day of the Week"], option["Type"])        # Add the `cv` type combination to the schedule
        for cv_option in combination:
            for option in cv_option:
                subject_name = option['Subject Name']
                if not schedule.has_subject(subject_name):
                    schedule.add_subject(subject_name)
                schedule.get_subject(subject_name).add_term_option(float(option["Start Time"]),float(option["End Time"]),option["Day of the Week"],option["Type"])
        schedules.append(schedule)
    index=0
    new_schedules=[]
    
    loguj=1
    for s in schedules:
        valid=1
        time_data=[]

        for predmet in s.subjects.values():
            
            for option in predmet.term_options:
                time_data.append([option["start_date"],option["end_date"], option["day_of_the_week"]])
        if(check_intervals_for_overlap_with_days(time_data)==False):
            valid=0

        for p in s.subjects.values():
            #print(p.term_options)
            count=0
            for to in p.term_options:
                
                if to["type"]=="cv":
                    count+=1
            if count>=2:

                valid=0
        if valid==1:
            new_schedules.append(s)
        loguj =0
        index+=1
            
    print(time_data) 
    return new_schedules
    
# Assuming ClassSchedule and add_term_option are defined to handle term options correctly


limit=2
print("CALCULATING SCHEDULES")
schedules = load_from_csv_and_create_schedules("PaVS.csv")

# Sort schedules by get_gaps_with_limit(2) in descending order
sorted_schedules = sorted(schedules, key=lambda s: s.get_gaps_with_limit(limit), reverse=True)

print(f"PRINTING ALL: POSSIBLE SCHEDULES ({len(sorted_schedules)})")
for s in sorted_schedules:
    s.print_schedule()
    print(s.get_gaps_with_limit(limit))
print(f"schedule amount = {len(sorted_schedules)}")


"""
Script representing the Aussie map problem as a subclass of our CSP problem
"""
from CSP_Solver import CSP_Solver
from CSP import CSP
from collections import defaultdict
import random
import time

class Assignment(CSP):
    """
    - Students is a map from student name to a set of possible slots that they are free to attend a meeting (Day,Time)
    - Leaders is a map from student name to a set of possible slots that they are free to host a meeting(Day,Time)
    """
    def __init__(self, students, leaders, possible_days, possible_times):

        self.problem_name = "CS1 Assignment"

        # need look ups so we can map the (Day, Time) pairs to a single index in the domains!
        self.day_to_index = {} 
        self.times_to_index = {}

        for i, day in enumerate(possible_days):
            self.day_to_index[day] = i

        for i, time in enumerate(possible_times):
            self.times_to_index[time] = i
    

        self.student_names, self.leaders_names = list(students.keys()), list(leaders.keys())

        self.n, self.k = len(self.student_names), len(self.leaders_names)
        self.all_names = self.student_names + self.leaders_names

        # can keep a dictonary that maps the names of the students and leaders to there variable index
        self.variable_lookup = {}
        for assignment_index, name in enumerate(self.all_names):
            self.variable_lookup[name] = assignment_index

        # keep a dictonary that maps the (Day,Time) tuple to an index
        value_lookup = data_time_to_index_map = self.data_time_to_index(possible_days,possible_times)
        
      
        self.transform_to_CSP(students, leaders, data_time_to_index_map)

        #super().__init__(assignment, domains, constraints, variable_lookup, value_lookup)
  


    """
    Given the list of students and leaders avalible times as an input, want to transform into a general CSP problem 
    """
    def transform_to_CSP(self,students,leaders,data_time_to_index_map):

        # ASSIGNMENT # 
        # for this problem: student/leader i takes on value j which is the slot in which they are going to be assigned
        total = len(self.all_names)
        assignment = ["*"]*total

        ### DOMAINS FOR THE VARIABLES ### 
        domains = defaultdict(set) # students/leaders index --> there time slots which are legal

        # legal slots for the students
        for student_name, free_times in students.items():
            student_index = self.variable_lookup[student_name]

            for free_time in free_times:
                slot = data_time_to_index_map[free_time]
                domains[student_index].add(slot)
        
        # legal slots for the leaders
        for leader_name, free_times in leaders.items():
            leader_index = self.variable_lookup[leader_name]

            for free_time in free_times:
                slot = data_time_to_index_map[free_time]
                domains[leader_index].add(slot)
        
        # CONSTRAINTS #
        # 1 --> No section leaders can have the same values. 
        # Loop over all pairs of section leaders, which have index n to total_names. Legal values for each of the constraints are values where they are not equal

        # looping over all pairs of section leaders.
        constraints = defaultdict(set)
        for l1 in range(self.n,total):
            for l2 in range(l1+1,total):
                # loop over all pairs of each legal value in each domain and only add those to the constraint map that are not the same

                for d1 in domains[l1]:
                    for d2 in domains[l2]:
                        if d1 != d2: constraints[(l1,l2)].add((d1,d2))
        
        # 2 and 3 --> These are global constraints! We will deal with them on the fly.

        print(constraints)


    def data_time_to_index(self,possible_days,possible_times):
      """
      Given a (Day,Time) option, map it to an index that we can store as a domain
      """
      day_time_to_index = {}
      total_num_times = len(possible_times)
      
      for day_val,day in enumerate(possible_days):
          for time_val,time in enumerate(possible_times):
              day_time_to_index[(day,time)] = day_val*total_num_times + time_val
              
      return day_time_to_index
      
            

def generate_random_example(slots_per_student=5, num_students=5,num_leaders=5, num_days=3, num_times=3):
    """
    Want a program that returns a random list of free times for a given student 
    Free times is represented as a list of tuples (Day, Time)
    Day can be any time during the week and Time is 30 min increments from 9-8
    """
    # create options for days and times for students 
    TOTAL_DAYS = ["M","T","W","TH","F"]
    TOTAL_TIMES = make_times()

    # picking random subset of free days and times depending on the parameter input. Enables us to control how contrained we want our problem to be
    days = random.choices(TOTAL_DAYS,k=num_days)
    times = random.choices(TOTAL_TIMES,k=num_times)


    # need to make a record of students and leaders. each of the students and leaders are going to have (Day,Time) that they are free
    students = defaultdict(set)
    leaders = defaultdict(set)

    # constructing examples for leaders and students of when they are free
    student_names = random.choices([x for x in range(97,123)],k=num_students)
    leader_names = random.choices([x for x in range(65, 91)],k=num_leaders)

    for _ in range(num_students):
        student_name = student_names.pop() # students will be lowercase
        for _ in range(slots_per_student):
            students[student_name].add((random.choice(days),random.choice(times)))
    
    for _ in range(num_leaders):
        leader_name = leader_names.pop()
        for _ in range(slots_per_student):
            leaders[leader_name].add((random.choice(days),random.choice(times)))
    
    return (students, leaders, days, times)

def make_times():
    """
    Times are between 9-8 on every 30 min increment
    """
    time_1 = [str(x) for x in range(1,13) if x != 8]
    time_3 = [x + ":30" for x in time_1]
    time_1.extend(time_3)
    return time_1


if __name__ == "__main__":
    students,leaders, possible_days, possible_times = generate_random_example()
    problem = Assignment(students,leaders, possible_days, possible_times)
    #problem.generate_free_times(1,1)
    pass

    
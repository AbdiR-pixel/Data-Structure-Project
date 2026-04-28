
def report_student(students, length_id, midterm_weight, final_weight): # Function to make a summary report
    print("\n","Here, we show a summary report".center(50,'*'))

    if length_id == 0: # check if there is at least one id
        print("However, there has'nt been any id yet. Firstly, add at least one id")
        return False
    id_term_grade={}
    for id_value_index in range(length_id): # Calculate all the term grades and put them in a dictionary where ids are the keys
        id_=list(students.keys())[id_value_index]
        student_value=students[id_]
        term_grade = midterm_weight * student_value["midterm"] + final_weight * student_value["final"]
        id_term_grade[id_]=term_grade
    class_size=len(students)    
    average_term_grade=sum(id_term_grade.values())/class_size
    term_grade_list = list(id_term_grade.values()) # put all the term grades in a list
    
    print(f"Class size: {class_size} \nAverage term grade: {average_term_grade:.2f}")
    number_success = 0
    number_failure = 0
    number_student = 0
    for id_value_index in id_term_grade.keys(): # Display a report according to conditions
        if id_term_grade[id_value_index] == max(term_grade_list): # top student
            print(f"Top student: {id_value_index} ({students[id_value_index]["full name"]}) -> {max(term_grade_list):.2f}")
        if id_term_grade[id_value_index] == min(term_grade_list): # last student
            print(f"Student with the least term grade: {id_value_index} ({students[id_value_index]["full name"]}) -> {min(term_grade_list):.2f}")
        if id_term_grade[id_value_index] >= 60: # succeed students
            number_success += 1
            if id_term_grade[id_value_index] >= average_term_grade: # above the average term grade
                number_student += 1
                print(f"\n{number_student}. Above the average term grade with success: {id_value_index} ({students[id_value_index]["full name"]}) -> {id_term_grade[id_value_index]:.2f}")
        if id_term_grade[id_value_index] < 60: # failed students
            number_failure += 1
            if id_term_grade[id_value_index] >= average_term_grade: # above the average term grade
                number_student += 1
                print(f"\n{number_student}. Above the average term grade with failure: {id_value_index} ({students[id_value_index]["full name"]}) -> {id_term_grade[id_value_index]:.2f}")
        if id_term_grade[id_value_index] >= 85: # Students with grade A
            if id_term_grade[id_value_index] >= 93:
                print(f"Student with grade A: {id_value_index} ({students[id_value_index]["full name"]})")     
            else:
                print(f"Student with grade B: {id_value_index} ({students[id_value_index]["full name"]})")    
    print(f"\nNumber of succeed students (at least 60): {number_success}\nNumber of failed students: {number_failure} ")

def display_all_students(students,length_id, midterm_weight, final_weight): #Function to display all students with phones and grades
    print("\n","Here, we display all students with their phones and their grades".center(30,'*'))    
    if length_id == 0: # check if there is at least one id
        print("However, there has'nt been any id yet. Firstly, add at least one id")
        return False

    else: # otherwise display all
        for id_value_index in range(length_id): # display the id first and then its value by index by order
            id_ordered=sorted(students.keys())[id_value_index]
            student_value=students[id_ordered]
            term_grade = midterm_weight * student_value["midterm"] + final_weight * student_value["final"]
            
            print(f"\n{id_ordered}: {student_value["full name"]} scored {student_value["midterm"]:.2f} from the midterm and "
                f"{student_value["final"]:.2f} from the final ; his\her end of term grade is calculated as "
                f"{term_grade:.2f} ; and his\her phone is {student_value["phone"]}.")
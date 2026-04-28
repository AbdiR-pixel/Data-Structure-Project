from src.validation import name_validation , id_validation, phone_validation, midterm_validation, final_validation

def show_menu(): # Function to show the menu
    print("\n","SERVICE DESK STUDENT".center(50,'='))
    print("1. Add a student.")
    print("2. Update a student by id.")
    print("3. Display every student with full information.")
    print("4. Search a student by id.")
    print("5. Find a student by name.")
    print("6. Delete a student by id.")
    print("7. Display summary report.")
    print("8. Exit the program...\n")

def add_student(students): # Function to add a student
    print("\n","Here, we add a student".center(50,'*'))    
    id_validated=id_validation()
    if id_validated == "menu":
        print("Go back to the menu.")
        return False
    elif id_validated in students.keys(): # check if the id already exists
        print("This id already exists!")
        return False
    else:
        students[id_validated] = {}
        students[id_validated]["full name"]=name_validation()
        students[id_validated]["phone"]=phone_validation()
        students[id_validated]["midterm"]=midterm_validation()
        students[id_validated]["final"]=final_validation() 
    print("Student added successfully.")
    return students # return an increased dictionary of students


def update_student(students, length_id): # Function to update a student
    print("\n","Here, we update a student's information by id".center(50,'*'))
    if length_id == 0: # check if there is at least one id
        print("However, there has'nt been any id yet. Firstly, add at least one id") 
        return False 

    else: # otherwise update 
        id_validated=id_validation() 
        if id_validated == "menu":
            print("Go back to the menu.")
            return False   
        if id_validated in students.keys(): # check if it exists        
            students[id_validated]["full name"] = name_validation()
            students[id_validated]["phone"] = phone_validation()
            students[id_validated]["midterm"] = midterm_validation()
            students[id_validated]["final"] = final_validation()
            print("Student updated successfully.")
        else: # check if it does not exist
            print("Student's id is not found!")
    return students # return the updated dictionary of students
    
def search_student(students,length_id, midterm_weight, final_weight): # Function to search a student by id
    print("\n","Here, we search a student by id".center(50,'*'))    
    if length_id == 0: # check if there is at least one id
        print("However, there has'nt been any id yet. Firstly, add at least one id")
        return False

    else: # otherwise search        
        id_validated=id_validation()
        if id_validated == "menu":
            print("Go back to the menu.")
            return False
        if id_validated in students.keys(): # check if it exists
            student_value=students[id_validated]
            term_grade = midterm_weight * student_value["midterm"] + final_weight * student_value["final"]
            print(f"\n{student_value["full name"]} scored {student_value["midterm"]:.2f} from the midterm and "
                f"{student_value["final"]:.2f} from the final ; his\her end of term grade is calculated as "
                f"{term_grade:.2f} ; and his\her phone is {student_value["phone"]}.")
        
        else: # check if it does not exist
            print("The student's id does not exist!")

def find_student(students,length_id, midterm_weight, final_weight):
    print("\n","Here, we search a student by name".center(50,'*'))    
    if length_id == 0: # check if there is at least one id
        print("However, there has'nt been any id yet. Firstly, add at least one id")
        return False
    name_validated=name_validation()
    if not any(name_validated.lower() in students[id_value_index]["full name"].lower() for id_value_index in students.keys()):
        print("The name is not found!")
        return False
    for id_value_index in students.keys():
        if (name_validated.lower() in students[id_value_index]["full name"].lower()): # check if it exists
            student_value=students[id_value_index]
            term_grade = midterm_weight * student_value["midterm"] + final_weight * student_value["final"]
            print(f"\n{id_value_index}: {student_value["full name"]} scored {student_value["midterm"]:.2f} from the midterm and "
                f"{student_value["final"]:.2f} from the final ; his\her end of term grade is calculated as "
                f"{term_grade:.2f} ; and his\her phone is {student_value["phone"]}.")
    
def delete_student(students, length_id): # Function to delete a student by id
    print("\n","Here, we delete a student by id".center(50,'*'))
    
    if length_id == 0: # check if there is at least one id
        print("However, there has'nt been any id yet. Firstly, add at least one id")
        return False

    else: # otherwise delete
        id_validated=id_validation()
        if id_validated in students.keys(): # check if it exists    
            del students[id_validated]
            print("The student is removed successfully.")
        else:  # check if it does not exist
            print("The student's id does not exist!")     
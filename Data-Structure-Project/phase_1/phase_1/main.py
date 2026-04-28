
from src.registry import show_menu, add_student, search_student, delete_student, update_student, find_student
from src.report_utils import display_all_students, report_student

# a dictionary to store students's informations
students = {}
midterm_weight = 0.4
final_weight = 0.6 # The length of the dictionary ids
def main():
    while True:
        length_id = len(students.keys()) # The length of the dictionary ids
        show_menu()
        choice=input("Enter your choice: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students,length_id)
        elif choice == "3":
            display_all_students(students,length_id, midterm_weight, final_weight)
        elif choice == "4":
            search_student(students, length_id, midterm_weight, final_weight)
        elif choice == "5":
            find_student(students,length_id,midterm_weight,final_weight)
        elif choice == "6":
            delete_student(students, length_id)
        elif choice == "7":
            report_student(students, length_id, midterm_weight, final_weight)    
        elif choice == "8":
            print("Exiting the program...!")
            break    
        else:
            print("Invalid choice! Please enter a correct number.") 

if __name__ == "__main__":
    main()


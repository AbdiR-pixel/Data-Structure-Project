def name_validation(): # Function to validate the name
    print("Please enter your name (at least 3 characters, only letters and spaces allowed).")
    while True: # Loop to keep asking for input until a valid name is entered
        name=input("Name: ")
        if len(name.strip()) < 3: # check if the name is less than 3 characters
            print("Name must be at least 3 characters long!")
        elif not all(x.isalpha() or x.isspace() for x in name):   
            print("Name can only contain letters and spaces, no any number or special character allowed!") 
        else:
            if name.isspace():
                print("Name cannot be empty or just spaces!")  
            else: break # if the name is valid, break the loop and return the name             
    return " ".join(name.title().split())  # return the name with the first letter of each word capitalized and remove leading and trailing spaces

def id_validation(): # Function to validate the id
    print("Please enter your id (a number between 101 and 999). If you want to go back to the menu, then write 'menu' or an existed ID. ")
    while True: # Loop to keep asking for input until a valid id is entered
        id_input = input("ID: ")        
        if id_input.strip().lower() == "menu": # check if the user wants to go back to the menu
            return id_input.strip().lower()
            break
        elif not id_input.strip().isdigit(): # check if the input is not a number
            print("ID must be an integer!")
        elif 101 > int(id_input) or int(id_input) > 999:
            print("ID must be between 101 and 999.") 
        else:
            break
    return int(id_input) 

def phone_validation(): # Function to validate the phone
    print("Enter your phone number. It should be a djiboutian phone like: 77698157.")
    while True: 
        phone=input("Phone: ")
        phone_required=phone.strip().replace("-","").replace(" ","")
        if len(phone_required) != 8:
            print("The phone number must be 8 digits long!")
        elif not phone_required.isdigit():
            print("Phone number must contain only digits!")
        elif  phone_required[0:2] != "77":
            print("The two first digits should be 77.")
        else:
            break
    return phone_required

def midterm_validation(): # Function to validate the midterm grade
    print("Enter your midterm grade. It should be a number between 0 and 100.")
    while True:
        midterm_input = input("Midterm grade: ")
        if not midterm_input.strip().replace('-','').isdigit():
            print("Midterm grade must be a number!")
        elif 0 > int(midterm_input) or int(midterm_input) > 100:
            print("Midterm grade must be between 0 and 100.")
        else:
            break
    return int(midterm_input)        

def final_validation(): # Function to validate the final grade
    print("Enter your final grade. It should be a number between 0 and 100.")
    while True:
        final_input = input("Final grade: ")
        if not final_input.strip().replace('-','').isdigit():
            print("Final grade must be a number!")
        elif 0 > int(final_input) or int(final_input) > 100:
            print("Final grade must be between 0 and 100.")
        else:
            break
    return int(final_input) 
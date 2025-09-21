# Import sqlite3 module
import sqlite3

# Import regular experssion module in order to check the correctness of emails
import re

# Import design module
import Design

# Open database if it existed else create it and save it in a varuable
db = sqlite3.connect("Members.db")

# Set connect to curser
cur = db.cursor()

# Create 'Members' table
cur.execute("create table if not exists 'Members' ( personal_id integer , name text , phone_number number , email text ) ")

# Making functions depending on options

# Show all data function
def show():

    # Choosing between showing all members or specific member depending on personal id
    choice = input("\nChoose between show all members(A) or specific member(B): ").upper()
    if choice == "A":

        # Select all information in data base
        cur.execute("select * from 'Members' ")

        # Frtch data from selected data
        result = cur.fetchone()

        # Check if data are existed or not. if True show it else print a masage
        if result == None:
            print("\n     ---<( There is no information in the table )>---")
        else:
            cur.execute("select * from 'Members' order by name")
            result = cur.fetchall()
            print()
            for row in result:
                print(f"  Id => {row[0]} | Name => {row[1]} | Phone => {row[2]} | Email => {row[3]}")

    elif choice == "B":

        # Asking for personal id in order to show it only
        Id = input("\nWrite your personal id from 9 numbers: ").strip()

        if len(Id) == 9:

            # Select all information in data base
            cur.execute(f"select * from 'Members' where personal_id = '{Id}' ")

            # Frtch data from selected data
            result = cur.fetchone()

            # Check if data are existed or not. if True show it else print a masage
            if result == None:
                print("     ---<( This row is not exists in the table )>---")
            else:
                print(f"\n  Id => {result[0]} | Name => {result[1]} | Phone => {result[2]} | Email => {result[3]}\n")

        else:
            print("     ---<( Invalid Id given )>---")

    else:
        print("     ---<( You should enter A or B )>---")        

# Adding row in the table
def add():

    print("\n    ---<( Here you go start fill your information )>---")

    # Input to fill columns
    Id = input("\nWrite your personal id from 9 numbers: ").strip()
    Name = input("write your Name: ").capitalize()
    Phone = input("write your phone number: ").strip()
    Email = input("write your email: ").strip()

    # Using re module to check given email
    pattern = r"[\w\.]+@[\w]+\.(com|net|info|org)"
    match = re.fullmatch(pattern,Email)

    # Checking if the added row is already exists from Id
    cur.execute(f"select * from 'Members' where personal_id = {Id} ")
    result = cur.fetchone()

    # Check if all given information is True or False
    if len(Id) == 9 and Id.isdigit() and Name.replace(" ","").isalpha() and Phone.isdigit() and len(Phone) == 8 and match and result == None:
        cur.execute(f"insert into 'Members' values ( ? , ? , ? , ? ) ",(Id,Name,Phone,Email))
        print("\n     ---<( Member has been added to the table )>---")
    elif result != None :
        choice = input("\nYou are already existed, whould you like to update your data (Y/N): ").upper().strip()
        if choice == "Y":
            cur.execute(f"update 'Members' set name = '{Name}' and phone_number = '{Phone}' and email = '{Email}'")
            print("\n     ---<( Member's information have been updated to the table )>---")
        else:
            print("\n     ---<( All done )>---")
    else:
        print("     --<( Invalid information given )>---")

# Deleting row in the table
def delete():

    # Choosing between delete all the table or one specific row depending on personal id
    choice = input("\nChoose between delete all rows(A) or one specific row(B): ").upper().strip()
    if choice == "A":

        # Check if the table is empty or not 
        cur.execute("Select * from 'Members' ")
        result = cur.fetchone()
        if result == None:

            # Printing a massage
            print("\n     ---<( Table is already clear )>---")

        else:

            # Clear the table
            cur.execute("delete from 'Members'")

            # Delete massage
            print("\nAll members cleared from the table")

    elif choice == "B":

        # Choosing Id to delete it 
        Id = input("\nWrite your personal id from 9 numbers: ").strip()
        
        # Check if the table is empty or not 
        cur.execute(f"Select * from 'Members' where personal_id = {Id} ")
        result = cur.fetchone()
        if result == None:

            # Printing a massage
            print("\n     ---<( Table is already clear )>---")

        else:

            # Clear the table
            cur.execute(f"delete from 'Members' where personal_id = {Id} ")

            # Delete massage
            print("\n    ---<( This member has deleted from the table )>---")


    else:
        print("\n     ---<( You should enter A or B )>---")

# Updating row in the table
def update():

    print("\n---<( Here you go start fill your information )>---")

    # # Asking for personal id in order to show it only
    Id = input("\nWrite your personal id from 9 numbers: ").strip()

    # # Checking if the Id in the table or no in order to update it
    cur.execute("SELECT * FROM Members WHERE personal_id = ?", (Id,))
    result = cur.fetchone()
    if result is None:
        choice = input("\nYou are not in the Members table, would you like to add yourself (Y/N): ").upper().strip()

        if choice == "Y":

            # The member is not in the table so turn to add function
            add()

        else:
            print("\n---<( All done )>---")

    else:
        print("\n---<( Ok we found your data, now write your new data )>---")
        new_name = input("\nWrite your new name: ").capitalize()
        new_phone = input("Write your new phone number: ").strip()
        new_email = input("Write your new email: ").strip()

        # Using re module to check given email
        pattern = r"[\w\.]+@[\w]+\.(com|net|info|org)"
        match = re.fullmatch(pattern,new_email)

        # Check if all given information is True or False
        if len(Id) == 9 and Id.isdigit() and new_name.replace(" ","").isalpha() and new_phone.isdigit() and len(new_phone) == 8 and match:

            # The tuple must be sorted
            cur.execute("UPDATE Members SET name = ?, phone_number = ?, email = ? WHERE personal_id = ?",(new_name, new_phone, new_email, Id))
            print("\n---<( Member's information has been updated )>---")

        else:
            print("---<( Invalid information given )>---")

# Printing wellcome letter
print()
Design.color("          Wellcome to Members database","white","bold")

# The main loop and sorting the functions
while True:

    # A letter to illustarte the idea
    letter = '''
    ---<( you have to choose one command )>---

's' => Show all members in the table or one specific member
'a' => Add a new member
'd' => Delete a specific member or clear the table
'u' => Update member's information
'c' => Close the data base

    Enter your choice: '''

    # Printing the letter as an input
    choice = input(letter).lower().strip()

    # Execute the input choice
    if choice == "s":
        show()
    elif choice == "a":
        add()
    elif choice == "d":
        delete()
    elif choice == "u":
        update()
    elif choice == "c":

         # Save (commit) changes
        db.commit()

        # Close Database
        db.close()
        print()
        exit()

    else:
        print("\n     ---<( You have to choose among ( s or a or d or u or c ) )>---")

    # Save all changes after every execute method
    db.commit()

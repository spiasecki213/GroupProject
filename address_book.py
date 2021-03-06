"""
Creates an Address Book

Names: Sam Piasecki, Vanessa Aguocha-Sam, Semi Ayo-Gbenjo
Assignment: Final Project
Subject: INST326
Date: 05_13_22
"""
from tkinter import *
import tkinter
from turtle import update
from ttkwidgets.autocomplete import AutocompleteCombobox
import tkinter.messagebox as mb
import sqlite3 as sql

# Connects and initializes the database that will store all of the contacts
connector = sql.connect('contacts.db')
cursor = connector.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ADDRESS_BOOK (S_NO INTEGER PRIMARY KEY 
                AUTOINCREMENT NOT NULL, FIRSTNAME TEXT, LASTNAME TEXT, ADDRESS TEXT, 
                PHONENUMBER TEXT, EMAIL TEXT, ALTEMAIL TEXT, PRONOUNS TEXT, NOTES TEXT, 
                GROUPS TEXT)""")

#################### GLOBAL FUNCTIONS ####################
def hide_widget(widget):
    """Temporarily hides the button from view

    Args:
        widget (tkinter button): the selected button
    """    
    widget.place_forget()

def show_widget(widget):
    """Shows the widget after being hidden

    Args:
        widget (tkinter button): the selected button
    """    
    widget.place(relx=0.3, rely=0.82)


class MainWindow(object):
    """A class for the main window of the address book

    Args:
        object (window root): the root of the tkinter page
        listbox (listbox): the list of contacts
    """
    #################### CONTACT FUNCTIONS ####################
    def add_contact(self):
        """Adds a contact to the database and updates
        the listbox with the newly created contact
 
        Does not return anything
        """    
        self.normal_fields() # Makes the fields editable
 
        # Get the text from the __init__ function
        fname = self.fname_strvar.get()
        lname = self.lname_strvar.get()
        address = self.address_entry.get(1.0, END)
        phone = self.phone_strvar.get()
        email = self.email_strvar.get()
        altemail = self.altemail_strvar.get()
        pronouns = self.pronouns_strvar.get()
        notes = self.notes_entry.get(1.0, END)
        group = self.group_entry.get()

        # If either the first name or last name fields are empty,
        # push an error message to the user
            # Otherwise, add the values to the table
        if fname == '' or lname == '':
            mb.showerror('Error!', "Please fill in the name fields")
        else:
            cursor.execute(
                """INSERT INTO ADDRESS_BOOK (FIRSTNAME, LASTNAME, ADDRESS,
                PHONENUMBER, EMAIL, ALTEMAIL, PRONOUNS, NOTES, GROUPS)
                VALUES (?,?,?,?,?,?,?,?,?)""", (fname, lname, address, phone,
                email, altemail, pronouns, notes, group)
            )
            connector.commit() # Commits the data to the database
            mb.showinfo('Contact added', "Your contact has been successfully added.")
            self.listbox.delete(0, END)
            self.list_contacts() # Shows the contacts including the newly added contact
            self.clear_fields() # Clears the contact fields


    def edit_contact(self):
        """Allows user to edit an existing contact
 
        Does not return anything
        """        
        self.normal_fields() # Makes fields editable
        current_contact = self.listbox.curselection()
        fname = self.fname_strvar.get()
        lname = self.lname_strvar.get()
        address = self.address_entry.get(1.0, END)
        phone = self.phone_strvar.get()
        email = self.email_strvar.get()
        altemail = self.altemail_strvar.get()
        pronouns = self.pronouns_strvar.get()
        notes = self.notes_entry.get(1.0, END)
        group = self.group_entry.get()
        
        # If either the first name or last name fields are empty,
        # push an error message to the user
            # Otherwise, update the values in the table
        if fname == '' or lname == '':
            mb.showerror('Error!', "Please fill in the name fields.")
        else:
            # Deletes old contact
            cursor.execute('DELETE FROM ADDRESS_BOOK WHERE FIRSTNAME=? AND LASTNAME=?', self.listbox.get(ACTIVE))
            # Inserts edited contact
            cursor.execute(
                """INSERT INTO ADDRESS_BOOK (FIRSTNAME, LASTNAME, ADDRESS,
                PHONENUMBER, EMAIL, ALTEMAIL, PRONOUNS, NOTES, GROUPS)
                VALUES (?,?,?,?,?,?,?,?,?)""", (fname, lname, address, phone,
                email, altemail, pronouns, notes, group))
            
            connector.commit()
            mb.showinfo('Contact edited', "Your contact has been successfully edited.")
            self.listbox.delete(0, END)
            self.list_contacts() # Shows the contacts + the newly edited contact
            self.clear_fields() # Clears the contact fields

    def list_contacts(self):
        """ Updates the listbox and shows the contacts
 
        Does not return anything
        """        
        curr = connector.execute('SELECT FIRSTNAME, LASTNAME FROM ADDRESS_BOOK')
        fetch = curr.fetchall() # Fetches all the contact info from the database
 
        for data in fetch:
            self.listbox.insert(END, data) # Displays data contact by contact in the listbox

    def delete_contact(self):
        """ Deletes the selected contact from the listbox
        and the database
 
        Does not return anything
        """        
        # If no contact is selected, push an error message to the user
        if not self.listbox.get(ACTIVE):
            mb.showerror('No contact selected', "Please select a contact you wish to delete.")
       
        # Ask the user if they are sure they want to delete the contact
        # If they don't, exit the window
        # If they do want to delete a contact, proceed with deleting the contact
        ans = mb.askyesno(title='Confirmation', message="""Are you sure you want to delete this contact? NOTE: This action cannot be undone.""")
        if ans:
            cursor.execute('DELETE FROM ADDRESS_BOOK WHERE FIRSTNAME=? AND LASTNAME=?', self.listbox.get(ACTIVE))
            connector.commit() # Commit the changes to the database
            mb.showinfo('Contact deleted', "The contact you have selected has been deleted.")
            self.listbox.delete(0, END)
            self.list_contacts() # Show the remaining contacts
        

    def delete_all_contacts(self):
        """ Deletes ALL of the address book entries from the listbox
        and the database
 
        Does not return anything
        """        
        # Ask the user if they are sure they want to delete the contact
        # If they don't, exit the window
        # If they do want to delete a contact, proceed with deleting the contact
        ans = mb.askyesno(title='Confirmation', message="""Are you sure you want to delete ALL contacts? NOTE: This action cannot be undone.""")
        if ans:
            cursor.execute('DELETE FROM ADDRESS_BOOK') # Deletes ALL contacts
            connector.commit() # Commit the changes to the database

            mb.showinfo('Success!', "All of the contacts in your address book have been deleted")
            
            self.listbox.delete(0, END)
            self.list_contacts()
        

    def view_contact(self):
        """ Shows the selected contact within the fields in the left frame
       
        Does not return anything
        """
        # If the listbox is empty, push an error message to the user
            # If the listbox is NOT empty but the user hasn't selected a contact, push an error message to the user
                # If the previous two conditions are satisfied, show the selected contact
        if self.listbox.size() == 0:
            mb.showerror('Error!', "There are no contacts to view. Please add a contact to continue.")
        elif not self.listbox.curselection():
            mb.showerror('Error!', "No contact selected. Please select a contact to continue.")
        else:      
            curr = cursor.execute('SELECT * FROM ADDRESS_BOOK WHERE FIRSTNAME=? AND LASTNAME=?', self.listbox.get(ACTIVE))
            values = curr.fetchall()[0]
            
            # Retrieve the contact info values from the __init__ method
            self.fname_strvar.set(values[1])
            self.lname_strvar.set(values[2])
            self.phone_strvar.set(values[4])
            self.email_strvar.set(values[5])
            self.altemail_strvar.set(values[6])
            self.pronouns_strvar.set(values[7])
            self.group_entry.set(values[9])
 
            self.address_entry.delete(1.0, END) # Because these are Text values, they are treated differently than Entry values
            self.address_entry.insert(END, values[3])
            self.notes_entry.delete(1.0, END)
            self.notes_entry.insert(END, values[8])
 
            self.read_only_fields() # Makes fields un-editable

    def clear_fields(self):
        """ Clears all of the text fields/entries
 
        Does not return anything
        """    
        self.normal_fields() # Makes fields editable
        self.listbox.selection_clear(0, END) # Unselects any contact
       
        self.fname_strvar.set('')
        self.lname_strvar.set('')
        self.phone_strvar.set('')
        self.email_strvar.set('')
        self.altemail_strvar.set('')
        self.pronouns_strvar.set('')
        self.group_entry.set('')
 
        self.address_entry.delete(1.0, END)
        self.notes_entry.delete(1.0, END)

    def search(self):
        """ Searches through the first name column of the database
        and returns the relevant results
 
        Does not return anything
        """        
        query = str(self.search_strvar.get()) # Gets the text value from the search bar
 
        # If the search term isn't empty, search through the address_book
            # Else, search through the address book
        if query != '' and query != "Search Contacts...":
            show_widget(self.back_button)
            self.listbox.delete(0, END)
            curr = connector.execute('''SELECT * FROM ADDRESS_BOOK WHERE (FIRSTNAME LIKE ?) OR (LASTNAME LIKE ?) 
                    OR (FIRSTNAME LIKE ? AND LASTNAME LIKE ?)''', ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
            check = curr.fetchall() # Fetches all of the search results
           
            # Displays the search results in the listbox
            for data in check:
                self.listbox.insert(END, (data[1], data[2]))
        else:
            mb.showerror('Error!', "Please enter a search term to proceed.")

    def read_only_fields(self):
        """Sets all of the fields to readonly so they
        cannot be edited.
 
        Does not return anything
        """    
        self.fname_entry.configure(state='readonly')
        self.lname_entry.configure(state='readonly')
        self.address_entry.configure(state='disabled')
        self.phone_entry.configure(state='readonly')
        self.email_entry.configure(state='readonly')
        self.altemail_entry.configure(state='readonly')
        self.pronouns_entry.configure(state='readonly')
        self.notes_entry.configure(state='disabled')
        self.group_entry.configure(state='disabled')

    def normal_fields(self):
        """Sets all fields back to normal so they
        are able to be edited.
 
        Does not return anything
        """        
        self.fname_entry.configure(state='normal')
        self.lname_entry.configure(state='normal')
        self.address_entry.configure(state='normal')
        self.phone_entry.configure(state='normal')
        self.email_entry.configure(state='normal')
        self.altemail_entry.configure(state='normal')
        self.pronouns_entry.configure(state='normal')
        self.notes_entry.configure(state='normal')
        self.group_entry.configure(state='normal') 
    
    def __init__(self, root):
        # Initialize the GUI window
        self.root = root
        root.title("Address Book")
        root.geometry('700x550')
        root.resizable(0,0)

        # Create the StringVar contact info variables
        self.fname_strvar = StringVar()
        self.lname_strvar = StringVar()
        self.phone_strvar = StringVar()
        self.email_strvar = StringVar()
        self.altemail_strvar = StringVar()
        self.pronouns_strvar = StringVar()
        self.group_entry = StringVar()
        self.search_strvar = StringVar() #stringvar for search bar

        # Title label
        Label(self.root, text="UMD Address Book", font=('Times New Roman', 24, "bold"), 
                    bg='red4', fg='White').pack(side=TOP, fill=X)

        # Color and font variables
        lf_bg = 'light goldenrod'  # Lightest Shade
        cf_bg = 'gold2'
        rf_bg = 'gold3'  # Darkest Shade
        frame_font = ("Garamond", 13, "bold") # Font for the overall frame
        entry_font = ("Arial", 10) # Font for the entry fields
        button_font = ("Garamond", 11, "bold") # Font for the buttons
        group_values = ["Student", "Professor", "TA", "AMP", "Administrator", "Other"] # Autocomplete values for the group entry

        # Left Frame
        left_frame = Frame(root, bg=lf_bg)
        left_frame.place(relx=0, relheight=1, y=37, relwidth=0.35)
        Label(left_frame, text="Contact Info", font=('Times New Roman', 14, "italic"), 
                    bg='Maroon', fg='White').pack(side=TOP, fill=X) # left frame label
        # Center Frame
        center_frame = Frame(root, bg=cf_bg)
        center_frame.place(relx=0.35, relheight=1, y=37, relwidth=0.3)
        Label(center_frame, text="Search/Edit", font=('Times New Roman', 14, "italic"), 
                    bg='Maroon', fg='White').pack(side=TOP, fill=X) # center frame label
        # Right Frame
        right_frame = Frame(root, bg=rf_bg)
        right_frame.place(relx=0.65, relwidth=0.35, relheight=1, y=37)

        """#######################"""
        """ LEFT FRAME COMPONENTS """
        """#######################"""

        ######### LABELS AND ENTRIES #########
        # FIRST NAME
        Label(left_frame, text="First Name:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.1)
        self.fname_entry = Entry(left_frame, width=17, font=entry_font, textvariable=self.fname_strvar)
        self.fname_entry.place(relx=0.44, rely=0.1)
        # LAST NAME
        Label(left_frame, text="Last Name:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.15)
        self.lname_entry = Entry(left_frame, width=17, font=entry_font, textvariable=self.lname_strvar)
        self.lname_entry.place(relx=0.44, rely=0.15)
        # ADDRESS
        Label(left_frame, text="Address:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.2)
        self.address_entry = Text(left_frame, width=17, font=entry_font, height=4)
        self.address_entry.place(relx=0.44, rely=0.2)
        # PHONE NUMBER
        Label(left_frame, text="Phone #:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.35)
        self.phone_entry = Entry(left_frame, width=17, font=entry_font, textvariable=self.phone_strvar)
        self.phone_entry.place(relx=0.44, rely=0.35)
        # EMAIL ADDRESS
        Label(left_frame, text="Email:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.4)
        self.email_entry = Entry(left_frame, width=17, font=entry_font, textvariable=self.email_strvar)
        self.email_entry.place(relx=.44, rely=0.4)
        # ALTERNATE EMAIL ADDRESS
        Label(left_frame, text="Alt. Email:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.45)
        self.altemail_entry = Entry(left_frame, width=17, font=entry_font, textvariable=self.altemail_strvar)
        self.altemail_entry.place(relx=.44, rely=0.45)
        # PRONOUNS
        Label(left_frame, text="Pronouns:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.5)
        self.pronouns_entry = Entry(left_frame, width=17, font=entry_font, textvariable=self.pronouns_strvar)
        self.pronouns_entry.place(relx=.44, rely=0.5)
        # NOTES
        Label(left_frame, text="Notes:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.55)
        self.notes_entry = Text(left_frame, width=17, font=entry_font, height=5)
        self.notes_entry.place(relx=.44, rely=0.55)
        # GROUP
        Label(left_frame, text="Group:", bg=lf_bg, font=frame_font).place(relx=0.03, rely=0.72)
        self.group_entry = AutocompleteCombobox(left_frame, width=15, font=entry_font, completevalues=group_values)
        self.group_entry.place(relx=.44, rely=0.72)

        ######### BUTTONS #########
        # Add Button
        self.add_button = Button(left_frame, text="Add", font=button_font, width=10,
            command=lambda:[self.add_contact(), hide_widget(self.add_button)])
        hide_widget(self.add_button) # Hides the button when the window opens
        # Edit Button
        self.save_edit_button = Button(left_frame, text="Save", font=button_font, width=10,
            command=lambda:[self.edit_contact(), hide_widget(self.save_edit_button)])
        hide_widget(self.save_edit_button) # Hides the button when the window opens

        """#########################"""
        """ CENTER FRAME COMPONENTS """
        """#########################"""
        
        # Deletes the temporary text in the search bar
        def temp_text(e):
            """ Deletes the temporary text in the
            search bar

            Args:
                e (arg): positional argument
            """            
            self.search_entry.delete(0,"end")

        # SEARCH BAR
        self.search_entry = Entry(center_frame, width=18, 
            font=("Arial", 12), textvariable=self.search_strvar)
        self.search_entry.insert(0, "Search Contacts...")
        self.search_entry.bind("<FocusIn>", temp_text)
        self.search_entry.place(relx=0.1, rely=0.2)

        # Search Button
        Button(center_frame, text="Search", font=button_font, width=12,
            command=lambda:[self.search()]).place(relx=0.23, rely=0.25)
        
        # Add Contact Button
        add_contact_button = Button(center_frame, text="Add Contact", font=button_font, width=12,
                command=lambda:[hide_widget(self.save_edit_button), show_widget(self.add_button)])
        add_contact_button.place(relx=0.24, rely=0.4)
        # View Contact Button
        Button(center_frame, text="View Contact", font=button_font, width=12,
                command=lambda:[self.view_contact()]).place(relx=0.24, rely=0.48)
        # Edit Contact Button
        edit_contact_button = Button(center_frame, text="Edit Contact", font=button_font, width=12,
                command=lambda:[self.view_contact(), self.normal_fields(), hide_widget(self.add_button),show_widget(self.save_edit_button)])
        edit_contact_button.place(relx=0.24, rely=0.56)
        # Delete Contact Button
        Button(center_frame, text="Delete Contact", font=button_font, width=12,
                command=lambda:[self.delete_contact(), hide_widget(self.add_button), 
                hide_widget(self.save_edit_button)]).place(relx=0.24, rely=0.7)
        # Delete All Contacts Button
        Button(center_frame, text="Delete All Contacts", font=button_font, width=15,
                command=lambda:[self.delete_all_contacts(), hide_widget(self.add_button), 
                hide_widget(self.save_edit_button)]).place(relx=0.168, rely=0.76)
        # Clear Fields Button
        Button(center_frame, text="Clear Fields", font=button_font, width=12,
                command=lambda:[self.clear_fields(), hide_widget(self.add_button), 
                hide_widget(self.save_edit_button)]).place(relx=0.24, rely=0.84)


        """########################"""
        """ RIGHT FRAME COMPONENTS """
        """########################"""

        # Frame Label
        Label(right_frame, text="Saved Contacts", bg=rf_bg, font=('Garamond', 16)).place(relx=0.2, rely=0.07)
        # CONTACT LISTBOX
        self.listbox = Listbox(right_frame, selectbackground='Gray82', 
                bg='white smoke', font=entry_font, height=20, width=27)
        self.scroller = Scrollbar(self.listbox, orient=VERTICAL, command=self.listbox.yview)
        self.scroller.place(relx=0.93, rely=0, relheight=1)
        self.listbox.config(yscrollcommand=self.scroller.set)
        self.listbox.place(relx=0.1, rely=0.15)

        # Button to reset the search bar and listbox
        self.back_button = Button(right_frame, text="Back", font=button_font, width=12,
            command=lambda:[self.listbox.delete(0, END), self.list_contacts(), hide_widget(self.back_button),
            self.search_entry.delete(0, END)])
        hide_widget(self.back_button)

        self.list_contacts() # List the contacts when the window opens

if __name__ == "__main__":
    root = tkinter.Tk()
    r = MainWindow(root)
    root.update()
    root.mainloop()

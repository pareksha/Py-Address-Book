from tkinter import *
from PIL import Image, ImageTk
import csv
from collections import OrderedDict


class Contact(object):
    """
    Class Contact stores information of every individual contact.
    A contact is stored in the form of:
    1. Name of the person
    2. Address of the person
    3. Email id of the person
    4. Mobile Number of the person
    """
    def __init__(self, name, address, email, mobile_number):
        self.__name = name
        self.__address = address
        self.__email = email
        self.__mobile_number = mobile_number

    # Setters for encapsulated data
    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_email(self, email):
        self.__email = email

    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number

    # Getters for encapsulated data
    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

    def get_mobile_number(self):
        return self.__mobile_number


class ManageCSV(object):
    """
    Interacts with the .csv file containing all contacts.
    That is, loads Contacts into RAM from Secondary Storage.
    """
    def __init__(self,csv_name):
        self.CSV = open(csv_name)

    def close_csv(self):
        self.CSV.close()

    # Load values to a python dictionary from the .csv file.
    def read_values(self):
        reader = csv.DictReader(self.CSV)
        dict_ = {}
        for row in reader:
            dict_[row['Name']] = [row['Address'], row['Mobile Number'], row['email']]
        self.close_csv()
        return OrderedDict(dict_)


class AddressBookWindow(object):
    """
    Manages the Graphic User Interface.
    GUI is made using tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.root.attributes("-zoomed", True) # Maximises the window.

    # set the image.
    def image(self):
        load = Image.open('addressbook.png')
        render = ImageTk.PhotoImage(load)
        img = Label(self.root, image=render)
        img.image = render
        img.place(x=0, y=50)

    # Add buttons for adding, modifying and deleting contacts.
    def options_frame(self):
        self.frame = Frame(self.root)
        self.new_contact_btn = Button(self.frame, text="Create New Contact", fg="blue", bg="yellow",width=20,height=2,font=('Comic Sans MS',30), command=self.new_contact_window())
        self.new_contact_btn.pack(pady=10)
        modify_contact_btn = Button(self.frame, text="Modify Existing Contact", fg="purple", bg="orange",width=20,font=('Comic Sans MS',30))
        delete_contact_btn = Button(self.frame, text="Delete Contact", fg="white", bg="red",width=20,font=('Comic Sans MS',30))

        modify_contact_btn.pack(pady=10)
        delete_contact_btn.pack(pady=10)
        self.frame.place(x=50, y=600)

    # Add heading.
    def heading_label(self):
        label = Label(self.root, text='My Address Book',font=('Comic Sans MS', 30))
        label.place(x=1000, y=50)

    # Display the address book in GUI.
    def address_book_display(self):
        frame = Frame(self.root)
        frame.place(x=600, y=130)
        row = Text(frame, height=40, width=116, padx=20, pady=10, font=(None, 0))
        row.pack()
        row.insert(END, 'Name' + '\t'*3 + 'Address' + '\t'*6 + 'Mobile Number' + '\t'*2 + 'email\n\n')

        contacts = ManageCSV('AddressBook.csv') # Load contacts from CSV
        contact_dict = contacts.read_values()

        for name in contact_dict:
            row.insert(END, name + '\t'*3 + contact_dict[name][0] + '\t'*6 + contact_dict[name][1] + '\t'*2 + contact_dict[name][2] + '\n')

        row.config(state=DISABLED) # No modification of the contacts in GUI.

    def new_contact_window(self):
        window = Toplevel(self.root)
        window.geometry("1000x600+400+0")


if __name__ == '__main__':
    address_book = AddressBookWindow()
    address_book.image()
    address_book.options_frame()
    address_book.heading_label()
    address_book.address_book_display()
    address_book.root.mainloop()
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
    def __init__(self):
        self.__name = None
        self.__address = None
        self.__email = None
        self.__mobile_number = None

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
    def __init__(self, csv_name):
        self.__CSV = open(csv_name)
        self.csv_name = csv_name

    def __close_csv(self):
        self.__CSV.close()

    # Load values to a python dictionary from the .csv file.
    def read_values(self):
        reader = csv.DictReader(self.__CSV)
        dict_ = {}
        for row in reader:
            dict_[row['Name']] = [row['Address'], row['Mobile Number'], row['email']]
        self.__close_csv()
        return dict_

    def write_values(self, contact=None, dict_=None):
        if contact is not None:
            dict_ = self.read_values()
            dict_[contact.get_name()] = [contact.get_address(), contact.get_mobile_number(), contact.get_email()]
        dict_ = dict(OrderedDict(sorted(dict_.items())))
        self.__CSV = open(self.csv_name, 'w')
        fieldnames = ['Name', 'Address', 'Mobile Number', 'email']
        writer = csv.DictWriter(self.__CSV, fieldnames=fieldnames)
        writer.writeheader()
        for name in dict_:
            writer.writerow({'Name': name, 'Address': dict_[name][0], 'Mobile Number': dict_[name][1], 'email': dict_[name][2]})
        self.__close_csv()


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
        frame = Frame(self.root)
        new_contact_btn = Button(frame, text="Create New Contact", fg="blue", bg="yellow",width=20,height=2,font=('Comic Sans MS',30), command=self.new_contact_window)
        new_contact_btn.pack(pady=10)
        modify_contact_btn = Button(frame, text="Modify Existing Contact", fg="purple", bg="orange",width=20,font=('Comic Sans MS',30), command=self.modify_contact_window)
        modify_contact_btn.pack(pady=10)
        delete_contact_btn = Button(frame, text="Delete Contact", fg="white", bg="red",width=20,font=('Comic Sans MS',30), command= self.delete_contact_window)
        delete_contact_btn.pack(pady=10)
        frame.place(x=50, y=600)

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
        contact_dict = dict(OrderedDict(sorted(contact_dict.items())))

        for name in contact_dict:
            row.insert(END, name + '\t'*3 + contact_dict[name][0] + '\t'*6 + contact_dict[name][1] + '\t'*2 + contact_dict[name][2] + '\n')

        row.config(state=DISABLED) # No modification of the contacts in GUI.

    def new_contact_window(self):
        window = Toplevel(self.root)
        window.geometry("1000x600+400+200")

        frame = Frame(window, height=400, width=600)
        frame.place(anchor='center', relx=.5, rely=.4)

        values = ['Name', 'Address', 'Mobile Number', 'email']
        entries = [str(x) for x in range(4)]

        for value in values:
            label = Label(frame, text=value, font=(None, 20))
            label.grid(row=values.index(value), column=0, sticky=E, pady=10, padx=15)

            entries[values.index(value)] = Entry(frame, font=(None, 20), width=30)
            entries[values.index(value)].grid(row=values.index(value), column=1)

        def get_values():
            values = [entry.get() for entry in entries]

            if values[0] == '':
                warn_label = Label(frame, text="You cannot leave Name blank!", font=(None, 30), fg="red")
                warn_label.grid(columnspan=2, pady=10, padx=15)
            else:
                window.destroy()
                new_contact = Contact()
                new_contact.set_name(values[0])
                new_contact.set_address(values[1])
                new_contact.set_mobile_number(values[2])
                new_contact.set_email(values[3])
                csv = ManageCSV('AddressBook.csv')
                csv.write_values(contact=new_contact)
                self.address_book_display()

        button = Button(frame, text="SUBMIT", font=('Comic Sans MS', 30), width=10, command=get_values)
        button.grid(column=1, sticky=SW, pady=30)

    def modify_contact_window(self):
        window = Toplevel(self.root)
        window.geometry("1000x600+400+200")

        frame = Frame(window, height=400, width=600)
        frame.place(anchor='center', relx=.5, rely=.4)

        values = ['Name', 'Address', 'Mobile Number', 'email']
        entries = [str(x) for x in range(4)]

        for value in values:
            label = Label(frame, text=value, font=(None, 20))
            label.grid(row=values.index(value), column=0, sticky=E, pady=10, padx=15)

            entries[values.index(value)] = Entry(frame, font=(None, 20), width=30)
            entries[values.index(value)].grid(row=values.index(value), column=1)

        def get_values():
            values = [entry.get() for entry in entries]
            csv = ManageCSV('AddressBook.csv')
            dict_ = csv.read_values()
            flag = False

            if values[0] == '':
                text = "Fill in the name you want to modify."
                flag = True
            elif values[0] not in dict_:
                text = "Contact of this name is not present."
                flag = True

            if flag is True:
                warn_label = Label(frame, text=text, font=(None, 20), fg="red")
                warn_label.grid(row=6,column=0,columnspan=2, pady=10)
            else:
                window.destroy()
                print(values)
                for x in range(1, 4):
                    if values[x] is not '':
                        dict_[values[0]][x-1] = values[x]
                csv = ManageCSV('AddressBook.csv')
                csv.write_values(dict_=dict_)
                self.address_book_display()

        button = Button(frame, text="SUBMIT", font=('Comic Sans MS', 30), width=10, command=get_values)
        button.grid(column=1, sticky=SW, pady=30)

        note_label = Label(frame, text="NOTE : Only fill the fields you want to modify along with the name.",
                           font=("Comic Sans MS", 20))
        note_label.grid(columnspan=2, pady=10, padx=15)

    def delete_contact_window(self):
        window = Toplevel(self.root)
        window.geometry("1000x600+400+200")

        frame = Frame(window, height=400, width=600)
        frame.place(anchor='center', relx=.5, rely=.4)

        label_name = Label(frame, text="Name", font=(None, 30))
        label_name.grid(row=0, column=0, pady=10, padx=15)

        entry_name = Entry(frame, font=(None, 30), width=20)
        entry_name.grid(row=0, column=1)

        def get_value():
            name = entry_name.get()
            csv = ManageCSV('AddressBook.csv')
            dict_ = csv.read_values()

            try:
                dict_.pop(name)
            except KeyError:
                label = Label(frame, text="Contact not present in Address Book", font=(None, 30), fg="red")
                label.grid(columnspan=2, pady=10, padx=15)
            else:
                window.destroy()
                csv.write_values(dict_=dict_)
                self.address_book_display()

        button = Button(frame, text="DELETE", font=('Comic Sans MS', 30), width=10, command=get_value)
        button.grid(column=1, sticky=SW, pady=30)


if __name__ == '__main__':
    address_book = AddressBookWindow(Tk())
    address_book.image()
    address_book.options_frame()
    address_book.heading_label()
    address_book.address_book_display()
    address_book.root.mainloop()
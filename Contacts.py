import sqlite3
import tkinter
from tkinter import *
conn = sqlite3.connect('Contacts.db')

#Checks if Contacts table exists and if not, creates the table and populates 2 sample contacts.
try:
    query = "SELECT * from Contacts"
    cursor = conn.execute(query)
except Exception:
    query = "CREATE TABLE Contacts (ID integer PRIMARY KEY autoincrement,Name text, Number text, Email text);"
    conn.execute(query)
    conn.commit()
    query = "INSERT into Contacts (Name, Number, Email) values ('Joe Bloggs', '025022022', 'joebloggs@gmail.com')"
    conn.execute(query)
    conn.commit()
    query = "INSERT into Contacts (Name, Number, Email) values ('Bob Example', '0222222222', 'bob@example.com')"
    conn.execute(query)
    conn.commit()

#Sets up some GUI elements.
root = Tk()

leftPanel = Frame(root)
leftPanel.pack(side = LEFT)

rightPanel = Frame(root)
rightPanel.pack(side = RIGHT)

buttonsContainer = Frame(leftPanel)
buttonsContainer.pack(side = TOP)

contactsContainer = Frame(leftPanel, width=300,height=400)
contactsContainer.pack(side = BOTTOM)



def deleteContact(ID):
    query = "DELETE FROM Contacts WHERE ID = " + str(ID)
    conn.execute(query)
    conn.commit()
    pullContacts(0, "")

def showAllContacts():
    pullContacts(0, "")
    clearRightPanel()

def clearBox():
    for ele in contactsContainer.winfo_children():
      ele.destroy()

def clearRightPanel():
    for ele in rightPanel.winfo_children():
      ele.destroy()
    
def addContact(name, number, email):
    query = "INSERT into Contacts (Name, Number, Email) values ('" + name + "', '" + number + "', '" + email + "')"
    conn.execute(query)
    conn.commit()

def editContact(ID, Name, Number, Email):
    if Name != "":
        query = "UPDATE Contacts SET Name = '" + Name + "' WHERE ID = " + str(ID)
        conn.execute(query)
        conn.commit()
    if Number != "":
        query = "UPDATE Contacts SET Number = '" + Number + "' WHERE ID = " + str(ID)
        conn.execute(query)
        conn.commit()
    if Email != "":
        query = "UPDATE Contacts SET Email = '" + Email + "' WHERE ID = " + str(ID)
        conn.execute(query)
        conn.commit()
    clearRightPanel()
    pullContacts(0, "")

#Pushes the GUI elements used to add contacts to the screen.
def pushAdd():
    clearRightPanel()
    L1 = Label(rightPanel, text="Name")
    L2 = Label(rightPanel, text="Number")
    L3 = Label(rightPanel, text="Email")

    E1 = Entry(rightPanel, bd=5)
    E2 = Entry(rightPanel, bd=5)
    E3 = Entry(rightPanel, bd=5)

    def add():
        addContact(E1.get(), E2.get(), E3.get())
        pullContacts(0, "")

    B1 = tkinter.Button(rightPanel, text ="Add", command = add)

    L1.pack()
    E1.pack()
    L2.pack()
    E2.pack()
    L3.pack()
    E3.pack()
    B1.pack()

#Pushes the update contact GUI elements to the screen.
def pushUpdate(ID, Name):
    clearRightPanel()
    L0 = Label(rightPanel, text="Update: " + Name)
    L1 = Label(rightPanel, text="Name")
    L2 = Label(rightPanel, text="Number")
    L3 = Label(rightPanel, text="Email")

    E1 = Entry(rightPanel, bd=5)
    E2 = Entry(rightPanel, bd=5)
    E3 = Entry(rightPanel, bd=5)

    def add():
        editContact(ID, E1.get(), E2.get(), E3.get())
        pullContacts(0, "")

    B1 = tkinter.Button(rightPanel, text ="Update Contact", command = add)

    L0.pack()
    L1.pack()
    E1.pack()
    L2.pack()
    E2.pack()
    L3.pack()
    E3.pack()
    B1.pack()

#Pushes the search GUI elements to the screen.
def pushSearch():
    clearRightPanel()
    L1 = Label(rightPanel, text="Name")
    E1 = Entry(rightPanel, bd=5)

    def search():
        pullContacts(1, E1.get())
        
    B1 = tkinter.Button(rightPanel, text ="Search Name", command = search)

    L1.pack()
    E1.pack()
    B1.pack()

#Pulls contacts from the database and pushes them to screen. Can utilise parameters to search for particular people.
def pullContacts(option, search):
    if option == 0:
        query = "SELECT * from Contacts"
    if option == 1:
        query = "SELECT * from Contacts WHERE Name like '%" + search + "%'"
    clearBox()
    cursor = conn.execute(query)
    for row in cursor:
        container = Frame(contactsContainer)
        T = Text(container, height=2, width=50)
        delButton = tkinter.Button(container, text ="Delete", command=lambda r=row[0]: deleteContact(r))
        updateButton = tkinter.Button(container, text ="Update", command=lambda r=row[0], n=row[1]: pushUpdate(r, n))
        
        T.insert(END, row[1] + " - " + row[2] + " - " + row[3])
        
        container.pack()
        T.pack(side = LEFT)
        delButton.pack(side = RIGHT)
        updateButton.pack(side = RIGHT)

#Adds buttons - Linked to methods defined above.
B1 = tkinter.Button(buttonsContainer, text ="Add Contact", command = pushAdd)
B4 = tkinter.Button(buttonsContainer, text ="Search Contact", command = pushSearch)
B5 = tkinter.Button(buttonsContainer, text ="Show All Contacts", command = showAllContacts)

B1.pack(side = LEFT)
B4.pack(side = LEFT)
B5.pack(side = LEFT)

#Initial pull of contacts from database to screen.
pullContacts(0, "")

root.mainloop()

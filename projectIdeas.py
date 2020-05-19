from tkinter import Tk, Button, Scrollbar, Listbox, StringVar, Entry, W, E, S, N, END
from tkinter import ttk
from tkinter import messagebox
from postgres_config import dbConfig
import psycopg2 as psyc

# variable containing the connection between the db adapter/driver and the db config file
con = psyc.connect(**dbConfig)

# cursor object - bridge between application and db
cursor = con.cursor()

# print(con)

# ---------------------------------------------
#          DB CLASS
# ---------------------------------------------


# class containing the database methods (functions)


class ProjectDb:

    def __init__(self):
        # setting the db config - so can be used when the methods are called
        self.con = psyc.connect(**dbConfig)
        self.cursor = con.cursor()
        print('DB connection successful')
        print(con)

    def __del__(self):
        self.con.close()

    # select * function
    def view(self):
        self.cursor.execute('SELECT * FROM project_ideas')
        rows = self.cursor.fetchall()
        return rows

    def search(self, name, category, description):
        '''
        sql = 'SELECT * FROM project_ideas WHERE p_name LIKE %%%s%% OR p_category LIKE %%%s%% OR p_description LIKE \
        %%%s%%'

        self.cursor.execute(sql, [name, category, description])

        rows = self.cursor.fetchall()

        return rows

        '''

        s = ''
        name = name
        category = category
        description = description

        if category is not True and description is not True:
            # sql = 'Select * FROM project_ideas WHERE p_name LIKE %s '
            # name = name + '%'
            s = self.cursor.execute('''Select * FROM project_ideas WHERE p_name LIKE ' {}% ' '''.format(name))
        elif description is not True:
            # sql = 'Select * FROM project_ideas WHERE p_name LIKE %s AND p_category LIKE %s'
            name = name + '%'
            category = category + '%'
            s = self.cursor.execute('Select * FROM project_ideas WHERE p_name LIKE {} AND p_category LIKE {}'.format(name, category))
        elif category is True and description is True:
            # sql = 'SELECT * FROM project_ideas WHERE p_name LIKE %s AND p_category LIKE %s AND p_description LIKE %s'
            name = name + '%'
            category = category + '%'
            description = description + '%'
            s = self.cursor.execute('SELECT * FROM project_ideas WHERE p_name LIKE %s AND p_category LIKE %s AND \
                                    p_description LIKE %s'.format(name, category, description))
        else:
            messagebox.showinfo(title='Invalid Search', message='Invalid search - name is minimum requirment for serach')
            print(name, category, description)

        return s

        '''rows = self.cursor.fetchall()

        return rows'''

    # insert function
    def insert(self, name, category, description):
        # variable storing the sql query - pointing to the table and columns
        sql = "INSERT INTO project_ideas (p_name, p_category, p_description) VALUES (%s, %s, %s)"
        # variable to store the user input
        values = [name, category, description]
        self.cursor.execute(sql, values)
        self.con.commit()
        messagebox.showinfo(title='Project Ideas Database', message='New project idea successfully inserted into'
                                                                    'project ideas table')

    # update function
    def update(self, name, category, description, id):
        update_sql = 'UPDATE project_ideas SET p_name = %s, p_category = %s, p_description = %s WHERE id = %s'
        self.cursor.execute(update_sql, [name, category, description, id])
        self.con.commit()
        messagebox.showinfo(title='Project Ideas Database', message='Project details have been successfully updated')

    # delete function
    def delete(self, id):
        del_sql = 'DELETE FROM project_ideas WHERE id = %s'
        self.cursor.execute(del_sql, [id])
        self.con.commit()
        messagebox.showinfo(title='Project Ideas Database', message='Project successfully deleted from database')


# --------------------------------
# instance of the ProjectDB class
# -------------------------------
db = ProjectDb()

# ----------------------------------
#          PROGRAM FUNCTIONS
# ----------------------------------

# event click function - so the program can handle events from the mouse clicks in the list box
def get_selected_row(event):
    global selected_tuple

    # create variable to find out the index of the selected row in the list_box
    index = list_box.curselection()[0]

    # variable - storing the item  returned from the index selected in the list box
    selected_tuple = list_box.get(index)

    # clear whats in pName_entry - 0 indicates from the start and to the end
    pName_entry.delete(0, 'end')
    # from the last end - insert the first item in the selected tuple in the pName_entry box
    pName_entry.insert('end', selected_tuple[1])
    pCategory_entry.delete(0, 'end')
    pCategory_entry.insert('end', selected_tuple[2])
    pDescription_entry.delete(0, 'end')
    pDescription_entry.insert('end', selected_tuple[3])


# function that works in conjunction with the view method from the db class
def view_records():
    # Clear whatever is in the list_box
    list_box.delete(0, 'end')
    # run a for loop to list through the records stored within the db.view method from the ProjectDb class
    for i in db.view():
        # insert each row into the list_box
        list_box.insert('end', i)


def search_record():

    list_box.delete(0, 'end')

    result = db.search(pName_text.get(), pCategory_text.get(), pDescription_text.get())

    list_box.insert(result[0])
    #for i in result:
        #list_box.insert('end', i)





# function that works in conjunction with the insert method from the db class
def add_record():
    # using the db instance, access the insert method and pass in the text variable for each entry box
    db.insert(pName_text.get(), pCategory_text.get(), pDescription_text.get())
    # clear the list_box
    list_box.delete(0, 'end')
    # insert the text variable capture from the entry boxes, into the list_box
    list_box.insert('end', (pName_text.get(), pCategory_text.get(), pDescription_text.get()))
    # clear entry boxes
    pName_entry.delete(0, 'end')
    pCategory_entry.delete(0, 'end')
    pDescription_entry.delete(0, 'end')
    con.commit()
    view_records()


# function that works in conjunction with the delete method from the db class
def del_record():
    # using the db instance, accessing the delete method and passing in the selected_tuple variable from the event \
    # handler function
    db.delete(selected_tuple[0])
    con.commit()
    view_records()


# function that clear the screen
def clear_screen():
    list_box.delete(0, 'end')
    pName_entry.delete(0, 'end')
    pCategory_entry.delete(0, 'end')
    pDescription_entry.delete(0, 'end')


def update_record():
    # using the db instance, access the update method and pass the text variables using the get built-in function
    db.update(pName_text.get(), pCategory_text.get(), pDescription_text.get(), selected_tuple[0])
    # clear the input boxes
    pName_entry.delete(0, 'end')
    pCategory_entry.delete(0, 'end')
    pDescription_entry.delete(0, 'end')
    con.commit()
    view_records()


def on_closing():
    # create instance on the db object to be used within function
    dd = db
    # open message box and access askokcancel builtin function
    if messagebox.askokcancel('QUIT', 'Are you sure you want to quit?'):
        # destroys the main window - closing the program
        window.destroy()
        # delete the db connection
        del dd


# -----------------------------------------------------
#      GUI - for DB application
# ----------------------------------------------------
# set the properties on the gui window
window = Tk() # main window

window.title('Research Project Ideas DB')
window .geometry('1250x550')
window.configure(background='light grey')
window.resizable(width=False, height=False)

# create project name label and entry box
pName_label = ttk.Label(window, text='Project Name', background='light grey', font=('Arial', 14))
pName_label.grid(row=0, column=0, sticky=W)
pName_text = StringVar()
pName_entry = ttk.Entry(window, width=24, background='light grey', textvariable=pName_text)
pName_entry.grid(row=0, column=1, sticky=W)

# create project category label and entry box
pCategory_label = ttk.Label(window, text='Project Category', background='light grey', font=('Arial', 14))
pCategory_label.grid(row=0, column=2, sticky=W)
pCategory_text = StringVar()
pCategory_entry = ttk.Entry(window, width=24, background='light grey', textvariable=pCategory_text)
pCategory_entry.grid(row=0, column=3, sticky=W)

# create project description label and entry box
pDescription_label = ttk.Label(window, text='Project Description', background='light grey', font=('Arial', 14))
pDescription_label.grid(row=0, column=4, sticky=W)
pDescription_text = StringVar()
pDescription_entry = ttk.Entry(window, width=24, background='light grey', textvariable=pDescription_text)
pDescription_entry.grid(row=0, column=5, sticky=W)

# create list box - where database result will displayed
list_box = Listbox(window, height=16, width=80, font='arial 14 bold', bg='white')
list_box.grid(row='3', column='0', columnspan=14, sticky=W + E, pady=40, padx=15)
# the list box widget/space needs to bind with the get_selected_row function - we need to pass in the 'ListboxSelect' \
# property
list_box.bind('<<ListboxSelect>>', get_selected_row)

# create the scroll back to be in included within the list box, allow yo scroll through multiple results returned
scroll_bar = Scrollbar(window)
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

# configure both scrollbar and list box
list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview())

# create clear button
clr_btn = Button(window, text='Clear', bg='white', fg='black', font='arial 16 bold', command=clear_screen)
clr_btn.grid(row=4, column=0, sticky=W)

# create add button
add_btn = Button(window, text='Add Project', bg='white', fg='black', font='Arial 16 bold', command=add_record)
add_btn.grid(row=4, column='1', sticky='W')

# create edit button
edit_btn = Button(window, text='Edit Project', bg='white', fg='black', font='arial 16 bold', command=update_record)
edit_btn.grid(row=4, column=2, sticky=W)

# create delete button
del_btn = Button(window, text='Delete Project', bg='white', fg='black', font='arial 16 bold', command=del_record)
del_btn.grid(row=4, column=3, sticky=W)

# create search button
search_btn = Button(window, text='Search', bg='white', fg='black', font='arial 16 bold', command=search_record)
search_btn.grid(row=4, column=5, sticky=E)

# create view button
view_btn = Button(window, text='View all records', bg='white', fg='black', font='arial 16 bold', command=view_records)
view_btn.grid(row=4, column=6, sticky=E)

# create exit button
exit_btn = Button(window, text='Exit', bg='black', fg='white', font='arial 16 bold', command=window.destroy)
exit_btn.grid(row=4, column=20, sticky=E)




window.mainloop()

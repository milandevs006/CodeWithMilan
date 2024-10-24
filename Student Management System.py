import mysql.connector
from tkinter import *
from tkinter import messagebox

def connect_db():
    """Connect to the MySQL database."""
    global mydb
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="milandev",
            database="StudentDB"
        )
        messagebox.showinfo("Connection", "Database connection successful!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")

def add_student(reg_no, name, dept, cgpa):
    """Add a student to the database."""
    try:
        cur = mydb.cursor()
        cur.execute("INSERT INTO students (reg_no, name, dept, cgpa) VALUES (%s, %s, %s, %s)",
                    (reg_no, name, dept, cgpa))
        mydb.commit()
        messagebox.showinfo("Success", "Student added successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        cur.close()
    view_students()

def view_students():
    """Fetch and display all students from the database."""
    cur = mydb.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    list_box.delete(0, END)
    for row in rows:
        list_box.insert(END, row)
    cur.close()

def search_students(name):
    """Search for students by name."""
    cur = mydb.cursor()
    cur.execute("SELECT * FROM students WHERE name LIKE %s", ('%'+name+'%',))
    rows = cur.fetchall()
    list_box.delete(0, END)
    for row in rows:
        list_box.insert(END, row)
    cur.close()

def update_student(reg_no, name, dept, cgpa):
    """Update a student's information in the database."""
    try:
        cur = mydb.cursor()
        cur.execute("UPDATE students SET name=%s, dept=%s, cgpa=%s WHERE reg_no=%s",
                    (name, dept, cgpa, reg_no))
        mydb.commit()
        messagebox.showinfo("Success", "Student updated successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        cur.close()
    view_students()

def delete_student(reg_no):
    """Delete a student from the database."""
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM students WHERE reg_no=%s", (reg_no,))
        mydb.commit()
        messagebox.showinfo("Success", "Student deleted successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        cur.close()
    view_students()

def get_selected_row(event):
    """Handle row selection events."""
    try:
        global selected_tuple
        index = list_box.curselection()[0]
        selected_tuple = list_box.get(index)
        entry_reg_no.delete(0, END)
        entry_reg_no.insert(END, selected_tuple[0])
        entry_name.delete(0, END)
        entry_name.insert(END, selected_tuple[1])
        entry_dept.delete(0, END)
        entry_dept.insert(END, selected_tuple[2])
        entry_cgpa.delete(0, END)
        entry_cgpa.insert(END, selected_tuple[3])
    except IndexError:
        pass

root = Tk()
root.title("Student Database System")
root.geometry('1920x1080')


Label(root, text='Reg No').grid(row=0, column=0)
Label(root, text='Name').grid(row=0, column=2)
Label(root, text='Dept').grid(row=1, column=0)
Label(root, text='CGPA').grid(row=1, column=2)

entry_reg_no = Entry(root)
entry_reg_no.grid(row=0, column=1)
entry_name = Entry(root)
entry_name.grid(row=0, column=3)
entry_dept = Entry(root)
entry_dept.grid(row=1, column=1)
entry_cgpa = Entry(root)
entry_cgpa.grid(row=1, column=3)


list_box = Listbox(root, height=10, width=50)
list_box.grid(row=3, column=0, columnspan=4)
sb = Scrollbar(root)
sb.grid(row=3, column=4)
list_box.configure(yscrollcommand=sb.set)
sb.configure(command=list_box.yview)
list_box.bind('<<ListboxSelect>>', get_selected_row)


Button(root, text="Add", command=lambda: add_student(entry_reg_no.get(), entry_name.get(), entry_dept.get(), entry_cgpa.get())).grid(row=4, column=0)
Button(root, text="Update", command=lambda: update_student(entry_reg_no.get(), entry_name.get(), entry_dept.get(), entry_cgpa.get())).grid(row=4, column=1)
Button(root, text="Delete", command=lambda: delete_student(selected_tuple[0])).grid(row=4, column=2)
Button(root, text="Search", command=lambda: search_students(entry_name.get())).grid(row=4, column=3)
Button(root, text="View all", command=view_students).grid(row=4, column=4)

connect_db()  
root.mainloop()  

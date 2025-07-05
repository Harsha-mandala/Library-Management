import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

# Database setup
connector = sqlite3.connect('library.db')
cursor = connector.cursor()
connector.execute(
    'CREATE TABLE IF NOT EXISTS Library (BK_NAME TEXT, BK_ID TEXT PRIMARY KEY NOT NULL, AUTHOR_NAME TEXT, BK_STATUS TEXT, CARD_ID TEXT)'
)

# Functions
def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'Enter Issuer\'s Card ID:')
    if not Cid:
        mb.showerror('Missing ID', 'Issuer ID cannot be empty.')
    else:
        return Cid

def display_records():
    tree.delete(*tree.get_children())
    for record in connector.execute('SELECT * FROM Library'):
        tree.insert('', END, values=record)

def clear_fields():
    bk_status.set('Available')
    for var in [bk_id, bk_name, author_name, card_id]:
        var.set('')
    bk_id_entry.config(state='normal')
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

def clear_and_display():
    clear_fields()
    display_records()

def add_record():
    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')
    surety = mb.askyesno('Confirm Entry', 'Add this record? Book ID cannot be changed later.')
    if surety:
        try:
            connector.execute(
                'INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                (bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(), card_id.get()))
            connector.commit()
            clear_and_display()
            mb.showinfo('Success', 'Record added successfully.')
        except sqlite3.IntegrityError:
            mb.showerror('Duplicate Book ID', 'This Book ID already exists.')

def view_record():
    if not tree.focus():
        mb.showerror('No Selection', 'Select a record to view.')
        return
    selection = tree.item(tree.focus())['values']
    bk_name.set(selection[0])
    bk_id.set(selection[1])
    author_name.set(selection[2])
    bk_status.set(selection[3])
    card_id.set(selection[4] if len(selection) > 4 else '')

def update_record():
    def update():
        if bk_status.get() == 'Issued':
            card_id.set(issuer_card())
        else:
            card_id.set('N/A')
        cursor.execute('UPDATE Library SET BK_NAME=?, BK_STATUS=?, AUTHOR_NAME=?, CARD_ID=? WHERE BK_ID=?',
                       (bk_name.get(), bk_status.get(), author_name.get(), card_id.get(), bk_id.get()))
        connector.commit()
        clear_and_display()
        edit.destroy()
        bk_id_entry.config(state='normal')
        clear.config(state='normal')
    view_record()
    bk_id_entry.config(state='disable')
    clear.config(state='disable')
    edit = Button(left_frame, text='Save Update', font=btn_font, bg=btn_hl_bg, fg='white', width=20, command=update)
    edit.place(x=50, y=375)

def remove_record():
    if not tree.selection():
        mb.showerror('No Selection', 'Select a record to delete.')
        return
    selection = tree.item(tree.focus())['values']
    cursor.execute('DELETE FROM Library WHERE BK_ID=?', (selection[1],))
    connector.commit()
    tree.delete(tree.focus())
    mb.showinfo('Deleted', 'Record deleted.')
    clear_and_display()

def delete_inventory():
    if mb.askyesno('Confirm', 'Delete all records? This cannot be undone.'):
        tree.delete(*tree.get_children())
        cursor.execute('DELETE FROM Library')
        connector.commit()

def change_availability():
    if not tree.selection():
        mb.showerror('No Selection', 'Select a book to change status.')
        return
    selection = tree.item(tree.focus())['values']
    BK_id = selection[1]
    BK_status = selection[3]
    if BK_status == 'Issued':
        if mb.askyesno('Return Confirmed?', 'Has the book been returned?'):
            cursor.execute('UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?', ('Available', 'N/A', BK_id))
            connector.commit()
        else:
            mb.showinfo('Not Returned', 'Book status remains Issued.')
    else:
        cursor.execute('UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?', ('Issued', issuer_card(), BK_id))
        connector.commit()
    clear_and_display()

# UI Variables and Styles
lf_bg = '#f0e6fa'  # Light lavender
rtf_bg = '#b3c6e7'  # Soft blue
rbf_bg = '#e6f2ff'  # Very light blue
btn_hl_bg = '#6a5acd'  # Slate blue
lbl_font = ('Verdana', 12)
entry_font = ('Segoe UI', 11)
btn_font = ('Segoe UI Semibold', 12)

# Main Window
root = Tk()
root.title('Library Management System')
root.geometry('1050x570')
root.resizable(0, 0)
root.configure(bg='#eaf6fb')

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Arial Rounded MT Bold", 18, 'bold'),
      bg=btn_hl_bg, fg='white').pack(side=TOP, fill=X)

# StringVars
bk_status = StringVar()
bk_name = StringVar()
bk_id = StringVar()
author_name = StringVar()
card_id = StringVar()

# Frames
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=40, relwidth=0.28, relheight=0.94)

RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.28, y=40, relheight=0.18, relwidth=0.72)

RB_frame = Frame(root, bg=rbf_bg)
RB_frame.place(relx=0.28, rely=0.22, relheight=0.78, relwidth=0.72)

# Left Frame Widgets
Label(left_frame, text='Book Name', bg=lf_bg, font=lbl_font).place(x=30, y=30)
Entry(left_frame, width=25, font=entry_font, textvariable=bk_name).place(x=30, y=60)

Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).place(x=30, y=100)
bk_id_entry = Entry(left_frame, width=25, font=entry_font, textvariable=bk_id)
bk_id_entry.place(x=30, y=130)

Label(left_frame, text='Author Name', bg=lf_bg, font=lbl_font).place(x=30, y=170)
Entry(left_frame, width=25, font=entry_font, textvariable=author_name).place(x=30, y=200)

Label(left_frame, text='Status', bg=lf_bg, font=lbl_font).place(x=30, y=240)
dd = OptionMenu(left_frame, bk_status, 'Available', 'Issued')
dd.configure(font=entry_font, width=12, bg='#e0d7f5')
dd.place(x=30, y=270)

submit = Button(left_frame, text='Add Record', font=btn_font, bg=btn_hl_bg, fg='white', width=20, command=add_record)
submit.place(x=30, y=320)

clear = Button(left_frame, text='Clear Fields', font=btn_font, bg=btn_hl_bg, fg='white', width=20, command=clear_fields)
clear.place(x=30, y=370)

# Right Top Frame Buttons
Button(RT_frame, text='Delete Record', font=btn_font, bg=btn_hl_bg, fg='white', width=16, command=remove_record).place(x=20, y=30)
Button(RT_frame, text='Delete All', font=btn_font, bg=btn_hl_bg, fg='white', width=16, command=delete_inventory).place(x=200, y=30)
Button(RT_frame, text='Update Details', font=btn_font, bg=btn_hl_bg, fg='white', width=16, command=update_record).place(x=380, y=30)
Button(RT_frame, text='Change Status', font=btn_font, bg=btn_hl_bg, fg='white', width=16, command=change_availability).place(x=560, y=30)

# Right Bottom Frame Table
Label(RB_frame, text='Book Inventory', bg=rbf_bg, font=("Arial Rounded MT Bold", 15, 'bold')).pack(side=TOP, fill=X)

tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Issuer Card ID'))
XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree.heading('Book Name', text='Book Name', anchor=CENTER)
tree.heading('Book ID', text='Book ID', anchor=CENTER)
tree.heading('Author', text='Author', anchor=CENTER)
tree.heading('Status', text='Status', anchor=CENTER)
tree.heading('Issuer Card ID', text='Issuer Card ID', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=180, stretch=NO)
tree.column('#2', width=80, stretch=NO)
tree.column('#3', width=140, stretch=NO)
tree.column('#4', width=110, stretch=NO)
tree.column('#5', width=120, stretch=NO)

tree.place(y=35, x=0, relheight=0.9, relwidth=1)

clear_and_display()

root.mainloop()


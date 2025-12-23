from sqlalchemy import create_engine, exc
import pyodbc
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import Function_call_test

def RadioVar():
    searchRB=RBvar.get()
    
def my_search(*args):
    search = filtervar.get().capitalize()
    searchRB = RBvar.get()

    if searchRB == ('Value 1'):
        facilities2 = pd.read_sql(qfacilities, conn)
        #filterdf = facilities2.isin([search]).any().any()
        search_str = str(search)
        facilities2['facility_id'] = facilities2['facility_id'].astype(str)
        filterdf = facilities2.loc[facilities2['facility_id'].str.contains(search_str)]
        r_set2 = filterdf.to_numpy().tolist()
    elif searchRB == ('Value 2'):
            facilities2 = pd.read_sql(qfacilities, conn)
        #filterdf = facilities2.isin([search]).any().any()
            filterdf = facilities2.loc[facilities['facility_name'].str.contains(search, case=False)]
            r_set2 = filterdf.to_numpy().tolist()
    else:
        facilities2 = pd.read_sql(qfacilities, conn)
        #filterdf = facilities2.isin([search]).any().any()
        filterdf = facilities2.loc[facilities['city'].str.contains(search, case=False, na=False)]
        r_set2 = filterdf.to_numpy().tolist()

    global count
    count=0
    clearTree=my_tree.get_children()
    my_tree.delete(*clearTree)

    for record in r_set2:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3], record[4], record[5]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3], record[4], record[5]), tags=('oddrow',))
        count += 1

def select_rec(e):
    # clear entry boxes
    fac_entry.delete(0, END)
    nm_entry.delete(0, END)
    addr_entry.delete(0, END)
    ct_entry.delete(0, END)
    st_entry.delete(0, END)
    zip_entry.delete(0, END)
    tree_selected = my_tree.focus()
    tree_values = my_tree.item(tree_selected, "values")
    fac_entry.insert(0, tree_values[0])
    nm_entry.insert(0, tree_values[1])
    addr_entry.insert(0, tree_values[2])
    ct_entry.insert(0, tree_values[3])
    st_entry.insert(0, tree_values[4])
    zip_entry.insert(0, tree_values[5])

def exe_func():
    tree_selected2 = my_tree.focus()
    tree_values2 = my_tree.item(tree_selected2, "values")
    fac_id = tree_values2[0]
    fac_nm = tree_values2[1]
    Function_call_test.wells(fac_id_pass=fac_id)
    #messagebody = f"You Selected: Facility ID {fac_id} Facility Name {fac_nm}, This search can now be used to execute another function"
    #messagebox.showinfo("Execute Function", messagebody)

#  Database connection and query
try:
    conn = ("mssql+pyodbc://@DMAPSQL1/EQuIS?driver=SQL Server")
    engine = create_engine(conn)
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate =='08001':
        messagebox.showerror("Connection Error", "Connection Failed due to network or server issues")
        exit()
    else:
        mess = f"Connection Failed: {sqlstate}"
        messagebox.showerror("Connection Error", mess)
        exit()
        
qfacilities =  'SELECT [facility_id], [facility_name], [address_1], [city], [state], [postal_code] FROM [EQuIS].[dbo].[dt_facility] ORDER BY [facility_id]'
facilities = pd.read_sql(qfacilities, conn)
r_set = facilities.to_numpy().tolist()

# Set up Frame and tree view

root = tk.Tk()
root.title("Search EQuIS")
root.geometry("1000x500")
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Treeview', bakground=[('selected',"#347083")])

search_frame=LabelFrame(root, text="Search")
search_frame.pack(anchor=W, padx=20)

search_label = Label(search_frame, text="Search", width=5, font=18)
search_label.grid(row=1, column=0, padx=15)

filtervar = StringVar()
search_entry = Entry(search_frame, width=35, bg="yellow", font=18, textvariable=filtervar)
search_entry.grid(row=1, column=1, padx=1)
filtervar.trace("w", my_search)
#search_entry.bind("<KeyRelease>", my_search)
RBvar = StringVar(value="Value 2")
R1 = Radiobutton(search_frame, text="Facility ID", variable=RBvar, value="Value 1", command=RadioVar)
R2 = Radiobutton(search_frame, text="Facility Name", variable=RBvar, value="Value 2", command=RadioVar)
R3 = Radiobutton(search_frame, text="City", variable=RBvar, value="Value 3", command=RadioVar)
R1.grid(row=1, column=2)
R2.grid(row=1, column=3)
R3.grid(row=1, column=4)

#search_button = Button(search_frame, text="Search", width=7, font=18, command=lambda: my_search())
#search_button.grid(row=1, column=3, padx=2)

tree_frame = Frame(root)
tree_frame.pack(pady=10)
tree_scroll=Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree=ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")

my_tree.pack()

tree_scroll.config(command=my_tree.yview)

# Define columns (excluding the default '#0' column)
my_tree['columns'] = ("facility_id", "facility_name", "address_1","city","state","postal_code")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("facility_id", anchor=W, width=70)
my_tree.column("facility_name", anchor=W, width=250)
my_tree.column("address_1", anchor=W, width=200)
my_tree.column("city", anchor=CENTER, width=140)
my_tree.column("state", anchor=CENTER, width=70)
my_tree.column("postal_code", anchor=CENTER, width=70)


# Define column headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("facility_id", text="Facility ID", anchor=W)
my_tree.heading("facility_name", text="Facility Name", anchor=W)
my_tree.heading("address_1", text="Address 1", anchor=W)
my_tree.heading("city", text="City", anchor=CENTER)
my_tree.heading("state", text="State", anchor=CENTER)
my_tree.heading("postal_code", text="Postal Code", anchor=CENTER)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

global count
count=0

for record in r_set:
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3], record[4], record[5]), tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3], record[4], record[5]), tags=('oddrow',))
    count += 1


data_frame = LabelFrame(root, text="Selected Record", borderwidth=0)
data_frame.pack(anchor=W, padx=20)

fac_lbl = Label(data_frame, text="Facility ID")
fac_lbl.grid(row=0, column=0, padx=10, pady=10)
fac_entry = Entry(data_frame, width=20)
fac_entry.grid(row=0, column=1, padx=10, pady=10)

nm_lbl = Label(data_frame, text="Facility Name")
nm_lbl.grid(row=0, column=2, padx=10, pady=10)
nm_entry = Entry(data_frame, width=20)
nm_entry.grid(row=0, column=3, padx=10, pady=10)

addr_lbl = Label(data_frame, text="Address")
addr_lbl.grid(row=1, column=0, padx=10, pady=10)
addr_entry = Entry(data_frame)
addr_entry.grid(row=1, column=1, padx=10, pady=10)

ct_lbl = Label(data_frame, text="City")
ct_lbl.grid(row=1, column=2, padx=10, pady=10)
ct_entry = Entry(data_frame)
ct_entry.grid(row=1, column=3, sticky=W, padx=10, pady=10)

st_lbl = Label(data_frame, text="State")
st_lbl.grid(row=1, column=4, sticky=W, padx=10, pady=10)
st_entry = Entry(data_frame)
st_entry.grid(row=1, column=5, sticky=W, padx=10, pady=10)

zip_lbl = Label(data_frame, text="Postal Code")
zip_lbl.grid(row=1, column=6, padx=10, pady=10)
zip_entry = Entry(data_frame)
zip_entry.grid(row=1, column=7, padx=10, pady=10)

button_frame = LabelFrame(root, text="Commands")
button_frame.pack(anchor=W, padx=20)

sel_button = Button(button_frame, text="Execute Function", command=exe_func)
sel_button.grid(row=0, column=0, padx=10, pady=10)

my_tree.bind("<ButtonRelease-1>", select_rec)

root.mainloop()
#conn.close()

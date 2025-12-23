from sqlalchemy import create_engine
import pyodbc
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk

def wells(fac_id_pass):
    conn = ("mssql+pyodbc://@DMAPSQL1/EQuIS?driver=SQL Server")
    engine = create_engine(conn)
    fac_id = fac_id_pass
    qfacilities =  f'SELECT [facility_id], [sys_loc_code], [well_id], [top_casing_elev], [depth_of_well] FROM [EQuIS].[dbo].[dt_well] WHERE [EQuis].[dbo].[dt_well].[facility_id]={fac_id}'
    facilities = pd.read_sql(qfacilities, conn)
    r_set = facilities.to_numpy().tolist()

    root = tk.Tk()
    root.title("Search EQuIS")
    root.geometry("1000x600")
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
    style.map('Treeview', bakground=[('selected',"#347083")])

    tree_frame = Frame(root)
    tree_frame.pack(pady=10)
    tree_scroll=Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree=ttk.Treeview(tree_frame, height=20, yscrollcommand=tree_scroll.set, selectmode="extended")

    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    # Define columns (excluding the default '#0' column)
    my_tree['columns'] = ("facility_id", "sys_loc_code", "well_id","top_casing_elev","depth_of_well")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("facility_id", anchor=W, width=70)
    my_tree.column("sys_loc_code", anchor=W, width=250)
    my_tree.column("well_id", anchor=W, width=200)
    my_tree.column("top_casing_elev", anchor=CENTER, width=140)
    my_tree.column("depth_of_well", anchor=CENTER, width=70)

    # Define column headings
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("facility_id", text="Facility ID", anchor=W)
    my_tree.heading("sys_loc_code", text="System Loction Code", anchor=W)
    my_tree.heading("well_id", text="Well ID", anchor=W)
    my_tree.heading("top_casing_elev", text="Top Of Casing Elevation", anchor=CENTER)
    my_tree.heading("depth_of_well", text="Depth of Well", anchor=CENTER)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")

    global count
    count=0

    for record in r_set:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3], record[4]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3], record[4]), tags=('oddrow',))
        count += 1

    root.mainloop()
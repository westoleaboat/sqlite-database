from tkinter import *
from tabulate import tabulate
import sqlite3


class Content:
    def __init__(self, root):

        #create database or connect to database
        conn = sqlite3.connect('sample-database.db')
        
        #create cursor
        c = conn.cursor()
        
        #create table
        try:

            c.execute("""CREATE TABLE profile (
            
                     brewer text,
                     brew_date text,
                     batch_size integer
                    
                     )""")
                    #end of TABLE profile

        except sqlite3.OperationalError:
            print('A database already exists, nothing created')


        def update():
            conn=sqlite3.connect('sample-database.db')
            #create cursor to generate commands
            c=conn.cursor()

            record_id = ID_of_record_to_delete.get()

            c.execute("""UPDATE profile SET
                brewer = :brewer,
                brew_date = :brew_date,
                batch_size = :batch_size

                WHERE oid = :oid""",
                {
                'brewer': brewer_editor.get(),
                'brew_date': brew_date_editor.get(),
                'batch_size': batch_size_editor.get(),
                'oid': record_id
                })
            conn.commit()
            conn.close()
            editor.destroy()

        def edit():
            #editor will open a new window in where to edit data
            global editor
            editor=Tk()
            editor.title('EDIT DATABASE')
            conn = sqlite3.connect('sample-database.db')
            # create cursor to generate commands
            c=conn.cursor()

            record_ID = ID_of_record_to_delete.get()
            #query the database
            try:

                c.execute("SELECT *, oid FROM profile WHERE oid = " + record_ID)
            except sqlite3.OperationalError:
                print('add a number to edit')
            records = c.fetchall()

            #create global variables for text box names
            global brewer_editor
            global brew_date_editor
            global batch_size_editor


            print_records =''

            for record in records:
                print_records += str(record[0]) + " "  + str(record[1]) + "\n"

            brewer_editor = Entry(editor)
            brewer_editor.grid(row=1, column=1)#, columnspan=3)#, sticky="we", padx=(0, XmarginColumn0), pady=(Ymargin2, 0))

            brew_date_editor = Entry(editor)
            brew_date_editor.grid(row=2, column=1)#, columnspan=3) #, sticky="we", padx=(0, XmarginColumn0))

            batch_size_editor = Entry(editor) #, width=width2)
            batch_size_editor.grid(row=3, column=1)#, sticky="w", padx=(0, XmarginColumn0))



            brewer_label = Label(editor, text='Brewer: ')
            brewer_label.grid(row=1, column=0) #, pady=(Ymargin2, 0), sticky="w", padx=(XmarginColumn0))

            brew_date_label = Label(editor, text='Brew Date: ')
            brew_date_label.grid(row=2, column=0) #, sticky="w", padx=(XmarginColumn0))

            batch_size_label = Label(editor, text='Batch Size: ')
            batch_size_label.grid(row=3, column=0) #, sticky="w", padx=(XmarginColumn0, 0))

        
            #loop through results
            for record in records:
                brewer_editor.insert(0, record[0])
                brew_date_editor.insert(0, record[1])
                batch_size_editor.insert(0, record[2])

            edit_btn = Button(editor, text='sabe', command=update)
            edit_btn.grid(row=34, column=5)

        #create function to delete record
        def delete():

            conn = sqlite3.connect('sample-database.db')
            c = conn.cursor()
            #delete a record
            record_ID = ID_of_record_to_delete.get()
            try:
                c.execute("DELETE from profile WHERE oid= " + ID_of_record_to_delete.get())
            except sqlite3.OperationalError:
                #print('add a number to delete')
                pass

            ID_of_record_to_delete.delete(0, END)

            conn.commit()

            conn.close()
            query()

        def delete_empty():
            conn = sqlite3.connect('sample-database.db')
            c = conn.cursor()
            records = c.fetchall()
            #c.execute("DELETE from profile WHERE ")
            

######## get al empty records 


            c.execute("DELETE from profile WHERE brewer = ''")

            conn.commit()
            conn.close()

      #      for record in records:
      #          if record == '':
      #              record.delete("1.0", "end")
            query()

#create submit function to database
        def submit():

            conn = sqlite3.connect('sample-database.db')
            c = conn.cursor()

            c.execute("INSERT INTO profile VALUES (:brewer, :brew_date, :batch_size)",

            {
            'brewer': brewer.get(),
            'brew_date': brew_date.get(),
            'batch_size': batch_size.get()
            })

            conn.commit()
            conn.close()

            brewer.delete(0, END)
            brew_date.delete(0, END)
            batch_size.delete(0, END)
            query()

        def query():
            conn = sqlite3.connect('sample-database.db')
            #create cursor to generate commands
            c = conn.cursor()
            #query the database
            c.execute("SELECT *, oid FROM profile")
            records = c.fetchall()

            show_txt['state']='normal'
            # delete old db info
            show_txt.delete("1.0", "end")
            #for loop
            print_records = ''


            for record in records:

                print_records += str(record[3])+ '\t' + str(record[0])+ '\t'  + str(record[1])+ '\t'  + str(record[2]) + "\n"

            print("{:<8} {:<15} {:<10} {:<10}".format('ID#','Tool','Amount','Warehouse'))
            for record in records:
                id1, tool, amount, warehouse = record
                print("{:<8} {:<15} {:<10} {:<10}".format( str(record[3]),str(record[0]),str(record[1]),str(record[2])))


            show_txt.insert(END, print_records)
            show_txt['state']='disabled'

            conn.commit()

            conn.close()


        new_item_lf = LabelFrame(text='New item',font='Verdana 15')
        new_item_lf.grid(row=0, column=0, rowspan=4, columnspan=2,pady=20, padx=20)

        manage_item_lf = LabelFrame(text='Manage Inventory',font='Verdana 15')
        manage_item_lf.grid(row=4, column=0, rowspan=4, columnspan=2,padx=20)


        #create entry widgets for data input
        #BREWDAY REPORT
        brewer = Entry(new_item_lf)
        brewer.grid(row=0, column=1)#, columnspan=3, sticky='we')
        
        brew_date = Entry(new_item_lf)
        brew_date.grid(row=1, column=1)#, columnspan=3, sticky='we')
        
        batch_size = Entry(new_item_lf)
        batch_size.grid(row=2, column=1)

        ID_of_record_to_delete = Entry(manage_item_lf)
        ID_of_record_to_delete.grid(row=0, column=1)
        
        
        
        #create text labels for entry widgets
        #BREWDAY REPORT (top of page)
        brewer_label = Label(new_item_lf, text='Tool: ')
        brewer_label.grid(row=0, column=0)
        
        brew_date_label = Label(new_item_lf, text='Amount: ')
        brew_date_label.grid(row=1, column=0)
        
        batch_size_label = Label(new_item_lf, text='Warehouse: ')
        batch_size_label.grid(row=2, column=0)

        ID_of_record_to_delete_label = Label(manage_item_lf, text='ID #: ')
        ID_of_record_to_delete_label.grid(row=0, column=0)

        # create btn to submit data to database
        submit_btn = Button(new_item_lf, text='Add record to database ', command=submit)
        submit_btn.grid(row=3, column=0, columnspan=3)

        # create btn to submit data to database
        submit_btn = Button(manage_item_lf, text='show record', width=20, command=query)
        #submit_btn.grid(row=1, column=0, columnspan=3)
        
        # create btn to delete data
        delete_btn = Button(manage_item_lf, text='delete records', width=20, command=delete)
        delete_btn.grid(row=2, column=0, columnspan=3)

        # create btn to edit data
        edit_btn = Button(manage_item_lf, text='edit record', width=20, command=edit)
        edit_btn.grid(row=3, column=0, columnspan=3)

        delete_empty_btn = Button(manage_item_lf, text='delete empty records', command=delete_empty)
        #delete_empty_btn.grid(row=4, column=0, columnspan=3)


        inventory_lf = LabelFrame(text='Your inventory',font='Verdana 15')
        inventory_lf.grid(row=1, column=2, rowspan=8,pady=20)
        

        #TEMPLATE2 = '{id1:^10} | {tool:^20} | {amount:^20} | {warehouse:^20}'
        inventory_head = Label(inventory_lf,font=20, text='ID #\tTool\tAmount\tWarehouse')
                #TEMPLATE2.format(id1='ID #', tool='Tool', amount='Amount', warehouse='Warehouse'))
        #head_elements = ['id1','tool','amount','warehouse']
        #for i in head_elements:
        #    print(i)
        #    h_e=i.center(10)
        #inventory_head = Label(inventory_lf, text=head_elements)

                #TEMPLATE2.format(id1='ID #', tool='Tool', amount='Amount', warehouse='Warehouse'))


        inventory_head.grid(row=0, column=0, sticky='w')

        #text widget to show inventory
        show_txt = Text(inventory_lf, font=20,width=50, height=20)
        show_txt['state']='disabled'
        show_txt.grid(row=1, column=0)#, rowspan=8)



        #commit changes
        conn.commit()
        
        #close connection
        conn.close()

        query()
        
        #root.mainloop()



def main():
    root=Tk()
    cnt = Content(root)
    root.geometry('820x470+300+300')
    root.resizable(0,0)
    root.title('My SQL Database')
    root.mainloop()

if __name__ == '__main__':
    main()

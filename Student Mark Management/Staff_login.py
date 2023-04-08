from tkinter import *
from tkinter import messagebox,ttk,filedialog
import pymysql,os
from random import *
from cryptography.fernet import Fernet
con = pymysql.connect(host="localhost",user="root",password="admin",database="studentregister")
cur = con.cursor()

root= Tk()
root.geometry('1920x1080+0+10')

bg = PhotoImage(file='pic1.png')
bgLabel = Label(root,image=bg)
bgLabel.place(x=0, y=0)
 
def owner_login():

   login_bg = '#FFF'
   global login_Frame
   login_Frame = Frame( padx=50, pady=20 , bg=login_bg )
   Label(login_Frame,text= 'Teacher Login' , font= ('Arial',22,'bold') , bg=login_bg ).pack(pady=10)
   Label(login_Frame,text='Email',textvariable='email' , font= ('Arial',14), bg=login_bg ).pack(pady=1)
   entry01 = ttk.Entry(login_Frame)
   entry01.pack(pady=2)
   Label(login_Frame,text='Password' , font= ('Arial',14),  bg=login_bg ).pack(pady=1)
   entry02 = ttk.Entry(login_Frame,show='*')
   entry02.pack(pady=2)

   def login_Close():
      if entry01.get() != '' and entry02.get() != '':
            cur.execute("select * from registerloginform where Email=%s and Password=%s",(entry01.get(),entry02.get()))
            row = cur.fetchone()
            #print(row)
            if row != None:
                if row[4] == 'Approved':
                    login_Frame.destroy()
                    staff_screen(row[1])
                    
                else:
                    messagebox.showinfo('Wait','Wait For Admin Approval.')
            else:
                messagebox.showerror('Failed','Login Failed.')
      else:
         messagebox.showwarning("Alert","Enter Email & Password Correctly !!")
   def tab3():
    root.destroy()
    import main1
   tab3_b=Button(root, text='HOME', font=('Times New Roman',13), command=tab3)
   tab3_b.place(x=1200, y=10, height=30, width=130,)


  
   def open_Register():
        login_Frame.destroy()
        owner_Register()

   ttk.Button(login_Frame,text='Login ✔' ,command=login_Close).pack(pady=10)
   Button(login_Frame,text='Not Registered ?' , bd= 0 , bg=login_bg , relief='flat' , overrelief='flat' , command=open_Register ).pack(pady=10)
   login_Frame.pack()
      

def owner_Register():
    register_bg = '#FFF'
    register_Frame = Frame(  padx=50, pady=20 , bg = register_bg )
    Label(register_Frame, text='Teacher Register' , font= ('Arial',22,'bold') , bg=register_bg ).pack(pady=10)

    Label(register_Frame, text='Name' ,underline= 0 ,bg=register_bg ).pack()
    reg_entry01 = ttk.Entry(register_Frame)
    reg_entry01.pack()
    Label(register_Frame, text='Email' ,bg=register_bg  ).pack()
    reg_entry02 = ttk.Entry(register_Frame)
    reg_entry02.pack()
    ttk.Label(register_Frame, text='Password' ,background=register_bg  ).pack()
    reg_entry03 = ttk.Entry(register_Frame , show='*' )
    reg_entry03.pack()
    ttk.Label(register_Frame, text='Re-Enter Password' ,background=register_bg  ).pack()
    reg_entry04 = ttk.Entry(register_Frame , show='*' )
    reg_entry04.pack()

    def register():
        if reg_entry01.get() != '' and reg_entry02.get() != '' and reg_entry03.get() != '':
            if reg_entry03.get() == reg_entry04.get():
                cur.execute("insert into registerloginform (Name,Email,Password,Status) values(%s,%s,%s,'Not Approved')",(reg_entry01.get(),reg_entry02.get(), reg_entry03.get() ))
                con.commit()
                
                register_Frame.destroy()
                
                owner_login()
            else:
                messagebox.showerror("Error","Password and Re-Enter Password doesn\'t Match.")
        else:
            messagebox.showerror('Error','Enter Name,Email and Password Correctly.')

    ttk.Button( register_Frame , text='Register' , command=register ).pack(pady=10)
    register_Frame.pack(pady=20)

owner_login()

def file_request(name):
    
    cur.execute("SELECT * FROM studentregister.file_request WHERE Owner_name = %s ;",(name))
    result = cur.fetchall()
   # print(*result)
    admin = Tk()
   

    admin_bg = '#FFF'
    admin_Frame = Frame( admin, padx=0, pady=20 , bg=admin_bg )
    
    list = [ 'S.No' , 'Roll_Num' , 'Owner_Name' , 'User_Name' , 'Status ' , 'File_Key' ]
    for i in range(len(list)):
        en1 = ttk.Entry(admin_Frame,width=16)
        en1.grid(row=3,column=i)
        en1.insert(END, list[i])
        en1.config(state='disabled',foreground='darkblue',justify='center',font=('bold'),background='#000',)

    i=6
    b = {}
    for s in result:
        for j in range(len(s)):
            if s[j] == 'Requested':
                b[s[j]] = ttk.Button(admin_Frame,width=16)
                def approve( x = s[j+1] ):
                    cur.execute("UPDATE file_request SET status = 'Accepted' WHERE file_key = %s;",(x))
                    con.commit()
                    #print(x)
                    messagebox.showinfo('Success','Done ✔')
                    admin.destroy()
                b[s[j]].config(text= 'Accept Request',command=approve)
                b[s[j]].grid(row=i,column=j)
            else:
                e = ttk.Entry(admin_Frame,width=16) 
                e.grid(row=i,column=j)
                e.insert(END, s[j])
                e.config(state ='disabled',justify='center',foreground='#000',font=('Arial'))

   
    admin_Frame.grid(row=5,column=10)
    
    admin.mainloop()
    
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
 
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE),'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]



    
def staff_screen(name):
    def fileupload():
          
       
           root.title(f'{name}')
           l1 = ttk.Label()
           l1.pack()

           key = [chr(x) for x in range(65,91) ]
           keys = ''
       
           for i in range(6):
                 keys += choice(key)
       
           Key_Label = ttk.Label(text=f'Key : {keys}')
           Key_Label.pack()
           titleLabel = Label(text='STUDENT DETAILS', font=('Times New Roman', 22, 'bold '), bg='white',
                              fg='black', )
           titleLabel.place(x=390, y=70)

           rollnumLabel = Label( text='ROLL NUM', font=('times new roman', 18, 'bold'), bg='white',
                          fg='black', )
           rollnumLabel.place(x=15, y=140, width=150)
           entryRollnum = Entry( font=('times new roman', 18), bg='lightgray')
           entryRollnum.place(x=180, y=140, width=150)

           nameLabel = Label(text=' NAME', font=('times new roman', 18, 'bold'), bg='white',
                             fg='black', )
           nameLabel.place(x=360, y=140, width=150)
           entryName= Entry(font=('times new roman', 18), bg='lightgray')
           entryName.place(x=530, y=140, width=150)

           StdLabel = Label( text='STD', font=('times new roman', 18, 'bold'), bg='white',
                        fg='black', )
           StdLabel.place(x=700, y=140, width=150)
           entryStd = Entry( font=('times new roman', 18), bg='lightgray')
           entryStd.place(x=860, y=140, width=150)

           semesterLabel = Label( text=' SEMESTER', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           semesterLabel.place(x=150, y=200, width=150)

           modelexamLabel = Label( text=' MODEL EXAM', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           modelexamLabel.place(x=590, y=200, width=200)
           sub1Label = Label( text='SUB1', font=('times new roman', 18, 'bold'), bg='white', fg='black', )
           sub1Label.place(x=15, y=260, width=150)
           Subone = Entry( font=('times new roman', 18), bg='lightgray')
           Subone.place(x=250, y=260, width=150)
           sub2Label = Label( text='SUB2', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub2Label.place(x=15, y=300, width=150)
           Subtwo= Entry(font=('times new roman', 18), bg='lightgray',)
           Subtwo.place(x=250, y=300, width=150)
           sub3Label = Label( text='SUB3', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           sub3Label.place(x=15, y=340, width=150)
           Subthree = Entry( font=('times new roman', 18), bg='lightgray')
           Subthree.place(x=250, y=340, width=150)

           sub4Label = Label( text='SUB4', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub4Label.place(x=15, y=380, width=150)
           Subfour = Entry(font=('times new roman', 18), bg='lightgray',)
           Subfour.place(x=250, y=380, width=150)
           sub5Label = Label(text='SUB5', font=('times new roman', 18, 'bold'), bg='white',
                             fg='black', )
           sub5Label.place(x=15, y=420, width=150)
           Subfive = Entry(font=('times new roman', 18), bg='lightgray')
           Subfive.place(x=250, y=420, width=150)
           sub6Label = Label( text='SUB6', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub6Label.place(x=15, y=460, width=150)
           Subsix = Entry(font=('times new roman', 18), bg='lightgray',)
           Subsix.place(x=250, y=460, width=150)


           totalLabel = Label( text='TOTAL', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           totalLabel.place(x=15, y=500, width=150)
           Total = Entry(  font=('times new roman', 18), bg='lightgray')
           Total.place(x=250, y=500, width=150)
           gradeLabel = Label(text='GRADE', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           gradeLabel.place(x=15, y=540, width=150)

           comboGrade = ttk.Combobox(font=("times new roman", 18,), state="readonly",)
           comboGrade['values'] = ("A1", "A","B1","B","C1","C","D1","D")
           comboGrade.place(x=250, y=540, width=150)

           sub1Label = Label( text='SUB1', font=('times new roman', 18, 'bold'), bg='white', fg='black', )
           sub1Label.place(x=500, y=260, width=150)
           Subseven = Entry( font=('times new roman', 18), bg='lightgray')
           Subseven.place(x=700, y=260, width=150)
           sub2Label = Label( text='SUB2', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub2Label.place(x=500, y=300, width=150)
           Subeight = Entry(font=('times new roman', 18), bg='lightgray',)
           Subeight.place(x=700, y=300, width=150)
           sub3Label = Label(text='SUB3', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           sub3Label.place(x=500, y=340, width=150)
           Subnine= Entry( font=('times new roman', 18), bg='lightgray')
           Subnine.place(x=700, y=340, width=150)

           sub4Label = Label(text='SUB4', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub4Label.place(x=500, y=380, width=150)
           Subten = Entry(font=('times new roman', 18), bg='lightgray',)
           Subten.place(x=700, y=380, width=150)


           sub5Label = Label( text='SUB5', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           sub5Label.place(x=500, y=420, width=150)
           Subeleven = Entry( font=('times new roman', 18), bg='lightgray')
           Subeleven.place(x=700, y=420, width=150)

           sub6Label = Label( text='SUB6', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub6Label.place(x=500, y=460, width=150)
           Subtwelve = Entry(font=('times new roman', 18), bg='lightgray',)
           Subtwelve.place(x=700, y=460, width=150)
           totalLabel = Label( text='TOTAL', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           totalLabel.place(x=500, y=500, width=150)
           Total1 = Entry(font=('times new roman', 18), bg='lightgray')
           Total1.place(x=700, y=500, width=150)
           gradeLabel = Label( text='GRADE', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           gradeLabel.place(x=500, y=540, width=150)
       
           comboGrade2 = ttk.Combobox( font=("times new roman", 18,), state="readonly",)
           comboGrade2['values'] = ("A1", "A","B1","B","C1","C","D1","D")
           comboGrade2.place(x=700, y=540, width=150)


           check = IntVar() 
           def upload():
               if entryRollnum.get() == '' or entryName.get() == '' or entryStd.get() == '' or Subone.get()== '' or \
                   Subtwo.get() == '' or Subthree.get() == '' or Subfour.get() == '' or Subfive.get()== '' or \
                   Subsix.get() == '' or Total.get() == '' or comboGrade.get() == '' or Subseven.get()== '' or \
                   Subeight.get() == '' or Subnine.get() == '' or Subten.get() == '' or Subeleven.get()== '' or \
                       Subtwelve.get() == ''  or Total1.get() == '' or comboGrade2.get() == '':
                       messagebox.showerror('Error', "All Fields Are Required")
       
       

               else:
                   try:
                       password = keys
    
                       def encrypt(raw, password):
                           private_key = hashlib.sha256(password.encode("utf-8")).digest()
                           raw = pad(raw)
                           iv = Random.new().read(AES.block_size)
                           cipher = AES.new(private_key, AES.MODE_CBC, iv)
                           return base64.urlsafe_b64encode(iv + cipher.encrypt(raw))
                        
                       message1 = Subone.get()
                       message2 = Subtwo.get()
                       message3 = Subthree.get()
                       message4 = Subfour.get()
                       message5 = Subfive.get()
                       message6 = Subsix.get()
                       message7 = Total.get()
                       message8 = comboGrade.get()
                       message9 = Subseven.get()
                       message10 = Subeight.get()
                       message11 = Subnine.get()
                       message12 = Subten.get()
                       message13 = Subeleven.get()
                       message14 = Subtwelve.get()
                       message15 = Total1.get()
                       message16 = comboGrade2.get()
                       encrypted1 = encrypt( message1, password)
                       encrypted2 = encrypt( message2, password)
                       encrypted3 = encrypt( message3, password)
                       encrypted4 = encrypt( message4, password)
                       encrypted5 = encrypt( message5, password)
                       encrypted6 = encrypt( message6, password)
                       encrypted7 = encrypt( message7, password)
                       encrypted8 = encrypt( message8, password)
                       encrypted9 = encrypt( message9, password)
                       encrypted10 = encrypt( message10, password)
                       encrypted11 = encrypt( message11, password)
                       encrypted12 = encrypt( message12, password)
                       encrypted13 = encrypt( message13, password)
                       encrypted14 = encrypt( message14, password)
                       encrypted15 = encrypt( message15, password)
                       encrypted16 = encrypt( message16, password)
                       con = pymysql.connect(host='localhost', user='root', password='admin', database='studentregister')
                       cur = con.cursor()
                       cur.execute("insert into studentreg (Rollnum, Name, Std, Subone, Subtwo, Subthree, Subfour, Subfive, Subsix, Total, Grade, Subseven, Subeight, Subnine, Subten, Subeleven, Subtwelve, Total1, Grade2, File_key, Owner_name, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')", (entryRollnum.get(), entryName.get(), entryStd.get(), encrypted1, encrypted2, encrypted3, encrypted4, encrypted5, encrypted6, encrypted7,encrypted8, encrypted9, encrypted10, encrypted11, encrypted12, encrypted13, encrypted14, encrypted15, encrypted16, password,name))
                       con.commit()
                       con.close()
                       messagebox.showinfo('Success', "Registration Successful")
                   except Exception as e:
                       showerror('Error', f"Error due to: {e}",)
                          
           registerbutton = Button(text="SUBMIT", bd=4, bg='white', command=upload, activebackground='white', activeforeground='white',)
           registerbutton.place(x=300, y=620, width=100, height=40)
           clearbutton = Button( text="CLEAR", bd=4, bg='white', command=fileupload, activebackground='white', activeforeground='white',)
           clearbutton.place(x=500, y=620, width=100, height=40)
           
             
           
                
    upload_Btn = ttk.Button(text='register',command=fileupload )        
    upload_Btn.pack()
    
    file_request(name)

 
    
logout_Btn = ttk.Button(text='Logout' , command=root.destroy)
logout_Btn.pack(padx=100,pady=10)
mainloop()



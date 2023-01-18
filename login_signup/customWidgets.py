import sqlite3
import tkinter.messagebox as mb
from tkinter import *
import re
import getpass
from hashlib import sha256

def checkMail(email):
    if bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)):
        return True
    else:
        return False

def showPassword(event):
    wdgt = event.widget
    wdgt['show'] = ''


def hidePassword(event):
    wdgt = event.widget
    wdgt['show'] = '*'

def checkexist(email) :   #check mail exitence
    db = sqlite3.connect("myDatabse.db")
    cursor = db.cursor()

    Qry = """SELECT * FROM Register where lname=?"""
    entry_vals = (email,)
    cursor.execute(Qry,entry_vals)
    #get db results
    db_res = cursor.fetchall()
    for x in db_res:
      print(x)
    if db_res == []:
        return True
    else:
        return False

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 8:
        print('length should be at least 8')
        val = False

    if len(passwd) > 20:
        print('length should be not be greater than 8')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return True
    else: return False
class LabeledEntry(LabelFrame):
    """label fram containig a entry and error display label and a label to add image
	some parameters:
	parent,
	lbltext :  acts as placeholder,
	err_msg :  by default none if wanted to warn add values get erased as Entry get the focus
	imglcn:  location for icon


	 """

    def __init__(self, master, lbltext, err_msg, imglcn=None, *args, **kwargs):
        LabelFrame.__init__(self, master, *args, **kwargs)
        self.config(bd=0, text=lbltext)

        self.lbltext = lbltext
        self.err_msg = err_msg

        # variable to hold entry data
        self.Entry_var = StringVar()

        self.ico = PhotoImage(file=imglcn)
        self.imglbl = Label(self, bd=0, image=self.ico, **kwargs)

        self.entry = Entry(self, bd=0, width=20, font=('', 12), textvariable=self.Entry_var, fg='white', bg='#212149')
        # frame draws a line just below entry
        self.line = Frame(self, bd=0, width=40, height=2, bg='white')
        # id any error occurs use this to deiplay
        self.error = Label(self, bd=0, fg='red', anchor='nw', text=self.err_msg, **kwargs)

        # packing labels
        self.error.pack(side='bottom', fill='x')
        self.imglbl.pack(side='left', anchor='nw', fill='y', ipadx=8)
        self.entry.pack(anchor='nw', fill='both', expand=1)
        self.line.pack(anchor='nw', fill='x')
        # binnding
        self.entry.bind("<FocusIn>", self.F_in)
        self.entry.bind("<FocusOut>", self.F_out)

    def F_in(self, event):
        if self.Entry_var.get() == self.lbltext:
            pass
        else:
            self.error['text'] = ' '
            self.line['bg'] = 'white'

    def F_out(self, event):
        # if entry is empty
        if self.Entry_var.get().strip() == '':
            self.line['bg'] = 'red'
            self.error['text'] = '\tthis is a required field'





class LoginPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        # change title
        self.master.title('secure chat')
        # icons used
        self.bg = PhotoImage(file='1.png')
        # main background image
        Label(self, image=self.bg).pack()

        # name lable entry and password
        self._id = LabeledEntry(self, '   ', '', 'user.png', bg='#202147')
        self._id.place(x=380, y=110)

        self.psw = LabeledEntry(self, '   ', '', 'lock.png', bg='#202147')
        self.psw.entry['show'] = '*'  # hide typing charcters
        self.psw.place(x=390, y=230)
        # show password
        self.psw.entry.bind("<Button-3>", showPassword)
        # on release
        self.psw.entry.bind("<ButtonRelease-3>", hidePassword)
        # login button
        self.login_btn = Button(self, text='Login', font=('arial', 22), width=7, fg='#DEEFE7', bg='#624697',
                                activebackground='#624697',activeforeground="white", bd=0)
        self.login_btn.place(x=470, y=350)

        # reber password button

        # if forgt password

        # register button
        self.register_btn = Button(self, text='Register', font=('arial', 15), width=7, fg='#b36599', bg='#202147',
                                   activebackground='#202147',activeforeground="white", bd=0)
        self.register_btn.place(x=550, y=430)

# register page interface for the app
class RegisterPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        # change title
        self.master.title('Register')
        # icons used
        self.bg = PhotoImage(file='2.png')
        self.intr = PhotoImage(file='internet.png')
        self.wa = PhotoImage(file='whatsapp.png')
        self.fb = PhotoImage(file='facebook.png')

        # main background image
        Label(self, image=self.bg).pack()

        # take id input and password
        default = {'bg': '#212048'}

        #email_entry
        self.fname = LabeledEntry(self, ' ', '', 'user.png', **default)
        # lower the width of entry
        self.fname.entry['width'] = 25
        self.fname.place(x=50, y=70)
        #card_entry
        self.card = LabeledEntry(self, ' ', '', 'user.png', **default)
        # lower the width of entry
        self.card.entry['width'] = 25
        self.card.place(x=400, y=180)

        #name_entry
        self.lanme = LabeledEntry(self, ' ', '', 'user.png', **default)
        # lower the width of entry
        self.lanme.entry['width'] = 25
        self.lanme.place(x=400, y=70)
        #pwd_entry
        self.psw = LabeledEntry(self, '', '', 'lock.png', **default)
        # lower the width of entry
        self.psw.entry.config(width=25, show='*')
        self.psw.place(x=50, y=200)
        #retyppwd_entry
        self.retype_psw = LabeledEntry(self, '', '', 'lock.png', **default)
        # lower the width of entry
        self.retype_psw.entry.config(width=25, show='*')
        self.retype_psw.place(x=50, y=310)
        # bind a function to hide or show password on right click
        # on press
        self.retype_psw.entry.bind("<Button-3>", showPassword)
        # on release
        self.retype_psw.entry.bind("<ButtonRelease-3>", hidePassword)

        # login butto
        self.register_btn = Button(self, text='Register', font=('arial', 22), width=6, fg='white', bg='#624697',
                                   activebackground='#624697',activeforeground="white", bd=0)
        self.register_btn.place(x=320, y=400)
        # register btn
        self.login_btn = Button(self, text='Login', font=('arial', 20), width=5, fg='#b36599', bg='#202147',
                                   activebackground='#202147',activeforeground="white", bd=0)
        self.login_btn.place(x=590, y=400.5)





    def on_register(self):
        a = self.fname.Entry_var.get().strip()  # username remove spaces before and after usinf strip()
        b = self.lanme.Entry_var.get().strip()  # email remove spaces before and after usinf strip()
        c =self.psw.Entry_var.get().strip()  # remove spaces before and after usinf strip())
        d = self.retype_psw.Entry_var.get().strip()  # remove spaces before and after usinf strip()
        r = self.card.Entry_var.get().strip()  # remove spaces before and after usinf strip()
        if a =='' or b =='' or c =='' or d == '':
            mb.showinfo(message='All fields are required')
        if password_check(c)==False:
            mb.showinfo(message='password should be strong')
        else:
             if c != d:
                 mb.showinfo(message='Retyped password did not matched')
             else:
                 if checkMail(b)==False:
                  mb.showinfo(message='mail not valid')
                 else:
                   if checkexist(b)==False:
                    mb.showinfo(message='mail exist')
                   else:
                    e = (sha256(c.encode()).hexdigest())
                    db = sqlite3.connect("myDatabse.db")  # connect to databse
                    # Qry_for_creating tables = """ CREATE TABLE Register(
                    # Fname varchar(100),
                    # Lname varchar(100),
                    # Psw   varchar(100)
                    # #  )  """
                    Qry = """INSERT INTO Register(fname,lname,card,Psw) VALUES(?,?,?,?)"""
                    entry_vals = (a,b,r,e)

                    cursor = db.cursor()  # create cursor
                    cursor.execute(Qry, entry_vals)  # execute the query using the cursor
                    cursor.execute("SELECT * FROM Register")

                    myresult = cursor.fetchall()

                    for x in myresult:
                     print(x)
                    db.commit()  # commit all changes to database
                    ask = mb.askyesno(message='Regsitration was succesfull!', detail='Do you want to Login!')
                    return ask







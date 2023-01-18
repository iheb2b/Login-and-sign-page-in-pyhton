from tkinter import *
import sqlite3
import tkinter.messagebox as mb
import customWidgets
from hashlib import sha256

class mainApp(Tk):

	def __init__(self):
		Tk.__init__(self)
		self.iconbitmap('chat.ico')
		self.resizable(0, 0)
		self.geometry('720x480')
		#grid both pages at the same position
		self.register_page = customWidgets.RegisterPage(self)
		self.register_page.grid(row=0,column=0)
		#bind button functions
		self.register_page.login_btn['command']=self.goto_LoginPage
		self.register_page.register_btn['command']=self.on_registerPage_click_Register

		self.login_page = customWidgets.LoginPage(self)
		self.login_page.grid(row=0,column=0)
		#functins of button on the pages
		self.login_page.login_btn['command']=self.on_loginPage_click_Login
		self.login_page.register_btn['command']=self.goto_registerPage
		#add some warning
		self.login_page.psw.error['text']='\tpress and hold right key to show password'

	def goto_registerPage(self):
		#raise register_page up to the login
		self.register_page.tkraise()

	def goto_LoginPage(self):
		#return to login page
		self.login_page.tkraise()

	def on_registerPage_click_Register(self):
		#if user is on register page and clicks to regsiter btn
		result=self.register_page.on_register()
			# if result is true
		if result:
			self.goto_LoginPage()
		else:
			print('adding failed')

	def on_loginPage_click_Login(self):
		#if user is on login page and clicks to login btn
		a=self.login_page._id.Entry_var.get().strip()
		b=self.login_page.psw.Entry_var.get().strip()

		if a==b=='':
			#if fields are empty
			mb.showinfo(message='Fill all required fields')
		else:
			db=sqlite3.connect("myDatabse.db")#connect to databse
			cursor=db.cursor()#create cursor

			Qry="""SELECT * FROM Register WHERE lname=? AND Psw=? """
			entry_vals=(a,(sha256(b.encode()).hexdigest()),)

			#execute the query using the cursor
			cursor.execute(Qry,entry_vals)
			#get db results
			db_res = cursor.fetchall()
			if db_res==[]:
				ask=mb.askyesno(message='We could not fine any results',detail='Do you want to register?')
				#if yes to register go to register page
				if ask:
					self.goto_registerPage()
			else:
				mb.showinfo(message=f'Hello {db_res[0][0]},',detail='Your login was succesfull! Cheers!')


#run

App = mainApp()
App.mainloop()
import tkinter as tk
import fonts
from tkinter import messagebox
from users_details import User
from users_details import UserDetails
from register import Register
import subprocess
import sys
import os

class Login:
    def __init__(self, window, csv_file_path):
        self.csv_file_path = csv_file_path
        self.user_details = UserDetails(csv_file_path)
        
        self.window = window
        self.window.title("Login")
        self.window.geometry("400x400")
        self.window.configure(bg="gray10")
        self.window.focus()
        self.window.grab_set()
        fonts.configure()

        self.frame = tk.Frame(window, bg="gray10")
        #self.frame.pack()
        self.frame.place(relx=0.5, rely=0.4, anchor="center")

        self.header = tk.Label(self.frame, text="Video Player", justify="center",bg="gray10", fg="mistyrose2")
        self.header.grid(row=0, column=0, columnspan=2, pady =10)

        self.user_enter = tk.Entry(self.frame, width=25,bg="gray90")
        self.user_enter.grid(row=1, column=0, columnspan=2 ,pady=10)
        self.user_enter.insert(0, 'Enter your username...')
        self.user_enter.config(fg="grey")
        self.user_enter.bind('<FocusIn>', lambda event : self.on_entry_click(event, self.user_enter, "Enter your username..."))
        self.user_enter.bind('<FocusOut>', lambda event: self.on_focusout(event, self.user_enter, "Enter your username..."))

        self.pwd_enter = tk.Entry(self.frame, width=25,bg="gray90")
        self.pwd_enter.grid(row=2, column=0, columnspan=2 ,pady=10)
        self.pwd_enter.insert(0, "Enter your password...")
        self.pwd_enter.config(fg="grey")
        self.pwd_enter.bind('<FocusIn>', lambda event: self.on_entry_click(event, self.pwd_enter, "Enter your password..."))
        self.pwd_enter.bind('<FocusOut>', lambda event: self.on_focusout(event, self.pwd_enter, "Enter your password..."))

        self.signin_btn = tk.Button(self.frame, text= "Log In", font=("Georgia", 15), command=self.login)
        self.signin_btn.grid(row=3,column=0, columnspan=2, pady=5)
        
        self.signup_lbl = tk.Label(self.frame, text="Don't have an account?", justify="center", bg= "gray10", fg= "mistyrose2", font=("Times New Roman",10))
        self.signup_lbl.grid(row=4, column=0, pady= 0)
        
        self.signup_btn = tk.Button(self.frame, text="Sign up", justify="center",border=0, bg="gray10", fg="steelblue1", font=("Times New Roman",10), command= self.signup, activebackground="gray10", activeforeground="steelblue2")
        self.signup_btn.grid(row=4, column=1, pady=0)
        
    def on_entry_click(self, event, entry, default):
        if entry.get() == default:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')
            if default != "Enter your username...":
                entry.config(show="*")
            
    def on_focusout(self, event, entry, default):
        if entry.get() == '':
            entry.insert(0, default)
            entry.config(fg = 'grey')
            if default != "Enter your username...":
                entry.config(show='')
                
    def validate(self, username, password):
        for user in self.user_details.get_users():
            if user.username == username and user.password == password:
                return True
        return False
    
    def login(self):
        username = self.user_enter.get()
        password = self.pwd_enter.get()
        if self.validate(username, password):
            tk.messagebox.showinfo(message="Login successfully!")
            self.window.destroy()
            #todo call form main len
        else:
            tk.messagebox.showerror(message="Invalid username or password")
            
    def signup(self):
        script_path = os.path.join(os.path.dirname(__file__), 'register.py')
        subprocess.Popen([sys.executable, script_path])
        self.window.destroy()



if __name__ == "__main__":
    csv_file_path = 'users.csv'
    window = tk.Tk()
    app = Login(window, csv_file_path)

    window.mainloop()
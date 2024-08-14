import csv
import tkinter as tk
import fonts
from tkinter import messagebox
from users_details import User
from users_details import UserDetails
import subprocess
import sys
import os

class Register:
    def __init__(self, window, csv_file_path):
        self.csv_file_path = csv_file_path
        self.user_details = UserDetails(csv_file_path)
        
        self.window = window
        self.window.title("Register")
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
        self.user_enter.insert(0, 'Enter an username...')
        self.user_enter.config(fg="grey")
        self.user_enter.bind('<FocusIn>', lambda event : self.on_entry_click(event, self.user_enter, "Enter an username..."))
        self.user_enter.bind('<FocusOut>', lambda event: self.on_focusout(event, self.user_enter, "Enter an username..."))

        self.pwd_enter = tk.Entry(self.frame, width=25,bg="gray90")
        self.pwd_enter.grid(row=2, column=0, columnspan=2 ,pady=10)
        self.pwd_enter.insert(0, "Enter a password...")
        self.pwd_enter.config(fg="grey")
        self.pwd_enter.bind('<FocusIn>', lambda event: self.on_entry_click(event, self.pwd_enter, "Enter a password..."))
        self.pwd_enter.bind('<FocusOut>', lambda event: self.on_focusout(event, self.pwd_enter, "Enter a password..."))
        
        self.repwd_enter = tk.Entry(self.frame, width=25,bg="gray90")
        self.repwd_enter.grid(row=3, column=0, columnspan=2 ,pady=10)
        self.repwd_enter.insert(0, "Re-enter password...")
        self.repwd_enter.config(fg="grey")
        self.repwd_enter.bind('<FocusIn>', lambda event: self.on_entry_click(event, self.repwd_enter, "Re-enter password..."))
        self.repwd_enter.bind('<FocusOut>', lambda event: self.on_focusout(event, self.repwd_enter, "Re-enter password..."))

        self.signup_btn = tk.Button(self.frame, text= "Sign Up", font=("Georgia", 15), command=self.signup)
        self.signup_btn.grid(row=4,column=0, columnspan=2, pady=5)
        
    def on_entry_click(self, event, entry, default):
        if entry.get() == default:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')
            if default != "Enter an username...":
                entry.config(show="*")
            
    def on_focusout(self, event, entry, default):
        if entry.get() == '':
            entry.insert(0, default)
            entry.config(fg = 'grey')
            if default != "Enter an username...":
                entry.config(show='')
                
    def validate(self, username, password):
        for user in self.user_details.get_users():
            if user.username == username and user.password == password:
                return True
        return False
    
    def signup(self):
        username = self.user_enter.get()
        password = self.pwd_enter.get()
        repassword = self.repwd_enter.get()
        exist = False
        for user in self.user_details.get_users():
            if user.username == username:
                tk.messagebox.showerror(message="This username has already existed!")
                exist = True
        if not exist:
            if password == repassword:
                with open(self.csv_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([username,password])
                self.user_details.users.append(User(username,password))  
                tk.messagebox.showinfo(message="Registered successfully!") 

                script_path = os.path.join(os.path.dirname(__file__), 'login.py')
                subprocess.Popen([sys.executable, script_path])
                self.window.destroy() 
            else:
                tk.messagebox.showerror(message="Passwords do not match")



if __name__ == "__main__":
    csv_file_path = 'users.csv'
    window = tk.Tk()
    app = Register(window, csv_file_path)

    window.mainloop()
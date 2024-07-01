from tkinter import *
from tkinter import messagebox
from random import random, randint, choice, shuffle
import pyperclip
import json

FONT_NAME = 'Arial'
PRIMARY_COLOR = '#009990'
SECONDARY_COLOR = '#3E4A56'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [choice(letters) for l_char in range(randint(8, 10))]
    password_list += [choice(symbols) for s_char in range(randint(2, 4))]
    password_list += [choice(numbers) for n_char in range(randint(2, 4))]

    shuffle(password_list)

    password_generated = "".join(password_list)

    # insert the generated password into the password entry
    entry_password.insert(END, password_generated)

    # call pyperclip to copy the generated password in the clipboard
    pyperclip.copy(password_generated)
    lb_password.config(text="Password Copied:", foreground='green')

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    new_data = {
        website: {
            "email": username,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Uncompleted form", message="Fill all box entries please!")
    else:
        is_save_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n\nEmail: {username}"
                                                                   f"\nPassword: {password}\n\nIs it ok to save?")
        if is_save_ok:
            try:

                with open('data.json', 'r') as password_data:

                    # reading old data
                    data = json.load(password_data)

                    # Updating old data with new_data
                    data.update(new_data)

                # Saving updated data
                with open("data.json", "w") as password_data:
                    json.dump(data, password_data, indent=4)

            except FileNotFoundError:
                with open("data.json", "w") as password_data:
                    json.dump(new_data, password_data, indent=4)

            entry_website.delete(0, END)
            entry_password.delete(0, END)
            lb_password.config(text="Password:", foreground='black')
            messagebox.showinfo(title='Password Manager', message='Sauvegarde bien effectuée !')


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = entry_website.get()
    try:
        with open('data.json', 'r') as data_file:
            data_dict = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title='Error', message='No Data File Found')
    else:
        if website in data_dict:
            messagebox.showinfo(title=website, message=f"Email: {data_dict[website]['email']}\n"
                                                       f"Password: {data_dict[website]['password']}")
        else:
            messagebox.showwarning(title='Error', message='No details for the Website exists')

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50, background='white')

# canvas with password logo
canvas = Canvas(width=200, height=200, background='white', highlightthickness=0)
password_logo = PhotoImage(file='pass-logo.png')
canvas.create_image(100, 100, image=password_logo)
canvas.grid(column=1, row=0)

# labels
lb_website = Label(text='Website:', background='white')
lb_website.grid(column=0, row=1)

lb_username = Label(text='Email/Username:', background='white')
lb_username.grid(column=0, row=2)

lb_password = Label(text='Password:', background='white')
lb_password.grid(column=0, row=3)

# Entries
entry_website = Entry(width=32, highlightthickness=1)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_username = Entry(width=50, highlightthickness=1)
entry_username.grid(column=1, row=2, columnspan=2)
entry_username.insert(END, "myemail@gmail.com")

entry_password = Entry(width=32, highlightthickness=1)
entry_password.grid(column=1, row=3)

# buttons
btn_generate = Button(text='Generate Password', highlightthickness=0, foreground='white',
                      command=password_generator, background=PRIMARY_COLOR)
btn_generate.grid(column=2, row=3)

btn_add = Button(text='Add', width=43, highlightthickness=0, background=PRIMARY_COLOR, foreground='white',
                 command=save_password)
btn_add.grid(column=1, row=4, columnspan=2)

btn_search = Button(width=14, text='Search', highlightthickness=0, background=SECONDARY_COLOR, foreground='white',
                    command=find_password)
btn_search.grid(column=2, row=1)

window.mainloop()

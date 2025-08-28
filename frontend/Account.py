from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
import requests
from tkcalendar import DateEntry
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class Account(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" , **kwargs)
        self.title_Label = ttk.Label(self,text="Account",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,40))

        # frame grid config
        self.columnconfigure(1,weight=1)

        self.Form = ttk.Frame(self,style="Form.TFrame",padding="20 40")
        self.Form.grid(column=1,row=2,sticky=(N,S,E,W))
        self.Form.columnconfigure(1,weight=1)

        # inputs

        self.username_Label = ttk.Label(self.Form,text="username",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.username_Label.grid(column=1,row=1)
        self.username_Label.grid_configure(pady=(4,0)) 

        self.username = StringVar()
        self.username_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.username,width=40,state="disabled")
        self.username_Entry.grid(column=1,row=2)
        self.username_Entry.grid_configure(pady=(4,0)) 

        self.fname_Label = ttk.Label(self.Form,text="fname",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.fname_Label.grid(column=1,row=3)
        self.fname_Label.grid_configure(pady=(4,0)) 

        self.fname = StringVar()
        self.fname_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.fname,width=40)
        self.fname_Entry.grid(column=1,row=4)
        self.fname_Entry.grid_configure(pady=(4,0)) 

        self.lname_Label = ttk.Label(self.Form,text="lname",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.lname_Label.grid(column=1,row=5)
        self.lname_Label.grid_configure(pady=(4,0)) 

        self.lname = StringVar()
        self.lname_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.lname,width=40)
        self.lname_Entry.grid(column=1,row=6)
        self.lname_Entry.grid_configure(pady=(4,0)) 

        self.email_Label = ttk.Label(self.Form,text="email",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.email_Label.grid(column=1,row=7)
        self.email_Label.grid_configure(pady=(4,0)) 

        self.email = StringVar()
        self.email_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.email,width=40)
        self.email_Entry.grid(column=1,row=8)
        self.email_Entry.grid_configure(pady=(4,0)) 


        self.password_Label = ttk.Label(self.Form,text="password",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.password_Label.grid(column=1,row=9)
        self.password_Label.grid_configure(pady=(4,0)) 

        self.password = StringVar()
        self.password_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.password,width=40)
        self.password_Entry.grid(column=1,row=10)
        self.password_Entry.grid_configure(pady=(4,0)) 

        self.submitButton = ttk.Button(self.Form,text="Submit",style="Normal.TButton",cursor="hand2",command=self.Submit)
        self.submitButton.grid(column=1,row=11)
        self.submitButton.grid_configure(pady=40)


        parent.option_add('*TCombobox*Listbox.background', '#2e2d2c')  
        parent.option_add('*TCombobox*Listbox.foreground', 'white')  
        parent.option_add('*TCombobox*Listbox.selectBackground', '#171716')  
        parent.option_add('*TCombobox*Listbox.selectForeground', 'white')

    def Trigger(self):
        self.getContent()
    def getContent(self) :
        try :
                tokens = self.parent.master.load_tokens()
                userId = tokens["id"]
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.get(f"{API_URL}user/{userId}",headers={"Authorization": f"Bearer {access_token}"})
                if(response.status_code == 401):
                    response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                    if (response.status_code == 200):
                        self.parent.master.update_tokens(response.json())
                        self.getContent()
                    else :
                        self.parent.master.logout()
                else :
                    row = response.json()
                    
                    if row:
                        self.username.set(row["username"])
                        self.fname.set(row["fname"])
                        self.lname.set(row["lname"])
                        self.email.set(row["email"])
                        self.password.set(row["password"])
                    

        except requests.exceptions.RequestException as e:
                messagebox.showerror("Server error",message=str(e))

    def Submit(self):
        if self.fname.get()!="" and self.lname.get().strip()!="" and self.email.get().strip()!="" and self.password.get().strip()!="":
            try :
                    tokens = self.parent.master.load_tokens()
                    userId = tokens["id"]
                    access_token = tokens["access_token"]
                    refresh_token = tokens["refresh_token"]
                    response = requests.put(f"{API_URL}user/{userId}",headers={"Authorization": f"Bearer {access_token}"},
                                            json={"fname":self.fname.get().strip(),"lname":self.lname.get().strip(),
                                                "email":self.email.get().strip(),"password":self.password.get().strip()})
                    if(response.status_code == 200) :
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                        self.parent.after(500,lambda : response_Label.destroy())
                    elif(response.status_code == 401):
                        response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                        if (response.status_code == 200):
                            self.parent.master.update_tokens(response.json())
                            self.Submit()
                        else :
                            self.parent.master.logout()
                    else :
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                        self.parent.after(2000,lambda : response_Label.destroy())
            except requests.exceptions.RequestException as e:
                        messagebox.showerror("Server error",message=str(e))
        else:
            response_Label = ttk.Label(self,text="All fields are required !",font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
            response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
            self.parent.after(1000,lambda : response_Label.destroy())
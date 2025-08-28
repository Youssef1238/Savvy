from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
import requests
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')



class RegisterPage(ttk.Frame) :
    def __init__(self, parent,**kwargs):
        self.parent = parent
        applyStyles(parent)
        super().__init__(master=parent,style="Normal.TFrame",**kwargs)
        self.title_Label = ttk.Label(self,text="Register",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,40)) 

        self.username_Label = ttk.Label(self,text="username",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.username_Label.grid(column=1,row=2)
        self.username_Label.grid_configure(pady=(4,0)) 

        self.username = StringVar()
        self.username_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.username,width=40)
        self.username_Entry.grid(column=1,row=3,sticky=(W,E))
        self.username_Entry.grid_configure(pady=(4,0)) 

        self.fname_Label = ttk.Label(self,text="fname",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.fname_Label.grid(column=1,row=4)
        self.fname_Label.grid_configure(pady=(4,0)) 

        self.fname = StringVar()
        self.fname_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.fname,width=40)
        self.fname_Entry.grid(column=1,row=5,sticky=(W,E))
        self.fname_Entry.grid_configure(pady=(4,0)) 

        self.lname_Label = ttk.Label(self,text="lname",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.lname_Label.grid(column=1,row=6)
        self.lname_Label.grid_configure(pady=(4,0)) 

        self.lname = StringVar()
        self.lname_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.lname,width=40)
        self.lname_Entry.grid(column=1,row=7,sticky=(W,E))
        self.lname_Entry.grid_configure(pady=(4,0)) 

        self.email_Label = ttk.Label(self,text="email",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.email_Label.grid(column=1,row=8)
        self.email_Label.grid_configure(pady=(4,0)) 

        self.email = StringVar()
        self.email_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.email,width=40)
        self.email_Entry.grid(column=1,row= 9,sticky=(W,E))
        self.email_Entry.grid_configure(pady=(4,0)) 


        self.password_Label = ttk.Label(self,text="password",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.password_Label.grid(column=1,row=10)
        self.password_Label.grid_configure(pady=(4,0)) 

        self.password = StringVar()
        self.password_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.password,width=40,show="•")
        self.password_Entry.grid(column=1,row=11,sticky=(W,E))
        self.password_Entry.grid_configure(pady=(4,0)) 

        

        self.RegisterButton = ttk.Button(self,text="Submit",style="Normal.TButton",cursor="hand2",command=self.Add)
        self.RegisterButton.grid(column=1,row=12)
        self.RegisterButton.grid_configure(pady=40) 

        self.login_link = ttk.Label(self,text="already have one ?",cursor="hand2",font=("Bodoni MT",15),foreground="lightblue",background="#333333",padding="20")
        self.login_link.grid(column=1,row=13,sticky=(W,E))
        self.login_link.grid_configure(pady=10) 
        self.login_link.bind("<Button-1>",lambda e: parent.switchPage("Login"))

    def Add(self,*args):
            _username = self.username.get().strip()
            _fname = self.fname.get().strip()
            _lname = self.lname.get().strip()
            _email = self.email.get().strip()
            _pass = self.password.get().strip()
            
            if _pass!="" and _username!="" and _fname!="" and _lname!="" and _email!="" :
                try :
                    response = requests.post(f"{API_URL}register",
                                            json={"username" : _username , 
                                                "fname" : _fname,
                                                "lname" : _lname,
                                                "email" : _email,
                                                "password" : _pass
                                                }
                    )
                    if(response.status_code == 200) :
                        response_Label = ttk.Label(self.parent,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                        response_Label.pack(side=TOP,fill='x',before=self)
                        self.parent.save_tokens(response.json())
                        self.password.set('')
                        self.username.set('')
                        self.fname.set('')
                        self.lname.set('')
                        self.email.set('')
                        self.parent.after(2000,lambda : response_Label.destroy())
                        self.parent.after(2000,lambda : self.parent.switchPage("Dashboard"))
                    else :
                        response_Label = ttk.Label(self.parent,text=response.text,font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                        response_Label.pack(side=TOP,fill='x',before=self)
                        if response.text == "username already used !":
                            self.username.set('')
                        self.parent.after(2000,lambda : response_Label.destroy())
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Server error",message=str(e))
            else:
                response_Label = ttk.Label(self.parent,text="All fields are required !",font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                response_Label.pack(side=TOP,fill='x',before=self)
                self.parent.after(1000,lambda : response_Label.destroy())







from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
import requests
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')



class LoginPage(ttk.Frame) :
    def __init__(self, parent,**kwargs):
        self.parent = parent
        applyStyles(parent)
        super().__init__(master=parent,style="Normal.TFrame",**kwargs)
        self.title_Label = ttk.Label(self,text="Login",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,40)) 

        self.username_Label = ttk.Label(self,text="username",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.username_Label.grid(column=1,row=2)
        self.username_Label.grid_configure(pady=10) 

        self.username = StringVar()
        self.username_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.username,width=40)
        self.username_Entry.grid(column=1,row=3,sticky=(W,E))
        self.username_Entry.grid_configure(pady=10) 


        self.password_Label = ttk.Label(self,text="password",font=("Bodoni MT",13),background="#333333",foreground="white")
        self.password_Label.grid(column=1,row=4)
        self.password_Label.grid_configure(pady=10) 

        self.password = StringVar()
        self.password_Entry = ttk.Entry(self,style="Normal.TEntry",textvariable=self.password,width=40,show="•")
        self.password_Entry.grid(column=1,row=5,sticky=(W,E))
        self.password_Entry.grid_configure(pady=10) 

        self.loginButton = ttk.Button(self,text="Submit",style="Normal.TButton",cursor="hand2",command=self.Verify)
        self.loginButton.grid(column=1,row=6)
        self.loginButton.grid_configure(pady=40) 

        self.register_link = ttk.Label(self,text="create new account",cursor="hand2",font=("Bodoni MT",15),foreground="lightblue",background="#333333",padding="20")
        self.register_link.grid(column=1,row=7,sticky=(W,E))
        self.register_link.grid_configure(pady=(0,10)) 
        self.register_link.bind("<Button-1>",lambda e: parent.switchPage("Register"))
        self.password_Entry.bind("<Return>",self.Verify)
        self.username_Entry.bind("<Return>",self.Verify)
        self.loginButton.bind("<Return>",self.Verify)
         
    def Verify(self,*args):
            _pass = self.password.get().strip()
            _username = self.username.get().strip()
            if _pass!="" and _username!="":
                try :
                    response = requests.post(f"{API_URL}login",
                                            json={"username" : _username , "password" : _pass}
                    )
                    if(response.status_code == 200) :
                        response_Label = ttk.Label(self.parent,text="Successfully Logged !",font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                        response_Label.pack(side=TOP,fill='x',before=self)
                        self.parent.save_tokens(response.json())
                        self.username.set("")
                        self.password.set("")
                        self.parent.after(500,lambda : response_Label.destroy())
                        self.parent.after(500,lambda : self.parent.switchPage("Dashboard"))
                    else :
                        response_Label = ttk.Label(self.parent,text=response.text,font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                        response_Label.pack(side=TOP,fill='x',before=self)
                        if response.text == "password incorrect !":
                            self.password.set('')
                        else : self.username.set('')
                        self.parent.after(2000,lambda : response_Label.destroy())
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Server error",message=str(e))
            else:
                response_Label = ttk.Label(self.parent,text="All fields are required !",font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                response_Label.pack(side=TOP,fill='x',before=self)
                self.parent.after(1000,lambda : response_Label.destroy())







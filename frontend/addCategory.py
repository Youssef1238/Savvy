from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
import requests
from tkcalendar import DateEntry
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class addCategory(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" , **kwargs)
        self.title_Label = ttk.Label(self,text="Add Category",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,40))

        # frame grid config
        self.columnconfigure(1,weight=1)

        self.Form = ttk.Frame(self,style="Form.TFrame",padding="20 40")
        self.Form.grid(column=1,row=2,sticky=(N,S,E,W))
        self.Form.columnconfigure(1,weight=1)

        # inputs

        self.name_Label = ttk.Label(self.Form,text="Name",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.name_Label.grid(column=1,row=2)
        self.name_Label.grid_configure(pady=10) 

        self.name = StringVar()
        self.name_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.name,width=40)
        self.name_Entry.grid(column=1,row=3)
        self.name_Entry.grid_configure(pady=10,padx=15)
        

        
        self.type_Label = ttk.Label(self.Form,text="Type",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.type_Label.grid(column=1,row=4)
        self.type_Label.grid_configure(pady=10) 

        self.type = StringVar()
        self.type_Entry = ttk.Combobox(self.Form,width=40,textvariable=self.type,style="Normal.TCombobox",state="readonly")
        self.type_Entry["values"] = ("EXPENSE","INCOME")
        self.type_Entry.grid(column=1,row=5)
        self.type_Entry.grid_configure(pady=10,padx=15)
        self.type.set("INCOME")


        self.submitButton = ttk.Button(self.Form,text="Submit",style="Normal.TButton",cursor="hand2",command=self.Submit)
        self.submitButton.grid(column=1,row=6)
        self.submitButton.grid_configure(pady=40)


        parent.option_add('*TCombobox*Listbox.background', '#2e2d2c')  
        parent.option_add('*TCombobox*Listbox.foreground', 'white')  
        parent.option_add('*TCombobox*Listbox.selectBackground', '#171716')  
        parent.option_add('*TCombobox*Listbox.selectForeground', 'white')

    def Trigger(self) :
        self.name.set("")
        self.type.set("")
    def Submit(self):
        if self.name.get().strip()!="" and self.type.get().strip().lower()!="":
            try :
                tokens = self.parent.master.load_tokens()
                userId = tokens["id"]
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.post(f"{API_URL}category",headers={"Authorization": f"Bearer {access_token}"},
                                        json={"name":self.name.get().strip(),"type":self.type.get().strip().lower(),"userId" :userId})
                if(response.status_code == 200) :
                    response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                    response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                    self.name.set("")
                    self.type.set("")
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
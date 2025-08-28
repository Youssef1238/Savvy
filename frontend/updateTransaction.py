from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
import requests
from tkcalendar import DateEntry
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class updateTransaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" , **kwargs)
        self.title_Label = ttk.Label(self,text="Update Transaction",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,40))
        self.categories = []
        # frame grid config
        self.columnconfigure(1,weight=1)
        

        self.Form = ttk.Frame(self,style="Form.TFrame",padding="20 40")
        self.Form.grid(column=1,row=2,sticky=(N,S,E,W))
        self.Form.columnconfigure(1,weight=1)


        # inputs

        self.amount_Label = ttk.Label(self.Form,text="Amount",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.amount_Label.grid(column=1,row=2)
        self.amount_Label.grid_configure(pady=10) 

        self.amount = StringVar()
        self.amount_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.amount,width=40)
        self.amount_Entry.grid(column=1,row=3)
        self.amount_Entry.grid_configure(pady=10,padx=15)
        
        self.date_Label = ttk.Label(self.Form,text="Date",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.date_Label.grid(column=1,row=4)
        self.date_Label.grid_configure(pady=10) 

        self.date = StringVar()
        self.date_Entry = DateEntry(self.Form,style="Normal.TEntry",textvariable=self.date,width=40)
        self.date_Entry.grid(column=1,row=5)
        self.date_Entry.grid_configure(pady=10,padx=15)
        
        self.category_Label = ttk.Label(self.Form,text="Category",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.category_Label.grid(column=1,row=6)
        self.category_Label.grid_configure(pady=10) 

        self.category = StringVar()
        self.category_Entry = ttk.Combobox(self.Form,width=40,textvariable=self.category,style="Normal.TCombobox",state="readonly")
        
        self.category_Entry.grid(column=1,row=7)
        self.category_Entry.grid_configure(pady=10,padx=15)
        

        # buttons holder
        self.buttonHolder = ttk.Frame(self.Form,style="Normal.TFrame")
        self.buttonHolder.grid(column=1,row=8)
        self.buttonHolder.grid_configure(pady=40)

        self.backButton = ttk.Button(self.buttonHolder,text="Back",style="Normal.TButton",cursor="hand2",command=lambda : self.parent.master.switchPage("Transaction"))
        self.backButton.pack(side=LEFT,padx=3)

        self.submitButton = ttk.Button(self.buttonHolder,text="Submit",style="Normal.TButton",cursor="hand2",command=self.Submit)
        self.submitButton.pack(side=LEFT)
        

        parent.option_add('*TCombobox*Listbox.background', '#2e2d2c')  
        parent.option_add('*TCombobox*Listbox.foreground', 'white')  
        parent.option_add('*TCombobox*Listbox.selectBackground', '#171716')  
        parent.option_add('*TCombobox*Listbox.selectForeground', 'white')

    def Trigger(self):
        self.getCategories()
        self.category_Entry["values"] = [c[1] for c in self.categories]
        if len(self.categories) != 0:
            self.category_Entry.set(self.categories[0][1])
        self.getContent()
    def getContent(self):
        try :
            Tid = self.parent.master.getTid()
            if Tid != None :
                tokens = self.parent.master.load_tokens()
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.get(f"{API_URL}transaction/{Tid}",headers={"Authorization": f"Bearer {access_token}"})
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
                        cat = [c[1] for c in self.categories if c[0]==row["categoryId"]][0]
                        self.amount.set(row["amount"])
                        self.date.set(row["Date"])
                        self.category.set(cat)

        except requests.exceptions.RequestException as e:
                messagebox.showerror("Server error",message=str(e))
    def getCategories(self):
            try:
                tokens = self.parent.master.load_tokens()
                userId = tokens["id"]
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.get(f"{API_URL}category/user/{userId}",headers={"Authorization": f"Bearer {access_token}"})
                if(response.status_code == 401):
                    response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                    if (response.status_code == 200):
                        self.parent.master.update_tokens(response.json())
                        self.getCategories()
                    else :
                        self.parent.master.logout()
                else :
                    rows = response.json()
                    if len(rows) != 0:
                        for row in rows :
                            self.categories.append((row["id"],row["name"]))

            except requests.exceptions.RequestException as e:
                    messagebox.showerror("Server error",message=str(e))
    def Submit(self):
        if self.amount.get().strip()!="" and self.date.get().strip()!="" and self.category.get().strip()!="":
            try :
                Tid = self.parent.master.getTid()
                tokens = self.parent.master.load_tokens()
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.put(f"{API_URL}transaction/{Tid}",headers={"Authorization": f"Bearer {access_token}"},
                                        json={"amount":int(self.amount.get()),
                                            "categoryId" : [c[0] for c in self.categories if c[1] == self.category.get()][0],"Date" : self.date.get() })
                if(response.status_code == 200) :
                    response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                    response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                    self.parent.master.setTid(None)
                    self.categories = []
                    self.parent.after(500,lambda : response_Label.destroy())
                    self.parent.after(500,lambda : self.parent.master.switchPage("Transaction"))
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
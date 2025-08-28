from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
import requests
from tkcalendar import DateEntry
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class addPlan(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" , **kwargs)
        self.title_Label = ttk.Label(self,text="Add Plan",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,10))

        # frame grid config
        self.columnconfigure(1,weight=1)

        self.Form = ttk.Frame(self,style="Form.TFrame",padding="20 40")
        self.Form.grid(column=1,row=2,sticky=(N,S,E,W))
        self.Form.columnconfigure(1,weight=1)

        # inputs

        self.planTitle_Label = ttk.Label(self.Form,text="Title",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.planTitle_Label.grid(column=1,row=1)
        self.planTitle_Label.grid_configure(pady=10) 

        self.planTitle = StringVar()
        self.planTitle_Entry = ttk.Entry(self.Form,style="Normal.TEntry",textvariable=self.planTitle,width=40)
        self.planTitle_Entry.grid(column=1,row=2)
        self.planTitle_Entry.grid_configure(pady=10,padx=15)
        
        
        self.description_Label = ttk.Label(self.Form,text="Description",font=("Bodoni MT",13),background="#171716",foreground="white")
        self.description_Label.grid(column=1,row=3)
        self.description_Label.grid_configure(pady=10) 

        textFrame = ttk.Frame(self.Form,style="Normal.TFrame")
        textFrame.grid(column=1,row=4)
        textFrame.grid_configure(pady=5,padx=15)


        self.description_Entry = Text(textFrame, wrap="word",height=9, width=50, font=("Bodoni MT",13), undo=True,background="#333333",foreground="white",insertbackground="white")
        self.description_Entry.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(textFrame, command=self.description_Entry.yview)
        scrollbar.pack(side="right", fill="y")
        self.description_Entry.config(yscrollcommand=scrollbar.set)
      

        self.bFrame = ttk.Frame(self.Form,style="Form.TFrame",padding="10 5")
        self.bFrame.grid(column=1,row=5,sticky=(W,E,N,S))
        self.bFrame.grid_configure(pady=(100,10),padx=(0,5))
        self.bFrame.grid_rowconfigure(0, weight=1)
        self.bFrame.grid_columnconfigure(0, weight=1)
        self.bFrame.grid_columnconfigure(1, weight=1)
        

        self.submitButton = ttk.Button(self.bFrame,text="Submit",style="Normal.TButton",cursor="hand2",command=self.Submit)
        self.submitButton.grid(column=0,row=0,sticky=(E))
        self.submitButton.grid_configure(padx=5)

        self.back = ttk.Button(self.bFrame,text="Back",style="Normal.TButton",cursor="hand2",command=lambda : self.parent.master.switchPage("Plans"))
        self.back.grid(column=1,row=0,sticky=(W))


        


    def Trigger(self) :
        self.planTitle.set("")
        self.description_Entry.delete("1.0","end")
    def Submit(self):
        if self.planTitle.get().strip()!="" and self.description_Entry.get("1.0","end").strip()!="":
            try :
                tokens = self.parent.master.load_tokens()
                userId = tokens["id"]
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.post(f"{API_URL}saving",headers={"Authorization": f"Bearer {access_token}"},
                                        json={"title":self.planTitle.get().strip(),"description":self.description_Entry.get("1.0","end").strip(),"userId" :userId})
                if(response.status_code == 200) :
                    response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                    response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                    self.planTitle.set("")
                    self.description_Entry.delete("1.0","end")
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
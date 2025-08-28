from tkinter import *
from tkinter import ttk , font,messagebox
from customtkinter import CTkScrollableFrame
from assets.styles import applyStyles
import requests
from assets.Card import Card
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class Plans(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" ,**kwargs)
        self.columnconfigure(1,weight=1)
        
        self.title_Label = ttk.Label(self,text="Plans",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,20))

        self.addButton = ttk.Button(self,text="Add",style="Normal.TButton",cursor="hand2",command=lambda : self.parent.master.switchPage("addPlan"))
        self.addButton.grid(column=1,row=2,sticky=(W))
        self.addButton.grid_configure(pady=5)
        
        self.cardsHolder = CTkScrollableFrame(self, width=350, height=500, corner_radius=0,fg_color="#333333")
        self.cardsHolder.grid(column=1,row=3,sticky=(W,E,N,S))
        self.cardsHolder.columnconfigure(1,weight=1)
        



    def Trigger(self) :
        self.getContent()
    def redirect(self,id):
        self.parent.master.setSid(id)
        self.parent.master.switchPage("updatePlan")
    def getContent(self):
        try :
            tokens = self.parent.master.load_tokens()
            userId = tokens["id"]
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            if userId != None :
                response = requests.get(f"{API_URL}saving/user/{userId}",headers={"Authorization": f"Bearer {access_token}"})
                if(response.status_code == 401):
                    response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                    if (response.status_code == 200):
                        self.parent.master.update_tokens(response.json())
                        self.getContent()
                    else :
                        self.parent.master.logout()
                else :
                    rows = response.json()
                    if len(rows) != 0:
                        for w in self.cardsHolder.winfo_children():
                            w.grid_forget()
                        for i,row in enumerate(rows):
                            descripton = row["description"] if len(row["description"]) < 100 else row["description"][:99] + "..."
                            Card(self.cardsHolder,title=row["title"],content=descripton,command=lambda id=row["id"] :self.redirect(id)).grid(column=1,row=i,sticky=(W,E))
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Server error",message=str(e))
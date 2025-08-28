from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
from customtkinter import CTkScrollableFrame
import requests
from tkcalendar import DateEntry
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class updatePlan(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" , **kwargs)
        self.title_Label = ttk.Label(self,text="Plan",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="10")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,10))

        # frame grid config
        self.columnconfigure(1,weight=1)

        self.enabled = True
        self.triggerUpdate = ttk.Button(self,text="Read",style="Normal.TButton",cursor="hand2",command=self.TriggerUpdate)
        self.triggerUpdate.grid(column=1,row=2,sticky=(W))
        self.triggerUpdate.grid_configure(pady=(0,5))

        self.Form = CTkScrollableFrame(self, width=350, height=500, corner_radius=0,fg_color="#171716")
        self.Form.grid(column=1,row=3,sticky=(N,S,E,W))
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

        self.descFrame = ttk.Frame(self.Form,style="Normal.TFrame")
        self.descFrame.grid(column=1,row=4)
        self.descFrame.grid_configure(pady=1,padx=15)
        

        

        self.description_Entry = Text(self.descFrame, wrap="word",height=9, width=50, font=("Bodoni MT",13), undo=True,background="#333333",foreground="white",insertbackground="white")
        self.description_Entry.pack(side="left", fill="both", expand=True)
        description_scrollbar = Scrollbar(self.descFrame, command=self.description_Entry.yview)
        description_scrollbar.pack(side="right", fill="y")
        self.description_Entry.config(yscrollcommand=description_scrollbar.set)

        
        
        self.solFrame = ttk.Frame(self.Form,style="Form.TFrame")



        self.analyseTitle = StringVar()
        self.analyse_title = ttk.Label(self.solFrame,textvariable=self.analyseTitle,font=("Bodoni MT",16,"bold"),background="#171716",foreground="white",anchor="center")
        self.analyse_title.grid(column=0,row=0,sticky=(W,N,S,E))
        self.analyse_title.grid_configure(pady=(0,2))

        self.analyseContent = StringVar()
        self.analyse = ttk.Label(self.solFrame,textvariable=self.analyseContent,font=("Bodoni MT",13),background="#171716",foreground="#bfbdba",anchor="center",wraplength=400)
        self.analyse.grid(column=0,row=1,sticky=(W,N,S,E))


        self.adviceTitle = StringVar()
        self.advice_title = ttk.Label(self.solFrame,textvariable=self.adviceTitle,font=("Bodoni MT",16,"bold"),background="#171716",foreground="white",anchor="center")
        self.advice_title.grid(column=0,row=2,sticky=(W,N,S,E))
        self.advice_title.grid_configure(pady=(0,2))

        self.adviceContent = StringVar()
        self.advice = ttk.Label(self.solFrame,textvariable=self.adviceContent,font=("Bodoni MT",13),background="#171716",foreground="#bfbdba",anchor="center",wraplength=400)
        self.advice.grid(column=0,row=3,sticky=(W,N,S,E))

      
        self.bFrame = ttk.Frame(self.Form,style="Form.TFrame",padding="10 5")
        self.bFrame.grid(column=1,row=5,sticky=(W,E,N,S))
        self.bFrame.grid_configure(pady=(100,10),padx=(0,5))
        self.bFrame.grid_rowconfigure(0, weight=1)
        self.bFrame.grid_columnconfigure(0, weight=1)

        self.submitButton = ttk.Button(self.bFrame,text="Update",style="Normal.TButton",cursor="hand2",command=self.Submit)
        self.submitButton.pack(side=LEFT, padx=(0,5))

        self.genarate = ttk.Button(self.bFrame,text="Generate",style="Normal.TButton",cursor="hand2",command=self.genreate_solution)
        self.genarate.pack(side=LEFT, padx=(0,5))

        self.delete = ttk.Button(self.bFrame,text="Delete",style="Normal.TButton",cursor="hand2",command=self.delete_plan)
        self.delete.pack(side=LEFT, padx=(0,5))

        self.backButton = ttk.Button(self.bFrame,text="Back",style="Normal.TButton",cursor="hand2",command=self.back)
        self.backButton.pack(side=LEFT, padx=(0,5))


    def TriggerUpdate(self):
        if self.enabled :
            self.enabled = False
            self.triggerUpdate.configure(text="Edit")
            self.planTitle_Entry.grid_forget()
            self.planTitle_Label.grid_forget()
            self.description_Label.grid_forget()
            self.descFrame.grid_forget()
            self.submitButton.configure(state="disabled")
            self.genarate.configure(state="disabled")
            self.delete.configure(state="disabled")
            self.bFrame.grid_configure(row=2)
            self.bFrame.grid_configure(pady=(60,10),padx=(0,5))
            self.solFrame.grid(column=1,row=1)
            self.solFrame.grid_configure(pady=(10,2),sticky=(W,N,S,E))
            self.solFrame.columnconfigure(0,weight=1)
            self.solFrame.rowconfigure(0,weight=1)
        else:   
            self.enabled = True
            self.triggerUpdate.configure(text="Read")
            self.planTitle_Label.grid(column=1,row=1)
            self.planTitle_Label.grid_configure(pady=10)
            self.planTitle_Entry.grid(column=1,row=2)
            self.planTitle_Entry.grid_configure(pady=10,padx=15)
            self.description_Label.grid(column=1,row=3)
            self.description_Label.grid_configure(pady=10) 
            self.descFrame.grid(column=1,row=4)
            self.descFrame.grid_configure(pady=1,padx=15)
            self.submitButton.configure(state="normal")
            self.genarate.configure(state="normal")
            self.delete.configure(state="normal")
            self.bFrame.grid_configure(row=5)
            self.bFrame.grid_configure(pady=(100,10),padx=(0,5))
            self.solFrame.grid_forget()
    def getContent(self):
        try :
            Sid = self.parent.master.getSid()
            if Sid != None :
                tokens = self.parent.master.load_tokens()
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                response = requests.get(f"{API_URL}saving/{Sid}",headers={"Authorization": f"Bearer {access_token}"})
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
                        self.planTitle.set(row["title"].strip())
                        self.description_Entry.delete("1.0","end")
                        self.description_Entry.insert("1.0",row["description"].strip())
                        solution = row["solution"]
                        if solution != "":
                            parts = solution.split("#")
                            self.analyseTitle.set(parts[1].strip())
                            self.analyseContent.set(parts[2].strip())
                            self.adviceTitle.set(parts[3].strip())
                            self.adviceContent.set(parts[4].strip())

        except requests.exceptions.RequestException as e:
                messagebox.showerror("Server error",message=str(e))
    def genreate_solution(self):
        try:
            
            self.Submit(0)
            tokens = self.parent.master.load_tokens()
            access_token = tokens["access_token"]
            id = tokens["id"]
            refresh_token = tokens["refresh_token"]
            Sid = self.parent.master.getSid()
            if Sid != None :
                waiting_Label = ttk.Label(self,text="Generating..",font=("Bodoni MT",16),background="#3297ad",foreground="white",padding="20",anchor="center")
                waiting_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                response = requests.post(f"{API_URL}saving/generate",headers={"Authorization": f"Bearer {access_token}"},
                                           json={"id": Sid,"userId" : id})
                if(response.status_code == 200) :
                        waiting_Label.destroy()
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))

                        self.parent.after(1000,lambda : response_Label.destroy())
                        self.parent.after(1000,lambda : self.parent.master.switchPage("updatePlan"))
                elif(response.status_code == 401):
                        waiting_Label.destroy()
                        response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                        if (response.status_code == 200):
                            self.parent.master.update_tokens(response.json())
                            self.delete()
                        else :
                            self.parent.master.logout()
                else :
                        waiting_Label.destroy()
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                        self.parent.after(2000,lambda : response_Label.destroy())


        except requests.exceptions.RequestException as e:
            messagebox.showerror("Server error",message=str(e))
    def delete_plan(self):
        try:
            tokens = self.parent.master.load_tokens()
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            Sid = self.parent.master.getSid()
            if Sid != None :
                response = requests.delete(f"{API_URL}saving/{Sid}",headers={"Authorization": f"Bearer {access_token}"})
                if(response.status_code == 200) :
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                        self.parent.master.setSid(None)
                        self.parent.after(500,lambda : response_Label.destroy())
                        self.parent.after(500,lambda : self.parent.master.switchPage("Plans"))
                elif(response.status_code == 401):
                        response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                        if (response.status_code == 200):
                            self.parent.master.update_tokens(response.json())
                            self.delete()
                        else :
                            self.parent.master.logout()
                else :
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#d66f7f",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                        self.parent.after(2000,lambda : response_Label.destroy())


        except requests.exceptions.RequestException as e:
            messagebox.showerror("Server error",message=str(e))
    def back(self):
        self.parent.master.setSid(None)
        self.parent.master.switchPage("Plans")
    def Trigger(self) :
        self.getContent()
        self.enabled = False
        self.TriggerUpdate()
    def Submit(self,redirect=1):
        if self.planTitle.get().strip()!="" and self.description_Entry.get("1.0","end").strip()!="":
            try :
                tokens = self.parent.master.load_tokens()
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
                Sid = self.parent.master.getSid()
                if Sid != None :
                    response = requests.put(f"{API_URL}saving/{Sid}",headers={"Authorization": f"Bearer {access_token}"},
                                            json={"title":self.planTitle.get().strip(),"description":self.description_Entry.get("1.0","end").strip()})
                    if(response.status_code == 200) :
                        response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                        response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                        self.parent.after(500,lambda : response_Label.destroy())
                        if redirect ==1:
                            self.parent.after(500,lambda : self.parent.master.switchPage("Plans"))
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
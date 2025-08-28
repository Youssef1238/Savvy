from tkinter import *
from tkinter import ttk ,messagebox
import requests
from Login import LoginPage
from Register import RegisterPage
from Dashboard import Dashboard
from Transaction import Transaction
from addCategory import addCategory
from Account import Account
from Plans import Plans
from addTransaction import addTransaction
from updateTransaction import updateTransaction
from addPlan import addPlan
from updatePlan import updatePlan
import os
import configparser
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')


class App(Tk) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CONFIG_FILE = "config.ini"
        self.config = configparser.ConfigParser()
        self.id = None
        self.Tid = None
        self.Sid = None
        self.title("Savvy")
        self.protocol("WM_DELETE_WINDOW",lambda : self.destroy())
        self.configure(background="#333333")
        self.geometry("+10+10")
        
        

        # container
        self.Container = ttk.Frame(self)
        self.Container.grid(column=1,row=0,sticky=(E,W,S,N))

        self.pages = {"Register" : RegisterPage(self),"Login" : LoginPage(self),"Dashboard" : Dashboard(self.Container),
                      "Transaction" : Transaction(self.Container),"Plans" : Plans(self.Container),"addCategory" : addCategory(self.Container)
                      ,"Account" : Account(self.Container),
                      "addTransaction" : addTransaction(self.Container),"updateTransaction" : updateTransaction(self.Container),
                       "addPlan" : addPlan(self.Container),"updatePlan" : updatePlan(self.Container)                                                                                     
                    }
        # Drawer
        self.Drawer = ttk.Frame(self,width=150,style="Drawer.TFrame")
        self.Drawer.grid(column=0,row=0,sticky=(N,S,W,E))
        self.Drawer.columnconfigure(0, weight=1)
        # drawer labels
        self.drawerLabels = []
        for i,page in enumerate(self.pages.keys()):
            if i >=2 and i<7:
                l = ttk.Label(self.Drawer,text=page,style="Drawer.TLabel",cursor="hand2")
                l.grid(column=0,row=i,sticky=(E,W))
                self.drawerLabels.append(l)
        
        for l in self.drawerLabels:
            l.bind("<Button-1>",lambda e ,page=l.cget("text"): self.switchPage(page))
        # Logout Button
        LogoutButton = ttk.Label(self.Drawer,text="Logout",style="Drawer.TLabel",cursor="hand2")
        LogoutButton.grid(column=0,row=len(self.pages)+1,sticky=(E,W))
        LogoutButton.bind("<Button-1>",self.Logout)
        # spacer
        spacer = ttk.Label(self.Drawer,text="",background="black",width="10")
        spacer.grid(column=0,row=len(self.pages),sticky=(N,E))
        spacer.rowconfigure(len(self.pages),weight=1)

        # root expansion config
        self.grid_columnconfigure(0, weight=0,minsize=150)  
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.bind("<Configure>", self.adjust_drawer_layout)

        self.switchPage("Login")

    def save_tokens(self,tokens):
        self.config['TOKENS'] = {
            'id' : tokens['id'],
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }
        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def load_tokens(self):
        if os.path.exists(self.CONFIG_FILE):
            self.config.read(self.CONFIG_FILE)
            return {
                'access_token': self.config['TOKENS']['access_token'],
                'refresh_token': self.config['TOKENS']['refresh_token'],
                'id' : self.config['TOKENS']['id']
            }
        return None
        
    def update_tokens(self,access_token):
        tokens = self.load_tokens()
        self.config['TOKENS'] = {
            'id' : tokens["id"],
            'access_token': access_token,
            'refresh_token': tokens['refresh_token']
        }
        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)
    def adjust_drawer_layout(self,e):
        self.Drawer.rowconfigure(len(self.pages),weight=1)

    def switchPage(self,page):
        self.geometry("800x700")
        for w in self.winfo_children():
            try:
                if w.pack_info():
                    w.pack_forget()
            except :
                pass  
    
            try:
                if w.grid_info():
                    w.grid_forget()
            except :
                pass
        if page != "Login" and page!= "Register":
            if(page == "Transaction"):
                self.pages["Transaction"] = Transaction(self.Container)
            if(page == "updateTransaction"):
                self.pages["updateTransaction"] = updateTransaction(self.Container)
            self.Drawer.grid(column=0,row=0,sticky=(N,S,W,E))
            self.Container.grid(column=1,row=0,sticky=(N,S,W,E))
            self.Container.rowconfigure(0,weight=1)
            self.Container.columnconfigure(0,weight=1)
            for w in self.Container.winfo_children():
                w.grid_forget()
            self.pages[page].grid(column=0,row=0,sticky=(N,S,W,E))
            self.pages[page].Trigger()
            
            
        else :
            self.pages[page].pack(padx=100,pady=(0,50))

    def Logout(self,*args) :
        try :
                tokens = self.load_tokens()
                refresh_token = tokens["refresh_token"]
                response = requests.post(f"{API_URL}logout",headers={"Authorization": f"Bearer {refresh_token}"}
                )
                if(response.status_code == 200) :
                    with open(self.CONFIG_FILE, 'w') as configfile:
                        configfile.write("")
                    self.switchPage("Login")
                else :
                    messagebox.showerror(title="Logout Error",message=response.text)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Server error",message=str(e))
        
        
    def setTid(self,id):
        self.Tid = id
    def getTid(self):
        return self.Tid
        
    def setSid(self,id):
        self.Sid = id
    def getSid(self):
        return self.Sid
    def run(self):
        self.mainloop()

    def stop(self):
        self.destroy()
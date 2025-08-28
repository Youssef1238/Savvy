from tkinter import *
from tkinter import ttk ,messagebox
import requests
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')

class Transaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" ,**kwargs)
        self.title_Label = ttk.Label(self,text="Transaction",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,40))
        self.rows = []
        self.categories = []



        #filter and managing Buttons

        self.filterFrame = ttk.Frame(self,style="Normal.TFrame")
        self.filterFrame.grid(column=1,row=2,sticky=(W,E,N,S))
        self.filterFrame.grid_rowconfigure(0, weight=1)
        self.filterFrame.grid_columnconfigure(0, weight=1)

        self.category = StringVar()
        self.filter_label = ttk.Label(self.filterFrame,text="Filter by caterory : ",font=("Bodoni MT",16,"bold"),background="#333333",foreground="white",anchor="center")
        self.filter_label.grid(column=0,row=0,sticky=(W,E))
        self.filtercomboBox = ttk.Combobox(self.filterFrame,width=40,textvariable=self.category,style="Normal.TCombobox",state="readonly")
        self.filtercomboBox.grid(column=1,row=0,columnspan=2,sticky=(W,E))
        
        self.filtercomboBox.grid_configure(padx=5)
        self.filtercomboBox.bind("<<ComboboxSelected>>", lambda e : self.filter())
        


        self.bFrame = ttk.Frame(self,style="Normal.TFrame",padding="0 20")
        self.bFrame.grid(column=1,row=3,sticky=(W,E,N,S))
        self.bFrame.grid_rowconfigure(0, weight=1)
        self.bFrame.grid_columnconfigure(0, weight=1)

        self.addButton = ttk.Button(self.bFrame,text="Add",style="Normal.TButton",cursor="hand2",command=lambda : self.parent.master.switchPage("addTransaction"))
        self.addButton.pack(side=LEFT, padx=(0,5))
        

        self.updateButton = ttk.Button(self.bFrame,text="Update",style="Normal.TButton",cursor="hand2",command=lambda : self.update())
        self.updateButton.pack(side=LEFT, padx=(0,5))

        self.deleteButton = ttk.Button(self.bFrame,text="Delete",style="Normal.TButton",cursor="hand2",command=lambda : self.delete())
        self.deleteButton.pack(side=LEFT, padx=(0,5))


        # frame for scrolling
        self.tableFrame = ttk.Frame(self,style="Normal.TFrame")
        self.tableFrame.grid(column=1,row=4,sticky=(W,E,N,S))
        self.tableFrame.grid_rowconfigure(0, weight=1)
        self.tableFrame.grid_columnconfigure(0, weight=1)

        columns = ("Category", "Type", "Amount","Date")
        self.tree = ttk.Treeview(self.tableFrame, columns=columns, show="headings", height=10,selectmode='browse')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")


        self.tree.tag_configure('oddrow', background='#444444')
        self.tree.tag_configure('evenrow', background='#555555')
        self.tree.grid(column=0,row=0,sticky=(N,W,S,E))


        # scrollbar
        scrollbar = ttk.Scrollbar(self.tableFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1,row=0,sticky=(N,S))


        # frame grid config
        self.columnconfigure(1,weight=1)

        parent.option_add('*TCombobox*Listbox.background', '#2e2d2c')  
        parent.option_add('*TCombobox*Listbox.foreground', 'white')  
        parent.option_add('*TCombobox*Listbox.selectBackground', '#171716')  
        parent.option_add('*TCombobox*Listbox.selectForeground', 'white')

    def Trigger(self):
        self.getCategories()
        self.filtercomboBox["values"] = ["All"] + [c[1] for c in self.categories]
        self.category.set("All")
        self.getContent()
    def update(self):
        selectedItems = self.tree.selection()
        if selectedItems:
            id = self.tree.item(selectedItems[0],"values")[-1]
            self.parent.master.setTid(id)
            self.rows = []
            self.categories = []
            self.parent.master.switchPage("updateTransaction")
    def filter(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.category.get() == "All":
            for i, row in enumerate(self.rows):
                        tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                        cat = [c[1] for c in self.categories if c[0]==row["categoryId"]][0]
                        type = [c[2] for c in self.categories if c[0]==row["categoryId"]][0].upper() 
                        item = (cat,type,row["amount"],row["Date"],row["id"])
                        self.tree.insert("", END, values=item, tags=(tag,))
        else :
            cat = [c[0] for c in self.categories if c[1]==self.category.get()][0]
            frows = [c for c in self.rows if c["categoryId"]==cat]
            for i, row in enumerate(frows):
                        tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                        cat = [c[1] for c in self.categories if c[0]==row["categoryId"]][0]
                        type = [c[2] for c in self.categories if c[0]==row["categoryId"]][0].upper() 
                        item = (cat,type,row["amount"],row["Date"],row["id"])
                        self.tree.insert("", END, values=item, tags=(tag,))
    def delete(self):
        try:
            tokens = self.parent.master.load_tokens()
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            selectedItems = self.tree.selection()
            if selectedItems:
                id = self.tree.item(selectedItems[0],"values")[-1]
                response = requests.delete(f"{API_URL}transaction/{id}",headers={"Authorization": f"Bearer {access_token}"})
                if(response.status_code == 200) :
                    response_Label = ttk.Label(self,text=response.text,font=("Bodoni MT",16),background="#58c777",foreground="white",padding="20",anchor="center")
                    response_Label.grid(column=0,row=0,columnspan=2,sticky=(E,W))
                    self.rows = []
                    self.categories = []
                    self.parent.after(500,lambda : response_Label.destroy())
                    self.parent.after(500,lambda : self.parent.master.switchPage("Transaction"))
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
                            self.categories.append((row["id"],row["name"],row["type"]))

            except requests.exceptions.RequestException as e:
                    messagebox.showerror("Server error",message=str(e))
    def getContent(self):
        try :
            tokens = self.parent.master.load_tokens()
            userId = tokens["id"]
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
            if userId != None :
                response = requests.get(f"{API_URL}transaction/user/{userId}",headers={"Authorization": f"Bearer {access_token}"})
                if(response.status_code == 401):
                    response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                    if (response.status_code == 200):
                        self.parent.master.update_tokens(response.json())
                        self.getContent()
                    else :
                        self.parent.master.logout()
                else :
                    self.rows = response.json()
                    if len(self.rows) != 0:
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                        for i, row in enumerate(self.rows):
                            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                            cat = [c[1] for c in self.categories if c[0]==row["categoryId"]][0]
                            type = [c[2] for c in self.categories if c[0]==row["categoryId"]][0].upper() 
                            item = (cat,type,row["amount"],row["Date"],row["id"])
                            self.tree.insert("", END, values=item, tags=(tag,))
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Server error",message=str(e))
from tkinter import *
from tkinter import ttk , font,messagebox
from assets.styles import applyStyles
from customtkinter import CTkFrame,CTkLabel
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv('API_URL')


class Dashboard(ttk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(master=parent,style="Normal.TFrame",padding="50 10" ,**kwargs)
        self.title_Label = ttk.Label(self,text="Dashboard",font=("Bodoni MT",24,"bold"),background="#333333",foreground="white",anchor="center",padding="40")
        self.title_Label.grid(column=1,row=1,sticky=(W,E))
        self.title_Label.grid_configure(pady=(0,10))


        self.cards_frame = CTkFrame(self, fg_color="#333333",corner_radius=0) 
        self.cards_frame.grid(row=2, column=1, padx=20, pady=2, sticky="we")

        self.cards_frame.columnconfigure((0, 1, 2), weight=1)  
        self.cards_frame.rowconfigure(0, weight=1) 


        self.exepnse = StringVar()
        self.Expense = CTkFrame(self.cards_frame,width=200,height=250,corner_radius=10,fg_color="#d1474e")
        self.Expense.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ttk.Label(self.Expense, text="Expense",font=("Bodoni MT",16),background="#d1474e",foreground="white").pack(side="top",pady=(5,10))
        ttk.Label(self.Expense, textvariable=self.exepnse,font=("Bodoni MT",13),background="#d1474e",foreground="white").pack(side="bottom",pady=(0,10))

        self.income = StringVar()
        self.Income = CTkFrame(self.cards_frame,width=200,height=250,corner_radius=10,fg_color="#31a831",)
        self.Income.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ttk.Label(self.Income, text="Income",font=("Bodoni MT",16),background="#31a831",foreground="white").pack(side="top",pady=(5,10))
        ttk.Label(self.Income, textvariable=self.income,font=("Bodoni MT",13),background="#31a831",foreground="white").pack(side="bottom",pady=(0,10))

        self.balance = StringVar()
        self.Balance = CTkFrame(self.cards_frame,width=200,height=250,corner_radius=10,fg_color="#3297ad",)
        self.Balance.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ttk.Label(self.Balance, text="Balance",font=("Bodoni MT",16),background="#3297ad",foreground="white").pack(side="top",pady=(5,10))
        ttk.Label(self.Balance, textvariable=self.balance,font=("Bodoni MT",13),background="#3297ad",foreground="white").pack(side="bottom",pady=(0,10))

        self.grid_columnconfigure(1, weight=1)

        months = []
        results = []

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure.patch.set_facecolor('#333333')  
        self.figure.tight_layout()

        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#333333')  
        self.ax.bar(months, results, color='#b66b16')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.set_title("Last Months Results", color='white',fontsize=16)  
        self.ax.set_xlabel("", color='white',fontsize=14)  
        self.ax.set_ylabel("", color='white',fontsize=14) 
        self.ax.tick_params(axis='x', colors='white')  
        self.ax.tick_params(axis='y', colors='white') 
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=1, padx=20, pady=20, sticky="we")
        self.canvas_widget.config(bg="#333333", highlightbackground="#333333")

    def Trigger(self) :
        self.getContent()
    def getContent(self):
        try :
            categories = []
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
                    rows = response.json()
                    if len(rows) != 0:
                        responseCat = requests.get(f"{API_URL}category/user/{userId}",headers={"Authorization": f"Bearer {access_token}"})
                        if(responseCat.status_code == 401):
                            response = requests.post(f"{API_URL}refresh",headers={"Authorization": f"Bearer {refresh_token}"})
                            if (response.status_code == 200):
                                self.parent.master.update_tokens(response.json())
                                self.getContent()
                            else :
                                self.parent.master.logout()
                        else :
                            Catrows = responseCat.json()
                            if len(Catrows) != 0:
                                for row in Catrows :
                                    categories.append((row["id"],row["type"]))
                                current_date = datetime.now()

                                for row in rows :
                                    row["type"] = [c[1] for c in categories if c[0]==row["categoryId"]][0]

                                current_month_transactions = [
                                    row for row in rows
                                    if datetime.strptime(row["Date"], '%m/%d/%y').strftime('%m/%Y') == current_date.strftime('%m/%Y')
                                ]
                                months = []
                                results = []
                                income = 0
                                for t in current_month_transactions:
                                    income += t["amount"] if t["type"] == "income" else 0
                                expense = 0
                                for t in current_month_transactions:
                                    expense += t["amount"] if t["type"] == "expense" else 0
                                balance = income - expense
                                self.exepnse.set(str(expense) + " $")
                                self.income.set(str(income) + " $")
                                self.balance.set(str(balance) + " $")

                                last_months_transaction = {}

                                for i in range(5):
                                    month_date = current_date - relativedelta(months=i)
                                    month_key = month_date.strftime('%Y-%m')  
                                    last_months_transaction[month_key] = []

                                for row in rows:
                                    transaction_date = datetime.strptime(row["Date"], '%m/%d/%y')
                                    transaction_month = transaction_date.strftime('%Y-%m')
                                    if transaction_month in last_months_transaction:
                                        last_months_transaction[transaction_month].append(row)
                                
                                for month,ts in last_months_transaction.items() :
                                    name = datetime.strptime(month, '%Y-%m').strftime('%B')
                                    result = 0
                                    for t in ts:
                                        result += t["amount"] if t["type"] == "income" else -1 * t["amount"] 
                                    months.append(name)
                                    results.append(result)
                                    

                                self.canvas_widget.pack_forget()
                                self.ax.clear()
                                self.ax.bar(months, results, color='#b66b16') 
                                self.ax.set_title("Last Months Results", color='white',fontsize=16) 
                                self.canvas = FigureCanvasTkAgg(self.figure,self)
                                self.canvas_widget = self.canvas.get_tk_widget()
                                self.canvas_widget.grid(row=3, column=1, padx=20, pady=20, sticky="we")
                                self.canvas_widget.config(bg="#333333", highlightbackground="#333333")

                                



        except requests.exceptions.RequestException as e:
                messagebox.showerror("Server error",message=str(e))
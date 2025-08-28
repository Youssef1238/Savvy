import sqlite3
import os
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime, timedelta

class User :
    def __init__(self) :
        self.db = sqlite3.connect('data.db')
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username varchar(20),
               fname varchar(20),
               lname varchar(20),
               email varchar(25), 
               password varchar(20)
        )

        """)

    def getAll(self):
        try:
            self.cursor.execute("""
                SELECT * FROM users 
            """)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def getOne(self,id):
        try:
            self.cursor.execute("""
                SELECT * FROM users WHERE id = {}
            """.format(id))
            res = self.cursor.fetchone()
            if(res == None): return None
            return dict(res)
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def Verify(self,username,password) :
        try:
            self.cursor.execute("""
                SELECT * FROM users WHERE username = '{}'
            """.format(username))
            res = self.cursor.fetchone()
            if res == None : return 0
            elif res["password"] != password : return 1
            else : return {"id" : res["id"]}
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def add(self,username,fname,lname,email,password):
        try:
            self.cursor.execute("""
                SELECT * FROM users WHERE username = '{}'
            """.format(username))
            res = self.cursor.fetchone()
            if res != None : return None
            self.cursor.execute("""
                    INSERT INTO users (username,fname,lname,email,password) VALUES ('{}','{}','{}','{}','{}')

            """.format(username,fname,lname,email,password))
            self.db.commit()
            self.cursor.execute("""
                SELECT * FROM users WHERE username = '{}'
            """.format(username))
            res = self.cursor.fetchone()
            return {"id" : res["id"]}
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def update(self,id,fname=None,lname=None,email=None,password=None):
        try:
            user = self.getOne(id)
            if( user == None) : return None
            _fname = user['fname'] if (fname == None) else fname
            _lname = user['lname'] if (lname == None) else lname
            _email = user['email'] if (email == None) else email
            _password = user['password'] if (password == None) else password
            self.cursor.execute("""
                    UPDATE users SET fname ='{}', lname ='{}',email ='{}',password ='{}' WHERE id = {} 

            """.format(_fname,_lname,_email,_password,id))
            self.db.commit()
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def delete(self,id):
        try:
            user = self.getOne(id)
            if( user == None) : return None
            self.cursor.execute("""
                DELETE FROM users WHERE id = {} 

            """.format(id))
            self.db.commit()
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def close(self):
        self.db.close()


class Transaction :
    def __init__(self) :
        self.db = sqlite3.connect('data.db')
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               amount INTEGER,
               categoryId INTEGER,
               userId INTEGER,
               Date DATE
        )
        """)

    def getAll(self):
        try:
            self.cursor.execute("""
                SELECT * FROM transactions 
            """)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def getByUser(self,id):
        try:
            self.cursor.execute("""
                SELECT * FROM transactions WHERE userId = {} 
            """.format(id))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def getOfLastMonth(self,userId):
        try:
            start_date = (datetime.today().replace(day=1)- timedelta(days=1)).replace(day=1)
            end_date = (datetime.today().replace(day=1) + timedelta(days=31)).replace(day=1)
            rows = self.getByUser(userId)
            filtered_rows = [
                row for row in rows 
                if start_date <= datetime.strptime(row['Date'], "%m/%d/%y") < end_date
            ]
            return [dict(row) for row in filtered_rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def getOne(self,id):
        try:
            self.cursor.execute("""
                SELECT * FROM transactions WHERE id = {}
            """.format(id))
            res = self.cursor.fetchone()
            if(res == None): return None
            return dict(res)
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        

    def add(self,userId,amount,categoryId,Date):
        try:
            self.cursor.execute("""
                    INSERT INTO transactions (userId,amount,categoryId,Date) VALUES ({},{},{},'{}')

            """.format(userId,amount,categoryId,Date))
            self.db.commit()
            return  0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def update(self,id,amount =None,categoryId=None,Date=None):
        try:
            transaction = self.getOne(id)
            if(transaction == None): return None
            _amount = transaction['amount'] if (amount == None) else amount
            _categoryId = transaction['categoryId'] if (categoryId == None) else categoryId
            _Date = transaction['Date'] if (Date == None) else Date
            self.cursor.execute("""
                    UPDATE transactions SET amount ={}, categoryId ={},Date ='{}' WHERE id = {} 

            """.format(_amount,_categoryId,_Date,id))
            self.db.commit()
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def delete(self,id):
        try:
            transaction = self.getOne(id)
            if(transaction == None): return None
            self.cursor.execute("""
                DELETE FROM transactions WHERE id = {} 

            """.format(id))
            self.db.commit()
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def close(self):
        self.db.close()

class Savings :
    def __init__(self) :
        self.db = sqlite3.connect('data.db')
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               description TEXT,
               solution TEXT,
               title TEXT,
               userId INTEGER
        )
        """)

    def getAll(self):
        try:
            self.cursor.execute("""
                SELECT * FROM savings 
            """)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def getOne(self,id):
        try:
            self.cursor.execute("""
                SELECT * FROM savings WHERE id = {}
            """.format(id))
            res = self.cursor.fetchone()
            if(res == None): return None
            return dict(res)
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def getByUser(self,userId):
        try:
            self.cursor.execute("""
                SELECT * FROM savings where userId = {}
            """.format(userId))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)  

    def add(self,userId,description,title):
        try:
            self.cursor.execute("""
                    INSERT INTO savings (userId,description,title,solution) VALUES ({},'{}','{}','')

            """.format(userId,description,title))
            self.db.commit()
            return  'savings plan added'
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def update(self,id,description=None,title=None,solution=None):
        try:
            saving = self.getOne(id)
            if(saving == None): return None
            _description = saving['description'] if (description == None) else description
            _title = saving['title'] if (title == None) else title
            _solution = saving['solution'] if (solution == None) else solution

            self.cursor.execute("""
                    UPDATE savings SET description ='{}', title ='{}', solution ='{}' WHERE id = {} 

            """.format(_description,_title,_solution,id)) 
            self.db.commit()
            return 'saving plan updated'
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        

    def generate(self,id,userId):
        
        try:
            transactions = Transaction().getOfLastMonth(userId)
            categories = Category().getAll()
            saving = self.getOne(id)
            load_dotenv()

            client = Groq(
                api_key=os.getenv("GROQ_API_KEY"),
            )

            transactions_string =""
            
            for t in transactions:
                t["Category"] = [c["name"] for c in categories if c["id"] == t["categoryId"]][0]
                t["Type"] = [c["type"] for c in categories if c["id"] == t["categoryId"]][0]

            for t in transactions:
                transactions_string += str(t["Category"]) + " : " + str(t["Type"]) + " , " + str(t["amount"]) + " dirhams\n"
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": """im gonna give you some information e.g : financial transactions and a goal that i wanna acheive and ur gonna give me an advice based on those transactions so that i can achieve the goal.
                            transactions in a month : <
                                """ +transactions_string+ """ 
                                >
                            goal : 
                            """ +saving["description"]+ """
                            your answer should structured in this way : expense and income analysis, advice.
                            and each section is structered as a title and a paragraph.
                            i want each title to be surrounded by this caracter # after it and before it
                            and make it breif , and in the response dont use this caracter : '
                        """,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )

            solution = chat_completion.choices[0].message.content

            self.update(id,solution=solution)
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def delete(self,id):
        try:
            saving = self.getOne(id)
            if(saving == None): return None
            self.cursor.execute("""
                DELETE FROM savings WHERE id = {} 

            """.format(id))
            self.db.commit()
            return 'saving plan with id '+ id + ' deleted'
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def close(self):
        self.db.close()

class Category :
    def __init__(self) :
        self.db = sqlite3.connect('data.db')
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name varchar(30),
               type TEXT,
               userId INTEGER, 
               CHECK (type IN ('expense','income'))
        )
        """)

    def getAll(self):
        try:
            self.cursor.execute("""
                SELECT * FROM categories 
            """)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def getOne(self,id):
        try:
            self.cursor.execute("""
                SELECT * FROM categories WHERE id = {}
            """.format(id))
            res = self.cursor.fetchone()
            if(res == None): return None
            return dict(res)
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def getByUser(self,userId):
        try:
            self.cursor.execute("""
                SELECT * FROM categories where userId = {}
            """.format(userId))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
    def add(self,name,type,userId):
        try:
            self.cursor.execute("""
                    SELECT * FROM categories WHERE name = '{}'

            """.format(name))
            category = self.cursor.fetchone()
            if(category != None) : return None
            self.cursor.execute("""
                    INSERT INTO categories (name,type,userId) VALUES ('{}','{}',{})

            """.format(name,type,userId))
            self.db.commit()
            return  0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def update(self,id,name =None,type=None):
        try:
            category = self.getOne(id)
            if(category == None): return None
            _name = category['name'] if (name == None) else name
            _type = category['type'] if (type == None) else type
            self.cursor.execute("""
                    UPDATE categories SET name ='{}', type ='{}' WHERE id = {} 

            """.format(_name,_type,id))
            self.db.commit()
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)
        
    def delete(self,id):
        try:
            category = self.getOne(id)
            if(category == None): return None
            self.cursor.execute("""
                DELETE FROM categories WHERE id = {} 

            """.format(id))
            self.db.commit()
            return 0
        except sqlite3.Error as e :
            return 'Database error : ' + str(e)

    def close(self):
        self.db.close()
from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from datetime import datetime


app = Flask(__name__)

# Create database table
class DataBase:
    def __init__(self):
        self.init_db()
    def init_db(self):
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()

        # Expenses table
        c.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                date TEXT,
                description TEXT,
                amount REAL
            )
        ''')

        # Credits table
        c.execute('''
            CREATE TABLE IF NOT EXISTS credits (
                date TEXT,
                person TEXT,
                amount REAL
            )
        ''')
        

        conn.commit()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(c.fetchall())
        conn.close()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'expense':
            #return redirect(url_for('expense'))
            return render_template('debit.html')
        
        elif action == 'income':
            return render_template('credit.html')

    return render_template('home.html')

@app.route('/expense', methods=['GET','POST'])
def expense():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']

        if date == '':
            date = datetime.now().strftime("%m/%d/%Y")
        else:
            print('its noneS')
        c.execute(
            """
                INSERT INTO expenses 
                    (date, description, amount) VALUES (?, ?, ?)
            """, (date, description, amount)
        )
        conn.commit()
        conn.close()
    return render_template('debit.html')

@app.route('/debit-db')
def view_data():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    data = c.fetchall()
    conn.close()

    return render_template('debit_view.html', expenses=data)

@app.route('/verification', methods=['GET', 'POST'])
def verify():

    if request.method == 'POST':

        action = request.form.get('action')
        email = request.form['email']
        passw = request.form['pass']

        verification = small_verification(email=email, password=passw)
        print(verification)
        if verification:
            if action == 'clear':
                conn = sqlite3.connect('expenses.db')
                c = conn.cursor()
                c.execute("DELETE FROM expenses")
                conn.commit()
                conn.close()

                return redirect('/debit-db')

            if action == 'modify':
                return redirect('/modify')
            
            if action == 'clear-credit':
                conn = sqlite3.connect('expenses.db')
                c = conn.cursor()
                c.execute("DELETE FROM credits")
                conn.commit()
                conn.close()

                return redirect('/credit-db')

        else:
            return "Invalid credentials"

    return render_template('verification.html')

def small_verification(email, password):
    # small verification for the email and password
        if email == 'santhoshravi072006@gmail.com' and password == 'passw':
            return True
                
        else:
            return False

@app.route('/data-cleared')
def after_clear():
    return render_template('clear_data.html')

@app.route('/credit-enter',  methods=['GET','POST'])
def credit():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    if request.method == 'POST':
        date = request.form['date']
        name = request.form['name']
        amount = request.form['amount']

        if date == '':
            date = datetime.now().strftime('%m/%d/%Y')
        
        else:
            print('None')

        c.execute(
            """
                INSERT INTO credits
                (date, person, amount) VALUES (?, ?, ?)
            """ ,
            (date, name, amount)
        )
        print(date, name, amount)

        conn.commit()
        conn.close()
    return render_template('credit.html')

"""@app.route('/credit-db')
def creditview():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credits")
    data = c.fetchall()
    conn.close()
    return render_template('credit_view.html', credit=data)"""

@app.route('/credit-db')
def creditview():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credits ORDER BY date DESC")
    data = c.fetchall()
    conn.close()

    return render_template('credit_view.html', credits=data)


if __name__ == '__main__':
    DataBase()
    app.run()



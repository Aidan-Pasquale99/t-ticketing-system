import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_ticket(ticket_id):
    conn = get_db_connection()
    ticket = conn.execute('SELECT * FROM tickets WHERE id = ?',
                        (ticket_id,)).fetchone()
    conn.close()
    if ticket is None:
        abort(404)
    return ticket

app = Flask(__name__)

app.config['secret_key']= 'cf2a034a12571d8847eca7f17b6bcabf75c23f3bd6d1daa8'

@app.route('/')
def index():
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM tickets').fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/<int:ticket_id>')
def ticket(ticket_id):
    ticket = get_ticket(ticket_id)
    return render_template('ticket.html', ticket=ticket)

@app.route('/create_ticket/', methods=(['GET','POST']))
def create_ticket():
  date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  if request.method == 'POST':
    ticket_name = request.form['ticket-name']
    ticket_description = request.form['ticket-description']
    ticket_status = request.form['ticket-status']
    ticket_department = request.form['department']
    ticket_due_date = request.form['due-date']
    ticket_category = request.form['category']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tickets (ticket_name, ticket_description, created_date, due_date, status, department, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (ticket_name, ticket_description, date, ticket_due_date, ticket_status, ticket_department, ticket_category )
              )
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

  # input validation

  # insert successful/unsuccessful message

  # TODO: Test required fields validation using required attribute in html vs if statements here
  # if not title:
  #     flash('Title is required!')
  # elif not content:
  #     flash('Content is required!')
  # else:
  #     return redirect(url_for('index'))
    
  return render_template('create_ticket.html')

@app.route('/update_ticket/<int:ticket_id>', methods=(['GET','POST']))
def update_ticket(ticket_id):
    ticket = get_ticket(ticket_id)
    return render_template('update_ticket.html', ticket=ticket)
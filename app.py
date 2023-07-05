from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

@app.route('/')
def list():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("starbucks_database")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM starbucks_database")
    rows = cur.fetchall()

    # Close the connection to the database
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("product.html",rows=rows)

'''
    con = sqlite3.connect("starbucks_database")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM starbucks_database")

    rows = cur.fetchall()
'''
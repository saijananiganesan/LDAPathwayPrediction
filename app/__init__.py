from flask import Flask, flash, render_template, request, url_for, redirect
import jinja2
import os,sys
sys.path.append('../src/pyext/')
from Model import Model
from Validation import Validation
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import numpy as np
import sqlite3 as sql
from dbconnect import create_users_table,create_login_table

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

def write_html(Template_Dict, template_file):
    template = templateEnv.get_template(template_file)
    outputText=template.render(Template_Dict)
    with open(os.path.join(dirName,output_file),"w") as fh:
        fh.write(outputText)


app = Flask(__name__)
        
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/application/")
def application():
    return render_template("application.html")

@app.route("/LDA1Result/")
def LDA1Result():
    return render_template("LDA1Result.html")

@app.route("/LDA2Result/")
def LDA2Result():
    return render_template("LDA2Result.html")

@app.route("/FTResult/")
def FTResult():
    return render_template("FTResult.html")


@app.route("/LDA1/", methods=['GET','POST'])
def LDA1():
    if request.method=='POST':
        enzyme_string=request.form['Enzyme']
        if enzyme_string:
            return redirect(url_for('LDA1Result'))
        else:
            return "<h1>Please enter enzyme list to proceed.</h1>"

    return render_template("LDA1.html")

@app.route("/LDA2/", methods=['GET','POST'])
def LDA2():
    if request.method=='POST':
        enzyme_string=request.form['link']
        if enzyme_string:
            return redirect(url_for('LDA2Result'))
        else:
            return "<h1>Please enter enzyme list to proceed.</h1>"

    return render_template("LDA2.html")

@app.route("/FastText/", methods=['GET','POST'])
def FastText():
    if request.method=='POST':
        enzyme_string=request.form['link']
        if enzyme_string:
            return redirect(url_for('FTResult'))
        else:
            return "<h1>Please enter enzyme list to proceed.</h1>"

    return render_template("FastText.html")


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name=request.form['Name']
        email=request.form['Email']
        if name and email:
            date,c, conn = create_users_table()
            entry_exists=c.execute("SELECT EXISTS (SELECT 1 FROM users WHERE login=?) AND (SELECT 1 FROM users WHERE email=?)",(name,email)).fetchall()[0][0]
            if entry_exists==0:
                c.execute('INSERT INTO users (date, login, email) VALUES (?,?,?)',(date, name, email))
                conn.commit()
            date,c1, conn1 = create_login_table()
            c1.execute('INSERT INTO login (date, login, email) VALUES (?,?,?)',(date, name, email))
            conn1.commit()
            return redirect(url_for('application'))
        else:
            return "<h1>Please fill your details to proceed.</h1>"

    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)

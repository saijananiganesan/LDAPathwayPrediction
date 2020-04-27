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
import gensim
import pickle
from results_LDA import test_sample

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

def write_html(Template_Dict, template_file,output_file):
    template = templateEnv.get_template('templates/'+template_file)
    outputText=template.render(Template_Dict)
    with open(os.path.join('templates/',output_file),"w") as fh:
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

@app.route("/Result/")
def Result():
    return render_template("CheckResults.html")


@app.route("/Check/", methods=['GET','POST'])
def Check():
    if request.method=='POST':
        enzyme_string=request.form['list']
        if enzyme_string:
            num,text1=test_sample().Check_format(enzyme_string)
            if num==1:
                return "<h1>{}</h1>".format(text1)
            if num==0:
                result=test_sample().Check_In_DB(enzyme_string)
                Template_Dict={}
                Template_Dict['result']=result
                write_html(Template_Dict,"CheckResult_temp.html","CheckResults.html")
                return redirect(url_for('Result'))
            else:
                return "<h1>Please enter valid enzyme list to proceed.</h1>"
        else:
            return "<h1>Please enter enzyme list to proceed.</h1>"
    return render_template("Check.html")


@app.route("/LDA2/", methods=['GET','POST'])
def LDA2():
    if request.method=='POST':
        enzyme_string=request.form['list']
        if enzyme_string:
            return redirect(url_for('LDA2Result'))
        else:
            return "<h1>Please enter enzyme list to proceed.</h1>"

    return render_template("LDA2.html")

@app.route("/FastText/", methods=['GET','POST'])
def FastText():
    if request.method=='POST':
        enzyme_string=request.form['list']
        print (enzyme_string,type(enzyme_string))
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

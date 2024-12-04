from urllib import response
from flask import Flask, jsonify, render_template,request
import requests 
from werkzeug.serving import run_simple
from multiprocessing import Process

practise= Flask(__name__)


@practise.route('/')
def welcome():
    return 'Welcome To Zero pay Nvigate to Home App'

#route fore a home welcome page
@practise.route('/home', methods=['GET','POST'])
def home():
    if request.method=='POST':
        data=request.form.to_dict()
        return jsonify(data)
    
    return render_template('home.html')

#route for the application
@practise.route('/home/App', methods=['Get','POST'])
def app():
     if request.method=='POST':
        data=request.form.to_dict()
        return jsonify(data)

     return render_template('index.html')

#this block runs when the script executed dirctly
if __name__=="__main__":
    practise.run(debug=True)




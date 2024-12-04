#posible imports 
import base64
import json
from tkinter import Image
import pandas as pd
from cgitb import grey
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import  Conv2D, Flatten, MaxPooling2D, Dense 
from urllib import response
from flask import Flask, jsonify, render_template,request
import requests 
from werkzeug.serving import run_simple
from multiprocessing import Process
import pytesseract
import nltk
from nltk.tokenize import word_tokenize

'''from machine_model import extract_text_from_image'''

protype= Flask(__name__)

protype.config['UPLOAD_FOLDER'] = 'uploads'

@protype.route('/upload', methods=['GET','POST'])
def upload_file():
     if request.method == 'POST':
        # Handle the receipt image upload
        receipt_image = request.files.get('file')  # Use .get() to avoid KeyError
        
        # Save the image to a file
        if receipt_image:
            filename = os.path.join(protype.config['UPLOAD_FOLDER'], receipt_image.filename)
            receipt_image.save(filename)
            return jsonify({"message": f"Receipt uploaded successfully. Saved as {filename}"})
        else:
            return jsonify({"error": "No receipt image provided"})
     
     return render_template('index.html') 
     
@protype.route('/extract', methods=['GET', 'POST']) 
def extract_text(): 
    if request.method == 'POST': 
        # Handle file upload 
        if 'file' not in request.files: 
            return jsonify({"error": "No file part"}), 400 
        file = request.files['file'] 
        if file.filename == '': 
            return jsonify({"error": "No selected file"}), 400 
        if file: filepath = os.path.join('uploads', file.filename) 
        file.save(filepath) 
        return jsonify({"message": "File uploaded successfully"}), 201 
    elif request.method == 'GET': 

        # Get the filename from the request 
        if request.is_json:
            data = request.get_json() 
            filename = data.get('filename', '') 

        if filename=='uploads': 
            # Perform OCR on the uploaded receipt image 
            image_path = os.path.join('uploads', filename) 
            text = pytesseract.image_to_string(Image.open(image_path)) 

            # Process the text as needed 
            processed_text = text.upper() # Example processing 

            # Convert the image to JSON 
            with open(image_path, "rb") as image_file: 
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8') 
                image_json = json.dumps({"image_data": encoded_string}) 
                return jsonify({'processed_text': processed_text, 'image_json': image_json}) 
        else: 
            return jsonify({"error": "No filename provided"}), 400

@protype.route('/split_bill',methods=['GET','POST'])
def split_manaual():
    if request.method == 'POST':
        data = request.get_json()
        total_amount = data.get('total_amount')
        num_people = data.get('num_people')

        if not total_amount or not num_people:
            return jsonify({'error': 'Invalid input'}), 400

        try:
            total_amount = float(total_amount)
            num_people = int(num_people)
            if num_people <= 0:
                raise ValueError('Number of people must be greater than zero')
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        amount_per_person = total_amount / num_people
        return jsonify({'amount_per_person': amount_per_person}), 200

    return '''
    <form method="post">
        Total Amount: <input type="text" name="total_amount"><br>
        Number of People: <input type="text" name="num_people"><br>
        <input type="submit" value="Split Bill">
    </form>
    '''

@protype.route('/reciepts', methods=['GET','POST'])
def get_reciepts():
    if request.method=='GET':
        #List all uploaded receipts 
        files = os.listdir('uploads') 
        return jsonify({"receipts": files}), 200

    '''
    implement python code using flask 
    to get all uploaded reciepts 
    '''
    return
      




if __name__ == '__main__':
    protype.run(debug=True)

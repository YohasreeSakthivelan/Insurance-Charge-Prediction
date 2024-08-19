import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
import pickle
from flask import Flask, render_template, request
import pandas as pd
from io import BytesIO
import base64

app = Flask(__name__)
stacking_regressor=pickle.load(open('stacking_regressor.pkl','rb'))
rfmodel=pickle.load(open('rfmodel.pkl','rb'))


@app.route('/')

@app.route('/index')
def index():
	return render_template('index.html')
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/upload')
def upload():
   return render_template('upload.html')
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('age', inplace=True)
        return render_template("preview.html",df_view = df)	

@app.route('/predict')
def predict():
    return render_template('predict.html') 

# Load the model (ensure this path is correct)
 

@app.route('/prediction', methods=['POST'])
def prediction():
        resul = {}  # Default empty dictionary
        result = ''  # Default empty string

        if request.method == 'POST': 
                resul = request.form.to_dict()
                print(resul)
                SEX= request.form['sex'] 
                if SEX == '0':
                   sex = 'male'
                elif SEX == '1':
                    sex = 'female'
                REGION = request.form['region'] 
                if REGION == '0':
                   reg = 'north west'
                elif REGION == '1':
                   reg = 'north east'
                elif REGION == '2':
                   reg = 'south east'
                elif REGION == '3':
                   reg = 'south west'
                SMOKER= request.form['smoker'] 
                if SMOKER == '0':
                   smoker='no'
                elif SMOKER == '1':
                   smoker='yes'

                AGE =int(request.form['age'])
                CHILDREN= int(request.form['children'])
                BMI =float(request.form['bmi'])
                MODEL = request.form['model']
                input_variables = pd.DataFrame([[AGE,SEX,BMI,CHILDREN,SMOKER,REGION]],
                                               columns=['age','sex','bmi','children','smoker','region'],
                                               index=['input'])
                final_features = input_variables.to_numpy()

                if MODEL =="Stacking Regressor":
                  re =stacking_regressor.predict(final_features)
                  
                  RESULT=int(re)
                  r=int(RESULT)*int(RESULT)*int(RESULT)
                  print('the prediction',r)
                elif MODEL == "Random Forest Regressor":
                 re  =rfmodel.predict(final_features)
                 RESULT=int(re)
                 r=int(RESULT)*int(RESULT)*int(RESULT)
                 print('the prediction',r)
                
        return render_template('userdata.html',result=r,MODEL=MODEL,smoker=smoker,sex=sex,BMI=BMI,CHILDREN=CHILDREN,reg=reg,age=AGE)
@app.route('/chart')
def chart():
    return render_template('chart.html') 
@app.route('/userdata')
def userdata():
    return render_template('userdata.html') 
if __name__ == '__main__':
	app.run(debug=True)
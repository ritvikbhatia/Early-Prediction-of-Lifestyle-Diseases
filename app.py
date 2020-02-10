from flask import Flask,render_template,url_for,request
from flask_material import Material

# EDA PKg
import pandas as pd 
import numpy as np 

# ML Pkg
from sklearn.externals import joblib

import requests
import dweepy
import os


app = Flask(__name__)
Material(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/preview')
def preview():
    df = pd.read_csv("data/d_sih.csv")
    return render_template("preview.html",df_view = df)

@app.route('/',methods=["POST"])
def analyze():
	if request.method == 'POST':
		
		age_input = request.form['age_input']
		# height_input = request.form['height_input'] 

		# bmi = (weight_input/(height_input/100)**2)

		gender_choice = request.form['gender_choice']
		smoking_input = request.form['smoking_input']
		exercise_input = request.form['exercise_input']
		drinking_input = request.form['drinking_input']
		bmi_input = request.form['bmi_input']
		# idhr se input le rhe hai html se
		sleep_input = request.form['sleep_input']
		# model_choice = request.form['model_choice']
		# weight_input = request.form['weight_input'] 
		junk_input = request.form['junk_input']

		# h = float(height_input)
		# w = float(weight_input)
		#bmi = (w/(h/100)**2)
		age = float(age_input);
		sex = float(gender_choice)
		bmi= float(bmi_input)
		smoking = float(smoking_input)
		excercise = float(exercise_input)
		sleep = float(sleep_input)
		drinking = float(drinking_input)
		junk = float(junk_input)
		
		a=0;
		b=0;
		c=0;
		x=0;
		y=0;
		z=0;
		if(smoking==1):
			a=a+15.2;
			b=b+15.2;
			c=c+13.1;
		else:
			a=a-3.3;
			b=b-3.3;
			c=c-1.1;
		if(sleep==1):
			a=a+20;
			b=b+11.4;
			c=c+13.2;
		elif(sleep==3):
			a=a+5;
			c=c+20;
			b=b+7.3;
		else:
			a=a-3.3;
			b=b-2.4;
			c=c-4.6;
		if(drinking==1):
			a=a+10;
			b=b+17.4;
			c=c+4;
		else:
			a=a-2.1;
			b=b-9.4;
			c=c-1.1;
		if(sex==1):
			a=a+a*0.6;
			b=b+b*0.3;
			c=c+c*0.4;
		else:
			a=a+a*0.4;
			b=b+b+0.6;
			c=c+c*1.5;
		if(excercise==1):
			a=a+10;
			b=b+5;
		elif(excercise==2):
			a=a-6.1;
			b=b-3.1;
		else:
			a=a-9.1;
			b=b-6.1;
		if(junk==2):
			a=a+5.1;
			b=b+8.1;
		elif(junk==3):
			a=a+15;
			b=b+15;
		else:
			a=a-7.4;
			b=b-5.3;
		if(bmi>30):
			a=a+30;
			b=b+30;
			c=c+9.6;
		elif(bmi<20):
			a=a+10;
			b=b+15.3;
			c=c+9.4;
		elif(bmi>26):
			a=a+5.3;
			b=b+6.1;
			c=c+3.4;
		if(age>45 and age<70):
			a=a+20.3;
			c=c+12.1;
			b=b+15.5;
		elif(age>70):
			a=a+5;
			c=c+10;
			b=b+25
		elif(age<45 and age>15):
			c=c+24;
			b=b+5;
		if(age<18 and bmi<30 and bmi>20):
			a=5;
			c=5;
			b=5;
		if(a>100):
			a=95;
		if(b>100):
			b=94;
		if(c>100):
			c=96;
		if(a<0):
			a=5;
		if(b<0):
			b=6;
		if(c<0):
			c=7;

		if(a>70):
			x=1;
		if(b>70):
			y=1;
		if(c>70):
			z=1;

		dweetIO='https://dweet.io/dweet/for/';
		myName='sih20';
		myName2='sih201';
		myName3='sih2019';
		myName4='sihx';
		myName5='sihy';
		myName6='sihz';

		myKey='Diabetes';
		myKey2='hyper';
		myKey3='depression';
		myKey4='x';
		myKey5='y';
		myKey6='z';
		rqString=dweetIO+myName+'?'+myKey+'='+str(a);
		rqs=requests.get(rqString);
		rqString2=dweetIO+myName2+'?'+myKey2+'='+str(b);
		rqString3=dweetIO+myName3+'?'+myKey3+'='+str(c);

		rqString4=dweetIO+myName4+'?'+myKey3+'='+str(x);
		rqString5=dweetIO+myName5+'?'+myKey3+'='+str(y);
		rqString6=dweetIO+myName6+'?'+myKey3+'='+str(z);

		rqs=requests.get(rqString);
		rqs2=requests.get(rqString2);
		rqs3=requests.get(rqString3);
		rqs4=requests.get(rqString4);
		rqs5=requests.get(rqString5);
		rqs6=requests.get(rqString6);


		# Clean the data by convert from unicode to float 
		sample_data = [age_input,bmi_input,drinking_input,exercise_input,gender_choice,junk_input,sleep_input,smoking_input]
		clean_data = [float(i) for i in sample_data]
		# lean_data = [int(i) for i in sample_data]

		# Reshape the Data as a Sample not Individual Features
		ex1 = np.array(clean_data).reshape(1,-1)

		

			# reloading model 
		logit_model = joblib.load('data/naman_sih.pkl')
		result_prediction = logit_model.predict(ex1)
		result_prediction = int(result_prediction)

	return render_template('index.html', 
		
		age_input = age_input,
		# height_input = height_input,
		gender_choice = gender_choice,
		# weight_input = weight_input,
		sleep_input = sleep_input,
		junk_input = junk_input,
		smoking_input = smoking_input,
		exercise_input = exercise_input,
		drinking_input = drinking_input,
		bmi_input = bmi_input,

		clean_data=clean_data,
		result_prediction=result_prediction)
		# model_selected=model_choice)



if __name__ == '__main__':
	app.run(debug=True)
	dweett()

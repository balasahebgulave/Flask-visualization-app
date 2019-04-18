from flask import Flask, render_template , jsonify , request, session
from random import sample
import pandas as pd
from config import BASE_DIR
import os 
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

file_directory = BASE_DIR+'/static/'
total_files = os.listdir(file_directory)

print('-----------file_directory-----------',file_directory)
print('------total_files------',total_files)

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"



data = pd.read_csv('static/student_record.csv')
jspm = data[data['college_name'] == 'JSPM CoE Hadapsar']
vishw = data[data['college_name'] == 'Vishwaniketan Khalapur']
keystone = data[data['college_name'] == 'Keystone School of Engineering']


@app.route('/configure', methods = ['GET','POST'])
def confugure():
	if request.method == 'POST':
		category = request.form.get('category')
		print('---------------category---------------',category)

		filename = request.form.get('file')
		filters = request.form.get('filter')
		limit = request.form.get('limit')
		plot = request.form.get('plot_type')
		columns = []
		final_result = {}
		if filename is not None:
			print('==========in if==========')
			file = file_directory+filename
			filedata = pd.read_csv(file, encoding = 'latin1')
			columns = list(filedata.columns)
			session['filename'] = filename
			session['columns'] = columns

		if plot is not None:
			try:
				x = 0
				y = 0
				print('==========in else==========',plot)
				filedata = pd.read_csv(file_directory + session['filename'], encoding='latin1')
				for col in filedata.columns:
					filedata[col] = encoder.fit_transform(filedata[col])
				# print('---------filedata----------',filedata)	
				selected_columns = []
				for i in session['columns']:
					# print('------i------',i)
					i = request.form.get(i)
					# print('=======columns======',i)
					if i != None:
						selected_columns.append(i)
				session['plot'] = plot
				session['x']=list(filedata[selected_columns[-2]])
				session['y']=list(filedata[selected_columns[-1]])
				minimum = min(session['y'])
				maximum = max(session['y'])
				session['minimum'] = minimum
				session['maximum'] = maximum
				x = session['x']
				y = session['y']
				final_result = {'results': y , 'labels': x , 'plot':session['plot'], 'minimum':session['minimum'], 'maximum':session['maximum']}

			except Exception as e:
				print('---------------------error_message-----------------',e)
				

		if filters is not None:
			print('-----------filter-------------',filters)
			x = []
			y = []
			for i , j in zip(session['x'],session['y']):
				if j == int(filters):
					x.append(i)
					y.append(j)
			final_result = {'results': y , 'labels': x , 'plot':session['plot'], 'minimum':session['minimum'], 'maximum':session['maximum']}

			print('------------------x,y----------------',x,y)


		if limit is not None:
			print('-----------limit-------------',limit)
			x = []
			y = []
			for i , j in zip(session['x'],session['y']):
				if j <= int(limit):
					x.append(i)
					y.append(j)
			final_result = {'results': y , 'labels': x , 'plot':session['plot'], 'minimum':session['minimum'], 'maximum':session['maximum']}


			
			if session['plot'] == None:
				session['plot'] = 'bar'
			# print('----------x-------------',x)


		print('-------final-------',final_result)
		return render_template('configure.html', columns = columns, total_files = total_files, final_result = final_result)
	return render_template('configure.html', total_files=total_files)






@app.route('/data')
def data():
	return jsonify({'results':[len(jspm), len(vishw), len(keystone)]})

@app.route('/', methods = ['POST', 'GET'])
def interactive():
	if request.method == 'POST':
		college = request.form.get('college')
		if college == "jspm":
			generated_result = {'results':list(jspm.score),'labels':list(range(len(jspm.name)))}
		if college == "vishwaniketan":
			generated_result = {'results':list(vishw.score),'labels':list(range(len(vishw.score)))}
		if college == "keystone":
			generated_result = {'results':list(keystone.score),'labels':list(range(len(keystone.score)))}

		return render_template('chart.html' , generated_result = generated_result)
		# return jsonify({'results':[red,blue,yellow,green,purple,orange]})

	return render_template('chart.html')



@app.route('/jspm' , methods = ['POST','GET'])
def jspm_filters():
	initial = int(min(list(jspm.score)))
	final = int(max(list(jspm.score)))
	filter_result ={'data':list(range(initial,final))}
	if request.method == 'POST':
		response = request.form.get('filter')
		limit = request.form.get('limit')
		print('======response=======',response)
		print('======limit=======',limit)

		if response is not None:
			y = [i for i in jspm.score if int(i)== int(response)]
			x = list(range(len(y)))
			filter_result = {'results':y, 'labels':x}
			if len(filter_result['results']) == 0:
				filter_result['error_message'] = 'No Matched Results Found'
			filter_result['data'] = list(range(initial,final))
		else:
			y = [i for i in jspm.score if int(i)<= int(limit)]
			x = list(range(len(y)))
			filter_result = {'results':y, 'labels':x}
			if len(filter_result['results']) == 0:
				filter_result['error_message'] = 'No Matched Results Found'
			filter_result['data'] = list(range(initial,final))
		
		print('=============',filter_result)

		return render_template('jspm.html', filter_result = filter_result)

	return render_template('jspm.html', data = filter_result['data'] )





@app.route('/vishw' , methods = ['POST','GET'])
def vishw_filters():
	initial = int(min(list(vishw.score)))
	final = int(max(list(vishw.score)))
	filter_result ={'data':list(range(initial,final))}
	if request.method == 'POST':
		response = request.form.get('filter')
		limit = request.form.get('limit')
		print('======response=======',response)
		print('======limit=======',limit)

		if response is not None:
			y = [i for i in vishw.score if int(i)== int(response)]
			x = list(range(len(y)))
			filter_result = {'results':y, 'labels':x}
			if len(filter_result['results']) == 0:
				filter_result['error_message'] = 'No Matched Results Found'
			filter_result['data'] = list(range(initial,final))
		else:
			y = [i for i in vishw.score if int(i)<= int(limit)]
			x = list(range(len(y)))
			filter_result = {'results':y, 'labels':x}
			if len(filter_result['results']) == 0:
				filter_result['error_message'] = 'No Matched Results Found'
			filter_result['data'] = list(range(initial,final))
		
		print('=============',filter_result)

		return render_template('vishw.html', filter_result = filter_result)

	return render_template('vishw.html', data = filter_result['data'] )




@app.route('/keystone' , methods = ['POST','GET'])
def keystone_filters():
	initial = int(min(list(keystone.score)))
	final = int(max(list(keystone.score)))
	filter_result ={'data':list(range(initial,final))}
	if request.method == 'POST':
		response = request.form.get('filter')
		limit = request.form.get('limit')
		print('======response=======',response)
		print('======limit=======',limit)

		if response is not None:
			y = [i for i in keystone.score if int(i)== int(response)]
			x = list(range(len(y)))
			filter_result = {'results':y, 'labels':x}
			if len(filter_result['results']) == 0:
				filter_result['error_message'] = 'No Matched Results Found'
			filter_result['data'] = list(range(initial,final))
		else:
			y = [i for i in keystone.score if int(i)<= int(limit)]
			x = list(range(len(y)))
			filter_result = {'results':y, 'labels':x}
			if len(filter_result['results']) == 0:
				filter_result['error_message'] = 'No Matched Results Found'
			filter_result['data'] = list(range(initial,final))
		
		print('=============',filter_result)

		return render_template('keystone.html', filter_result = filter_result)

	return render_template('keystone.html', data = filter_result['data'] )




if __name__ == '__main__':
	app.run(host = 'localhost', debug = True)
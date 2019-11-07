from flask import Flask,jsonify,request,render_template
import requests
import datetime
import os
import mysql.connector
from dbClass import MyDB

app = Flask(__name__)







@app.route('/handle_data',methods=['GET','POST'])
def handle_data():
    myvariable = request.form.get("clinDropDown")

    req = requests.get('https://clinicaltrialsapi.cancer.gov/v1/clinical-trial/' + myvariable)
    req = req.json()
    listDiseases = []
    clinValue = request.form.get("clinValues")
    if(clinValue == 'diseases'):
        for key in req:
            if key ==  'diseases':
                for disease in req.get(key):
                    for dis in disease:
                        if dis == 'display_name':
                            listDiseases.append(disease.get(dis))
                            
        return render_template('clinical.html',diseaseTable=listDiseases,clinid=myvariable)

    else:
        summary = ""
        for key in req:
            if key ==  clinValue:
                summary = req.get(key)

        return render_template('clinical.html',data=summary,clinid=myvariable)


  



@app.route('/')  # 'http://www.google.com/'  home page
def home():
	return  render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clinical')
def clinicalhome():
    return render_template('clinical.html')


@app.route('/nasahome')
def nasahome():
    return render_template('nasa.html')
@app.route('/employeehome')
def employeehome():
    return render_template('company.html')



@app.route('/nasa_today',methods=['POST'])
def nasa_today():
    myvariable = request.form.get("ddnasatoday")
    req = requests.get('https://api.nasa.gov/planetary/apod?api_key=yUfM1D3hMBjlmIZzhG8GjHwI0LigOR5ub59bi3i6')
    req = req.json()
    for key in req:
      if(key == myvariable):
        title = req[key]

    return render_template('nasa.html',data=title)




@app.route('/clinical/<string:clinid>')
def clinical(clinid):
	req = requests.get('https://clinicaltrialsapi.cancer.gov/v1/clinical-trial/' + clinid)  
	req = req.json()
	summary = ""
	for key in req:
		if key == 'brief_summary':
			summary = req.get(key)
	return render_template('clinical.html',data=summary)

 




@app.route('/rates/<string:name>')
def getRates(name):
	inName = name
	req = requests.get('https://api.ratesapi.io/api/latest')
	req = req.json()
	rates = req['rates']
	cur = str(rates[inName])
	return  render_template('index.html',rate = cur)



@app.route('/employees')
def get_employees():
	data = ""
	requeset_data = request.get_json()
	for emp in employees:
		data = emp['lastname'] + emp['firstname'] + '\n'


	return data	



@app.route('/davinci')
def getEmployees():
     
   lastname = ""
   firstname = ""

   db = MyDB('localhost','davinci')
   conn =   None
   conn = db.getConn()

   cursor = conn.cursor()



   cursor.execute("SELECT *  FROM employees " )
   data = cursor.fetchall()
   cursor.close()
   conn.close()
 
   return  render_template('index.html',data=data)







@app.route('/company')
def getCompanies():
     

   db = MyDB('localhost','davinci')
   conn =   None
   conn = db.getConn()

   cursor = conn.cursor()



   cursor.execute("SELECT *  FROM company " )
   data = cursor.fetchall()
   cursor.close()
   conn.close()
 
   return  render_template('index.html',data=data)








@app.route('/davinci/<string:dept>')
def getDept(dept):
     
   
   db = MyDB('localhost','davinci')
   conn =   None
   conn = db.getConn()

   cursor = conn.cursor()



   cursor.execute("SELECT *  FROM employees where dept =  "  + dept)
   data = cursor.fetchall()
   cursor.close()
   conn.close()
 
   return  render_template('index.html',data=data)





@app.route('/davinci')
def getDavinci():
    return render_template('index.html')



"""
    Connect to MySQL database 
    conn = None
    conn = mysql.connector.connect(host='localhost',
                                       database='davinci',
                                       user='dpm',
                                       password='sql')
#    if conn.is_connected():
#        print('Connected to MySQL database')
#    return conn 
# if __name__ == '__main__':
#    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    emps = {} 
    app.run(debug=True)
    row = cursor.fetchone()
 
    while row is not None:
        emps.update({row[0]:row[1] + ',' + row[2]})
        print(row)
        row = cursor.fetchone()
 
    cursor.close()
    conn.close()
    empstr = ""
    for emp in emps:
        empstr += str(emp) + "==>" + emps.get(emp) + '\n'

    

    return empstr
 
"""



if __name__ == "__main__":
    app.run(port=5000,debug=True)


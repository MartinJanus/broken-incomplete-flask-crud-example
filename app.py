from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '127.0.0.1'
mysql.init_app(app)

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  if not name and not email:
      return '{"Error":"Name or email required for update"}'

  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email) # kludge - use stored proc or params
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Added Student Success"}' # Really? maybe we should check!
  
@app.route("/") #Default - Show Data
def read(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format

@app.route("/update/<int:studentId>")
def update(studentId):
  name = request.args.get('name')
  email = request.args.get('email')

  if not name and not email:
      return '{"Error":"Name or email required for update"}'

  cur = mysql.connection.cursor()
  query = '''UPDATE students SET studentName='{}', email='{}' WHERE studentID={}'''.format(name, email, studentId)
  cur.execute(query)
  mysql.connection.commit()
  cur.close()
  return '{"Result":"Update Success"}' 


@app.route("/delete/<int:studentId>")
def delete(studentId):
    cur = mysql.connection.cursor()
    queryCheck = '''SELECT * FROM students WHERE studentID={}'''.format(studentId)
    cur.execute(queryCheck)
    student = cur.fetchone() #checking if student exists

    if not student:
        cur.close()
        return '{"Error":"Student ID not found"}'

    queryDelete = '''DELETE FROM students WHERE studentID={}'''.format(studentId)
    cur.execute(queryDelete)
    mysql.connection.commit()
    cur.close()
    return '{"Result":"Delete Success"}' 


if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080
from flask import Flask, request, jsonify
import json
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
  host="188.166.221.246",
  user="training",
  password="training",
  database="retail_db"
)

class Customers:
  def __init__(self, customer_id, customer_fname, customer_lname, customer_email, customer_password,
    customer_street, customer_city, customer_state, customer_zipcode):
    self.customer_id = customer_id
    self.customer_fname = customer_fname
    self.customer_lname = customer_lname
    self.customer_email = customer_email
    self.customer_password = customer_password
    self.customer_street = customer_street
    self.customer_city = customer_city
    self.customer_state = customer_state
    self.customer_zipcode = customer_zipcode

@app.route("/", methods=['GET']) # http://127.0.0.1:5000/ (GET API tanpa parameter)
def apiGetCustomerHandler():
  # SELECT dari database
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM customers")
  myresult = mycursor.fetchall()

  # Pindahkan data dari hasil SELECT Database ke array of object
  data_customers = []
  for x in myresult:
    customers = Customers(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    data_customers.append(customers)
  
  # Ubah array of object menjadi JSON string (JSON yang dijadikan string)
  json_string = json.dumps([ob.__dict__ for ob in data_customers])

  # Menyiapkan response yang diberikan
  response = app.response_class(
    response = json_string,
    status = 200,
    mimetype = "application/json" # Header content-type
  )
  return response

@app.route("/getcustomerbyid", methods=['GET']) # http://127.0.0.1:5000/getcustomerbyid?id=1 (GET API dengan parameter)
def apiGetCustomerByIdHandler():
  # Mendapatkan GET request parameter
  args = request.args
  id = args.get("id")

  mycursor = mydb.cursor()
  # Pehatikan! Query dengan menggunakan WHERE
  mycursor.execute("SELECT * FROM customers WHERE customer_id=" + id)
  myresult = mycursor.fetchall()

  data_customers = []
  for x in myresult:
    customers = Customers(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    data_customers.append(customers)
  
  json_string = json.dumps([ob.__dict__ for ob in data_customers])

  response = app.response_class(
    response = json_string,
    status = 200,
    mimetype = "application/json" # Header content-type
  )
  return response

# NGETEST HARUS INSTALL POSTMAN !!!
@app.route("/postcustomerbyid", methods=['POST']) # (POST API dengan parameter berupa JSON)
def apiPostCustomerByIdHandler():
  # Mendapatkan POST request parameter
  data = request.get_json()
  id = data.get("id")

  mycursor = mydb.cursor()
  # Pehatikan! Query dengan menggunakan WHERE
  mycursor.execute("SELECT * FROM customers WHERE customer_id=" + id)
  myresult = mycursor.fetchall()

  data_customers = []
  for x in myresult:
    customers = Customers(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    data_customers.append(customers)
  
  json_string = json.dumps([ob.__dict__ for ob in data_customers])

  response = app.response_class(
    response = json_string,
    status = 200,
    mimetype = "application/json" # Header content-type
  )
  return response

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8005, debug=True)
  app.run()
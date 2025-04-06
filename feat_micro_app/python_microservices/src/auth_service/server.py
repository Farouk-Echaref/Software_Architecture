import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

# allow our app to connecnt to our db and to query our mysql database
mysql = MySQL(server)

# mysql config 

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# setup a basic route for the login using POST method cs we are posting login data
@server.route("/login", methods=["POST"])
def login(): # function to handle login
    # easily extract credentials from the Authorization header in a request. It works when you're using HTTP Basic Auth
    auth = request.authorization 

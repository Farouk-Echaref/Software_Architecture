import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

# this auth service will have its own mysql database
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

    # can't have a request header without authentication
    if not auth:
        return "Missing Credentials", 401
    
    # in case we have credentials, we check if they exist in the DB
    # need to make a query to the mysql db using cursor object
    # think of the cursor like a tmp pointer for navigating and interacting with the database.
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    # at least one user was found
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid Credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid Credentials", 401


@server.route("/validate", methods=["POST"])
def validate():

    # retrieve the JWT token, will be validated through the API Gateway
    encoded_jwt = request.headers["Authorization"]

    # if its not passed through the request
    if not encoded_jwt:
        return "Missing Credentials", 401
    
    # the header thats sent with the jwt : Authorization: Bearer <token>
    # retrieve the token
    encoded_jwt = encoded_jwt.split(" ")[1]
    
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "Not Authorized", 403
    
    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            # user is admin or not
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )

# expose the server to be called from elsewhere
if __name__ == "__main__":
    # this works if the service can belong to multiple networks, but can be better, map the ip of the docker container
    server.run(host="0.0.0.0", port=5000)
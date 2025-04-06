# Microservice Architecture and System Design with Python & Kubernetes

![alt text](micro_app.png)

## Dependencies:

- install k9s
- install minikube
- setup flask
- pip install jwt
- install flask mysql : sudo pip3 install Flask-MySQLdb --break-system-packages
- MySQL for the auth service
- start and connect to it :
```bash
brew services start mysql
mysql -uroot
```

## Auth Service:
### 🧠 What is `request.authorization`?

`request.authorization` is a **Flask** feature that lets you easily extract credentials from the **Authorization header** in a request. It works when you're using **HTTP Basic Auth**.

#### 🔒 What’s HTTP Basic Auth?

Basic Auth is a simple way to send a **username and password** with an HTTP request. The client includes an `Authorization` header that looks like this:

```
Authorization: Basic base64(username:password)
```

For example:

- Username: `alice`
- Password: `1234`
- Combined: `alice:1234`
- Base64 encoded: `YWxpY2U6MTIzNA==`

The full header becomes:
```
Authorization: Basic YWxpY2U6MTIzNA==
```

---

### 🔍 How does Flask handle this?

When the request comes in, Flask decodes that header automatically. If you do:

```python
auth = request.authorization
```

`auth` becomes an object with:

```python
auth.username  # 'alice'
auth.password  # '1234'
```

If there's no Authorization header or it’s not in Basic format, `auth` will be `None`.

---

### 🧪 Use Case Example

Let’s say we want to protect the `/login` route with Basic Auth and only allow a specific username/password combo:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    
    # If no auth provided or wrong credentials
    if not auth or auth.username != "admin" or auth.password != "secret":
        return jsonify({"message": "Authentication failed"}), 401

    return jsonify({"message": "Welcome, admin!"}), 200
```

#### 🔐 How to test it:

Using **curl**:
```bash
curl -X POST -u admin:secret http://localhost:5000/login
```

Using **Postman**:
- Choose `POST` and URL `http://localhost:5000/login`
- Go to `Authorization` tab
- Choose `Basic Auth`
- Set username = `admin`, password = `secret`

---

### Database "auth" for our auth service


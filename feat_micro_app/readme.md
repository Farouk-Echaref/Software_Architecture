# Microservice Architecture and System Design with Python & Kubernetes

![alt text](micro_app.png)

- general resource: 
    * https://www.youtube.com/watch?v=hmkF77F9TLw&t=4077s

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

### Connect to DB and execute a query:

- use mysql.connection which is the active DB connection.
- using a cursor object (allows to execute SQL queries and retrieve results)
- A cursor in SQL is a database object used to retrieve and manipulate data row by row, rather than fetching an entire result set at once.

- resources:
    - https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-cursor.html
    - https://flask-mysql.readthedocs.io/en/stable/

#### why **email=%s**, and not string formatting

- this uses parametrized queries:
```sql
SELECT email, password FROM user WHERE email=%s
```

- then safely passes the value as a tuple:
```python
(auth.username,)
```

- why is this better than doing:
```python
f"SELECT ... WHERE email='{auth.username}'"
```

- Because:
    * **it's safe against SQL Injection attacks**.
    * The database driver handles escaping and formatting internally.

### Gateway overview and the use of JwT tokens (Basic auth and JSON Web Tokens): 

- resources:
    - https://dev.to/jaypmedia/jwt-explained-in-4-minutes-with-visuals-g3n
    - https://stackoverflow.com/questions/37582444/jwt-vs-cookies-for-token-based-authentication
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Authentication


- Our microservices are going to be running in a k8s cluster, and that cluster internal network is not going to be accessible to or from the outside world.

- our client will be making requests from outside the cluster, with the intention of making use of our distributed system deployed within our private k8s cluster via our system's **Gateway**, so our **Gateway** service is going to be the entrypoint to the overall application, and the gateway service is going to be the service that receives requests from the client, it will be the service that communicates with the necessary internal services to fulfill the requests received from the client.

- Our **Gateway** is going to be also where we define the functionality of our overall application.

- So if our internal services live within an internal network, how to we determine when should allow requests in from the open internet? 

- This is where our auth service comes in, we can give clients access to our application, by creating credentials for them within our auth DB (User Password Combination).

- this is where the authentication scheme called **Basic Authentication** or **Basic Access Authentication** comes in...

- after success login (match in the credentials in our db), we know the user has access, and we return a JWT to the client, which the client will use for subsequent requests to our gateway's upload and download endpoints.

- for json web tokens (jwt) look the provided docs.
- Authentication scheme  bearer: **Authorization: Bearer <token>**
- encoding and decoding jwt flask resource: 
    * https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-hs256

### Build dockerfile

- used of cached layer to optimize the build of docker images (requirements layer before app layer). 

- pip3 freeze > requirements.txt
- build image
- use docker scan
- use of docker hub to store images
- name the repo auth (for the auth service)
- docker tag ... (tag the image)
- docker push hub_name/auth:tag

### Manifests for k8s configs

- k8s archi and interaction with k8s api.
- deployment strategies (strategy to use to replace existing pods with new ones):
    * how to know the metrics of max surge...
    * https://www.youtube.com/watch?v=lxc4EXZOOvE
    * https://medium.com/@muppedaanvesh/rolling-update-recreate-deployment-strategies-in-kubernetes-%EF%B8%8F-327b59f27202
- configMap and Secret:
    * https://www.getambassador.io/blog/kubernetes-configurations-secrets-configmaps
- use of vault:
    * https://www.vaultproject.io/use-cases/kubernetes
    * https://developer.hashicorp.com/vault/tutorials/kubernetes/vault-secrets-operator
- the manifests when applied will interface with the k8s api, which is the api for our k8s cluster, to create our components (deployment, services...)
    ```bash
    kubectl apply -f ./
    ```

## Gateway Service:

![alt text](API_GATEWAY.png)

- use of NGINX as API Gateway:
    * https://medium.com/@nirmalkumar30/a-simple-guide-to-configure-nginx-as-an-api-gateway-684924cd51d0
    * https://www.solo.io/topics/nginx/nginx-api-gateway
- resource: https://www.youtube.com/watch?v=6ULyxuHKxg8
- resource: https://www.youtube.com/watch?v=JNmiOw26PGg&t=3s

- an API Gateway is a single point of entry to the clients of an application. it sits between the clients and a collection of backend services for the application. it provides:
    * Authentication and security policy enforcements.
    * load balancing and circuit breaking. 
    * protocol translation and service discovery.
    * monitoring, logging, analytics and billing.
    * caching.

## MongoDB and gridFS:

- docs: https://www.mongodb.com/docs/manual/reference/limits/
- docs: https://www.mongodb.com/docs/manual/core/gridfs/
- mongoDB used to store mp3 files and videos (BSON docs).
- gridFS divides files into parts or chunks (handle files larger than 16m by sharding the files).

## RabbitMQ (DIstributed System)

- resource: https://www.youtube.com/watch?v=7rkeORD4jSw

### Video to MP3 Microservice Architecture
---

#### Flow Description (RabbitMQ)

1. **Client Upload**:
    - A user uploads a video through the **Client App**.
    - The request is routed to the **API Gateway** (producer).
    - The **API Gateway** authenticates the user via the **Auth Service** and stores the video in **MongoDB (Storage DB)**.

2. **Queue Message #1**:
    - The API Gateway sends a message to **RabbitMQ**, indicating a new video is available for processing.

3. **Video Processing**:
    - The **Video-to-MP3 Converter Service** consumes the message from RabbitMQ.
    - It retrieves the video from **MongoDB**, converts it to MP3, and stores the MP3 back in **MongoDB**.

4. **Queue Message #2**:
    - After conversion, the service pushes a new message to RabbitMQ, stating that the MP3 is ready.

5. **Notification**:
    - The **Notification Service** consumes the "conversion complete" message.
    - It sends an email to the user containing the **MP3 ID**.

6. **Download**:
    - The user sends a request with the **MP3 ID** and **JWT** to the API Gateway.
    - The **API Gateway** authenticates the user and fetches the MP3 from **MongoDB**, then returns it to the client.

---

#### Components

- **Client**
- **API Gateway**
- **Auth Service**
- **RabbitMQ**
- **Video to MP3 Service**
- **Notification Service**
- **Auth DB**
- **Storage DB (MongoDB)**

---

#### ASCII Architecture Flow

```
              ┌────────────┐
              │   Client   │
              └────┬───────┘
                   │
         Upload Video (JWT + file)
                   ▼
           ┌──────────────┐
           │ API Gateway  │
           └────┬──┬──────┘
                │  │
      Auth Req. │  └─────> Put message on RabbitMQ
                ▼
        ┌────────────┐
        │ Auth Svc   │
        └────┬───────┘
             ▼
       ┌──────────┐
       │ Auth DB  │
       └──────────┘

--- Queue Triggered Processing ---

           ┌────────────────────────┐
           │ Video to MP3 Service   │◄─────────────┐
           └─────────┬──────────────┘              │
                     ▼                             │
              ┌────────────┐                       │
              │ Storage DB │ (Video & MP3)         │
              └────┬───────┘                       │
                   │                               │
        Convert Video to MP3                       │
                   ▼                               │
      Push "conversion done" message ──────────────┘

--- Notification Stage ---

           ┌────────────────────┐
           │ Notification Svc   │◄─────────────┐
           └──────────┬─────────┘              │
                      ▼                        │
             Email MP3 ID to Client            │
                                               │
--- Client Downloads MP3 ----------------------┘

              ┌────────────┐
              │   Client   │
              └────┬───────┘
                   │
       Request MP3 (JWT + mp3_id)
                   ▼
           ┌──────────────┐
           │ API Gateway  │
           └────┬─────────┘
                ▼
           ┌────────────┐
           │ Storage DB │
           └────┬───────┘
                ▼
          MP3 file returned
```

---

## Key Concepts for the architeture :

* Asynchronous and Synchronous Interservice Communication.
* Strong and Eventual Consistency.

---

### Synchronous Interservice Communication

> **Synchronous communication** occurs when the **calling service waits (blocks)** for a response from the **called service** before proceeding.

- In this model, the **client service is blocked** and **cannot continue** other tasks until it receives a response.
- This form of communication is **blocking** in nature.
- In our system, the **API Gateway communicates synchronously with the Auth Service**.
- For instance, when a user logs in:
  - The **Gateway** sends an **HTTP POST request** to the **Auth Service**.
  - The **Gateway is blocked** until the **Auth Service responds** with a **JWT** or an **error**.
- This creates **tight coupling** between the two services.

**Key Takeaways**:
- **Blocking call**
- Gateway <-> Auth Service
- Tightly coupled interaction

---

#### ASCII Diagram

```
[ Client ]
    │
    ▼
[ API Gateway ]
    │  HTTP POST (login)
    ▼
[ Auth Service ]
    │     ▲
    │     │
    └─────┘
   Wait for response
```

> The API Gateway waits (blocks) here until the Auth Service responds.

---

### Asynchronous Interservice Communication

> **Asynchronous communication** allows the calling service to continue its tasks without waiting for a response from the downstream service — this is called **non-blocking** communication.

- In your architecture, this is achieved using a **message queue**.
- For example:
  - The **API Gateway** needs to communicate with the **Converter Service**.
  - If done synchronously, the **Gateway would be blocked**, especially when processing large videos or handling multiple requests.
- Instead, the **Gateway pushes a message to the queue**, and the **Converter Service consumes it later**.
- This design means:
  - The **Gateway and Converter Service are loosely coupled**.
  - The **Gateway doesn’t wait** for a response — it performs a **"fire-and-forget"** action.
  - Similarly, once conversion is done, the **Converter Service pushes another message** to the queue for the **Notification Service**, continuing the **asynchronous flow**.

**Key Takeaways**:
- Non-blocking requests
- Queue-based decoupling
- Gateway ↔ Converter ↔ Notification via queue
- Loose coupling between services

---

#### ASCII Diagram

```
[ Client ]
    │
    ▼
[ API Gateway ]
    │
    ├──► Store video in MongoDB
    │
    └──► Push message to Queue ─────► [ Converter Service ]
                                          │
                                          ├──► Pull video from MongoDB
                                          ├──► Convert to MP3
                                          └──► Push message to Queue ───► [ Notification Service ]
                                                                                │
                                                                                └──► Send Email
```

> Messages are pushed to the queue, and services process them **asynchronously** when they are ready.

---

### Strong Consistency:
### Eventual Consistency:

## Gateway Logic:

- login route to communicate with auth service after client want to login.
- **__init__.py** in auth_svc to mark the directory as a package.
- use of **requests** package to make HTTP request between the gateway and the auth service.
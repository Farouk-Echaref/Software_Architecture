# API (Application Programming Interface)

An API is a set of rules and protocols that allow one piece of software to interact with another. Think of it like a menu in a restaurant — it tells you what you can order (i.e., what the system can do) and what input it needs.

- **Example**: A weather API lets you ask for the weather by city name, zip code, or GPS coordinates.
- An API contains multiple endpoints.
- APIs are collections of **endpoints**. Each endpoint is a precise point of communication in the API.
- An API is just code — a part of an application (usually on a server) that listens for specific requests and responds with data.
- You can think of it as a set of functions or methods exposed over the internet (or locally) that other programs can call.

> “An API, or Application Programming Interface, is a set of defined rules that allows two applications to communicate. Physically, it’s just code running on a server that listens for HTTP requests (like GET or POST) on specific URLs — which we call endpoints — and responds with data, usually in JSON format. So when I call an API, I'm sending a request to that code, and it's returning something useful like user info, weather data, or whatever it's designed to provide.”

---

## Example in Real Terms

Let’s say you’re building a weather app:

- The **Weather API** is hosted on a server.
- It has an endpoint:  
  `https://api.weather.com/current?city=Paris`
- When you send a `GET` request to that endpoint:
  - The code running on their server receives it,
  - Processes it,
  - Fetches the weather data,
  - And returns it to you as **JSON**.

### So physically:

- It's a **web server**.
- With **code** (often in Node.js, Python, etc.).
- That defines **routes** (`/current`, `/forecast`).
- And handles **HTTP requests and responses**.

---

# Endpoint

An **endpoint** is a specific URL within an API that performs a particular function. It's the "address" where the resource lives and the actual path you hit to get or send data.

- **Example (Weather API)**:
  - `GET /weather?city=Paris`
  - `GET /forecast?lat=48.85&lon=2.35`

Each endpoint does something specific — like returning current weather or a 7-day forecast.

---

# Basic Flask API with One Endpoint

```python
from flask import Flask, jsonify

# Create the Flask app
app = Flask(__name__)

# Define an endpoint
@app.route('/hello', methods=['GET'])
def say_hello():
    return jsonify({"message": "Hello, world!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

- **API**: The whole app is our API — it handles requests.
- **Endpoint**: The `/hello` route is an endpoint. It listens for GET requests and returns JSON.

### Once this is running:

Visit [http://127.0.0.1:5000/hello](http://127.0.0.1:5000/hello) in your browser or use `curl`:

```bash
curl http://127.0.0.1:5000/hello
```

**Output:**

```json
{
  "message": "Hello, world!"
}
```

---

## Another Endpoint for User Info

Let’s say you want to get user info:

```python
@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    return jsonify({"username": username, "status": "active"})
```

Now, hitting:

```bash
http://127.0.0.1:5000/user/john
```

**Returns:**

```json
{
  "username": "john",
  "status": "active"
}
```

---

# NestJS API

NestJS uses **controllers** to define endpoints.

### 1. Install NestJS (if you haven’t already):

```bash
npm i -g @nestjs/cli
nest new my-api
cd my-api
```

### 2. Edit the main controller: `src/app.controller.ts`

```ts
import { Controller, Get, Param } from '@nestjs/common';

@Controller()
export class AppController {

  @Get('hello')
  getHello(): any {
    return { message: 'Hello, world!' };
  }

  @Get('user/:username')
  getUser(@Param('username') username: string): any {
    return {
      username: username,
      status: 'active',
    };
  }
}
```

### Explanation

- `@Controller()` declares a controller (like a Flask app).
- `@Get('hello')` is an endpoint that handles `GET /hello`.
- `@Get('user/:username')` is a dynamic route like `/user/john`.

---

### Run the API

```bash
npm run start
```

Then test in your browser or Postman:

- `GET http://localhost:3000/hello`  
  → `{ "message": "Hello, world!" }`

- `GET http://localhost:3000/user/john`  
  → `{ "username": "john", "status": "active" }`

--- 

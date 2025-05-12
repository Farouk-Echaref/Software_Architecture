# 🔁 Middleware vs API Gateway

| Feature      | **Middleware**                                                 | **API Gateway**                                           |
| ------------ | -------------------------------------------------------------- | --------------------------------------------------------- |
| **Location** | Inside the **application codebase**                            | A **separate component** sitting in front of services     |
| **Scope**    | Per application (or service)                                   | System-wide (across services)                             |
| **Purpose**  | Modify/inspect requests/responses as they pass through the app | Handle cross-cutting concerns before reaching any backend |
| **Example**  | Express.js middleware (`app.use(authMiddleware)`)              | NGINX, Kong, Envoy, AWS API Gateway                       |

---

## 🧱 Monolith vs Microservices: Where Each Fits

| Concern                                 | Monolith (using Middleware)              | Microservices (using API Gateway)                    |
| --------------------------------------- | ---------------------------------------- | ---------------------------------------------------- |
| **Authentication / Token Validation**   | Middleware checks JWT/session            | API Gateway offloads token check before forwarding   |
| **Rate Limiting**                       | Implemented via middleware or web server | Centralized in API Gateway (per IP/client/token)     |
| **Caching**                             | Middleware/headers per route             | API Gateway caches responses (e.g., GET `/products`) |
| **Logging/Tracing**                     | Middleware adds logs to app logs         | Gateway handles centralized logging, correlation ID  |
| **Routing**                             | Internal route resolution                | Gateway maps endpoints to specific services          |
| **Security (e.g., CORS, IP Whitelist)** | Middleware handles per route             | Gateway enforces rules globally                      |
| **Compression, Request Size Limits**    | App-level (e.g., `body-parser`)          | Gateway can reject/compress upstream                 |

---

## 🛠 Example Scenario: Authenticated Request to `GET /products`

### **Monolith**

* Request hits `Express` server.
* **Middleware flow**:

  1. CORS Middleware
  2. Rate Limiting Middleware (e.g., `express-rate-limit`)
  3. Token Auth Middleware
  4. Business Logic
* Response cached in app or CDN.

### **Microservices with API Gateway**

* Request hits API Gateway.

  1. CORS headers added
  2. Rate limit enforced at Gateway
  3. JWT token validated via Auth Plugin
  4. Caching (e.g., Redis or built-in)
  5. Forwarded to `Product Service`
* Downstream services are protected and clean.

---

## ✅ When to Use What

* **Use Middleware when**:

  * You're in a monolith or want tight coupling with logic.
  * Concerns are specific to one app (e.g., logging for just the user-service).

* **Use API Gateway when**:

  * You have multiple microservices.
  * You want centralized control of auth, routing, caching, rate limiting, etc.
  * You want to simplify and decouple cross-cutting logic from services.

---

## ⚖️ Summary

| Feature          | Middleware (App Code)   | API Gateway (Infra Level)     |
| ---------------- | ----------------------- | ----------------------------- |
| Token Validation | ✔️ (per app)            | ✔️ (central)                  |
| Rate Limiting    | ⚠️ (hard to coordinate) | ✔️ (easy & unified)           |
| Caching          | ⚠️ (manual)             | ✔️ (built-in or plugin-based) |
| Service Routing  | ❌                       | ✔️                            |
| Scaling          | Tied to app             | Independent, scalable         |


---

## ⚙️ MIDDLEWARE (MONOLITH) IMPLEMENTATIONS

---

### 🟦 1. **NestJS (Monolith - Middleware)**

```ts
// jwt.middleware.ts
@Injectable()
export class JwtMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const token = req.headers['authorization']?.split(' ')[1];
    if (!token) return res.status(401).json({ message: 'Unauthorized' });

    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      req['user'] = decoded;
      next();
    } catch {
      return res.status(403).json({ message: 'Forbidden' });
    }
  }
}

// Apply globally in main.ts
app.use(new JwtMiddleware().use);
```

**Rate limiting example (NestJS)** using `nestjs-rate-limiter` or NestJS guards.

```ts
@UseGuards(RateLimiterGuard)
@Get('profile')
getProfile(@Req() req) {
  return req.user;
}
```

---

### 🟨 2. **Flask (Monolith - Middleware)**

```python
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

@app.before_request
def check_token():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "Missing token"}), 401
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        request.user = payload
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 403
```

**Rate limiting**: Use `flask-limiter`.

```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route("/api")
@limiter.limit("5 per minute")
def api(): return "limited"
```

---

### 🟩 3. **.NET (Monolith - Middleware)**

```csharp
// JwtMiddleware.cs
public class JwtMiddleware {
    private readonly RequestDelegate _next;

    public JwtMiddleware(RequestDelegate next) => _next = next;

    public async Task Invoke(HttpContext context) {
        var token = context.Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last();
        if (token != null) {
            try {
                var tokenHandler = new JwtSecurityTokenHandler();
                var key = Encoding.ASCII.GetBytes("secret_key");
                tokenHandler.ValidateToken(token, new TokenValidationParameters {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(key),
                    ValidateIssuer = false,
                    ValidateAudience = false,
                }, out SecurityToken validatedToken);
                context.Items["User"] = ((JwtSecurityToken)validatedToken).Claims;
            } catch {
                context.Response.StatusCode = 403;
                return;
            }
        }
        await _next(context);
    }
}

// Add to pipeline
app.UseMiddleware<JwtMiddleware>();
```

**Rate limiting** in .NET: use `AspNetCoreRateLimit`.

---

## 🧱 MICROSERVICES WITH API GATEWAY

Use **Kong**, **NGINX**, **Traefik**, or **AWS API Gateway** in front of services.

---

### 🌐 Example: **Kong Gateway** with Microservices (NestJS, Flask, .NET)

#### ✅ Setup API Gateway (Kong)

```bash
curl -i -X POST http://localhost:8001/services/ \
  --data name=userservice \
  --data url=http://localhost:3001

curl -i -X POST http://localhost:8001/routes \
  --data service.name=userservice \
  --data paths[]=/user
```

#### ✅ Token Validation Plugin

```bash
curl -i -X POST http://localhost:8001/services/userservice/plugins \
  --data "name=jwt"
```

Kong will now **validate JWT** *before* forwarding to NestJS/Flask/.NET.

---

### 🧊 Caching Example (Kong plugin)

```bash
curl -i -X POST http://localhost:8001/services/productservice/plugins \
  --data "name=proxy-cache"
```

This caches `GET` responses—so NestJS/Flask/.NET don’t need to handle it.

---

### 🛡 Rate Limiting Example (Kong)

```bash
curl -i -X POST http://localhost:8001/services/anyservice/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=5"
```

---

## 🧭 Summary Comparison

| Concern          | **NestJS Middleware**           | **NestJS via API Gateway**        |
| ---------------- | ------------------------------- | --------------------------------- |
| Auth Token Check | In NestJS code (JWT middleware) | Offloaded to Gateway (JWT plugin) |
| Rate Limiting    | NestJS Guard or middleware      | Gateway plugin (Kong, NGINX)      |
| Caching          | Custom logic or CDN headers     | Proxy cache plugin                |
| Complexity       | Easy for small apps             | Best for microservices            |

Same logic applies to Flask and .NET—middleware for monoliths, gateway plugins for microservices.

---


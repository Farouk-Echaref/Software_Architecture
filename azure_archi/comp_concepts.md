# 💡 What is HATEOAS?

HATEOAS is a REST API principle that enables clients to navigate through resources dynamically via hyperlinks provided in responses.

- Each API response contains **links** that guide what operations can be performed next.
- Clients don’t need to hard-code endpoint URLs—they discover them from the response.
- It's like a **finite state machine**: each state (API response) tells how to move to another state (next possible operation).

#### Example:
```json
{
  "orderID": 3,
  "productID": 2,
  "quantity": 4,
  "orderValue": 16.60,
  "links": [
    {
      "rel": "self",
      "href": "https://api.example.com/orders/3",
      "action": "GET"
    },
    {
      "rel": "customer",
      "href": "https://api.example.com/customers/3",
      "action": "GET"
    }
  ]
}
```

---

## ✅ Implementation Examples

### **1. NestJS (TypeScript)**

```ts
@Get(':id')
findOne(@Param('id') id: number) {
  const order = this.orderService.findById(id);
  return {
    ...order,
    links: [
      {
        rel: 'self',
        href: `https://api.example.com/orders/${id}`,
        action: 'GET'
      },
      {
        rel: 'customer',
        href: `https://api.example.com/customers/${order.customerId}`,
        action: 'GET'
      }
    ]
  };
}
```

### **2. Flask (Python)**

```python
from flask import jsonify, url_for

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = get_order_by_id(order_id)
    response = {
        "orderID": order.id,
        "productID": order.product_id,
        "quantity": order.quantity,
        "orderValue": order.total,
        "links": [
            {
                "rel": "self",
                "href": url_for('get_order', order_id=order.id, _external=True),
                "action": "GET"
            },
            {
                "rel": "customer",
                "href": url_for('get_customer', customer_id=order.customer_id, _external=True),
                "action": "GET"
            }
        ]
    }
    return jsonify(response)
```

### **3. .NET (C# - ASP.NET Core)**

```csharp
[HttpGet("{id}")]
public IActionResult GetOrder(int id)
{
    var order = _orderService.GetOrderById(id);
    var result = new {
        order.OrderID,
        order.ProductID,
        order.Quantity,
        order.OrderValue,
        links = new[] {
            new {
                rel = "self",
                href = Url.Action(nameof(GetOrder), new { id }),
                action = "GET"
            },
            new {
                rel = "customer",
                href = Url.Action("GetCustomer", "Customer", new { id = order.CustomerId }),
                action = "GET"
            }
        }
    };
    return Ok(result);
}
```

---

### Summary

| Concept         | Description |
|----------------|-------------|
| **Goal**        | Guide clients using embedded hyperlinks in API responses |
| **Benefits**    | Improves discoverability, decouples clients from hardcoded URLs |
| **Key Elements**| `rel`, `href`, `action`, `types` |
| **Where to Use**| REST APIs with dynamic navigation and evolving operations |
| **Frameworks**  | Easily implemented in NestJS, Flask, ASP.NET Core with JSON response enhancements |

# What Are Multitenant Web APIs?

**Multitenant Web APIs** are APIs designed to serve **multiple tenants**—that is, multiple clients, users, or organizations—**from a single application instance** while keeping their data and configurations logically separated.

---

#### Key Concepts

- **Tenant**: A distinct user, organization, or customer using the API.
- **Single codebase**: One running app serves multiple tenants.
- **Data isolation**: Each tenant accesses only their own data.
- **Configuration flexibility**: APIs can adjust behavior per tenant (e.g., limits, branding, features).

---

#### Why Use Multitenancy?

- **Cost-efficiency**: Lower infrastructure costs compared to one app per tenant.
- **Simplified updates**: Easier to maintain and deploy.
- **Scalability**: Add new tenants without spinning up new instances.

---

#### Common Isolation Techniques

| Isolation Level      | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| **Database-per-tenant** | Each tenant has its own DB. Strong isolation, more overhead.               |
| **Schema-per-tenant**   | Same DB, different schemas. Balance of isolation and manageability.       |
| **Shared schema**        | Same DB and schema, rows are tagged with tenant ID. Most efficient, riskier. |

---

#### Tenant Identification Methods

- **URL path**: `/tenant1/api/orders`
- **Subdomain**: `tenant1.api.example.com`
- **Header**: Custom headers like `X-Tenant-ID`
- **Token-based**: Tenant info embedded in JWT or OAuth tokens

---

#### Security Concerns

- Enforce **strict access control** to prevent data leakage.
- Validate **tenant identity** in every request.
- Implement **rate limiting** and **resource quotas** per tenant.

---

#### Summary

**Multitenant APIs** let a single API instance serve many customers, isolating their data and behavior while reducing operational overhead. Tenant context must be identified in each request, and isolation strategy should balance performance, cost, and security.

**Simple examples of multitenant web APIs** implemented in both **NestJS** and **Flask**, using the **shared schema with tenant ID tagging** approach. Each request includes a tenant ID via a **custom HTTP header (`X-Tenant-ID`)**.

### 🔹 NestJS Example – Multitenancy via Middleware


```ts
// tenant.middleware.ts
import { Injectable, NestMiddleware, BadRequestException } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class TenantMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const tenantId = req.header('X-Tenant-ID');
    if (!tenantId) throw new BadRequestException('Missing X-Tenant-ID header');
    req['tenantId'] = tenantId;
    next();
  }
}
```

```ts
// app.module.ts
import { MiddlewareConsumer, Module, RequestMethod } from '@nestjs/common';
import { TenantMiddleware } from './tenant.middleware';
import { AppController } from './app.controller';

@Module({
  controllers: [AppController],
})
export class AppModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(TenantMiddleware)
      .forRoutes({ path: '*', method: RequestMethod.ALL });
  }
}
```

```ts
// app.controller.ts
import { Controller, Get, Req } from '@nestjs/common';
import { Request } from 'express';

@Controller('customers')
export class AppController {
  @Get()
  getCustomers(@Req() req: Request) {
    const tenantId = req['tenantId'];
    // In practice, you'd query: SELECT * FROM customers WHERE tenant_id = ?
    return [`Customer A of tenant ${tenantId}`, `Customer B of tenant ${tenantId}`];
  }
}
```

---

### 🔹 Flask Example – Multitenancy via Request Header

```python
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.before_request
def get_tenant():
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        abort(400, 'Missing X-Tenant-ID header')
    request.tenant_id = tenant_id

@app.route('/customers')
def get_customers():
    tenant_id = request.tenant_id
    # In real DB query: SELECT * FROM customers WHERE tenant_id = ?
    return jsonify([
        f"Customer A of tenant {tenant_id}",
        f"Customer B of tenant {tenant_id}"
    ])

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Summary

| Feature            | NestJS                                  | Flask                                 |
|-------------------|------------------------------------------|----------------------------------------|
| Tenant ID Source   | Middleware via `X-Tenant-ID` header      | `before_request` hook, same header     |
| Isolation Method   | Logical (filter by tenant ID in queries) | Logical (same)                         |
| Use Case           | Scalable Node.js apps with decorators    | Lightweight Python apps or services    |


# What is an ETag (Entity Tag)?

An **ETag** is like a **version ID** for a specific resource (file, object, page) on a server.

- It’s a **string** (often a hash or timestamp) that uniquely identifies the **current version** of the resource.
- When the resource **changes**, the ETag **changes** too.

Think of it like:  
*“Version 1 of this document has ETag `abc123`. If the document changes, its ETag becomes `def456`.”*

---

## How ETags Are Used

1. **Server** sends the resource with an ETag in the response header:

   ```http
   HTTP/1.1 200 OK
   ETag: "abc123"
   ```

2. **Client** saves that ETag along with the resource.

3. Later, when the client wants to get the resource **again**, it sends:

   ```http
   GET /document HTTP/1.1
   If-None-Match: "abc123"
   ```

4. **Server** checks:
   - If the resource **hasn't changed** (ETag matches), server replies with **304 Not Modified** (no body → saves bandwidth!).
   - If the resource **has changed**, server sends **new data** with a **new ETag**.

---

## Why Use ETags?

| Benefit                     | How |
|:-----------------------------|:----|
| **Save Bandwidth**           | No need to resend unchanged data. |
| **Improve Performance**      | Faster client-side updates. |
| **Avoid Conflicts**          | Helps detect when two clients are updating the same resource (optimistic concurrency control). |

---

## Simple Example

### Server returns data with ETag
```http
HTTP/1.1 200 OK
ETag: "v2orders123"
Content-Type: application/json

{"orderID":2, "productID":4, "quantity":2}
```

### Client checks if it changed later
```http
GET /orders/2 HTTP/1.1
If-None-Match: "v2orders123"
```

### If unchanged:
```http
HTTP/1.1 304 Not Modified
```

### If changed:
```http
HTTP/1.1 200 OK
ETag: "v3orders456"
{"orderID":2, "productID":4, "quantity":5}
```

---

## ETag in C# Web API

In that `OkResultWithCaching` example you saw earlier:

```csharp
response.Headers.ETag = ETag;
```

This line is where you **attach an ETag** to your API responses.

You can generate ETags by:
- Hashing the content (like MD5 or SHA1)
- Using a database version/timestamp
- A simple version number if the data is versioned manually

Awesome — you want **ETag** examples in **.NET**, **NestJS**, and **Flask**.  
I'll show you **short, working examples** for all three. 🚀

---

## .NET Web API Example (.NET 6+)

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    [HttpGet("{id}")]
    public IActionResult GetOrder(int id)
    {
        var order = new { Id = id, Product = "Laptop", Quantity = 1 };

        var json = System.Text.Json.JsonSerializer.Serialize(order);
        var etag = GenerateETag(json);

        // Check if the client's ETag matches
        if (Request.Headers.ContainsKey("If-None-Match") &&
            Request.Headers["If-None-Match"] == etag)
        {
            return StatusCode(304); // Not Modified
        }

        Response.Headers.ETag = etag;
        return Ok(order);
    }

    private string GenerateETag(string content)
    {
        using var sha = System.Security.Cryptography.SHA256.Create();
        var hashBytes = sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(content));
        return "\"" + Convert.ToBase64String(hashBytes) + "\"";
    }
}
```

*Explanation:*  
- Generate ETag based on JSON body.
- If client sends `If-None-Match` and matches, return **304** (no body).
- Otherwise, return the resource with a fresh ETag.

---

## NestJS Example

```typescript
import { Controller, Get, Header, Req, Res } from '@nestjs/common';
import { Request, Response } from 'express';
import * as crypto from 'crypto';

@Controller('orders')
export class OrdersController {
  @Get(':id')
  getOrder(@Req() req: Request, @Res() res: Response) {
    const order = { id: 1, product: 'Laptop', quantity: 1 };
    const body = JSON.stringify(order);
    const etag = generateETag(body);

    const clientETag = req.headers['if-none-match'];
    if (clientETag && clientETag === etag) {
      return res.status(304).end(); // Not Modified
    }

    res.setHeader('ETag', etag);
    return res.status(200).json(order);
  }
}

function generateETag(content: string): string {
  return `"${crypto.createHash('sha256').update(content).digest('base64')}"`;
}
```

*Explanation:*  
- Same idea: hash the body to generate ETag.
- Check if `If-None-Match` matches.
- Respond with **304** if no changes.

---

## Flask (Python) Example

```python
from flask import Flask, request, jsonify, make_response
import hashlib
import base64

app = Flask(__name__)

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = {"id": id, "product": "Laptop", "quantity": 1}
    body = jsonify(order).get_data()
    etag = generate_etag(body)

    client_etag = request.headers.get('If-None-Match')
    if client_etag == etag:
        return '', 304  # Not Modified

    response = make_response(jsonify(order))
    response.headers['ETag'] = etag
    return response

def generate_etag(content):
    hash_digest = hashlib.sha256(content).digest()
    return '"' + base64.b64encode(hash_digest).decode() + '"'

if __name__ == '__main__':
    app.run(debug=True)
```

*Explanation:*  
- Use `sha256` and `base64` to generate ETag.
- Check if client provided matching `If-None-Match`.
- Send **304** if data is still valid.

---

## Summary Table

| Framework | ETag generated by | ETag checked on | ETag sent in |
|:-----------|:------------------|:----------------|:-------------|
| .NET       | `SHA256` of content | `Request.Headers` | `Response.Headers` |
| NestJS     | `SHA256` of content | `req.headers` | `res.setHeader` |
| Flask      | `SHA256` of content | `request.headers` | `response.headers` |

---

# **Theory: Automatic ETag Handling ("middleware style")**

👉 **Problem:**  
Manually generating and checking ETags for *every* endpoint is repetitive and error-prone.

👉 **Solution:**  
Use **middleware** to:
- **Intercept** the outgoing HTTP response.
- **Hash** the response body.
- **Compare** it with the `If-None-Match` header from the client.
- **If matched**, **stop** the response and return `304 Not Modified`.
- **If not matched**, **attach the new ETag** to the outgoing response.

This way:
- You **don't modify** individual controllers.
- You **automatically** optimize bandwidth and performance for the entire API.

---

# 🧩 Code for Each Framework

---

## 1. .NET 6+ (ASP.NET Core) — Middleware

```csharp
public class ETagMiddleware
{
    private readonly RequestDelegate _next;

    public ETagMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var originalBodyStream = context.Response.Body;
        using var memoryStream = new MemoryStream();
        context.Response.Body = memoryStream;

        await _next(context);

        if (context.Response.StatusCode == 200 && 
            context.Response.ContentType != null && 
            context.Response.ContentType.Contains("application/json"))
        {
            memoryStream.Seek(0, SeekOrigin.Begin);
            var bodyBytes = await new StreamReader(memoryStream).ReadToEndAsync();
            var etag = GenerateETag(bodyBytes);

            var clientETag = context.Request.Headers["If-None-Match"].FirstOrDefault();
            if (clientETag == etag)
            {
                context.Response.Clear();
                context.Response.StatusCode = StatusCodes.Status304NotModified;
            }
            else
            {
                context.Response.Headers["ETag"] = etag;
                memoryStream.Seek(0, SeekOrigin.Begin);
                await memoryStream.CopyToAsync(originalBodyStream);
            }
        }
        else
        {
            memoryStream.Seek(0, SeekOrigin.Begin);
            await memoryStream.CopyToAsync(originalBodyStream);
        }
    }

    private static string GenerateETag(string content)
    {
        using var sha = System.Security.Cryptography.SHA256.Create();
        var hashBytes = sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(content));
        return "\"" + Convert.ToBase64String(hashBytes) + "\"";
    }
}

// In Program.cs
app.UseMiddleware<ETagMiddleware>();
```

✅ Now **all JSON responses** get ETags automatically.

---

## 2. NestJS — Interceptor

```typescript
import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import * as crypto from 'crypto';

@Injectable()
export class ETagInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const response = context.switchToHttp().getResponse();
    const request = context.switchToHttp().getRequest();
    const clientETag = request.headers['if-none-match'];

    return next.handle().pipe(
      map((data) => {
        const body = JSON.stringify(data);
        const etag = `"${crypto.createHash('sha256').update(body).digest('base64')}"`;

        if (clientETag === etag) {
          response.status(304).end();
          return;
        }

        response.setHeader('ETag', etag);
        return data;
      }),
    );
  }
}
```

```typescript
// In main.ts
import { ETagInterceptor } from './etag.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalInterceptors(new ETagInterceptor());
  await app.listen(3000);
}
bootstrap();
```

✅ All endpoints globally are protected now!

---

## 3. Flask — After Request Hook

```python
from flask import Flask, request, jsonify, make_response
import hashlib
import base64

app = Flask(__name__)

@app.after_request
def add_etag(response):
    if response.status_code == 200 and response.content_type == 'application/json':
        body = response.get_data()
        etag = generate_etag(body)
        
        client_etag = request.headers.get('If-None-Match')
        if client_etag == etag:
            return '', 304

        response.headers['ETag'] = etag
    return response

def generate_etag(content):
    hash_digest = hashlib.sha256(content).digest()
    return '"' + base64.b64encode(hash_digest).decode() + '"'

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = {"id": id, "product": "Laptop", "quantity": 1}
    return jsonify(order)

if __name__ == '__main__':
    app.run(debug=True)
```

✅ Every response from Flask with JSON will have an ETag automatically.

---

# 🔥 Final recap

| Framework | What we created | Where |
|:-----------|:----------------|:------|
| .NET Core  | Custom Middleware | `app.UseMiddleware<ETagMiddleware>()` |
| NestJS     | Global Interceptor | `app.useGlobalInterceptors(new ETagInterceptor())` |
| Flask      | After-request hook | `@app.after_request` |

✅ Now you **don’t need to manually** generate ETags in each controller!


---

# 📖 **Theory: Strong vs Weak ETags**

When you generate an ETag, there are **two types**:

| Type   | What it means | Use Case |
|:-------|:--------------|:---------|
| **Strong ETag** | The content must be **bit-for-bit identical**. | Static files, exact JSON, precise versioning. |
| **Weak ETag** | The content can be **semantically equivalent** even if minor changes exist (like whitespace or metadata changes). | Dynamic content where exact bytes aren't critical, but logical meaning is important. |

---

## ✏️ Example

- **Strong ETag:**  
  > "4f9d4c3d8b60c3e4f0c6a7eab8e6d3d2"  
  *(Hash of actual exact body)*

- **Weak ETag:**  
  > `W/"4f9d4c3d8b60c3e4f0c6a7eab8e6d3d2"`  
  *(Notice the **`W/`** prefix = "Weak")*

---

## 🔥 When should you use **Strong** or **Weak**?

| Situation | Recommendation |
|:----------|:----------------|
| Static APIs (e.g., product catalog, file download) | **Strong ETag** |
| Dynamic APIs (e.g., dashboard data, timestamps) | **Weak ETag** |
| APIs with minor differences not affecting user experience | **Weak ETag** |
| APIs where byte-for-byte integrity matters (e.g., cache validation) | **Strong ETag** |

---

# 🛠️ How to Implement

## 1. **Strong ETag** (default — what we already did)

✅ Hash the **full** body.  
✅ Attach the ETag like:  
```http
ETag: "hashvalue"
```

(Already done in the .NET, NestJS, and Flask code!)

---

## 2. **Weak ETag** (easy tweak)

Just add the `"W/"` prefix manually when setting the ETag.

### .NET example (modify `GenerateETag`):

```csharp
private static string GenerateETag(string content)
{
    using var sha = System.Security.Cryptography.SHA256.Create();
    var hashBytes = sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(content));
    return "W/\"" + Convert.ToBase64String(hashBytes) + "\"";  // Notice W/ prefix
}
```

---

### NestJS example (modify Interceptor):

```typescript
const etag = `W/"${crypto.createHash('sha256').update(body).digest('base64')}"`;
```

---

### Flask example (modify `generate_etag`):

```python
def generate_etag(content):
    hash_digest = hashlib.sha256(content).digest()
    return 'W/"' + base64.b64encode(hash_digest).decode() + '"'
```

---

# ⚡ Quick Summary

| Feature | Strong ETag | Weak ETag |
|:--------|:------------|:----------|
| Hash bytes exactly | ✅ | ✅ |
| "W/" prefix | ❌ | ✅ |
| Changes in whitespace or order matter? | Yes | No |
| Recommended for APIs? | Static | Dynamic |

---

# 🎯 Quick Final Advice
- **Default to strong ETags** unless you know you have slight non-important variations.
- **Weak ETags** help when minor updates (like timestamps) would otherwise cause unnecessary cache invalidations.

---

### 💡 What is HATEOAS?

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

### What Are Multitenant Web APIs?

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


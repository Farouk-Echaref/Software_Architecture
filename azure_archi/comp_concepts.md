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


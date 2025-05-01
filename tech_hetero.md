### 1. **Machine Learning Inference Service**
- **Service Function**: Perform real-time predictions using a trained ML model.
- **Technology Choice**: Python with FastAPI or Flask.
- **Why Not the Main Stack (e.g., Java/NestJS/etc.)**:
  - Python has mature ML libraries like TensorFlow, PyTorch, and scikit-learn.
  - Easier and faster to prototype and deploy ML services.

---

### 2. **Real-time Chat Service**
- **Service Function**: Handle real-time WebSocket communication for messaging.
- **Technology Choice**: Node.js with Socket.IO or Elixir with Phoenix.
- **Why Not Java or Python**:
  - Node.js and Elixir are better suited for handling thousands of concurrent socket connections efficiently due to their event-driven or actor-based concurrency models.

---

### 3. **Billing and Payments Service**
- **Service Function**: Handle secure transactions, generate invoices, and interact with payment gateways.
- **Technology Choice**: Java (Spring Boot) or .NET.
- **Why Not JavaScript/Python**:
  - Strong type safety, better performance, and maturity in handling financial applications.
  - Support for transactional integrity and enterprise-grade security.

---

### 4. **Media Encoding Service**
- **Service Function**: Encode videos/images in different formats.
- **Technology Choice**: Go or Rust.
- **Why Not Python or JavaScript**:
  - Go and Rust offer better raw performance and concurrency management.
  - Ideal for CPU-intensive tasks like video processing.

---

### 5. **Search Service**
- **Service Function**: Provide fast, full-text search over large datasets.
- **Technology Choice**: Use a dedicated engine like **Elasticsearch** or **Apache Solr**, possibly wrapped with a Python or Node.js API.
- **Why Not Use Standard DB Queries**:
  - Specialized search engines are optimized for indexing, relevance scoring, and complex queries.

---

### 6. **Data Aggregation / ETL Service**
- **Service Function**: Aggregate data from multiple sources for analytics.
- **Technology Choice**: Python with Pandas or Apache Spark (Scala).
- **Why Not JavaScript or .NET**:
  - Python and Scala have better ecosystems for data wrangling and batch processing.

---

### Summary Table

| Feature/Function                | Best Tech Choice       | Reason for Heterogeneity                                      |
|-------------------------------|------------------------|---------------------------------------------------------------|
| ML Inference                  | Python (FastAPI)       | Mature ML libraries                                           |
| Real-time Chat                | Node.js / Elixir       | Efficient real-time connections                              |
| Billing                       | Java / .NET            | Enterprise-grade reliability and security                    |
| Media Processing              | Go / Rust              | Performance for CPU-bound tasks                              |
| Full-text Search              | Elasticsearch          | Advanced search capabilities                                 |
| ETL/Data Aggregation          | Python / Scala         | Data analysis & processing libraries                         |

---

## ⚙️ Example 1: Machine Learning Inference Service (Python) in a Java/NestJS-based Microservices System

### 🔧 Use Case:
You have a main system in NestJS or Java, but want to expose a service that performs ML predictions (e.g., churn prediction).

---

### 📁 Project Structure (Python - FastAPI):

```
ml-inference/
├── app/
│   ├── __init__.py
│   ├── model.py         # load model
│   ├── schemas.py       # input/output data models
│   └── main.py          # FastAPI entry point
├── model/
│   └── model.pkl        # pre-trained scikit-learn model
├── requirements.txt
└── Dockerfile
```

---

### 🧠 Sample Code:

**`app/model.py`**
```python
import joblib

model = joblib.load("model/model.pkl")

def predict(features):
    return model.predict([features])[0]
```

**`app/schemas.py`**
```python
from pydantic import BaseModel

class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float

class Prediction(BaseModel):
    result: str
```

**`app/main.py`**
```python
from fastapi import FastAPI
from app.schemas import InputData, Prediction
from app.model import predict

app = FastAPI()

@app.post("/predict", response_model=Prediction)
def make_prediction(data: InputData):
    result = predict([data.feature1, data.feature2, data.feature3])
    return {"result": result}
```

**Dockerfile**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`requirements.txt`**
```
fastapi
uvicorn
scikit-learn
joblib
pydantic
```

---

### 🔗 Integration
- Other services (e.g., Java Spring Boot or NestJS) can call this via HTTP: `POST http://ml-inference:8000/predict`.

---

## ⚙️ Example 2: Real-Time Notification Service (Node.js) in a Python or Java System

### 🔧 Use Case:
You need real-time notifications via WebSockets.

---

### 📁 Project Structure (Node.js + Socket.IO):

```
notification-service/
├── index.js
├── package.json
└── Dockerfile
```

---

### 🧠 Sample Code:

**`index.js`**
```js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

io.on('connection', (socket) => {
  console.log('User connected: ' + socket.id);
  socket.on('notify', (msg) => {
    console.log("Notification:", msg);
    io.emit('new_notification', msg);
  });
});

server.listen(3000, () => {
  console.log('Notification service running on port 3000');
});
```

**`package.json`**
```json
{
  "name": "notification-service",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.7.1"
  }
}
```

**Dockerfile**
```dockerfile
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "index.js"]
```

---

### 🔗 Integration
- Your backend can emit events via Socket.IO client.
- Frontend (React, etc.) listens to `new_notification`.

---

## ⚙️ Example 3: Billing and Payment Service (.NET) in a Node.js/Python Ecosystem

### 🔧 Use Case:
Handle secure user billing, generate invoices, and connect with Stripe or PayPal.

.NET is chosen here because of:
- Strong type safety and better compile-time error detection.
- Rich support for background services, asynchronous queues.
- Maturity in handling transactional business logic.

---

### 📁 Project Structure (ASP.NET Core Web API):

```
billing-service/
├── BillingService.sln
├── BillingService/
│   ├── Controllers/
│   │   └── BillingController.cs
│   ├── Models/
│   │   └── InvoiceRequest.cs
│   ├── Services/
│   │   └── BillingProcessor.cs
│   ├── Program.cs
│   └── BillingService.csproj
├── Dockerfile
└── appsettings.json
```

---

### 🧠 Sample Code:

**`Models/InvoiceRequest.cs`**
```csharp
public class InvoiceRequest
{
    public string CustomerId { get; set; }
    public decimal Amount { get; set; }
    public string Currency { get; set; }
}
```

---

**`Services/BillingProcessor.cs`**
```csharp
using System;

public class BillingProcessor
{
    public string GenerateInvoice(InvoiceRequest request)
    {
        // Simulate invoice generation
        return $"Invoice_{request.CustomerId}_{DateTime.UtcNow.Ticks}";
    }
}
```

---

**`Controllers/BillingController.cs`**
```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class BillingController : ControllerBase
{
    private readonly BillingProcessor _processor = new BillingProcessor();

    [HttpPost("invoice")]
    public IActionResult GenerateInvoice([FromBody] InvoiceRequest request)
    {
        var invoiceId = _processor.GenerateInvoice(request);
        return Ok(new { invoiceId });
    }
}
```

---

**`Program.cs`**
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapControllers();
app.Run();
```

---

**`Dockerfile`**
```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "BillingService.dll"]
```

---

### 🔗 Integration:
- Other services (like a Python order manager or Node.js cart) send POST requests to:  
  `POST http://billing-service:5000/api/billing/invoice`

**Example Request (from another microservice):**
```json
{
  "CustomerId": "user_123",
  "Amount": 99.99,
  "Currency": "USD"
}
```

---

## ✅ Summary: Technology Heterogeneity in Action

| Microservice            | Tech Stack        | Reason                                      |
|------------------------|-------------------|---------------------------------------------|
| ML Inference           | Python + FastAPI  | Leverage ML ecosystem (scikit-learn, etc.) |
| Notifications          | Node.js + Socket.IO | Real-time event handling                   |
| Billing & Payments     | .NET Core         | Enterprise-grade security, type safety     |

---


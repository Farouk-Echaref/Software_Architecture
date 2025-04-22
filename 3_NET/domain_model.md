## 🧠 What Is a **Domain Model**?

### 🔍 In short:
A **domain model** is a *structured representation* of the **real-world business concepts**, **rules**, and **logic** of the problem you're trying to solve in software.

---

### 🧱 Key Components of a Domain Model

1. **Entities** – Represent core business objects with identity.  
   _Example:_ `User`, `Order`, `Payment`, etc.

2. **Value Objects** – Objects that describe aspects of an entity but have no identity.  
   _Example:_ `Address`, `Money`, `DateRange`.

3. **Aggregates** – Groups of entities and value objects that are treated as a unit.  
   _Example:_ `Order` may contain `OrderItems`.

4. **Domain Services** – Contain business logic that doesn't naturally belong to an entity.  
   _Example:_ `DiscountCalculatorService`, `PaymentProcessor`.

5. **Repositories** – Abstractions for accessing and storing aggregates.  
   _Example:_ `UserRepository`, `OrderRepository`.

---

### 🧾 Example (for an Online Store)

Let’s say your **domain** is: **E-commerce platform**

#### Domain model might include:

| Entity         | Description                                 |
|----------------|---------------------------------------------|
| `User`         | Customer using the site                     |
| `Product`      | Item being sold                             |
| `Order`        | Tracks what a user has purchased            |
| `Payment`      | Tracks how the order was paid               |

These aren’t just database tables — they have:
- Business rules (e.g., “an order must have at least 1 item”),
- Behaviors (e.g., `order.calculate_total()`),
- Relationships (e.g., a `User` places multiple `Orders`).

---

### 🧭 So what’s the **purpose** of a Domain Model?

- To **mirror the real-world logic** of the business in code
- To **enable clean, understandable**, and **testable** software
- To **separate concerns** between *how things work* and *how things look (UI)* or *how things are stored (DB)*

---

## 📦 In Microservices

Each microservice has its **own domain model** that is:

- **Focused on a single business capability**
- **Independent** (it doesn’t need to know how the rest of the system works)
- Often **shares identity** (e.g., the same `user.id`) but **not the structure** (e.g., different fields in each service)

> A `User` might be called a `Buyer` in the ordering service and a `Payer` in the payment service — different context, different attributes, same identity.

---

## 🏢 Real-World Analogy: A Large Company

Imagine a company that organizes a big **international tech conference**. Different departments in the company manage different parts of this event.

---

### 🎯 The “User” across Departments

All departments deal with **people** (users), but they **see and treat them differently**, based on what they need to do.

#### 1. **Sales Department (Ordering Microservice)**  
- Refers to them as: **Buyers**  
- Cares about:  
  - Buyer ID  
  - Purchased tickets  
  - Applied discounts  
  - Payment status  

#### 2. **Payments Department (Payment Microservice)**  
- Refers to them as: **Payers**  
- Cares about:  
  - Payer ID  
  - Credit card number  
  - Billing address  
  - Payment method  

#### 3. **Support Department (Customer Service Microservice)**  
- Refers to them as: **Customers**  
- Cares about:  
  - Customer ID  
  - Contact info  
  - Complaint history  
  - Ticket status  

#### 4. **Event Team (Conferences Microservice)**  
- Refers to them as: **Users**  
- Cares about:  
  - Full name  
  - Seat assignments  
  - Conference preferences  
  - Badge info  

---

### ⚙️ So what’s happening under the hood?

Even though they’re all talking about the **same person**, each department has its **own model** of what a “user” is — with different data and behavior.

This is exactly how **domain models** work in **microservices**:
- Each microservice (department) has its **own bounded context**
- Each defines its **own domain model** based on what matters to it
- They may **share the same ID**, but that’s it — everything else is **contextual**

---

## 🔒 Why Is This Powerful?

- Each service is **autonomous** — no need to sync the entire structure of a user everywhere.
- Each team can **evolve** its service **independently**.
- No bloated or generic “User” entity trying to satisfy everyone.


Let's build a **simple microservices example** where different services model the same **user** (same ID) differently based on their **domain**.

We’ll cover:

1. **Conferences Service** (Python) — deals with full user info  
2. **Payments Service** (NestJS) — deals with payment-specific info  
3. A shared **User ID** (across services)  

---

## 🧩 1. Conferences Microservice (Python — FastAPI)

```python
# conferences_service/main.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: str
    full_name: str
    email: str
    seat_number: str
    badge_type: str

@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: str):
    # Simulate user data
    return User(
        id=user_id,
        full_name="Alice Johnson",
        email="alice@example.com",
        seat_number="A12",
        badge_type="VIP"
    )
```

---

## 💳 2. Payments Microservice (NestJS)

```ts
// payments-service/src/user/user.entity.ts

export class Payer {
  id: string;
  paymentMethod: 'CreditCard' | 'PayPal';
  cardLast4Digits: string;
  billingEmail: string;
}
```

```ts
// payments-service/src/user/user.controller.ts

import { Controller, Get, Param } from '@nestjs/common';
import { Payer } from './user.entity';

@Controller('payer')
export class UserController {
  @Get(':id')
  getPayer(@Param('id') id: string): Payer {
    return {
      id,
      paymentMethod: 'CreditCard',
      cardLast4Digits: '1234',
      billingEmail: 'billing@alicepay.com'
    };
  }
}
```

---

## 🔗 Shared Concept: Identity by `user.id`

Even though `User` and `Payer` have **different shapes**, they **represent the same real-world person**, tied by the same `id`.

---

## 🧠 Summary

| Microservice         | Model Name | Knows About                  |
|----------------------|------------|------------------------------|
| `ConferencesService` | `User`     | Full name, email, badge      |
| `PaymentsService`    | `Payer`    | Payment method, billing info |
| Shared Across        | `id`       | Globally unique identifier   |

---

We'll implement **asynchronous communication** between two microservices:

- `UserService`: Publishes an event when a new user is created.
- `PaymentService`: Listens for the "user created" event and creates a corresponding payer.

We’ll do this using **RabbitMQ** as the message broker.

---

## 🐍 Python (FastAPI + aio_pika for RabbitMQ)

### 📁 Structure

```
user_service/
  main.py
  publisher.py

payment_service/
  main.py
  consumer.py
```

### `user_service/main.py`

```python
from fastapi import FastAPI
from publisher import publish_user_created

app = FastAPI()

@app.post("/users/")
async def create_user(user_id: int, name: str):
    await publish_user_created(user_id, name)
    return {"status": "User created and event published"}
```

### `user_service/publisher.py`

```python
import aio_pika
import json

async def publish_user_created(user_id, name):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps({"id": user_id, "name": name}).encode(),
            content_type="application/json"
        ),
        routing_key="user.created"
    )
    await connection.close()
```

---

### `payment_service/main.py`

```python
import asyncio
from consumer import consume_user_created

if __name__ == "__main__":
    asyncio.run(consume_user_created())
```

### `payment_service/consumer.py`

```python
import aio_pika
import json

async def consume_user_created():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("user.created", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body)
                print(f"[PaymentService] Creating payer for user: {data['id']} - {data['name']}")
```

---

## 🦄 NestJS with RabbitMQ (using `@nestjs/microservices`)

### 1. UserService (`user.service.ts`)

```ts
import { Controller, Post, Body } from '@nestjs/common';
import { ClientProxy, ClientProxyFactory, Transport } from '@nestjs/microservices';

@Controller('users')
export class UserController {
  private client: ClientProxy;

  constructor() {
    this.client = ClientProxyFactory.create({
      transport: Transport.RMQ,
      options: {
        urls: ['amqp://guest:guest@localhost:5672'],
        queue: 'user_created_queue',
      },
    });
  }

  @Post()
  async createUser(@Body() body: { id: number; name: string }) {
    await this.client.emit('user_created', body);
    return { status: 'User created and event published' };
  }
}
```

---

### 2. PaymentService (`main.ts` and `payment.service.ts`)

#### `main.ts`

```ts
import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(AppModule, {
    transport: Transport.RMQ,
    options: {
      urls: ['amqp://guest:guest@localhost:5672'],
      queue: 'user_created_queue',
    },
  });

  await app.listen();
}
bootstrap();
```

#### `payment.service.ts`

```ts
import { Controller } from '@nestjs/common';
import { EventPattern, Payload } from '@nestjs/microservices';

@Controller()
export class PaymentService {
  @EventPattern('user_created')
  handleUserCreated(@Payload() data: any) {
    console.log(`[PaymentService] Creating payer for user: ${data.id} - ${data.name}`);
  }
}
```

---

### 🧪 To Test

1. Start RabbitMQ on localhost (`docker run -p 5672:5672 rabbitmq`)
2. Start each microservice (FastAPI or NestJS)
3. Call `POST /users/` from UserService with a new user
4. Watch logs of PaymentService for the printed message

---

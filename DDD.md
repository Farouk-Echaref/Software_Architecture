# Domain-Driven Design (DDD) Explained

## What is Domain-Driven Design?
Domain-Driven Design (DDD) is a software development approach that focuses on modeling software to match a business domain as closely as possible. Introduced by Eric Evans, DDD emphasizes collaboration between technical and domain experts to create a shared understanding and a codebase that reflects business rules and processes.

---

## Core Concepts

### 1. **Domain**
The subject area the software is designed to handle (e.g., e-commerce, banking).

### 2. **Entity**
An object with a distinct identity that runs through different states (e.g., `User`, `Order`).

### 3. **Value Object**
An object that represents a concept with no identity, defined only by its attributes (e.g., `Money`, `Address`).

### 4. **Aggregate**
A cluster of domain objects treated as a single unit, with one root entity (e.g., `Order` with `OrderItems`).

### 5. **Repository**
An abstraction for retrieving and persisting aggregates (e.g., `OrderRepository`).

### 6. **Service**
Encapsulates domain logic that doesn’t naturally fit inside an entity or value object (e.g., `PaymentService`).

### 7. **Bounded Context**
A logical boundary where a particular domain model is defined and applicable (e.g., `Inventory` vs `Sales`).

### 8. **Ubiquitous Language**
A shared language between developers and domain experts used in code, conversations, and documentation.

---

## Theoretical Example: Online Store

- **Entity**: `Order`, `Customer`
- **Value Object**: `Address`, `Money`
- **Aggregate**: `Order` (root) and its `OrderItems`
- **Repository**: `OrderRepository` to fetch/store orders
- **Service**: `InventoryService` to check stock
- **Bounded Contexts**: `Billing`, `Shipping`, `Catalog`

---

## DDD in NestJS

### Structure:
```plaintext
src/
├── orders/
│   ├── domain/             # Entities, aggregates, value objects
│   ├── application/        # Use cases, services
│   ├── infrastructure/     # Repositories, persistence logic
│   └── api/                # Controllers, DTOs
```

### Example:
- `Order` entity and `OrderItem` value object in the `domain` layer
- `CreateOrderService` in `application`
- `TypeORMOrderRepository` in `infrastructure`

NestJS uses modules to organize bounded contexts cleanly. Interfaces help decouple domain from implementation.

---

## DDD in Flask (Python)

### Structure (Onion/Clean Architecture):
```plaintext
src/
├── domain/             # Entities, value objects, interfaces
├── services/           # Application logic
├── infrastructure/     # Repositories, database
├── api/                # Flask routes, schemas
```

### Example:
- `Order` and `OrderItem` in `domain`
- `order_service.py` to encapsulate logic
- `sqlalchemy_order_repository.py` in `infrastructure`

Flask decorators handle HTTP, calling service methods that interact with repositories defined by domain interfaces.

---

## DDD in NestJS

### Structure:
```plaintext
src/
├── orders/
│   ├── domain/             # Entities, aggregates, value objects
│   ├── application/        # Use cases, services
│   ├── infrastructure/     # Repositories, persistence logic
│   └── api/                # Controllers, DTOs
```

### Example Code:
**order.entity.ts**
```ts
export class Order {
  constructor(
    public readonly id: string,
    public readonly customerId: string,
    public readonly items: OrderItem[],
  ) {}
}

export class OrderItem {
  constructor(public readonly productId: string, public readonly quantity: number) {}
}
```

**order.service.ts**
```ts
@Injectable()
export class OrderService {
  constructor(private readonly orderRepo: OrderRepository) {}

  async createOrder(dto: CreateOrderDto): Promise<void> {
    const order = new Order(uuid(), dto.customerId, dto.items.map(i => new OrderItem(i.productId, i.quantity)));
    await this.orderRepo.save(order);
  }
}
```

---

## DDD in Flask (Python)

### Structure (Onion/Clean Architecture):
```plaintext
src/
├── domain/             # Entities, value objects, interfaces
├── services/           # Application logic
├── infrastructure/     # Repositories, database
├── api/                # Flask routes, schemas
```

### Example Code:
**order.py** (Domain Entity)
```python
class OrderItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

class Order:
    def __init__(self, id, customer_id, items):
        self.id = id
        self.customer_id = customer_id
        self.items = items
```

**order_service.py**
```python
class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def create_order(self, customer_id, items):
        order = Order(str(uuid.uuid4()), customer_id, [OrderItem(**item) for item in items])
        self.repository.save(order)
```

**api.py**
```python
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    service.create_order(data['customer_id'], data['items'])
    return '', 204
```

---

## DDD in .NET (C#)

### Structure:
```plaintext
src/
├── Domain/
├── Application/
├── Infrastructure/
├── WebApi/
```

### Example Code:
**Order.cs**
```csharp
public class Order {
    public Guid Id { get; }
    public Guid CustomerId { get; }
    public List<OrderItem> Items { get; }

    public Order(Guid customerId, List<OrderItem> items) {
        Id = Guid.NewGuid();
        CustomerId = customerId;
        Items = items;
    }
}

public class OrderItem {
    public Guid ProductId { get; }
    public int Quantity { get; }

    public OrderItem(Guid productId, int quantity) {
        ProductId = productId;
        Quantity = quantity;
    }
}
```

**OrderService.cs**
```csharp
public class OrderService {
    private readonly IOrderRepository _repository;

    public OrderService(IOrderRepository repository) {
        _repository = repository;
    }

    public void CreateOrder(Guid customerId, List<OrderItem> items) {
        var order = new Order(customerId, items);
        _repository.Save(order);
    }
}
```

---

## DDD in Microservices

### 1. **Bounded Context = Microservice**
Each microservice encapsulates one bounded context (e.g., `BillingService`, `InventoryService`).

### 2. **Decentralized Models**
Each service owns its data and domain model. They communicate via:
- REST APIs
- Async events (Kafka, RabbitMQ)

### 3. **Benefits**
- Clear ownership
- Independent deployment
- Domain-aligned scaling

### 4. **Example Communication**
- `OrderService` emits `OrderCreated` event
- `InventoryService` listens and reduces stock

---

## Summary
Domain-Driven Design structures software around the business domain. By defining bounded contexts, using entities, value objects, and services, and by aligning software terminology with real business concepts, DDD creates systems that are easier to maintain, scale, and evolve—especially in microservices architectures.


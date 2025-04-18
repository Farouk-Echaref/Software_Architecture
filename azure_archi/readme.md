# Application Architecture Fundamentals:

- resource: https://learn.microsoft.com/en-us/azure/architecture/guide/

## Intro: 
* Cloud-hosted applications are designed to meet business requirements using cloud-native components and functionality.
* key considerations:
    * reliability.
    * security.
    * performance.
    * cost effiency.
    * operational management.
* No specific architecture (e.g., microservices) is required, but cloud-native patterns are more accessible in the cloud.https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
### Design Apps and achieve good workload:

- Aligning to organizational cloud adoption standards means ensuring your application fits within your organization's overall cloud strategy and governance.
- **Use the Azure Well-Architected Framework to guide your application design across five core pillars: reliability, security, cost optimization, operational excellence, and performance efficiency.** This helps ensure your app meets business needs while being secure, scalable, and cost-effective. Also consider additional principles like sustainability or ethics based on your organization’s values.
    * resource: https://learn.microsoft.com/en-us/azure/well-architected/
- **Once you understand your organization's environment and design principles, choose an architecture style that fits your goals—like microservices, N-tier, or big data.** Each style has different strengths and tradeoffs, so also consider the right data store model for managing state effectively.
- **Use workload-specific guidance** from the Well-Architected Framework (e.g., for mission-critical, AI/ML, or SaaS apps) to apply relevant design principles across key areas like compute, data, and networking.
- **Follow best practices** for areas like API design, autoscaling, data partitioning, and caching to build efficient, scalable cloud applications.
- **Apply design patterns** to solve common architectural problems. These proven, reusable solutions help meet business goals while balancing tradeoffs, especially in distributed systems. Azure provides a catalog tailored for cloud scenarios.
- **Once you've chosen your architecture and patterns, select the key technologies to support your design.** Focus on:
    - **Compute:** Choose the right hosting model or platform (e.g., containers, hybrid).
    - **Data stores:** Select databases and storage based on your app’s persistence needs.
    - **Messaging:** Use asynchronous messaging to enable reliable communication between components.
    - **AI:** Leverage AI services for complex, intelligent functionality.

## Architecture Styles: 

- resource: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/

- **N-tier (multi-tier) Architecture** presentation logic, business logic, data access.
- **Web-Queue-Worker (Asynchronous)** suitable for relatively simple domains with some resource-intensive tasks. (can be used within an event driven system)
    * resource: https://codeopinion.com/web-queue-worker-architecture-style-for-scaling/
- **Microservices**
- **EDA: Event-Driven Architecture (Asynchronous APIs)**:  is a way of designing applications where components communicate by producing and responding to events.
    - Something happens → An event is created.
    - That event is published to an event broker or message queue.
    - One or more consumers (other parts of the system) subscribe to the event and act on it.
    - tools that enable EDA: rabbitmq, Webhooks, socket programming C/C++ or low-level Unix programming (socket(), poll()), WebSockets.
- **BigData/BigCompute** for HPC.

## Design Principles (to go back to):
### Design for Self-Healing:

- resource: https://mainak-saha.medium.com/5-self-healing-patterns-important-for-distributed-systems-ef4a4e3f92a9

- use decoupled components (e.q via queues)
- retry pattern.
- Load leveling (Load balancer or queue based load leveling).

### Make all things redundant (to go back to)
### Minimize Coordination (to go back to)

### Design to scale out:
- Core Principles:
    * Match demand with more instances.
    * Minimize bottlenecks and tight coupling.
    * Maximize throughput per added resource.
- Recommendations: 
    * Avoid instance stickiness:
        - Don't tie a user to one server — store session data externally (e.g., in Redis).
    * Use autonomous, decoupled components: 
        - Communicate via async protocols (queues, events) to scale parts independently.
    * Use autoscaling based on metrics:
        - Scale in/out based on CPU, queue length, or scheduled patterns.
    * Use autoscaling based on metrics:
        - Scale in/out based on CPU, queue length, or scheduled patterns.

### Partition around limits (to go back to)
### Design for operations ()
### Use an identity service (important)

## Technology Choices(to go back to):

### choose a messaging service (Asynchronous Messaging):

## Best Practices:
### RESTful API Design:

#### Whats RESTful Web API:
- Web API that follows REST principles, and follows a stateless, loosely coupled interface between client and server.
- it uses HTTP methods to interact with resources.
- it returns data representation (JSON or XML) along with HTTP Status Codes and Optional hypermedia links (HATEOAS).

- Core principles:
    * Platform Independence:
        - Any client can call the API (mobile, web...)
        - Uses standard protocol: HTTP.
        - Uses stantard data formats (JSON/XML)
        - Requires Docs.
    * Loose Coupling:
        - Client and server can evolve independently.
        - Neither side needs to know how the other is implemented.
        - Achieved by:
            * Using standard protocols (HTTP)
            - Agreeing on data formats for communication

#### RESTful Web API design concepts:

- **URI (Uniform Resource Identifier)**: each resource should be represented by a unique URI that identifies that resource:
    ```http
        https://api.contoso.com/orders/1
    ```

- **Resource Representation**: how a resource --identified by its URI-- is encoded and transported over the HTTP protocol in a specific format like JSON.
a client can make a GET request to the URI identifier `https://api.contoso.com/orders/1` in order to receive the following JSON body:
    ```json
        {"orderId":1,"orderValue":99.9,"productId":1,"quantity":1}
    ```

- **Uniform Interface**: Use of HTTP methods.

- **Stateless Request Model**: 

- **Hypermedia links**: 

#### Define RESTful web API resource URIs:

- A RESTful web API is organized around resources. To organize your API design around resources, define resource URIs that map to the business entities. When possible, resource URIs should be based on nouns (the resource) and not verbs (the operations on the resource).
- To create an order, a client sends the order information in an HTTP POST request to the resource URI. The HTTP response to the request indicates whether the order creation is successful. The orders URI could be something like this:
```http
https://api.contoso.com/orders // Good
```
- avoid using verbs in URIs to represent operations:
```
https://api.contoso.com/create-order // Avoid
```
- Group related entities into **collections** (e.g., `orders`, `customers`), each with its own **URI**:

- Example collection URI:  
  `https://api.contoso.com/orders`

- To get a specific item, use its **resource URI** (using HTTP Get request):  
  `https://api.contoso.com/orders/1`

- Example response (JSON):  
  ```json
  {"orderId":1,"orderValue":99.9,"productId":1,"quantity":1}
  ```

#### RESTful URI Naming Conventions**  

- **Use nouns for resources** (e.g., `/orders`, not `/create-order`). HTTP methods (GET, POST) imply actions.  
- **Pluralize collection URIs**: Organize hierarchically (e.g., `/customers` for collections, `/customers/5` for individual items).  
- **Model relationships carefully**: Use paths like `/customers/5/orders` for associations, but avoid deep nesting (e.g., `/customers/1/orders/99/products`). Prefer HATEOAS links in responses for related resources.  
- **Simplify URIs**: Keep paths intuitive (collection/item/collection). Avoid mirroring complex internal hierarchies.  
- **Avoid chatty APIs**: Minimize small resources; denormalize data when possible to reduce requests. Balance with payload size.  
- **Abstract internal structures**: Avoid exposing database schemas. Treat APIs as business entity abstractions, not direct table mappings.  
- **Handle non-resource operations sparingly**: Use query parameters for edge cases (e.g., `/add?operand1=99&operand2=1`). Keep this approach minimal.  

*Focus on clarity, scalability, and intuitive design over rigid structural rules.*

#### Define RESTful Web API methods:
##### RESTful API Methods  

**Core HTTP Methods**  
- **GET**: Retrieve resource(s). Idempotent.  
  - *Collections*: `/customers` → List all.  
  - *Single Item*: `/customers/1` → Details.  
  - Status Codes: `200` (OK), `204` (No Content), `404` (Not Found).  

- **POST**: Create new resource. Server assigns URI.  
  - Submit to collection URI (e.g., `/customers`).  
  - Status Codes: `201` (Created), `200`/`204` (non-resource actions), `400` (Bad Request).  

- **PUT**: Replace entire resource (idempotent).  
  - *Item*: `/customers/1` → Update or create (if supported).  
  - Status Codes: `200`, `201`, `204`, `409` (Conflict).  

- **PATCH**: Partial update via patch document (e.g., JSON Merge/Patch).  
  - *Formats*:  
    - **JSON Merge Patch**: Modify fields (set `null` to delete).  
    - **JSON Patch** (RFC 6902): Sequence of operations (add, replace, etc.).  
  - Status Codes: `200`, `400`, `409`, `415` (Unsupported Media Type).  

- **DELETE**: Remove resource. Idempotent.  
  - Status Codes: `204` (Success), `404` (Not Found).  

**Key Guidelines**  
- **Idempotence**: PUT/DELETE are safe to retry; POST/PATCH are not.  
- **Bulk Operations**: Use PUT on collections (e.g., `/customers` for batch updates).  
- **Avoid Overload**: POST for non-CRUD actions (e.g., `/search`).  

**Example Workflow**  
1. **Create Customer**: POST `/customers` → Returns `201` with URI `/customers/5`.  
2. **Update Customer**: PUT `/customers/5` → Full replacement.  
3. **Partial Update**: PATCH `/customers/5` → Send `{"status": "active"}`.  
4. **Delete**: DELETE `/customers/5` → `204`.  

*Focus on method semantics, idempotency, and clear status codes for robust APIs.*

##### RESTful Resource MIME Types:  

- **Media Types**: Define data formats (e.g., `application/json`, `application/xml`).  
- **Content-Type**: Specifies request body format.  
  ```http
  POST /orders HTTP/1.1
  Content-Type: application/json
  
  {"Id":1,"Name":"Gizmo","Category":"Widgets","Price":1.99}
  ```
  - **Error**: `415 Unsupported Media Type` if the server rejects the format.  

- **Accept**: Requests a specific response format.  
  ```http
  GET /orders/2 HTTP/1.1
  Accept: application/json, application/xml
  ```
  - **Error**: `406 Not Acceptable` if the server can’t meet the client’s format.  

**Key Workflow**:  
1. **Client sends data**: Includes `Content-Type` (e.g., JSON).  
2. **Server responds**: Uses format matching `Accept` header (defaults to its preferred type if `Accept` is missing).  

*Use headers to ensure clear client-server communication and handle format mismatches gracefully.*

#### Implement Asynchronous Methods:

**Use Case**: Long-running POST/PUT/PATCH/DELETE requests.  
**Response**: Return `202 Accepted` immediately with a status endpoint:  
```http  
HTTP/1.1 202 Accepted  
Location: /api/status/12345  
```  

**Client Workflow**:  
1. **Poll status endpoint** (from `Location` header):  
```http  
GET /api/status/12345  
```  
2. **Status response** (e.g., `200 OK`):  
```json  
{  
  "status": "In progress",  
  "link": { "rel":"cancel", "method":"delete", "href":"/api/status/12345" }  
}  
```  

**Completion Handling**:  
- If the async task **creates a resource**, redirect to its URI once done:  
```http  
HTTP/1.1 303 See Other  
Location: /api/orders/12345  
```  

**Key Guidelines**:  
- **202 Accepted**: Signals async processing started (no result yet).  
- **Status endpoint**: Let clients track progress, cancel, or estimate time.  
- **303 Redirect**: Post-completion, direct clients to the new resource.  

*Ensure clients handle polling gracefully and respect redirects.*
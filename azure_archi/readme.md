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

#### Implement Data Pagination and Filtering:
**Pagination**:  
- Use `limit` (max items per page) and `offset` (starting index) parameters.  
  ```http  
  GET /orders?limit=25&offset=50  
  ```  
  - **Defaults**: `limit=25`, `offset=0`.  
  - **Security**: Enforce a `max-limit` (e.g., 100). Exceeding it truncates or returns `400 Bad Request`.  

**Filtering**:  
- Support query params for criteria (e.g., `minCost`, `status`):  
  ```http  
  GET /orders?minCost=100&status=shipped  
  ```  

**Best Practices**:  
- **Sorting**: Use `sort` parameter (e.g., `sort=price`).  
  - ⚠️ *Caching Impact*: Query strings affect cache keys; sorted results may bypass cached data.  
- **Field Selection**: Let clients request specific fields via `fields=id,name`:  
  ```http  
  GET /orders?fields=ProductID,Quantity  
  ```  
  - Validate fields to prevent unauthorized data exposure.  

**Workflow Example**:  
1. **Paginate**: `GET /products?limit=10&offset=20` → Returns items 21-30.  
2. **Filter & Sort**: `GET /products?category=books&sort=-price` → High-to-low priced books.  
3. **Select Fields**: `GET /products?fields=title,price` → Only titles and prices.  

*Balance efficiency with security: validate inputs, enforce limits, and document query options clearly.*

#### Support Partial Responses:

**Key Features**:  
- **Partial Retrieval**: Enable clients to fetch chunks of large files (e.g., images) using byte ranges.  
- **Headers**:  
  - **`Accept-Ranges: bytes`**: Indicates partial requests are supported.  
  - **`Content-Range`**: Specifies returned byte range and total size.  

**HEAD Requests**:  
- Check resource metadata (size, type, partial support) without downloading the body:  
  ```http  
  HEAD /products/10?fields=productImage  
  ```  
  Example response:  
  ```http  
  HTTP/1.1 200 OK  
  Accept-Ranges: bytes  
  Content-Type: image/jpeg  
  Content-Length: 4580  
  ```  

**Partial GET Workflow**:  
1. **Request first chunk**:  
  ```http  
  GET /products/10?fields=productImage  
  Range: bytes=0-2499  
  ```  
  Response:  
  ```http  
  HTTP/1.1 206 Partial Content  
  Content-Length: 2500  
  Content-Range: bytes 0-2499/4580  
  ```  
2. **Fetch remaining data**:  
  ```http  
  GET /products/10?fields=productImage  
  Range: bytes=2500-4579  
  ```  

**Guidelines**:  
- Use `206 Partial Content` for successful range requests.  
- Return `416 Range Not Satisfiable` if the range is invalid.  
- **Optimization**: Use `HEAD` to pre-check resource size and capabilities.  

*Improve performance and reliability for large files by enabling chunked transfers and client-controlled retrieval.*

#### Implement HATEOAS (Hypertext as the Engine of Application State)
##### **Explanation: What is HATEOAS (Hypertext as the Engine of Application State)?**

###### **What is the problem it's solving?**
In RESTful APIs, clients should not have to **hardcode or guess** the structure of API endpoints or understand complex URI patterns. Instead, the server should guide the client dynamically by providing links to related resources and available actions.

---

###### **HATEOAS Concept**
HATEOAS is a key constraint of REST, where:

- Every response from the server includes **hyperlinks** (i.e., "hypertext") that:
  - Link to related resources.
  - Indicate possible operations (GET, PUT, DELETE, etc.).
  - Describe what kind of content types can be sent or received.

- This allows the **client to discover** and interact with the API dynamically, **without prior knowledge of its URI structure**.

> The system behaves like a finite state machine — each response tells the client what to do next.

---

###### **Example:**
Here’s what a HATEOAS response might look like:

```json
{
  "orderID": 3,
  "productID": 2,
  "quantity": 4,
  "orderValue": 16.60,
  "links": [
    {
      "rel": "customer",
      "href": "https://api.contoso.com/customers/3",
      "action": "GET",
      "types": ["application/json"]
    },
    {
      "rel": "self",
      "href": "https://api.contoso.com/orders/3",
      "action": "DELETE",
      "types": []
    }
  ]
}
```

###### What this tells us:
- We’re looking at order **#3**.
- To view the customer who made this order: follow the `"customer"` link and perform a `GET`.
- To delete this order: follow the `"self"` link with a `DELETE` request.

So, the client doesn't need to "know" how to build the customer or order URL—it’s **told** what the next actions are.

---

###### **Key Components in HATEOAS:**
- `rel`: Relationship type (e.g., "self", "customer").
- `href`: The URI to the resource.
- `action`: HTTP method (GET, PUT, etc.).
- `types`: MIME types accepted or returned.

---

###### **Important Notes:**
- There’s **no universal standard** for implementing HATEOAS—each API can define its own format.
- HATEOAS promotes **loose coupling**, making APIs more flexible and self-explanatory.

---

###### **Summary:**

| Concept                      | Description |
|-----------------------------|-------------|
| **HATEOAS**                 | A REST constraint where responses include hypermedia links guiding the client on possible next actions. |
| **Goal**                     | Let clients discover related resources and operations **dynamically** through hyperlinks in responses. |
| **Structure**                | Each link in a response includes `rel`, `href`, `action`, and `types`. |
| **Benefit**                  | Clients don't need prior knowledge of API structure, making systems easier to evolve. |
| **State-dependent links**    | The set of available links can **change depending on the resource's state**, enabling dynamic workflows. |

#### Implement versioning:

APIs evolve; versioning ensures **backward compatibility** for existing clients while enabling **new features** for newer ones.

##### No Versioning
- Works for small/internal APIs.
- Adding fields is safe; removing/renaming fields breaks clients.
- Simple, but risky for long-term changes.

##### URI Versioning
- Embed version in URI: `/v1/customers/3`
- Easy to route.
- Breaks REST purity (same resource, different URI).
- Makes HATEOAS harder to maintain.

##### Query String Versioning
- Append version: `/customers/3?version=2`
- Keeps URI consistent.
- Affects caching behavior in some proxies/browsers.
- Also complicates HATEOAS links.

##### Header Versioning
- Use custom headers: `Custom-Header: api-version=2`
- Keeps URI clean.
- Requires clients to set headers.
- Harder to cache, more complex logic.

##### Media Type Versioning
- Use `Accept` header: `Accept: application/vnd.contoso.v1+json`
- Most RESTful.
- Works well with HATEOAS.
- Complex to implement and parse.
- Least cache-friendly.

##### Key Considerations
- Choose a strategy that fits your API’s clients and scale.
- Balance between purity (media type) and simplicity (URI).
- Always prioritize **non-breaking changes** for existing consumers.

#### Multitenant web APIs:

A multitenant web API serves multiple tenants (organizations or groups) through a single API infrastructure. Multitenancy impacts API design, requiring clear tenant identification and ensuring isolation, scalability, and customization.

**Tenant identification methods**:
- **Subdomains or custom domains**: Routing requests through tenant-specific domains (e.g., `tenant1.api.com`). Requires proper DNS setup.
- **HTTP headers**: Passing tenant information via headers (e.g., `X-Tenant-ID`). Simplifies API paths but complicates caching and requires Layer 7 gateways.
- **JWT tokens**: Embedding tenant ID in token claims for secure, centralized authentication.
- **URI paths**: Including tenant ID in the URL (e.g., `/tenants/tenant1/orders/3`). Straightforward but less RESTful.

**Design considerations**:
- Impacts endpoint structure, request handling, authentication, and authorization.
- Influences API gateway and load balancer configurations.
- Requires careful caching strategies to prevent data leakage across tenants.

#### Enabling distributed tracing and trace context in APIs

### Web API Implementation:

#### Processing Requests 

**Idempotency**:  
GET, PUT, DELETE, HEAD, and PATCH should be idempotent—repeating the same request should not change the system state beyond the first request.

**POST Operations**:  
POST should only affect the new resource (and directly linked resources), without causing unrelated side effects.

**Avoid Chatty APIs**:  
Minimize small, repetitive POST, PUT, and DELETE operations. Support batch operations on collections to reduce network and compute overhead.

**Follow HTTP Specification**:  
Return proper status codes, headers, and formatted response bodies. Example: POST must return 201 Created and include the new resource’s URI.

**Content Negotiation**:  
Support multiple response formats (like JSON, XML) based on the client's `Accept` header. Default to a sensible format (e.g., JSON) if none is specified.

**HATEOAS Support**:  
Include navigational links in responses so clients can discover related resources and actions dynamically. Each link should describe:
- Relation (`rel`)
- URI (`href`)
- HTTP action (`action`)
- Supported content types (`types`)

#### Handling Exceptions 

**Capture and return meaningful errors**:  
Don't let exceptions crash the system. Catch them and return proper HTTP responses with helpful error messages (not just generic 500 errors).

**Use appropriate status codes**:  
- 400 (Bad Request): when the request is invalid.  
- 404 (Not Found): when a resource doesn’t exist.  
- 409 (Conflict): for conflicts like constraint violations.  
- 500 (Internal Server Error): for unhandled/unexpected errors.

**Example practice**:  
Catch errors inside your controller methods and respond properly based on the situation (example given with `DeleteCustomer` endpoint).

**Security tip**:  
Don't expose sensitive server/internal information in error responses (protect against attackers).

**Authentication and Authorization**:
- 401 (Unauthorized): when authentication fails (handled often by the server itself).  
- 403 (Forbidden): when a user is authenticated but not allowed to access a resource.

**Consistency and logging**:  
Implement **global exception handling** and **error logging** — log full error details privately, not exposed to clients.

**Client vs Server errors**:  
Respect the 4xx (client error) vs 5xx (server error) distinction when setting response codes.

```C#
[HttpDelete]
[Route("customers/{id:int}")]
public IHttpActionResult DeleteCustomer(int id)
{
    try
    {
        // Find the customer to be deleted in the repository
        var customerToDelete = repository.GetCustomer(id);

        // If there is no such customer, return an error response
        // with status code 404 (Not Found)
        if (customerToDelete == null)
        {
            return NotFound();
        }

        // Remove the customer from the repository
        // The DeleteCustomer method returns true if the customer
        // was successfully deleted
        if (repository.DeleteCustomer(id))
        {
            // Return a response message with status code 204 (No Content)
            // To indicate that the operation was successful
            return StatusCode(HttpStatusCode.NoContent);
        }
        else
        {
            // Otherwise return a 400 (Bad Request) error response
            return BadRequest(Strings.CustomerNotDeleted);
        }
    }
    catch
    {
        // If an uncaught exception occurs, return an error response
        // with status code 500 (Internal Server Error)
        return InternalServerError();
    }
}
```

#### Optimizing client-side data access:

**Network is a bottleneck**:  
Minimize traffic between client and server to improve performance.

##### Support Client-Side Caching

**HTTP 1.1 caching** uses the `Cache-Control` header to tell clients and proxies how to cache responses.

Example HTTP request and response:

```http
GET https://adventure-works.com/orders/2 HTTP/1.1
```

```http
HTTP/1.1 200 OK
Cache-Control: max-age=600, private
Content-Type: text/json; charset=utf-8
Content-Length: ...
{"orderID":2,"productID":4,"quantity":2,"orderValue":10.00}
```

**Meaning**:
- `max-age=600`: Cache valid for 600 seconds.
- `private`: Only the client (not shared caches) can store it.

Other options:
- `public`: Allows shared caching (e.g., proxy caches).
- `no-store`: Prohibits caching entirely.

---

###### Example: Setting Cache-Control in a C# Web API

```csharp
public class OrdersController : ApiController
{
    [Route("api/orders/{id:int:min(0)}")]
    [HttpGet]
    public IHttpActionResult FindOrderByID(int id)
    {
        Order order = ...; // Fetch order

        var cacheControlHeader = new CacheControlHeaderValue
        {
            Private = true,
            MaxAge = new TimeSpan(0, 10, 0) // 10 minutes
        };

        OkResultWithCaching<Order> response = new OkResultWithCaching<Order>(order, this)
        {
            CacheControlHeader = cacheControlHeader
        };
        return response;
    }
}
```

Here, the controller uses a **custom `IHttpActionResult`** to attach cache headers.

---

###### Custom IHttpActionResult Example (`OkResultWithCaching`)

```csharp
public class OkResultWithCaching<T> : OkNegotiatedContentResult<T>
{
    public CacheControlHeaderValue CacheControlHeader { get; set; }
    public EntityTagHeaderValue ETag { get; set; }

    public OkResultWithCaching(T content, ApiController controller)
        : base(content, controller) { }

    public override async Task<HttpResponseMessage> ExecuteAsync(CancellationToken cancellationToken)
    {
        HttpResponseMessage response = await base.ExecuteAsync(cancellationToken);
        response.Headers.CacheControl = this.CacheControlHeader;
        response.Headers.ETag = ETag;
        return response;
    }
}
```

Handles setting:
- `Cache-Control`
- `ETag` headers

Handles cancellation by returning HTTP 409 (Conflict) if the operation is canceled.

---

###### Important Notes

- `no-cache` **doesn't** mean "don't cache" — it means "cache but always validate before using."
- `max-age` is only a *hint*, not a guarantee — data might still change within that time.
- Proper cache management can **significantly** save bandwidth and improve performance.

---

###### Browser and Proxy Behaviors

- **Modern browsers** respect cache headers (even with query strings).
- **Older browsers and proxies** may refuse to cache URLs that have a query string (`?param=value`).  
  (This is less of an issue for modern custom clients.)

##### Provide ETags to optimize query processing:

When a client retrieves an object, the server response can include an **ETag**, an opaque string identifying the version of the resource. Each time a resource changes, the ETag also changes. Clients should cache the ETag with the resource.

Example of adding ETag in C#:

```csharp
public class OrdersController : ApiController
{
    public IHttpActionResult FindOrderByID(int id)
    {
        Order order = ...;
        var hashedOrder = order.GetHashCode();
        string hashedOrderEtag = $"\"{hashedOrder}\"";
        var eTag = new EntityTagHeaderValue(hashedOrderEtag);

        OkResultWithCaching<Order> response = new OkResultWithCaching<Order>(order, this)
        {
            ETag = eTag
        };
        return response;
    }
}
```

Example HTTP response:

```
HTTP/1.1 200 OK
Cache-Control: max-age=600, private
Content-Type: text/json; charset=utf-8
ETag: "2147483648"
Content-Length: ...
{"orderID":2,"productID":4,"quantity":2,"orderValue":10.00}
```

Tip:  
For security, avoid caching sensitive or HTTPS data.

###### Conditional GET requests using ETag

The client can send the cached ETag with an `If-None-Match` header to check if the resource has changed.

Example HTTP GET with `If-None-Match`:

```
GET https://adventure-works.com/orders/2 HTTP/1.1
If-None-Match: "2147483648"
```

Server behavior:
- If ETag matches → return `304 Not Modified` with no body.
- If ETag does not match → return `200 OK` with updated resource.
- If resource is missing → return `404 Not Found`.

If `Cache-Control: no-store` is present, the client must not cache, regardless of the status code.

###### C# Example supporting `If-None-Match`

```csharp
public class OrdersController : ApiController
{
    [Route("api/orders/{id:int:min(0)}")]
    [HttpGet]
    public IHttpActionResult FindOrderByID(int id)
    {
        try
        {
            Order order = ...;
            if (order == null)
                return NotFound();

            var hashedOrder = order.GetHashCode();
            string hashedOrderEtag = $"\"{hashedOrder}\"";
            var cacheControlHeader = new CacheControlHeaderValue { Public = true, MaxAge = new TimeSpan(0, 10, 0) };
            var eTag = new EntityTagHeaderValue(hashedOrderEtag);

            var nonMatchEtags = Request.Headers.IfNoneMatch;

            if (nonMatchEtags.Count > 0 && String.CompareOrdinal(nonMatchEtags.First().Tag, hashedOrderEtag) == 0)
            {
                return new EmptyResultWithCaching()
                {
                    StatusCode = HttpStatusCode.NotModified,
                    CacheControlHeader = cacheControlHeader,
                    ETag = eTag
                };
            }
            else
            {
                return new OkResultWithCaching<Order>(order, this)
                {
                    CacheControlHeader = cacheControlHeader,
                    ETag = eTag
                };
            }
        }
        catch
        {
            return InternalServerError();
        }
    }
}
```

###### Helper class for 304 Not Modified responses

```csharp
public class EmptyResultWithCaching : IHttpActionResult
{
    public CacheControlHeaderValue CacheControlHeader { get; set; }
    public EntityTagHeaderValue ETag { get; set; }
    public HttpStatusCode StatusCode { get; set; }
    public Uri Location { get; set; }

    public async Task<HttpResponseMessage> ExecuteAsync(CancellationToken cancellationToken)
    {
        HttpResponseMessage response = new HttpResponseMessage(StatusCode);
        response.Headers.CacheControl = this.CacheControlHeader;
        response.Headers.ETag = this.ETag;
        response.Headers.Location = this.Location;
        return response;
    }
}
```

Tip:  
If the ETag can be computed without retrieving the data (e.g., based on a version number or a known checksum), this can avoid fetching large or remote data unnecessarily.

##### Use ETags to Support Optimistic Concurrency

- This section explains how **ETags** can be used to support **optimistic concurrency control**.  
When a client updates (PUT) or deletes (DELETE) a resource, it should include the ETag in an `If-Match` header.  
The API compares the provided ETag with the current resource’s ETag to decide:
- If they match → perform the operation (update or delete).
- If they don’t → return **412 Precondition Failed** (someone else modified the resource).
- If the resource is missing → return **404 Not Found**.

This ensures that **updates don't overwrite** changes made by others.  
**Tip**: Always include `If-Match` to avoid lost updates.

- ETags enable optimistic concurrency by ensuring updates only happen if the resource has not changed.

###### Process Overview
- Client sends a `PUT` or `DELETE` request with an `If-Match` header containing the cached ETag.
- Server compares the current ETag of the resource with the provided one.
- Depending on the comparison:
  - **Match**: Perform the update or delete, return **204 No Content** with updated ETag and Location header.
  - **Mismatch**: Return **412 Precondition Failed** (resource has changed).
  - **Resource missing**: Return **404 Not Found**.

###### Example PUT Request
```http
PUT https://adventure-works.com/orders/1 HTTP/1.1
If-Match: "2282343857"
Content-Type: application/x-www-form-urlencoded
Content-Length: ...
productID=3&quantity=5&orderValue=250
```

###### How the Web API Should Handle It
- Fetch the resource (e.g., order 1).
- Compare the ETag with the value in `If-Match`.
- Perform update or respond with 412/404 accordingly.

###### Example Code (C#)
```csharp
public class OrdersController : ApiController
{
    [HttpPut]
    [Route("api/orders/{id:int}")]
    public IHttpActionResult UpdateExistingOrder(int id, DTOOrder order)
    {
        try
        {
            var baseUri = Constants.GetUriFromConfig();
            var orderToUpdate = this.ordersRepository.GetOrder(id);
            if (orderToUpdate == null)
                return NotFound();

            var hashedOrder = orderToUpdate.GetHashCode();
            string hashedOrderEtag = $"\"{hashedOrder}\"";
            var matchEtags = Request.Headers.IfMatch;

            if ((matchEtags.Count > 0 &&
                 String.CompareOrdinal(matchEtags.First().Tag, hashedOrderEtag) == 0) ||
                matchEtags.Count == 0)
            {
                orderToUpdate.OrderValue = order.OrderValue;
                orderToUpdate.ProductID = order.ProductID;
                orderToUpdate.Quantity = order.Quantity;

                // Save order ...

                var cacheControlHeader = new CacheControlHeaderValue()
                {
                    Private = true,
                    MaxAge = new TimeSpan(0, 10, 0)
                };

                hashedOrder = order.GetHashCode();
                hashedOrderEtag = $"\"{hashedOrder}\"";
                var eTag = new EntityTagHeaderValue(hashedOrderEtag);

                var location = new Uri($"{baseUri}/{Constants.ORDERS}/{id}");

                return new EmptyResultWithCaching()
                {
                    StatusCode = HttpStatusCode.NoContent,
                    CacheControlHeader = cacheControlHeader,
                    ETag = eTag,
                    Location = location
                };
            }

            return StatusCode(HttpStatusCode.PreconditionFailed);
        }
        catch
        {
            return InternalServerError();
        }
    }
}
```

###### Tip
- If `If-Match` is **omitted**, the server will always perform the update, risking overwriting another user’s change.
- **Always include** `If-Match` to prevent lost updates.


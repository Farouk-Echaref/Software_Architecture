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
    * ```http
        https://api.contoso.com/orders/1
    ```

- **Resource Representation**: how a resource --identified by its URI-- is encoded and transported over the HTTP protocol in a specific format like JSON.
a client can make a GET request to the URI identifier `https://api.contoso.com/orders/1` in order to receive the following JSON body:
    ```json
        {"orderId":1,"orderValue":99.9,"productId":1,"quantity":1}
    ```

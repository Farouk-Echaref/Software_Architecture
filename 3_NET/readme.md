# Net Microservices
## Chap3: Architecting container and microservice-based applications

- **Microservice architecture patterns are essential** for building scalable, maintainable applications.  
- **Containers are helpful but not required** for microservices—they're just a good fit.  
- **Understanding Domain-Driven Design (DDD) patterns and container orchestration** is crucial for handling complex, enterprise-level applications.  
- The guide emphasizes the **intersection of microservices and containers**, reflecting real-world usage.  

### Container Design Principles:

- **Each container should represent a single process**—this defines a clear process boundary.
- The **`ENTRYPOINT` in a Dockerfile** defines the main process that controls the container's lifecycle.
- **When the process ends or fails, the container stops**, and the **orchestrator** (like Kubernetes) may restart it.
- Containers can be used for both:
  - **Long-running processes** (e.g., web servers)
  - **Short-lived batch jobs**
- **Orchestrators manage container failures and scaling**, ensuring availability and reliability.
- **Running multiple processes in one container is possible**, but it's **uncommon and not recommended**—better to use one process per container for simplicity and scalability.

### Containerizing monolithic applications:

![alt text](docker_infra_mono.png)

- A **monolithic application** can be deployed as a **single container**, even if it has multiple internal layers (e.g., application, domain, data access).
- **Scaling is done by cloning the container** and using a load balancer—simple, but coarse-grained.
- This approach **conflicts with the container principle**: *“a container does one thing in one process”*, but can still be acceptable in some scenarios.
- **Scaling issues** arise when only part of the app needs more resources—monoliths force **scaling everything**, leading to inefficiency.
- **Changing one component requires full redeployment and retesting**, increasing complexity as the app grows.
- Despite drawbacks, **monolithic apps are common** due to simpler development and historical infrastructure/tooling limitations.
- Platforms like **Azure App Service and Azure VM Scale Sets** support scaling monolithic apps easily, including those in Docker containers.
- Monolithic deployment is manageable using traditional methods (e.g., `docker run`, `docker-compose`) or modern CD pipelines. 

### Deploying a monolithic application as a container:

- **Containers simplify and speed up scaling** compared to traditional VMs.
- **Docker images start quickly** (in seconds), making rollouts and updates much faster.
- **Stopping and restarting containers is fast and easy** (e.g., `docker stop`).
- **Containers are immutable**, reducing risks of configuration drift or corruption common with VMs.
- **Deploying updates via Docker images** is more efficient and consistent than using update scripts on VMs.
- **Container orchestrators add more benefits**, like managing container lifecycles and scaling.
- **Breaking down the monolith into subsystems** is the first step toward transitioning to **microservices**. 

### Publishing a single-container-based application to Azure App Service

![alt text](azure_container_registry.png)

- **Azure App Service supports scalable single-container deployments**, ideal for validation or production use.
- **Integration with Git and Visual Studio** makes it easy to build and deploy directly to Azure.
- **Before container support**, you were limited by the dependencies supported in App Service.
- **With containers, you can include any required dependencies** in your Dockerfile/image.
- **Visual Studio (2017+) supports containerized deployments**, offering flexibility and control.
- **Images are published through a container registry**, such as:
  - **Azure Container Registry** (secure and Azure-integrated)
  - **Docker Hub** or other registries (including on-premises ones)

### Manage State and Data in Docker Applications:

![alt text](data_container.png)

- **Containers are ephemeral**: Data inside a container is temporary and not persistent.
- **Docker Volumes**: Preferred method for persistent data. They are isolated from the host and can outlast the container’s lifecycle.
- **Bind Mounts**: Allow containers to access specific host directories, but less secure and prone to data inconsistencies.
- **tmpfs Mounts**: Store data in memory, fast but non-persistent.
- **Remote Storage Options**: Use cloud services like **Azure Storage**, **SQL databases**, or **NoSQL databases** for persistent, critical data.
- **Best Practice**: Use Docker volumes for non-critical state and rely on remote storage for important data.

### Service-oriented architecture:

- **SOA Overview**: SOA decomposes applications into multiple services (typically HTTP services) that are categorized into subsystems or tiers.
- **SOA with Docker**: Docker containers help with deployment by bundling dependencies within the container image.
- **Scaling SOA**: Single Docker hosts may face scalability and availability challenges; clustering or orchestrators help address these issues.
- **SOA vs. Microservices**: Microservices come from SOA but avoid common SOA patterns (e.g., central brokers, Enterprise Service Bus). Microservices are considered a refined version of SOA.
- **Focus on Microservices**: This guide emphasizes microservices due to their more prescriptive requirements compared to SOA.

### Microservices architecture:

![alt text](mono_vs_micro.png)

- **Definition**: Microservices architecture builds applications as a set of small, independent services. Each service:
  - Runs in its own process
  - Communicates via HTTP/HTTPS, WebSockets, or AMQP
  - Has its own domain data, logic, and storage (SQL/NoSQL)

- **Key Principles**:
  - Focus on **loose coupling** and **high cohesion**, not size
  - Services should be **autonomous**, **independently deployable**, and **individually scalable**

- **Benefits**:
  - Better maintainability for complex, scalable systems
  - Independent scaling reduces cost (scale only what’s needed)
  - Faster development and deployment
  - Supports CI/CD and agile practices
  - Enables isolated testing and evolution of services without breaking others

- **Monolith vs. Microservices**:
  - Monolith: scale whole app
  - Microservices: scale only required services → more efficient and agile

- **Production Success Factors**:
  - Service and infrastructure monitoring
  - Scalable cloud infrastructure and orchestrators
  - Robust security: auth, secrets, secure comms
  - DevOps practices and rapid delivery pipelines

### Data sovereignty per microservice:

![alt text](data_micro.png)

- **Data ownership**: Each microservice must **own its own data and logic**, with an independent lifecycle and deployment.

- **Bounded Contexts (DDD)**: Each microservice represents a specific business domain (bounded context) and maintains its own domain model.

- **Monolithic vs. Microservice Data**:
  - *Monolithic*: Single centralized SQL database, easier for cross-table queries, but leads to tightly coupled systems and massive, bloated tables.
  - *Microservices*: Each service has its **own isolated database**, promoting autonomy and scalability.

- **Data Access in Microservices**:
  - Data is private to each microservice.
  - Shared access must go through **APIs (REST, gRPC, SOAP)** or **messaging (AMQP, etc.)**.
  - Prevents tight coupling and allows independent evolution.

- **Trade-offs**:
  - Lose ability for ACID transactions across services → must use **eventual consistency** for multi-service workflows.
  - Can't do distributed SQL joins or constraints across microservices.

- **Polyglot Persistence**:
  - Microservices can use **different types of databases** (SQL, NoSQL) depending on needs.
  - Enables better **performance**, **scalability**, and **manageability**, but adds **complexity** in data coordination.

#### The relationship bettween Microservices and the Bounded Context:

- **Bounded Contexts**:
  - Divide large domain models into **distinct, well-defined areas**.
  - Each has **its own model, database**, and **ubiquitous language** (terms used consistently by devs and domain experts).
  - Terms can vary across contexts even if they represent the same identity (e.g., *User* in one BC may be *Buyer* in another).

- **Microservices = Bounded Contexts as distributed services**:
  - Each microservice aligns with a BC and is deployed as a **separate process**.
  - Communicates via **distributed protocols** (HTTP, WebSockets, AMQP, etc.).

- **Difference**:
  - BCs don't require distribution—they can exist inside a monolithic app.
  - Microservices enforce distribution and independence.

- **Design tip**:
  - It's smart to align one microservice per Bounded Context.
  - But flexibility exists—some BCs may consist of **multiple microservices**.

- **Shared principle**:
  - Both patterns emphasize **owning the domain model** and **not sharing it across services**.

# Microservices

## Micro simplified :

- resource: https://www.youtube.com/watch?v=lL_j7ilk7rc&ab_channel=5MinutesorLess

- architecture paradigm that address the limitations of legacy application.
- monolethic => multitier => microservices. 

### Monolethic App:

![alt text](monolethic.png)

- straightforward day to build a simple app where u design a single piece of code encapsulating data storage and access, business logic and processes, and user interfaces. 

- limitations when building complex systems, since everything is tangled together, it becames difficult to mantain, evolve and scale.

### Multitier architecture:

![alt text](multitier.png)

- architecture components are separated into layers based on technical functions.
common model three-tier archi.

- presentation layer (frontend): covers code and components responsible for interaction with usecrs through user interfaces.
- logic layer (backend): business logic and processes, relative to business functions.
- data layer: storing, accessing and retrieving data when needed.

- separting logic and data made things better, it was still a centralized way to designing application and still monolethic.

![alt text](app_complexity.png)

### Microservices:

![alt text](microservices.png)

- best way to tackle complexity is by decomposing it into manageable chunks, breaking everything into smaller pieces.

![alt text](microservices2.png)

- every microservice deals with one business function, end to end independently from other microservices, they present simple easy to understand apis (API Gateway), and communicate with eachother through common protocols like HTTP

![alt text](microservices3.png)

- when an app is designed with microservices, different teams can work separatly and indefrently on different microservices, theoratically teams could use different programming languages and deploy their microservices to different infrastructre, however, for cost reduction, operational optimization, efficiency improvement, we limit our team choices to a set of approved tools, infra providers (clouds), programming languages.
- deploy in this screenshot is done via CI/CD.

- to manage the complexity of the highly distributed microservices, we have solutions like containerazition, container orchestration, pipeline automation for CI/CD, asynchronous messaging for message brokers and queus (kafka), performance monitoring (prometheues) to track microservice performance, logging and audit tools that helps track everyhting within the system(datadog).

![alt text](microservices4.png)


## Microservices explained - the What, Why and How?

- resource: https://www.youtube.com/watch?v=rv4LlmLmVWk&ab_channel=TechWorldwithNana

### Monolethic and its downsides:

* drawbacks of monolethic:

![alt text](micro_limits.png)

* higher infra costs in terms of scaling

![alt text](micro_challenges_1.png)

![alt text](micro_challneges_2.png)

### Microservices solutions:

![alt text](micro_archi.png)

* answers to the micro questions: 

![alt text](micro_archi_solution.png)

* note: Apps should be **Loosely Coupled**

* if you change something in one service, that only service will be built and deployed

![alt text](one_service_deploy.png)

* versioning for each service:

![alt text](each_version.png)

### Communications between services:

#### Communication using API calls (Synchronous Communication => send request and wait for response)

![alt text](micro_http_communication.png)

#### Communication using message broker (Asynchronous - eg: RabbitMQ)

![alt text](micro_msg_broker.png)

#### Communication via Service Mesh (Used with K8S):

![alt text](micro_service_mesh.png)

### Possible Downsides: 

![alt text](micro_issues.png)

* for example when configuring the communication between the services, a microservice may be down, unhealthy or just not ready and not responding yet, while another service starts sending requests to its API expecting a fullfied response. 

### Tools to tackle these challenges: 

* we need tools for:
- IaC (Terraform from Hashicorp)
- security (Vault for secret management from Hashicorp)
- orchestration (K8S)
- containers
- messaging
- service mesh (apart from K8S, )
- monitoring

### CI/CD Pipelines for Microservices:
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

- to manage the complexity of the highly distributed microservices, we have solutions like containerazition, container orchestration, pipeline automation for CI/CD, asynchronous messaging for message brokers and queus (kafka), performance monitoring (prometheues) to track microservice performance, logging and audit tools that helps track everyhting within the system(datadog).

![alt text](microservices4.png)

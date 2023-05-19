#  Pizza ordering service using Django REST framework

### In this project, we implemented CRUD RESTful APIs with Django and Django REST framework, to implement a pizza ordering services with the following functionality:

• Order pizzas:
    
    • It should be possible to specify the desired flavours of pizza (margarita, marinara, salami), the number of pizzas and their size (small, medium, large).
    • An order should contain information regarding the customer.
    • It should be possible to track the status of delivery.
    • It should be possible to order the same flavour of pizza but with different sizes multiple times

• Update an order:

    • It should be possible to update the details — flavours, count, sizes — of an order
    • It should not be possible to update an order for some statutes of delivery (e.g. delivered).
    • It should be possible to change the status of delivery.
    
• Remove an order.

• Retrieve an order:
  
    • It should be possible to retrieve the order by its identifier.
• List orders:
    
    • It should be possible to retrieve all the orders at once.
    • Allow filtering by status / customer.

### pizza_order_api application

This application used for implement the APIs and logic for CRUD actions for pizza order implementation.

    - Models: We used two models: PizzaOrderModel, PizzaOrderItemsModel
    - Serializers: Used for converting and mapping between the DTO and models, as well as logics for create and update models.
    - Views: Implement the logic functionalities for CRUD APIs (as GenericViewSet)

### Run locally
In order to run the project on local machine, first you need to have a PostgreSQL database up. So using the docker-compose
setup available in the project, by using the following command, you can setup a database, which used in the project.
   
    docker-compose up -d postgres_db
    
After setup the database, run the following commands sequentially in order to perform database migrations on the database:
    
    make makemigrations
    make migrate

So the table of models must be created on the DB. And finally using the following command, the application server starts up:
   
    make server
    
### Swagger-ui documentation
First, you must run the following command, in order to collect static files required for swagger-ui.

    make collectstatic
    
Then, by running the application, Note that the default value for base address {{url}} of the application is: http://127.0.0.1:8000.
So the swagger web page is accessible on: 
    
    {{url}}/swagger


### Tests
In this project, we implemented some API test cases for the following scenarios:

    - Create a new order
    - Search on orders to fetch a list of order matching the customer name and specific status
    - Retrieve a specifc order (by its Identifier)

In order to run the tests, use the following command:

    make test
    
### Docker set-up and how to run
We provide a docker setup using a Dockerfile (for build the project as a docker image, as well as commands to start as a docker container).
Also a docker-compose.yml file in order to start the PostgreSQL database as well as the project application in containers.
A volume is considered for the database, in order to persist the data on Disk, and a local docker network is considered for communication between the
project application and the database. (So we can using the container name inplace of host in database setting of the project)
    
    
In order to start the project application and the database in containerized mode, do the following commands:

Start the database:
    
    docker-compose up -d postgres_db
    docker-compose up -d django_app

So the server must be start up at the:
 
    http://{{IP_ADDRESS_OF_THE_SERVER}}:8000


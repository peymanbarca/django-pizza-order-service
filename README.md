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

    - Models
    - Serializers
    - Views
    
### Swagger-ui documentation
    
### Tests
    
    
### Docker set-up and how to run

    - docker-compose up -d postgres_db
    


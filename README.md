# central-distribution-system
## Project for distribution system lecture

### System description:
* Each product manufacturer provides an interface indicating the quantity of goods they can supply.
* Every month, the Central Distributor communicates with individual Manufacturers to retrieve data on the offered goods.
* Each Customer communicates with the Central Distributor to purchase the necessary goods. The Central Distributor can serve multiple customers simultaneously. Once all customers have purchased the goods or the available goods have been depleted, the Central Distributor informs the Manufacturers.

The goal of the described system is to enable the distribution of goods from manufacturers to customers. The system allows manufacturers to list their goods, collects information on the availability of those goods, and provides it to customers through the Distribution Center interface. Customers can choose which goods they want to buy and from which manufacturer, while the Distribution Center manages the entire process, including updating the database and notifying manufacturers about the quantity of goods sold.

### System scope:   
The system scope also includes parallel production of goods by manufacturers and the ability of the Distribution Center to serve multiple customers simultaneously. The system gathers information on the availability of goods from manufacturers and stores it in the Distribution Center. The system aims to effectively serve customers by selling them goods based on accurate information about the current stock status.

# problems and adjustments:
- ~~What if customer adds products to cart or try to buy product and in the meantime they won't be available anymore?~~   
    ~~↳ Add removing not available products (all row even if only one of many is not available) and show popup to inform user about that~~
- ~~Add verification from database when adding item to cart, watching cart add popup if some items are not available anymore~~
- Add helpers to simulate random network traffic for presentation (calls from users adding items to cart, buying them) 
- ### Add queue system:
To ensure that the information about a purchased product is updated in the manufacturer's database before responding to subsequent calls from the central distributor to get all available products, you can introduce a synchronization mechanism.

One possible approach is to use a message queue system, such as RabbitMQ or Apache Kafka, to decouple the communication between the central distributor and the manufacturer apps. Here's how you can modify your code to incorporate a message queue:

1. Set up a message queue system: Install and configure RabbitMQ or Apache Kafka according to your preference. This will serve as the communication channel between the central distributor and the manufacturer apps.

2. Modify the manufacturer apps:
   - Instead of exposing the `/all_products` endpoint directly, the manufacturer apps should listen to messages from the message queue system.
   - When a message is received indicating a product purchase, the app should update its local database with the purchased product information.

3. Modify the central distributor app:
   - Instead of directly calling the manufacturer endpoints, the central distributor app should publish a message to the message queue system indicating a product purchase.
   - After publishing the message, the central distributor can proceed with other tasks.
   - The central distributor can have a separate endpoint for retrieving all available products, which can be called periodically or on demand by other services.
   - When the central distributor receives a response from a manufacturer indicating that the product purchase message has been processed and the manufacturer's database is updated, it can then fetch the updated product information from the manufacturer and respond to subsequent requests for all available products.

With this approach, the central distributor and the manufacturer apps are decoupled, and the synchronization is achieved through the message queue system. The manufacturer apps update their local databases upon receiving purchase messages, and the central distributor fetches the updated product information after receiving confirmation from the manufacturer.

Note: Implementing a message queue system requires additional setup and configuration. You may need to familiarize yourself with the specific message queue system you choose and adjust the code accordingly.

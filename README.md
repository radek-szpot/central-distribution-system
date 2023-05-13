# central-distribution-system
## Project for distribution system lecture

### System description:
* Each product manufacturer provides an interface indicating the quantity of goods they can supply.
* Every month, the Central Distributor communicates with individual Manufacturers to retrieve data on the offered goods.
* Each Customer communicates with the Central Distributor to purchase the necessary goods. The Central Distributor can serve multiple customers simultaneously. Once all customers have purchased the goods or the available goods have been depleted, the Central Distributor informs the Manufacturers.

The goal of the described system is to enable the distribution of goods from manufacturers to customers. The system allows manufacturers to list their goods, collects information on the availability of those goods, and provides it to customers through the Distribution Center interface. Customers can choose which goods they want to buy and from which manufacturer, while the Distribution Center manages the entire process, including updating the database and notifying manufacturers about the quantity of goods sold.

### System scope:   
The system scope also includes parallel production of goods by manufacturers and the ability of the Distribution Center to serve multiple customers simultaneously. The system gathers information on the availability of goods from manufacturers and stores it in the Distribution Center. The system aims to effectively serve customers by selling them goods based on accurate information about the current stock status.

### Project structure:
```
centralized_distribution_system/
├── manufacturers/
│   ├── manufacturer1.py
│   ├── manufacturer2.py
│   └── ...
├── distributor/
│   ├── distributor.py
│   ├── database.py
│   └── message_broker.py
├── customers/
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   └── ...
│   └── __init__.py
├── load_balancer/
│   ├── load_balancer.py
│   └── config.yml
└── main.py
```

### Ray usage:
* manufacturers/:
* * The manufacturers module can use Ray to parallelize tasks related to fetching and processing goods information from individual manufacturers. For example, if you have multiple manufacturers and need to fetch their product information concurrently, you can distribute the task of fetching information using Ray's task-based parallelism.

* distributor/:
* * Parallelizing database operations: If the distributor needs to perform heavy database operations, such as querying or updating the distributed database, you can use Ray to parallelize those tasks across multiple workers, improving performance.   
* * Asynchronous processing of customer requests: Ray's task-based model can be utilized to handle incoming customer requests asynchronously. For example, when a customer places an order, you can dispatch a Ray task to process the order, allowing the distributor to continue serving other customers concurrently.

* load_balancer/:
* * The load_balancer module can benefit from Ray when distributing customer requests to the distributor instances. Ray can be used to manage and distribute the load balancing tasks across the available distributor instances.

By integrating Ray into these modules, you can take advantage of its distributed computing capabilities, such as task parallelism, load balancing, and resource management. It allows you to scale your system, improve performance, and make efficient use of available resources.



# Problemy:
- jak customer doda do koszyka towary i da kup to co jak ich nie bedzie ma kupić to co się da 
(dostać popup i zaznaczyć czy kupić co się da czy wyczyścić koszyk i wrócic do dashboardu)
- fajnie by bylo dodac jakas metode refresh'a do dashboard'a tak zeby widac bylo jak sie zmienia quantity
- dodac obsluge wyjatkow w modify account register itp niektore sa ale tak tylko dla pewnosci


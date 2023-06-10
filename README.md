# central-distribution-system
## Project for distributed systems lecture 

### System description:
* Each product manufacturer provides an interface indicating the quantity of goods they can supply.
* Every month, the Central Distributor communicates with individual Manufacturers to retrieve data on the offered goods.
* Each Customer communicates with the Central Distributor to purchase the necessary goods. The Central Distributor can serve multiple customers simultaneously. Once all customers have purchased the goods or the available goods have been depleted, the Central Distributor informs the Manufacturers.

The goal of the described system is to enable the distribution of goods from manufacturers to customers. The system allows manufacturers to list their goods, collects information on the availability of those goods, and provides it to customers through the Distribution Center interface. Customers can choose which goods they want to buy and from which manufacturer, while the Distribution Center manages the entire process, including updating the database and notifying manufacturers about the quantity of goods sold.

### System scope:   
The system scope also includes parallel production of goods by manufacturers and the ability of the Distribution Center to serve multiple customers simultaneously. The system gathers information on the availability of goods from manufacturers and stores it in the Distribution Center. The system aims to effectively serve customers by selling them goods based on accurate information about the current stock status.

### Configuration
To run system simulation download project and run command in terminal `python run.py`

# Problems and adjustments:
- ~~What if customer adds products to cart or try to buy product and in the meantime they won't be available anymore?~~   
    ~~↳ Add removing not available products (all row even if only one of many is not available) and show popup to inform user about that~~
- ~~On dashboard items with 0 quantity shouldn't be displayed~~


- ~~Add verification from database when adding item to cart, watching cart add popup if some items are not available anymore~~
- ~~Add button to remove items from cart~~ 
- ~~Add tab with history of bought items~~ 
- ~~Map manufacturer from id to name~~ 
- ~~Add auto-refresh to dashboard template~~ 
- ~~Add validation that user is logged in and has credit card info~~ 
- ~~Add logic to call manufacturers to gain info from them~~ 
- ~~Add simulation of random network traffic for presentation (calls from users adding items to cart, buying them)~~ 

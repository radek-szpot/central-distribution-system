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


# TODO i problemy:
- ~~Zakładka na hisotrie zakupionych produktów + jakieś statusy~~
- ~~Mapping producenta z id na nazwe~~
- jak customer doda do koszyka towary i da kup to co jak ich nie bedzie:
    Dodać wyrzucenie towarów niedostępnych wszystkich z danej kategorii i wyświetlić komunikat powrót do koszyka
- ~~fajnie by bylo dodac jakas metode refresh'a do dashboard'a tak zeby widac bylo jak sie zmienia quantity~~
- Dodać call do manufacturerow i update produktow moduł `distribiutor.py`
- ~~jesli quantity towaru spada na 0 nie powinien byc displayowany~~
- ~~usuwanie z cart'a~~
- ~~dodać weryfikacje czy uztkownik jest zalogowany i czy ma podpieta karte do endpointow~~
- ~~Dodać unique na email + formatowanie karty kredytowej~~
- ~~Dodać ogranmiczenie na input itemow do koszyka max tyle co jest na display'u~~
- Dodać weryfikacje z bazy przy klikniecu add item (czy sa jeszcze itemy) i przy kliknieciu w cart rownież
- Dodać helpersy ktore beda tworzyc randomowy ruch uzytkownikow np call dodawania do koszyka call kupowania call usuwania
# Derash Food Delivery
A simplistic web application meant to connect food lovers, restaurant owners, and drivers in a single platform. This web app is mainly made of flask, with Jquery on the front-end

## Table of Content
* [Technologies](#technologies)
* [Installation](#installation)
* [Models](#models)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Technologies


## Installation
* Clone the repository: `git clone https://www.github.com/Zennoon/Derash.git`
* Install python dependencies that are listed in [requirements.txt](./requirements.txt)
* Install MySQL client and create a derash_db database, and a derash_user user
* In the root directory of the project, run `python3 -m derash_flask.app`

## Models
### BaseModel
A base class containing all the common attributes of the concrete classes. It is inherited by all the other classes.

### User
Another inherited class that includes all common attributes of the three user types (customer, driver, and owner).

### Customer
A concrete class representing a user that is able to make orders to a restaurant.

### Driver
A concrete class representing a user that delivers orders from restaurants to customers

### Owner
A concrete class representing a user that owns/manages restaurants

### Restaurant
A concrete class representing a restaurant that accepts orders from customers

### Dish
A concrete class representing a dish that a restaurant servers

### Order
A concrete class representing an order that is made by a customer, prepared by a restaurant, and delivered by a driver.

### Review
A concrete class representing a restaurant review that is made by a customer

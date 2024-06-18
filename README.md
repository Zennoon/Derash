# Derash Food Delivery
A simplistic web application meant to connect food lovers, restaurant owners, and drivers in a single platform. This web app is mainly made of flask, with Jquery on the front-end

## Table of Content
* [Technologies](#technologies)
* [Installation](#installation)
* [Models](#models)
* [Tests](#tests)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Technologies
<img src="tech_logos/python-logo.jpeg" width="100" height="100">

## Installation
* Clone the repository: `git clone https://www.github.com/Zennoon/Derash.git`
* Install python dependencies that are listed in [requirements.txt](./requirements.txt)
* Install MySQL client and create a derash_db database, and a derash_user user
* In the root directory of the project, run `python3 -m derash_flask.app`

## [Models](models)
### [BaseModel](models/base_model.py)
A base class containing all the common attributes of the concrete classes. It is inherited by all the other classes.
### [User](models/user.py)
Another inherited class that includes all common attributes of the three user types (customer, driver, and owner).
### [Customer](models/customer.py)
A concrete class representing a user that is able to make orders to a restaurant.
### [Driver](models/driver.py)
A concrete class representing a user that delivers orders from restaurants to customers
### [Owner](models/owner.py)
A concrete class representing a user that owns/manages restaurants
### [Restaurant](models/restaurant.py)
A concrete class representing a restaurant that accepts orders from customers
### [Dish](models/dish.py)
A concrete class representing a dish that a restaurant servers
### [Order](models/order.py)
A concrete class representing an order that is made by a customer, prepared by a restaurant, and delivered by a driver.
### [Review](models/review.py)
A concrete class representing a restaurant review that is made by a customer

## [Tests](tests)
The tests directory contains unittest tests for the application
### [test_models/](tests/test_models/)
Contains files which hold unittest test cases for the models
### [test_db_storage](tests/test_models/test_engine/test_db_storage.py)
Contains unittest test cases for the storage engine

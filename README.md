[![Build Status](https://travis-ci.org/mashafrancis/fast-food-fast-api.svg?)](https://travis-ci.org/mashafrancis/fast-food-fast-api)
[![Coverage Status](https://coveralls.io/repos/github/mashafrancis/fast-food-fast-api/badge.svg?branch=ft-jwt-security-160785403)](https://coveralls.io/github/mashafrancis/fast-food-fast-api?branch=ft-jwt-security-160785403)
[![Maintainability](https://api.codeclimate.com/v1/badges/011428b399554183244c/maintainability)](https://codeclimate.com/github/mashafrancis/fast-food-fast-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/011428b399554183244c/test_coverage)](https://codeclimate.com/github/mashafrancis/fast-food-fast-api/test_coverage)

# Fast-Food-Fast
Fast-Food-Fast is a food delivery service app for a restaurant.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.7
* Virtualenv

### Features
* Users can create accounts and sign in
* Users can view available food items
* Users can place an order for a specific food item
* Admin can view all orders
* Admin can view a specific food order
* Admin can update the order status
* Admin can add, edit and remove a new menu
* Admin can add, edit and remove a new meal

### Technologies Used
**Flask** For API implementation

**Pytest** For testing

### Installation
1. To clone this repo run ``https://github.com/mashafrancis/fast-food-fast-api/tree/master`` from your local terminal
2. `git checkout develop` to use the develop branch
3. Cd into the fast-food-fast Folder
4. Create a virtual environment `python3 -m venv venv`
5. Activate the virtual environment `source venv/bin/activate`
6. Install requirements `pip install -r requirements.txt` This should install all dependancies including flask
7. Create a `.env` file in the root folder
8. Copy the contents of `.env.sample` into `.env`
9. In the terminal run `source .env` to export the settings
10. Now Run the app `python run.py`

### Usage
The API implements a CRUD interface for the orders using GET, POST, PUT, PATCH and DELETE HTTP methods. The API has 
an auth route for registration and login.

### Available Endpoints
| Method             | Endpoint                                       | Functionality
|:------------------:|:----------------------------------------------:|:--------------------------------------:|
 POST                | /api/v2/auth/register                          | Register a new account
 POST                | /api/v2/auth/login                             | Login into application
 GET                 | /api/v2/orders                                 | Get a list of all available orders
 POST                | /api/v2/orders                                 | Create a new order
 DELETE              | /api/v2/orders                                 | Delete all orders
 GET                 | /api/v2/orders/<order_id>                      | Get order with specified order_id
 DELETE              | /api/v2/orders/<order_id>                      | Delete order with specified order_id
 PUT                 | /api/v2/orders/<order_id>                      | Update the status of a specific order
 POST                | /api/v2/menu                                   | Create a new menu category
 GET                 | /api/v2/menu                                   | Get all menu
 DELETE              | /api/v2/menu                                   | Delete all menu
 GET                 | /api/v2/menu/<menu_id>                         | Get menu with specified menu_id
 DELETE              | /api/v2/menu/<menu_id>                         | Delete menu with specified menu_id
 PUT                 | /api/v2/menu/<menu_id>                         | Update the details of a specific menu
 GET                 | /api/v2/menu/<menu_id>/meal                    | Get all meals under a specified menu
 DELETE              | /api/v2/menu/<menu_id>/meal                    | Delete all meals under a specified menu
 POST                | /api/v2/menu/<menu_id>/meal                    | Create a new meal under a specific menu
 GET                 | /api/v2/menu/<menu_id>/meal<meal_id>           | Get meal with specified meal_id
 DELETE              | /api/v2/menu/<menu_id>/meal<meal_id>           | Delete meal with specified meal_id
 PUT                 | /api/v2/menu/<menu_id>/meal<meal_id>           | Update the details of a specific meal
 

The endpoints can be tested using Postman
**Note** After login or signup, an access token is returned that needs to be passed in the header of all the other requests.

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

#### Users (For Authentication):
(1). POST /v2/auth/signup (All)
      
      
      "user_registration":
         {
            "username": "tester",
            "email": "test@gmail.com",
            "password": "mrjunk1",
            "confirm_password": "mrjunk1"
         }

(2). POST /v2/auth/login (All)


      "user_login":
         {
            "email": "test@gmail.com",
            "password": "mrjunk1"
         }

#### Users
(3). GET /v2/users - Get all users (Admin)

(4). GET /v2/users/{{user_id}} - Get a single user by user_id (Admin)

(5). POST /v2/users/orders - Post a single order (User)

(6). GET /v2/users/orders - Get all order history (User)

#### Orders: 
(7). GET /v2/orders - Get all orders (Admin)

(8). POST /v2/orders - Create a new order (All and non-registered)


      "order":
         {
            "name": "Burger",
            "quantity": 4,
            "price": 1000
         }
         
(9). DELETE /v2/orders - Delete all orders (Admin)

(10). GET /v2/orders/{{order_id}} - Get an order by order_id (Admin)

(11). PUT /v2/orders/{{order_id}} - Edit an existing order (Admin)

    "order":
       {
          "status": "Pending" or "Accepted" or "Declined"
       }
         
         
(13). DELETE /v2/orders/{{order_id}} - Delete an existing order by order_id

#### Menu
(14). GET /v2/menu - Get all menu (All)

(15). POST /v2/menu - Create a new menu (Admin)

      "menu_id 1":
         {
            "name": "Breakfast",
            "description": "Get your Breakfast!"
         }
         
(16). DELETE /v2/menu - Delete all menu categories (Admin)

(17). GET /v2/menu/{{menu_id}} - Get all menu category items by its menu_id (All)

(18). PUT /v2/menu/{{menu_id}} - Edit an existing menu category (Admin)

    "menu_id 2":
         {
            "name": "Breakfast-2",
            "description": "Get your Breakfast-2!"
         }
         
         
(19). DELETE /v2/menu/{{menu_id}} - Delete an existing menu by menu_id (Admin)

#### Meal
(20). GET /v2/menu/{{menu_id}}/meals - Get all meals offered (All)

(21). POST /v2/menu/{{menu_id}}/meals - Offer a new meal (Admin)

      "meal_id 1":
         {
            "name":"Junk",
            "description": "Get your junk!",
            "price": "100"
         }
         
(22). DELETE /v2/menu{{menu_id}}/meals - Delete all meals offered (Admin)

(23). GET /v2/menu/{{menu_id}}/meals/{{meal_id}} - Get a single meal offered (All)

(24). PUT /v2/menu/{{menu_id}}/meal/{{meal_id}} - Edit an existing meal (Admin)

    "meal_id 1":
         {
            "name":"Junk-1",
            "description": "Get your junk-1!",
            "price": "200"
         }
         
         
(25). DELETE /v2/menu/{{menu_id}}/meals/{{meal_id}} - Delete an existing meal by its meal_id (Admin)


 


## Version
Most recent version: Version 2

## Documentation Links

### Frontend Templates
[Github Pages](https://mashafrancis.github.io/fast-food-fast/)

### Run in Postman
[![Run in Postman](https://run.pstmn.io/button.svg)](postman://app/collections/import/1082100-037e53da-021e-4607-bcfe-082a7f3be688-RWgnWL3R?referrer=https%3A%2F%2Fdocumenter.getpostman.com%2Fview%2F1082100%2FRWgnWL3R#?)

View in browser [here](https://documenter.getpostman.com/view/1082100/RWgnWL3R)

## Author
* [Francis Masha](https://github.com/mashafrancis)

Agile-API
=========

Installation
------------

Clone the repository in your computer.
```sh
git clone git@github.com:pythondev0101/agile-api.git
```
Install the pipenv and requirements.
```sh
pip3 install pipenv
pipenv install -r requirements.txt
```
Create database(mysql)
```sh
mysql -u root -p
create database db_api;
```
Run the application.
```sh
flask run
```

Use username=admin and password=password for authentication

Add new terminal begin accessing the endpoints:
1. http:localhost:5000/api/v1.0/values
2. http:localhost:5000/api/v1.0/principles
3. http:localhost:5000/api/v1.0/values/{id}
4. http:localhost:5000/api/v1.0/principles/{id}
```sh
curl -u admin:password -i http://localhost:5000/api/v1.0/values
curl -u admin:password -i http://localhost:5000/api/v1.0/principles
curl -u admin:password -i http://localhost:5000/api/v1.0/values/1
curl -u admin:password -i http://localhost:5000/api/v1.0/principles/1
```

To create new values and principles:
```sh
curl -u admin:password -i -H "Content-Type: application/json" -X POST -d '{"data":"New value"}' http://localhost:5000/api/v1.0/values
curl -u admin:password -i -H "Content-Type: application/json" -X POST -d '{"data":"New principle"}' http://localhost:5000/api/v1.0/principles
```
Essentially on Windows you have to use double quotes to enclose the body of the request, and then inside it you escape a double quote by writing three of them in sequence.

To update values and principles:
```sh
curl -u admin:password -i -H "Content-Type: application/json" -X PUT -d '{"data":"Update value"}' http://localhost:5000/api/v1.0/values/1
curl -u admin:password -i -H "Content-Type: application/json" -X PUT -d '{"data":"Update principle"}' http://localhost:5000/api/v1.0/principles/1
```
To delete values and principles:
```sh
curl -u admin:password -i -H "Content-Type: application/json" -X DELETE -d http://localhost:5000/api/v1.0/values/1
curl -u admin:password -i -H "Content-Type: application/json" -X DELETE -d http://localhost:5000/api/v1.0/principles/1
```


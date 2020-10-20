# user_api_test
# Interview Test

This repository is an interview test solving, where I was challenged to create API restful using Python e its frameworks.
It is expected to build an API to manipulate registers of USERS.
It was developed using:
- Language: Python 3.8
- Framework: Flask
- Database: MongoDB

## Prerequisites
To run this project it will run in a Docker Container, therefore is necessary to install:
Docker

## Starting MongoDB 
We are using MongoDB as the database for this project. To start it, first, you have to pull the MongoDB image from the Docker repository:
```
$ docker run --name mongo-latest -p 27017:27017 -d mongo
```
That command will download a mongo image if it not exists, and create a mongo container called mongo-latest, mapping your localhost's port 27017 to 27017 container's port and run it as a daemon.

## Prepare to execution
Once you have cloned this repository, first you have to build a docker image of the application:
From the root application dir, execute:
```
$ sudo docker build -t api_users:latest .
```

Next, you have to start the container by the command bellow:
```
$ sudo docker run -itd --rm --name flask_api_users_latest -p 5001:5000  -e SECRET_KEY=hard-secret-key --link mongo-latest:dbserver -e MONGODB_URI=mongodb://dbserver:27017/api-users api_users:latest
```

The application will be ready, waiting for requests in the container, in background on the address:
```
localhost:5000
```


### Methods available
The followings methods are available:
#### Users
##### POST
Create a new user:
HTTP Method: POST
Path: /users

User data:
```
    full_name
    user_name
    date_of_born (format: YYYY/MM/DD
    email
    address
    phone
    password    
    admin (use this field equals true to create a user admin)
    created_at
```

Address data:
```
    zip_code
    street
    number
    complement
    neighborhood
    city
    state
    country
```

Sample:
```
$ 
curl --header "Content-Type: application/json" \
-d '{ 
    "full_name":"Luiz Silva", 
    "user_name":"luizinho", 
    "email":"luiz@teste.com", 
    "password":"123456", 
    "confirm_password":"123456", 
    "address": {"street":"Rua onde moro"}}' \
localhost:5000/users
```

To access the following methods you have to get a authorization from JWT sending the user_name and password registered:

HTTP Method: POST
Path: /auth
Data:
```
    user_name
    password
```

Sample:
```
$ curl --header "Content-Type: application/json" -d '{"user_name": "luizinho", "password": "123456"}' localhost:5000/auth
```
Copy the token that will be return. Lets call this token: $TOKEN, to simplify this document

##### GET
###### List all clients
If the user were a admin, he can see a list of all users registered:
HTTP Method: GET
Path: /admin/users
Params: 
```
    page
    page_size
```

Sample:
```
curl localhost:5000/admin/users -H "Authorization Bearer $TOKEN
```

Paginate Sample:
```
curl "localhost:5000/admin/users?page=2&page_size=2" Authorization Bearer $TOKEN 
```

###### Get a specific user by ID
You can see only your own data:

HTTP Method: GET
Path: /users/{user_name}

Sample:
```
$ curl localhost:5000/users/luizinho -H "Authorization Bearer $TOKEN"
```

##### DELETE
You can only delete your own data

HTTP Method: DELETE
Path: /users/{user_name}

Sample:
```
$ curl -X DELETE -i localhost:5000/users/luizinho -H "Authorization Bearer $TOKEN"
```

##### UPDATE
You can only update your own data

HTTP method: PUT
Path: localhost:5000/{user_name}
Data:
```
    full_name
    user_name
    email
    admin
    address (all address sub fields)
``` 

Sample:
```
curl --header "Content-Type: application/json" -d \
'{ \
    "full_name":"Luiz Silva JR", 
    "user_name":"luizinho", \
    "email":"luizao@teste.com", \
    "password":"123456", \
    "address": {"street":"Rua onde moro"} \
}' \
localhost:5000/users -H "Authorization Bearer $TOKEN"
```

##### CHANGE PASSWORD
To change the user password:

HTTP Method: PUT
Path: /users/password
Data:
```
    current_password
    new_password:
    confirm_password
```

Sample:
```
$ curl -X PUT --header "Content-Type: application/json" \
-d '{ \
    "current_password": "123457", \
    "new_password": "novasenha", \
    "confirm_password": "outrasenha" \
} \
localhost:5000/users/password
```
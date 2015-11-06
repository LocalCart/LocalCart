curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "password" : "125", "user_type": "customer", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Nguyen", "password" : "125", "user_type": "customer", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Triangle", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Carl", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Lucy", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "name":"Bob", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "name":"Bob", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Lucy", "name":"Magical Shop of Wonders", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

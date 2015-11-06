curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "password" : "125", "user_type": "customer", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Nguyen", "password" : "125", "user_type": "customer", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Triangle", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Carl", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Lucy", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

#curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "name":"Bob", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

#curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "name":"Bob", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

#curl -X POST -H "Content-Type: application/json" --data '{"username": "Lucy", "name":"Magical Shop of Wonders", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

curl -X POST -H "Content-Type: application/json" --data '{"storeID": 3}' https://fierce-island-3989.herokuapp.com/api/inventory/create

curl -X POST -H "Content-Type: application/json" --data '{"storeID": 4}' https://fierce-island-3989.herokuapp.com/api/inventory/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Vanilla Ice Cream", "description" : "Deliciously creamy", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Hot Pants", "description" : "Everyone will love you when you go outside with these pants on", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Deodorant", "description" : "You know you need it", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Basketball", "description" : "Why not", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Chocolate", "description" : "Who dislikes chocolate?", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Razor", "description" : "Smooth appendages seems to be in", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Hot Pink Sunglasses", "description" : "This just speaks center of attention", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Soccer Ball", "description" : "Makes you run a lot", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "password" : "125", "user_type": "customer", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Nguyen", "password" : "125", "user_type": "customer", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Triangle", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Carl", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Lucy", "password" : "125", "user_type": "merchant", "email": "a@abc.com"}' https://fierce-island-3989.herokuapp.com/api/user/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Bob", "name":"Bob", "address":"2605 Channing\n\nBerkeley\nCA\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

curl -X POST -H "Content-Type: application/json" --data '{"username": "Lucy", "name":"Magical Shop of Wonders", "address":"1234 Rainbow Road\n\nFrustration\nToTheMax\n94704", "phone_number":"1-234-567-4422" }' https://fierce-island-3989.herokuapp.com/api/store/create

# curl -X POST -H "Content-Type: application/json" --data '{"storeID": 1}' https://fierce-island-3989.herokuapp.com/api/inventory/create

# curl -X POST -H "Content-Type: application/json" --data '{"storeID": 2}' https://fierce-island-3989.herokuapp.com/api/inventory/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Vanilla Ice Cream", "description" : "Deliciously creamy", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Hot Pants", "description" : "Everyone will love you when you go outside with these pants on", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Deodorant", "description" : "You know you need it", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Basketball", "description" : "Why not", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Chocolate", "description" : "Who dislikes chocolate?", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Razor", "description" : "Smooth appendages seems to be in", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Hot Pink Sunglasses", "description" : "This just speaks center of attention", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Soccer Ball", "description" : "Makes you run a lot", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Red Pen", "description" : "To tell people they suck", "price" : 10000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Blue Pen", "description" : "Cuz you want to be different", "price" : 10000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Black Pen", "description" : "Who has time for this", "price" : 10000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Pencil", "description" : "Too afraid of making mistakes", "price" : 100000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Watch", "description" : "For those who do not have phones", "price" : 1234}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Computer", "description" : "Everyone needs this", "price" : 10000000000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Axe", "description" : "Time to feel young again", "price" : 0.01}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Baseball", "description" : "Cuz sports", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Toothbrush", "description" : "Dental is important", "price" : 11}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Toothpaste", "description" : "Whiten your teeth", "price" : 111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Toothbrush and toothpaste set", "description" : "In case you need it on the go", "price" : 1111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Toilet Paper", "description" : "1 ply", "price" : 1111111111111111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Towel", "description" : "Wash yourself", "price" : 111111111111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Sleeping Bag", "description" : "For subzero temperature but who actually goes outside", "price" : 1111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Chicken", "description" : "Yes, a live chicken", "price" : 1}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Dog", "description" : "Your next best friend", "price" : 111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Cat", "description" : "Softer than dogs", "price" : 10000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Water", "description" : "RARE COMMODITY", "price" : 10000000000001111111111111}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "Lined Paper", "description" : "For those who go to school", "price" : 10000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 1, "name" : "White Paper", "description" : "Printer paper", "price" : 100000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Mandarins", "description" : "Cuties", "price" : 1234}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Sleep", "description" : "Everyone needs this", "price" : 10000000000}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Chair", "description" : "Blue", "price" : 15}' https://fierce-island-3989.herokuapp.com/api/item/create

curl -X POST -H "Content-Type: application/json" --data '{"inventoryID": 2, "name" : "Desk", "description" : "Standing", "price" : 70}' https://fierce-island-3989.herokuapp.com/api/item/create

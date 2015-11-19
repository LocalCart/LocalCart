var app = angular.module('LocalCart', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('IndexController', function($http, $window){
  var vm = this;
  vm.User = {};
  vm.searchQuery = "";
  vm.query = "";



  // add link get request
  vm.searchResults = results;
  vm.shoppingList = inventory;
  
  vm.current_user = "";
  $http.get("api/user/get").then(
       function successCallBack(response) {
         var data = response.data;
         if (data.errors.length == 0) {
           // if (vm.newUser.user_type == 'merchant'){
           //   $window.location.href = 'merchant';
           // } else {
           //   $window.location.href = 'home';
           // }
           // hide login, register buttons
           vm.current_user = data.username;
           console.log(data.username);
           if (data.user_type == "merchant") {
            $window.location.href("merchant");
           }
         } else {
           // for (var i = 0; i < data.errors.length; i++) {
             // alert(e);
             // $window.alert(data.errors[i]);
             // console.error(e);
           // }
         }
       }, function errorCallBack(response) {
         alert('An error has occured');
       })

  vm.search = function() {
    vm.query = vm.searchQuery;
  }
  vm.remove = function(index) {
    vm.shoppingList.splice(index, 1);
    // var editData = {};
    // editData.listID = 120391023901284091823904130948;//CURRENT LIST ID
    // editData.contents = vm.shoppingList; // REPLACE WITH CURRENT SHOPPING LIST
    // $http.post("api/list/edit", editData).then(successListError, errorCallBackGeneral);
  }
  vm.addItem = function(index) {
    vm.shoppingList.push(vm.searchResults[index]);
    // var editData = {};
    // editData.listID = 120391023901284091823904130948;//CURRENT LIST ID
    // editData.contents = vm.shoppingList; // REPLACE WITH CURRENT SHOPPING LIST
    // $http.post("api/list/edit", editData).then(successListError, errorCallBackGeneral);
  }
  vm.loginAttempt = function() {
    $http.post("/api/user/login", vm.User).then(
       function successCallBack(response) {
         var data = response.data;
         if (data.errors.length == 0) {
           if (data.user_type == 'merchant'){
             $window.location.href = 'merchant';
           } else {
             $window.location.href = 'home';
           }
         } else {
           for (var i = 0; i < data.errors.length; i++) {
             // alert(e);
             $window.alert(data.errors[i]);
             // console.error(e);
           }
         }
       }, errorCallBackGeneral)
    // $http.post("api/user/login", vm.User);
    // console.log("yolo");
  }
  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.href = "home";
  }
  // vm.addItem = function(itemToAdd) {
  //   var item = {};
  //   item.inventory = "1"
  //   item.name = itemToAdd
  //   item.description = "anything"
  //   item.price = "1.00"
  //   item.picture = "add picture text"
  //   $http.post("api/item/create", item);
  // }

});

app.controller('MerchantController', function() {
  var vm = this;
  vm.editable = false;
  vm.editInfo = function() {
    vm.editable = !vm.editable
  }
  vm.storeInfo = {};
  vm.storeInfo.storeName = "";
  vm.tempStoreInfo = angular.copy(vm.storeInfo);
  vm.saveInfo = function() {
    vm.storeInfo = angular.copy(vm.tempStoreInfo);
    vm.editInfo();
  }
  vm.cancel = function() {
    vm.tempStoreInfo = angular.copy(vm.storeInfo);
    vm.editInfo();
  }
});


app.controller('RegisterController', function($http, $window) {
  var vm = this;
  vm.newUser = {}
  vm.newUser.username = "";
  vm.newUser.user_type = "";

  vm.createUser = function() {
    if (vm.newUser.password == vm.confirmPassword) {
      $http.post("/api/user/create", vm.newUser).then(
       function successCallBack(response) {
         var data = response.data;
         if (data.errors.length == 0) {

           if (vm.newUser.user_type == 'merchant'){
             $window.location.href = 'merchant';
           } else {
             $window.location.href = 'home';
           }
         } else {
           for (var i = 0; i < data.errors.length; i++) {
             // alert(e);
             $window.alert(data.errors[i]);
             // console.error(e);
           }
         }
       }, errorCallBackGeneral)
    } else {
      // testing
      // console.log("incorrect");
      // console.log(vm.newUser.user_type);
      alert('Passwords must match')
    }
  }
});


app.controller('LoginController', function($http, $window) {
  var vm = this;
  // vm.isCustomer = true;


  vm.doGreeting = function(greeting) {
    // if get requset
    $window.alert(greeting);
  };
});

app.controller('InventoryController', function($http) {
  var vm = this;
  vm.inventory = inventory;
  vm.tempItem = {}
  vm.remove = function(index) {
    console.log("wtf");
    vm.inventory.splice(index, 1);
  }
  count = 4
  vm.addItem = function() {
    vm.tempItem.itemID = count;
    count += 1;
    vm.inventory.push(vm.tempItem);
    vm.tempItem = {}
  }
});

var results = [
{ storeName: "GameStop", name: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "Target", name: "Shampoo",  description: "New shampoo for dry hair", price: "5.00"},
{ storeName: "Costco", name: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
{ storeName: "GameStop", name: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "Target", name: "Shampoo",  description: "New shampoo for dry hair", price: "5.00"},
{ storeName: "Costco", name: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
{ storeName: "GameStop", name: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "Target", name: "Shampoo",  description: "New shampoo for dry hair", price: "5.00"},
{ storeName: "Costco", name: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
  ];  

var inventory = [
{ storeName: "GameStop", itemID: "1", name: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "GameStop", itemID: "2", name: "Shampoo",  description: "New shampoo for dry hair", price: "5.50"},
{ storeName: "GameStop", itemID: "3", name: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
  ];  

successListError = function(response) {
  var data = response.data;
  if (data.errors.length > 0) {
    for (var i = 0; i < data.errors.length; i++) {
      // alert(e);
      $window.alert(data.errors[i]);
      // console.error(e);
    }
  }
};
errorCallBackGeneral = function(response) {
  alert('An error has occured');
};
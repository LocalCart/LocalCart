var app = angular.module('LocalCart', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('IndexController', function($http){
  var vm = this;
  vm.searchResults = results
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
  vm.storeInfo.storeName = "test store";
});

app.controller('RegisterController', function($http) {
  var vm = this;
  vm.newUser = {}
  vm.newUser.username = "testaccount";
  vm.user_type = "customer"
  vm.createUser = function() {
    if (vm.newUser.password == vm.confirmPassword) {
      $http.post("/api/user/create", vm.newUser);
    } else {
      console.log("incorrect");
    }
  }
});


var results = [
{ storeName: "GameStop", item: "Halo 5",  description: "A first person shooter video game", price: 80.00},
{ storeName: "Target", item: "Shampoo",  description: "New shampoo for dry hair", price: 5.00},
{ storeName: "Costco", item: "Deodorant",  description: "Use this to tackle body odor!", price: 7.00},
{ storeName: "GameStop", item: "Halo 5",  description: "A first person shooter video game", price: 80.00},
{ storeName: "Target", item: "Shampoo",  description: "New shampoo for dry hair", price: 5.00},
{ storeName: "Costco", item: "Deodorant",  description: "Use this to tackle body odor!", price: 7.00},
{ storeName: "GameStop", item: "Halo 5",  description: "A first person shooter video game", price: 80.00},
{ storeName: "Target", item: "Shampoo",  description: "New shampoo for dry hair", price: 5.00},
{ storeName: "Costco", item: "Deodorant",  description: "Use this to tackle body odor!", price: 7.00},
  ];  


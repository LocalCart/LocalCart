var app = angular.module('LocalCart', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('IndexController', function($http){
  var vm = this;
  vm.searchResults = results;
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


app.controller('RegisterController', function($http) {
  var vm = this;
  vm.newUser = {}
  vm.newUser.username = "testaccount";
  vm.newUser.user_type = "";
  vm.createUser = function() {
    if (vm.newUser.password == vm.confirmPassword) {
      $http.post("/api/user/create", vm.newUser);
      console.log(vm.newUser.user_type);
    } else {
      console.log("incorrect");
      console.log(vm.newUser.user_type);
    }
  }
});


app.controller('LoginController', function($http) {
  var vm = this;
  vm.isCustomer = true;
  vm.User = {}
  vm.user_type = ""
  vm.User.username = "testaccount";
});

app.controller('InventoryController', function($http) {
  var vm = this;
  vm.inventory = inventory;
  vm.tempItem = {}
  vm.remove = function(itemID) {
    console.log(vm.inventory.length);
    for (var i =0; i < vm.inventory.length; i++) {
      console.log(vm.inventory[i]);
      if (vm.inventory[i].itemID == itemID) {
        console.log("wtf");
        vm.inventory.splice(i, 1);
      }
    }
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
{ storeName: "GameStop", item: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "Target", item: "Shampoo",  description: "New shampoo for dry hair", price: "5.00"},
{ storeName: "Costco", item: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
{ storeName: "GameStop", item: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "Target", item: "Shampoo",  description: "New shampoo for dry hair", price: "5.00"},
{ storeName: "Costco", item: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
{ storeName: "GameStop", item: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ storeName: "Target", item: "Shampoo",  description: "New shampoo for dry hair", price: "5.00"},
{ storeName: "Costco", item: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
  ];  

var inventory = [
{ itemID: "1", name: "Halo 5",  description: "A first person shooter video game", price: "80.00"},
{ itemID: "2", name: "Shampoo",  description: "New shampoo for dry hair", price: "5.50"},
{ itemID: "3", name: "Deodorant",  description: "Use this to tackle body odor!", price: "7.00"},
  ];  


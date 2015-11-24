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
  vm.searchResults = [];
  vm.shoppingList = [];
  vm.listIndex = 0;
  vm.listIDs = [];
  vm.currentListID = -1;
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
      }, errorCallBackGeneral);
  if (current_user != "") {
    $http.get("api/list/getID").then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            vm.listIDs = data.listIDs;
            vm.listIndex = 0;
            vm.currentListID = vm.listIDs[vm.listIndex];
            $http.get("api/list/get?listID=" + vm.currentListID).then(
              function successCallBack(response) {
                var data = response.data;
                if (data.errors.length == 0) {
                  vm.shoppinglist = data.list;
                }
              }, errorCallBackGeneral);
          } else {
            vm.currentListID = -1;
          }
        }, errorCallBackGeneral);
  }

  vm.search = function() {
    vm.query = vm.searchQuery;
  }
  vm.remove = function(index) {
    vm.shoppingList.splice(index, 1);
    if (current_user != "") {
      vm.updateList();
    }
  }
  vm.addItem = function(index) {
    vm.searchResults[index].type = "id"
    vm.shoppingList.push(vm.searchResults[index]);
    if (current_user != "") {
      vm.updateList();
    }
  }
  vm.updateList = function() {
    if (current_user != "") {
      var contents = [];

      for (var i = 0; i < vm.shoppingList.length; i++) {
        var entry = {};
        var item = vm.shoppinglist[i];
        if (item.type == "name") {
          entry.type = "name";
          entry.name = item.name;
        } else {
          entry.type = "id";
          entry.name = item.itemID;
        }
      }
      var editData = {};
      editData.listID = vm.currentListID;//CURRENT LIST ID
      editData.contents = vm.contents;
      $http.post("api/list/edit", editData).then(successListError, errorCallBackGeneral);
    }
  }
  vm.mapList = function() {
    var listData = {};
    listData.listID = vm.currentListID;//CURRENT LIST ID
    $http.post("api/list/map", listData).then(successListError, errorCallBackGeneral).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            var mapMarkers = response.data.mapMarkers;
            var bounds = google.maps.LatLngBounds();
            var infowindow = new google.maps.InfoWindow();
            var map = new google.maps.Map(document.getElementById('list_map'), {
              zoom: 4,
              center: new google.maps.LatLng(mapMarkers[0].latitude, mapMarkers[0].longitude),
              mapTypeId: google.maps.MapTypeId.ROADMAP
            });
 
            for (var i = 0; i < mapMarkers.length; i++) {
              var marker = new google.maps.Marker({
                position: new google.maps.LatLng(mapMarkers[i].latitude, mapMarkers[i].longitude),
                map: map
              });
              bounds.extend(marker.position);
              google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                  infowindow.setContent(locations[i].pin_name);
                  infowindow.open(map, marker);
                }
              })(marker, i));
            }
            map.fitBounds(bounds);
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              alert(e);
              $window.alert(data.errors[i]);
              console.error(e);
            }
          }
        }, errorCallBackGeneral)
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
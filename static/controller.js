var app = angular.module('LocalCart', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('IndexController', function($http, $window) {
  var vm = this;
  vm.User = {};
  vm.searchQuery = "";
  vm.query = "";
  // add link get request
  // vm.searchResults = [];
  vm.tab = 0; // ListIDs index
  vm.listIDs = [];
  vm.currentListID = -1;
  vm.searchResults = results;
  vm.shoppingLists = shoppingLists;
  vm.newItemName = "";
  vm.current_user = "";
  vm.current_user_type = "";
  vm.mapped = "list" // search or list
  $http.get("api/user/get").then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          // if (data.user_type == 'merchant'){
          //   $window.location.href = 'merchant';
          // }
          // hide login, register buttons
          vm.current_user = data.username;
          vm.current_user_type = data.user_type;
          console.log(data.username);
          // if (data.user_type == "merchant") {
          //  $window.location.href = "merchant";
          // }
          $http.get("api/list/getUser").then(
              function successCallBack(response) {
                var data = response.data;
                if (data.errors.length == 0) {
                  vm.listIDs = data.listIDs;
                  vm.tab = 0;
                  vm.currentListID = vm.listIDs[vm.tab];
                  vm.shoppingLists = data.allLists;
                } else {
                  vm.currentListID = -1;
                }
              }, errorCallBackGeneral);
        } else {
          // for (var i = 0; i < data.errors.length; i++) {
            // alert(e);
            // $window.alert(data.errors[i]);
            // console.error(e);
          // }
        }
      }, errorCallBackGeneral);


  vm.search = function() {
    vm.query = vm.searchQuery;
  }

  vm.remove = function(index) {
    vm.shoppingLists[vm.tab].contents.splice(index, 1);
    if (vm.current_user != "") {
      vm.updateList();
    }
  }

  vm.addItem = function(index) {
    vm.searchResults[index].type = "id"
    vm.shoppingLists[vm.tab].contents.push(vm.searchResults[index]);
    if (vm.current_user != "") {
      vm.updateList();
    }
    if (vm.mapped == "list") {
      vm.mapList()
    }
  }

  vm.addTextItem = function() {
    var addText = {};
    addText.type = "name";
    addText.name = vm.newItemName;
    vm.shoppingLists[vm.tab].contents.push(addText);
    if (vm.current_user != "") {
      vm.updateList();
    }
    vm.newItemName = "";
  }

  vm.updateList = function() {
    if (vm.current_user != "") {
      var contents = [];

      for (var i = 0; i < vm.shoppingLists[vm.tab].contents.length; i++) {
        var entry = {};
        var item = vm.shoppingLists[vm.tab].contents[i];
        if (item.type == "name") {
          entry.type = "name";
          entry.name = item.name;
        } else {
          entry.type = "id";
          entry.name = item.itemID;
        }
        contents.push(entry)
      }
      var editData = {};
      editData.listID = vm.currentListID; //CURRENT LIST ID
      editData.contents = contents;
      $http.post("api/list/edit", editData).then(successListError, errorCallBackGeneral);
    }
  }
  vm.mapList = function() {
    vm.mapped = "list"
    var listData = {};
    listData.listID = vm.currentListID; //CURRENT LIST ID
    $http.post("api/list/map", listData).then(successListError, errorCallBackGeneral).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          var mapMarkers = response.data.mapMarkers;
          var bounds = google.maps.LatLngBounds();
          var infowindow = new google.maps.InfoWindow();
          vm.map = new google.maps.Map(document.getElementById('list_map'), {
            zoom: 4,
            center: new google.maps.LatLng(mapMarkers[0].latitude, mapMarkers[0].longitude),
            mapTypeId: google.maps.MapTypeId.ROADMAP
          });

          for (var i = 0; i < mapMarkers.length; i++) {
            var marker = new google.maps.Marker({
              position: new google.maps.LatLng(mapMarkers[i].latitude, mapMarkers[i].longitude),
              map: vm.map
            });
            bounds.extend(marker.position);
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
              return function() {
                infowindow.setContent(locations[i].pin_name);
                infowindow.open(vm.map, marker);
              }
            })(marker, i));
          }
          vm.map.fitBounds(bounds);
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
            if (data.user_type == 'merchant') {
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

  vm.tab = 0;

  vm.isSet = function(checkTab) {
    return vm.tab === checkTab;
  };

  vm.setTab = function(setTab) {
    vm.tab = setTab;
    vm.currentListID = vm.listIDs[vm.tab];
  };
  // vm.addItem = function(itemToAdd) {
  //   var item = {};
  //   item.inventory = "1"
  //   item.name = itemToAdd
  //   item.description = "anything"
  //   item.price = "1.00"
  //   item.picture = "add picture text"
  //   $http.post("api/item/create", item);
  // }
  vm.addList = function() {
    var listData = {};
    listData.name = vm.newListName;
    if (vm.newListName != "") {
      $http.post("api/list/create", listData).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            vm.listIDs.push(data.listID);
            vm.shoppingLists.push({listName: vm.newListName, contents: []});
            vm.newListName = "";
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              // alert(e);
              $window.alert(data.errors[i]);
              // console.error(e);
            }
          }
          
        }, errorCallBackGeneral);
    }

  }


  vm.removeList = function() {
    var listData = {};
    listData.listID = vm.currentListID;
    vm.listIDs.splice(vm.tab, 1);
    vm.shoppingLists.splice(vm.tab, 1);
    $http.post("api/list/deleteid", listData);
    if (vm.listIDs.length == 0) {
      vm.addList();
    }
    vm.tab = 0;
    vm.currentListID = vm.listIDs[vm.tab];
  }

});

app.controller('MerchantController', function($http, $window) {
  var vm = this;
  vm.editable = false;
  vm.noStore = false;
  vm.editInfo = function() {
    vm.editable = !vm.editable;
  }
  vm.storeInfo = {};
  vm.tempStoreInfo = angular.copy(vm.storeInfo);
  vm.saveInfo = function() {
    vm.storeInfo = angular.copy(vm.tempStoreInfo);
    vm.editStore();
  }
  vm.cancel = function() {
    vm.tempStoreInfo = angular.copy(vm.storeInfo);
    vm.editInfo();
  }
  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.href = "home";
  }
  vm.createStore = function() {
    // vm.saveInfo()
    vm.requestInfo = angular.copy(vm.tempStoreInfo)
    vm.requestInfo.address = vm.tempStoreInfo.address_street + '\n\n' + vm.tempStoreInfo.address_city + '\n' + vm.tempStoreInfo.address_state + '\n' + vm.tempStoreInfo.address_zip;
    $http.post("/api/store/create", vm.requestInfo).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.getUserStore()
          vm.storeInfo = angular.copy(vm.tempStoreInfo);
          vm.editable = !vm.editable;
          vm.noStore = false;
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            // alert(e);
            $window.alert(data.errors[i]);
            // console.error(e);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.editStore = function() {
    console.log(vm.storeInfo)
    $http.post("/api/store/edit", vm.storeInfo).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.editInfo();

          // if (vm.newUser.user_type == 'merchant') {
          //   $window.location.href = 'merchant';
          // } else {
          //   $window.location.href = 'home';
          // }
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            // alert(e);
            $window.alert(data.errors[i]);
            // console.error(e);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.current_user = "";
  $http.get("api/user/get").then(
    function successCallBack(response) {
      var data = response.data;
      if (data.errors.length == 0) {
        vm.current_user = data.username;
        console.log(data.username);
      } else {
        $window.location.href = "home";
      }
    },
    function errorCallBack(response) {
      alert('An error has occured');
    }
  )
  vm.getUserStore = function() {
    $http.get("api/store/getUser").then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.storeInfo = data.store;
          vm.tempStoreInfo = angular.copy(vm.storeInfo);
          console.log(data)
          if (vm.storeInfo.storeID == -1) {
            vm.editable = true
            vm.noStore = true
          }
        }
      },
      function errorCallBack(response) {
        alert('An error has occured');
      }
    )
  }
  vm.getUserStore()
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
            $window.location.href = 'home';
            // if (vm.newUser.user_type == 'merchant') {
            //   $window.location.href = 'merchant';
            // } else {
            //   $window.location.href = 'home';
            // }
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
  vm.User = {};
  vm.loginAttempt = function() {
    $http.post("/api/user/login", vm.User).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            if (data.user_type == 'merchant') {
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
        // if (data.user_type == "merchant") {
        //  $window.location.href = "merchant";
        // }
      } else {
        // for (var i = 0; i < data.errors.length; i++) {
        // alert(e);
        // $window.alert(data.errors[i]);
        // console.error(e);
        // }
      }
    },
    function errorCallBack(response) {
      alert('An error has occured');
    }
  )
});

app.controller('InventoryController', function($http) {
  var vm = this;
  vm.inventory = [];
  vm.inventoryID = -1;
  vm.tempItem = {}
  vm.count = 0
  vm.current_user = "";
  $http.get("api/user/get").then(
    function successCallBack(response) {
      var data = response.data;
      if (data.errors.length == 0) {
        vm.current_user = data.username;
        console.log(data.username);
        $http.get("api/inventory/getUser").then(
            function successCallBack2(response) {
              var data2 = response.data;
              if (data2.errors.length == 0) {
                vm.inventory = data2.contents;
                vm.count = vm.inventory.length;
                vm.inventoryID = data2.inventoryID;
                vm.tempItem.inventoryID = vm.inventoryID;
              }
            }, errorCallBackGeneral)
      } else {
        $window.location.href = "home";
      }
    }, errorCallBackGeneral)
  vm.remove = function(index) {
    var removedID = {};
    removedID.itemID = vm.inventory[index].itemID;
    $http.post("api/item/delete", removedID).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.inventory.splice(index, 1);
          for (var i = index; i < vm.inventory.length; i++) {
            vm.inventory[index].index -= 1;
          }
          count -= 1;
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            $window.alert(data.errors[i]);
            console.error(e);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.addItem = function() {
    vm.tempItem.inventoryID = vm.inventoryID;
    $http.post("api/item/create", vm.tempItem).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.tempItem.itemID = data.itemID;
          vm.count += 1;
          vm.tempItem.index = vm.count;
          vm.inventory.push(vm.tempItem);
          vm.tempItem = {}
          vm.tempItem.inventoryID = vm.inventoryID;
        } else {
          for (var i = 0; i < data.errors.length; i++) {
          $window.alert(data.errors[i]);
          console.error(e);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.href = "home";
  }

});

var results = [{
  storeName: "GameStop",
  name: "Halo 5",
  description: "A first person shooter video game",
  price: "80.00"
}, {
  storeName: "Target",
  name: "Shampoo",
  description: "New shampoo for dry hair",
  price: "5.00"
}, {
  storeName: "Costco",
  name: "Deodorant",
  description: "Use this to tackle body odor!",
  price: "7.00"
}, {
  storeName: "GameStop",
  name: "Halo 5",
  description: "A first person shooter video game",
  price: "80.00"
}, {
  storeName: "Target",
  name: "Shampoo",
  description: "New shampoo for dry hair",
  price: "5.00"
}, {
  storeName: "Costco",
  name: "Deodorant",
  description: "Use this to tackle body odor!",
  price: "7.00"
}, {
  storeName: "GameStop",
  name: "Halo 5",
  description: "A first person shooter video game",
  price: "80.00"
}, {
  storeName: "Target",
  name: "Shampoo",
  description: "New shampoo for dry hair",
  price: "5.00"
}, {
  storeName: "Costco",
  name: "Deodorant",
  description: "Use this to tackle body odor!",
  price: "7.00"
}, ];

var inventory = [{
  storeName: "GameStop1",
  index: "1",
  name: "Halo 5",
  description: "A first person shooter video game",
  price: "80.00"
}, {
  storeName: "GameStop1",
  index: "2",
  name: "Shampoo",
  description: "New shampoo for dry hair",
  price: "5.50"
}, {
  storeName: "GameStop1",
  index: "3",
  name: "Deodorant",
  description: "Use this to tackle body odor!",
  price: "7.00"
}]

var shoppingLists = [{
  listName: 'listName0',
  contents: [{
    storeName: "GameStop1",
    itemID: "1",
    name: "Halo 5",
    description: "A first person shooter video game",
    price: "80.00"
  }, {
    storeName: "GameStop1",
    itemID: "2",
    name: "Shampoo",
    description: "New shampoo for dry hair",
    price: "5.50"
  }, {
    storeName: "GameStop1",
    itemID: "3",
    name: "Deodorant",
    description: "Use this to tackle body odor!",
    price: "7.00"
  }]
}, {
  listName: 'listName1',
  contents: [{
    storeName: "GameStop2",
    itemID: "1",
    name: "Halo 5",
    description: "A first person shooter video game",
    price: "80.00"
  }, {
    storeName: "GameStop2",
    itemID: "2",
    name: "Shampoo",
    description: "New shampoo for dry hair",
    price: "5.50"
  }]
}];

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

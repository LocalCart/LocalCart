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
  vm.shoppingList = [];
  vm.tab = 0; // ListIDs index
  vm.listIDs = [];
  vm.currentListID = -1;
  vm.searchResults = results;
  vm.shoppingLists = shoppingLists;
  vm.current_user = "";
  vm.mapped = "list" // search or list
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
      }, errorCallBackGeneral);
  if (vm.current_user != "") {
    $http.get("api/list/getID").then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            vm.listIDs = data.listIDs;
            vm.tab = 0;
            vm.currentListID = vm.listIDs[vm.tab];
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
    if (vm.current_user != "") {
      vm.updateList();
    }
  }
  vm.addItem = function(index) {
    vm.searchResults[index].type = "id"
    vm.shoppingList.push(vm.searchResults[index]);
    if (vm.current_user != "") {
      vm.updateList();
    }
    if (vm.mapped == "list") {
      vm.mapList()
    }
  }
  vm.updateList = function() {
    if (vm.current_user != "") {
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
          }
        }, errorCallBackGeneral);
      vm.shoppingLists.push({});
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
  vm.editInfo = function() {
    vm.editable = !vm.editable
  }
  vm.storeInfo = {};
  vm.storeInfo.storeName = "";
  vm.tempStoreInfo = angular.copy(vm.storeInfo);
  vm.saveInfo = function() {
    vm.storeInfo = angular.copy(vm.tempStoreInfo);
    vm.editInfo();
    vm.editUser()
  }
  vm.cancel = function() {
    vm.tempStoreInfo = angular.copy(vm.storeInfo);
    vm.editInfo();
  }
  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.href = "home";
  }
  vm.editStore = function() {
    $http.post("/api/store/edit", vm.storeInfo).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {

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

            if (vm.newUser.user_type == 'merchant') {
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
        $window.location.href = "home";
      }
    },
    function errorCallBack(response) {
      alert('An error has occured');
    }
  )
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

var shoppingLists = [
  {listName: 'listName0', contents: [{
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
  }]},
  {listName: 'listName1', contents: [{
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
  }]}
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

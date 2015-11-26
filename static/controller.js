var app = angular.module('LocalCart', []);
var defaultImage = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+PGRlZnMvPjxyZWN0IHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgZmlsbD0iI0VFRUVFRSIvPjxnPjx0ZXh0IHg9IjEzLjQ2MDkzNzUiIHk9IjMyIiBzdHlsZT0iZmlsbDojQUFBQUFBO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1mYW1pbHk6QXJpYWwsIEhlbHZldGljYSwgT3BlbiBTYW5zLCBzYW5zLXNlcmlmLCBtb25vc3BhY2U7Zm9udC1zaXplOjEwcHQ7ZG9taW5hbnQtYmFzZWxpbmU6Y2VudHJhbCI+NjR4NjQ8L3RleHQ+PC9nPjwvc3ZnPg==";
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.config(function($locationProvider) {
  $locationProvider.html5Mode({
    enabled: true,
    requireBase: false
  });
});


app.controller('IndexController', function($http, $window) {
  var vm = this;
  vm.User = {};
  vm.searchQuery = "";
  vm.query = "";
  vm.searchLocation = "";
  // add link get request
  // vm.searchResults = [];
  vm.tab = 0; // ListIDs index
  vm.listIDs = [];
  vm.currentListID = -1;
  vm.searchResults = [];
  vm.shoppingLists = [];
  vm.newItemName = "";
  vm.current_user = "";
  vm.current_user_type = "";
  vm.resolveLocation = "";
  vm.mapped = "list" // search or list
  vm.searchMarkers = [];
  vm.listMarkers = [];
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
                  if (vm.listIDs.length > 0) {
                    vm.currentListID = vm.listIDs[vm.tab];
                  } else {
                    vm.currentListID = -1
                  }
                  
                  vm.shoppingLists = data.allLists;
                } else {
                  vm.currentListID = -1;
                }
                
                if ((vm.current_user_type == "customer") && (vm.currentListID != -1)) {
                  vm.mapList();
                }
              }, errorCallBackGeneral);
        } else {
          // for (var i = 0; i < data.errors.length; i++) {
            // $window.alert(data.errors[i]);
          // }
        }
      }, errorCallBackGeneral);

  vm.remove = function(index) {
    vm.shoppingLists[vm.tab].contents.splice(index, 1);
    if (vm.current_user != "") {
      vm.updateList();
    }
    if (vm.currentDirections == "list") {
      vm.directionsDisplay.setMap(null);
      vm.directionsDisplay.setPanel(null);
      vm.directionsDisplay = new google.maps.DirectionsRenderer({preserveViewport: true});
      vm.directionsDisplay.setMap(vm.map);
      vm.directionsDisplay.setPanel(document.getElementById("DirectionsPanel"));
    }
  }

  vm.addItem = function(index) {
    if (vm.listIDs.length == 0) {
      alert("Cannot add item until a list has been created. Create a list in the View Shopping List menu.");
    } else {
      var addItem = {};
      addItem.type = "id";
      addItem.name = vm.searchResults[index].itemID;
      vm.shoppingLists[vm.tab].contents.push(vm.searchResults[index]);
      if (vm.current_user != "") {
        vm.updateList();
      }
    }
  }

  vm.addTextItem = function() {
    if (vm.listIDs.length == 0) {
      alert("Cannot add item until a list has been created. Create a list in the View Shopping List menu.");
    } else {
      var addText = {};
      addText.type = "name";
      addText.name = vm.newItemName;
      vm.shoppingLists[vm.tab].contents.push(addText);
      if (vm.current_user != "") {
        vm.updateList();
      }
      vm.newItemName = "";
    }
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
      $http.post("api/list/edit", editData).then(
      function successCallBack(response) {
        if (response.data.errors.length == 0){
          var currentTab = vm.listIDs.indexOf(response.data.entry.listID);
          vm.shoppingLists[currentTab].contents = response.data.entry.contents;
          if (vm.mapped == "list") {
            vm.mapList()
          }
        }
      }, errorCallBackGeneral);
    }
  }

  vm.resolveList = function() {
    if (vm.listIDs.length == 0) {
      alert("Cannot resolve. No lists exist. Build a list using the below Item Name field.");
    } else if (vm.resolveLocation == "") {
      alert("Must enter location to resolve list.");

    } else {
      var listData = {};
      listData.listID = vm.currentListID;
      listData.location = vm.resolveLocation;  //CURRENT LIST ID
      $http.post("api/list/resolve", listData).then(
      function successCallBack(response) {
        if (response.data.errors.length == 0) {
          var currentTab = vm.listIDs.indexOf(response.data.entry.listID);
          vm.shoppingLists[currentTab].contents = response.data.entry.contents;
          if (vm.mapped == "list") {
            vm.mapList()
          }
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            $window.alert(data.errors[i]);
          }
        }
      }, errorCallBackGeneral);
    }
  }

  vm.bounds = new google.maps.LatLngBounds();
  vm.infowindow = new google.maps.InfoWindow();
  vm.map = new google.maps.Map(document.getElementById('LocalCartMap'), {
    zoom: 17,
    center: new google.maps.LatLng(37.8723917, -122.2661629),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  vm.directionsDisplay = new google.maps.DirectionsRenderer({preserveViewport: true});
  vm.directionsDisplay.setMap(vm.map);
  vm.directionsDisplay.setPanel(document.getElementById("DirectionsPanel"));
  vm.directionsService = new google.maps.DirectionsService();
  vm.currentDirections = "search";
  vm.searchCoord = null;

  vm.calcRoute = function(start, dest) {
    var request = {
      origin: start,
      destination: dest,
      travelMode: google.maps.TravelMode.DRIVING,
    };
    vm.directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        vm.directionsDisplay.setDirections(response);
        vm.map.fitBounds(vm.bounds);
      }
    });

  }


  vm.mapList = function() {
    for (var i = 0; i < vm.listMarkers.length; i++) {
      vm.listMarkers[i].setMap(null);
    }
    vm.listMarkers = [];
    if (vm.shoppingLists.length > 0) {
      vm.mapped = "list"
      var listData = {};
      listData.listID = vm.currentListID; //CURRENT LIST ID
      $http.post("api/list/map", listData).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            console.log(data)
            var mapMarkers = response.data.map_markers;
            for (var i = 0; i < mapMarkers.length; i++) {
              var pos = mapMarkers[i].position;
              var pinColor = "4E9F35";
              var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + pos + "|" + pinColor,
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(10, 34));
              var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
                new google.maps.Size(40, 37),
                new google.maps.Point(0, 0),
                new google.maps.Point(12, 35));
              var marker = new google.maps.Marker({
                position: new google.maps.LatLng(mapMarkers[i].latitude, mapMarkers[i].longitude),
                icon: pinImage,
                shadow: pinShadow,
                map: vm.map
              });
              vm.bounds.extend(marker.position);
              google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                  vm.infowindow.setContent(mapMarkers[i].pin_name);
                  vm.infowindow.open(vm.map, marker);
                  vm.currentDirections = "list";
                  if (vm.searchCoord == null) {
                    vm.currentDirections = "search";
                  } else {
                    vm.calcRoute(vm.searchCoord, marker.position);
                  }
                }
              })(marker, i));
              vm.listMarkers.push(marker);
            }
            vm.map.fitBounds(vm.bounds);
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              $window.alert(data.errors[i]);
            }
          }
        }, errorCallBackGeneral)
      }
  }



  vm.search = function() {
    var searchData = {};
    searchData.query = vm.searchQuery;
    searchData.location = vm.searchLocation;
    vm.searchResults = [];
    if (vm.currentDirections == "search") {
      vm.directionsDisplay.setMap(null);
      vm.directionsDisplay.setPanel(null);
      vm.directionsDisplay = new google.maps.DirectionsRenderer({preserveViewport: true});
      vm.directionsDisplay.setMap(vm.map);
      vm.directionsDisplay.setPanel(document.getElementById("DirectionsPanel"));
    }
    if ((vm.searchQuery != "") && (vm.searchLocation != "")) {
      $http.get("api/search/items", {params: searchData}).then(
          function successCallBack(response) {
            var data = response.data;
            if (data.errors.length == 0) {
              vm.searchResults = data.items;
              vm.query = vm.searchQuery;
              for (var i = 0; i < vm.searchMarkers.length; i++) {
                vm.searchMarkers[i].setMap(null);
              }
              vm.searchMarkers = [];
              vm.searchCoord = new google.maps.LatLng(data.latitude, data.longitude);
              var pinColorLoc = "4375A3";
              var pinImageLoc = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColorLoc,
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(10, 34));
              var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
                new google.maps.Size(40, 37),
                new google.maps.Point(0, 0),
                new google.maps.Point(12, 35));
              var markerLoc = new google.maps.Marker({
                position: vm.searchCoord,
                icon: pinImageLoc,
                shadow: pinShadow,
                map: vm.map
              });
              vm.bounds.extend(markerLoc.position);
              google.maps.event.addListener(markerLoc, 'click', (function() {
                  vm.infowindow.setContent("Location");
                  vm.infowindow.open(vm.map, markerLoc);
                }));
              vm.searchMarkers.push(markerLoc);


              var alreadyMarked = [] // Done store IDs
              for (var i = 0; i < vm.searchResults.length; i++) {
                if ((vm.searchResults[i].coordinates == 1) && (alreadyMarked.indexOf(vm.searchResults[i].storeID) == -1)) {
                  var pos = vm.searchResults[i].index;
                  var pinColor = "FE6256";
                  var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + pos + "|" + pinColor,
                    new google.maps.Size(21, 34),
                    new google.maps.Point(0,0),
                    new google.maps.Point(10, 34));
                  var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(vm.searchResults[i].latitude, vm.searchResults[i].longitude),
                    icon: pinImage,
                    shadow: pinShadow,
                    map: vm.map
                  });
                  vm.bounds.extend(marker.position);
                  google.maps.event.addListener(marker, 'click', (function(marker, i) {
                    return function() {
                      vm.infowindow.setContent(vm.searchResults[i].storeName);
                      vm.infowindow.open(vm.map, marker);
                      vm.currentDirections = "search";
                      vm.calcRoute(vm.searchCoord, marker.position);
                    }
                  })(marker, i));
                  vm.searchMarkers.push(marker);
                  alreadyMarked.push(vm.searchResults[i].storeID);
                }
              }
              vm.map.fitBounds(vm.bounds);


            } else {
              for (var i = 0; i < data.errors.length; i++) {
                $window.alert(data.errors[i]);
              }
            }
          }, function successCallBack(response) {
              for (var i = 0; i < vm.searchMarkers.length; i++) {
                vm.searchMarkers[i].setMap(null);
              }
              vm.searchMarkers = [];
          });
    } else {
      alert("Must provide search query and location")
    }
  }

  vm.loginAttempt = function() {
    $http.post("/api/user/login", vm.User).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            if (data.user_type == 'merchant') {
              $window.location.href = 'merchant';
            } else {
              $window.location.reload();
            }
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              $window.alert(data.errors[i]);
            }
          }
        }, errorCallBackGeneral)
  }
  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.reload();
  }

  vm.isSet = function(checkTab) {
    return vm.tab === checkTab;
  };

  vm.setTab = function(setTab) {
    vm.tab = setTab;
    vm.currentListID = vm.listIDs[vm.tab];
    vm.mapList();
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
            vm.shoppingLists.push({
              listName: vm.newListName,
              contents: []
            });
            vm.newListName = "";
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              $window.alert(data.errors[i]);
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
    if (vm.currentDirections == "list") {
      vm.directionsDisplay.setMap(null);
      vm.directionsDisplay.setPanel(null);
      vm.directionsDisplay = new google.maps.DirectionsRenderer({preserveViewport: true});
      vm.directionsDisplay.setMap(vm.map);
      vm.directionsDisplay.setPanel(document.getElementById("DirectionsPanel"));
    }
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
            $window.alert(data.errors[i]);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.editStore = function() {
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
            $window.alert(data.errors[i]);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.current_user = "";
  vm.current_user_type = "";
  $http.get("api/user/get").then(
    function successCallBack(response) {
      var data = response.data;
      if (data.errors.length == 0) {
        vm.current_user = data.username;
        vm.current_user_type = data.user_type;
        if (vm.current_user_type != "merchant") {
          $window.location.href = "home";
        }
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
              $window.alert(data.errors[i]);
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
              $window.alert(data.errors[i]);
            }
          }
        }, errorCallBackGeneral);
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
        // $window.alert(data.errors[i]);
        // }
      }
    },
    function errorCallBack(response) {
      alert('An error has occured');
    }
  )
});

app.controller('InventoryController', function($http, $window, $scope) {
  var vm = this;
  vm.inventory = [];
  vm.inventoryID = -1;
  vm.tempItem = {}
  vm.current_user = "";
  vm.current_user_type = "";
  $http.get("api/user/get").then(
    function successCallBack(response) {
      var data = response.data;
      if (data.errors.length == 0) {
        vm.current_user = data.username;
        vm.current_user_type = data.user_type;
        console.log(data.username);
        if (vm.current_user_type == "merchant") {
          $http.get("api/inventory/getUser").then(
            function successCallBack2(response) {
              var data2 = response.data;
              if (data2.errors.length == 0) {
                vm.inventory = data2.contents;
                vm.inventoryID = data2.inventoryID;
                vm.tempItem.inventoryID = vm.inventoryID;
              }
            }, errorCallBackGeneral)
        } else {
          $window.location.href = "home";
        }
      } else {
        $window.location.href = "home";
      }
    }, errorCallBackGeneral)
  vm.remove = function(index) {
    var removedID = {};
    removedID.itemID = vm.inventory[index].itemID;
    removedID.index = index;
    $http.post("api/item/delete", removedID).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.inventory.splice(data.index, 1);
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            $window.alert(data.errors[i]);
          }
        }
      }, errorCallBackGeneral)
  }
  vm.removeAll = function() {
    var len = vm.inventory.length;
    for (var index = len - 1; index >= 0; index--) {
      var removedID = {};
      removedID.itemID = vm.inventory[index].itemID;
      removedID.index = index;
      $http.post("api/item/delete", removedID).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            vm.inventory.splice(data.index, 1);
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              $window.alert(data.errors[i]);
            }
          }
        }, errorCallBackGeneral)
    }
  }
  vm.addItem = function() {
    vm.tempItem.inventoryID = vm.inventoryID;
    $http.post("api/item/create", vm.tempItem).then(
      function successCallBack(response) {
        var data = response.data;
        if (data.errors.length == 0) {
          vm.tempItem.itemID = data.itemID;
          vm.inventory.push(vm.tempItem);
          vm.tempItem = {}
          vm.tempItem.inventoryID = vm.inventoryID;
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            $window.alert(data.errors[i]);
          }
        }
      }, errorCallBackGeneral)
  }
  $scope.importInventory = function(files) {
    var form = new FormData();
    form.append("dataset", files[0]);
    form.append("inventoryID", vm.inventoryID);

    $http.post("api/inventory/import", form, {
      headers: {'Content-Type': undefined},
      transformRequest: angular.identity
    }).then(
          function successCallBack(response) {

            var data = response.data;
            if (data.errors.length == 0) {
              vm.inventory = data.items
            } else {
              for (var i = 0; i < data.errors.length; i++) {
                $window.alert(data.errors[i]);
              }
            }
          }, errorCallBackGeneral);
  }

  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.href = "home";
  }

});


app.controller('StoreController', function($http, $location, $window) {
  var vm = this;
  // populate store info
  vm.storeInfo = {}
  var curr_storeID = $location.search();
  vm.products = [];
  vm.tab = 0;
  vm.listIDs = [];
  vm.currentListID = -1;
  vm.shoppingLists = [];
  vm.newItemName = "";
  vm.current_user = "";
  vm.current_user_type = "";
  vm.resolveLocation = "";


  // get request for reviews for store
  vm.reviews = [];
  vm.review = {};
  vm.review.rating = -1;
  vm.review.text = '';
  $http.post("api/store/storeID", curr_storeID).then(
    function successCallBack(response) {
      // console.log(response.data);
      var data = response.data;
      if (data.errors.length == 0) {
        vm.storeInfo = data.store;
      }
    }, errorCallBackGeneral)

  $http.post("api/inventory/store", curr_storeID).then(
    function successCallBack(response) {
      var data = response.data;
      if (data.errors.length == 0) {
        vm.products = data.contents;
        console.log(vm.products)
      }
    }, errorCallBackGeneral)
    // mocked inventory items, look at results
  $http.get("api/user/get").then(
    function successCallBack(response) {
      var data = response.data;
      console.log(data);
      if (data.errors.length == 0) {
        vm.current_user = data.username;
        vm.current_user_type = data.user_type;
        console.log(vm.current_user_type);
      }
    })
  $http.get("api/review/storeID", {params: curr_storeID}).then(
    function successCallBack(response) {
      var data = response.data;
      console.log("storereview");
      if (data.errors.length == 0) {
        vm.reviews = data.reviews
        console.log(vm.current_user_type);
      }
    })

  vm.loginAttempt = function() {
    $http.post("/api/user/login", vm.User).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            $window.location.reload();
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              $window.alert(data.errors[i]);
            }
          }
        }, errorCallBackGeneral)
  }

  vm.logout = function() {
    $http.post("api/user/logout");
    $window.location.reload();
  }
  vm.storeTab = 0
  vm.isTabSet = function(checkTab) {
    return vm.storeTab === checkTab;
  };

  vm.setStoreTab = function(setTab) {
    vm.storeTab = setTab;
  };


  //need to add post request 
  vm.addReview = function(product) {
    vm.review.user = vm.current_user;
    vm.review.username = vm.current_user;
    vm.review.storeID = curr_storeID.storeID;
    if (vm.review.rating == -1) {
      alert("Must provide a rating");
    } else if (vm.current_user == "") {
      alert("Must be logged in to leave a review");
    } else {
      $http.post("api/review/add", vm.review).then(
      function successCallBack(response) {
        var data = response.data;
        console.log(data);
        if (data.errors.length == 0) {
          vm.reviews.push(vm.review);
          vm.review = {};
        }
      }, errorCallBackGeneral);
    }
  };


  vm.isSet = function(checkTab) {
    return vm.tab === checkTab;
  };

  vm.setTab = function(setTab) {
    vm.tab = setTab;
    vm.currentListID = vm.listIDs[vm.tab];
  };

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
                  if (vm.listIDs.length > 0) {
                    vm.currentListID = vm.listIDs[vm.tab];
                  } else {
                    vm.currentListID = -1
                  }
                  
                  vm.shoppingLists = data.allLists;
                } else {
                  vm.currentListID = -1;
                }
                
              }, errorCallBackGeneral);
        } else {
          // for (var i = 0; i < data.errors.length; i++) {
            // $window.alert(data.errors[i]);
          // }
        }
      }, errorCallBackGeneral);

  vm.remove = function(index) {
    vm.shoppingLists[vm.tab].contents.splice(index, 1);
    if (vm.current_user != "") {
      vm.updateList();
    }
  }

  vm.addProduct = function(index) {
    if (vm.listIDs.length == 0) {
      alert("Cannot add item until a list has been created. Create a list in the View Shopping List menu.");
    } else {
      var addItem = {};
      addItem.type = "id";
      addItem.name = vm.products[index].itemID;
      vm.shoppingLists[vm.tab].contents.push(vm.products[index]);
      if (vm.current_user != "") {
        vm.updateList();
      }
    }
  }

  vm.addTextItem = function() {
    if (vm.listIDs.length == 0) {
      alert("Cannot add item until a list has been created. Create a list in the View Shopping List menu.");
    } else {
      var addText = {};
      addText.type = "name";
      addText.name = vm.newItemName;
      vm.shoppingLists[vm.tab].contents.push(addText);
      if (vm.current_user != "") {
        vm.updateList();
      }
      vm.newItemName = "";
    }
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
      $http.post("api/list/edit", editData).then(
      function successCallBack(response) {
        if (response.data.errors.length == 0){
          var currentTab = vm.listIDs.indexOf(response.data.entry.listID);
          vm.shoppingLists[currentTab].contents = response.data.entry.contents;
        }
      }, errorCallBackGeneral);
    }
  }

  vm.addList = function() {
    var listData = {};
    listData.name = vm.newListName;
    if (vm.newListName != "") {
      $http.post("api/list/create", listData).then(
        function successCallBack(response) {
          var data = response.data;
          if (data.errors.length == 0) {
            vm.listIDs.push(data.listID);
            vm.shoppingLists.push({
              listName: vm.newListName,
              contents: []
            });
            vm.newListName = "";
          } else {
            for (var i = 0; i < data.errors.length; i++) {
              $window.alert(data.errors[i]);
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

  vm.resolveList = function() {
    if (vm.listIDs.length == 0) {
      alert("Cannot resolve. No lists exist. Build a list using the below Item Name field.");
    } else if (vm.resolveLocation == "") {
      alert("Must enter location to resolve list.");

    } else {
      var listData = {};
      listData.listID = vm.currentListID;
      listData.location = vm.resolveLocation;  //CURRENT LIST ID
      $http.post("api/list/resolve", listData).then(
      function successCallBack(response) {
        if (response.data.errors.length == 0) {
          var currentTab = vm.listIDs.indexOf(response.data.entry.listID);
          vm.shoppingLists[currentTab].contents = response.data.entry.contents;
        } else {
          for (var i = 0; i < data.errors.length; i++) {
            $window.alert(data.errors[i]);
          }
        }
      }, errorCallBackGeneral);
    }
  }


});

successListError = function(response) {
  var data = response.data;
  if (data.errors.length > 0) {
    for (var i = 0; i < data.errors.length; i++) {
      alert(data.errors[i]);
    }
  }
};
errorCallBackGeneral = function(response) {
  alert('An error has occured');
};

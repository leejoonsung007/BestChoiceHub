// GoogleMap intinazing elements
var markers = [];
var latlng ;
var map ;
var service ;

function initMap() {

    latlng = new google.maps.LatLng(53.3498118, -6.2711979);
    map = new google.maps.Map(document.getElementById('map'), {
        center: latlng,
        zoom: 12,
        gestureHandling: 'greedy'
    });
    service = new google.maps.places.PlacesService(map);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {

            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            latlng = pos;

            map.setCenter(latlng);

            var marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title:"You are here!"
            });

        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}

var documentHeight = 0;
function scrolling(jQueryObj,offsetTop) {

    var topPadding = 15;

    documentHeight = $(document).height();
    $(window).scroll(function () {
        var sideBarHeight = jQueryObj.height();
        if ($(window).scrollTop() > offsetTop) {
            var newPosition = ($(window).scrollTop() - offsetTop) + topPadding;
            var maxPosition = documentHeight - (sideBarHeight + 368);
            if (newPosition > maxPosition) {
                newPosition = maxPosition;
            }
            jQueryObj.stop().animate({
                marginTop: newPosition
            });
        } else {
            jQueryObj.stop().animate({
                marginTop: 0
            });
        }
        ;
        //console.log("documentHeight: " + documentHeight + " ObjOffset.top: " + offsetTop + " window.scrollTop: " + $(window).scrollTop());
        //console.log("sideBarHeight: " + sideBarHeight + " newPosition: " + newPosition + " maxPosition: " + maxPosition);
    });// window.scroll end

}

var currentMarker = null;
function showSelectedLocation(obj) {

    var infowindow = new google.maps.InfoWindow();

    if (currentMarker != null) {
        currentMarker.setMap(null);
        currentMarker = null;
    }

    service.getDetails({
        placeId: obj.getAttributeNode("name").value
    }, function (place, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            console.log("placeID: " + obj.getAttributeNode("name").value);
            console.log("Google return: place "+ place + "status "+ status);
            map.setCenter(place.geometry.location);
            map.setZoom(12);
            var marker;

            if (typeof(place.photos) == "undefined") {
                marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location,
                    title: place.name,
                    //这里控制 地图上marker的显示大小
                    icon: "../../static/img/search/not_found-big.png"
                });

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent("<div id='" + place.place_id + "' style='width: 220px'>" +
                                                "<img class='img' src='../../static/img/search/not_found.jpg' alt='marker' width='80'><br>" +
                                                "<strong>" + place.name + '</strong><br>' +
                                                "<strong>Place ID: </strong>" + place.place_id + "<br>" +
                                                "<strong>Address: </strong>" + place.formatted_address +
                                          "</div>");
                    infowindow.open(map, this);
                });

            } else {
                marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location,
                    title: place.name,
                    //这里控制 地图上marker的显示大小
                    icon: place.photos[0].getUrl({
                        'maxWidth': 40,
                        'maxHeight': 40
                    })
                });

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent(
                        "<div id='" + place.place_id + "' style='width: 220px'>" +
                            "<img class='img' src='" + place.photos[0].getUrl({ 'maxWidth': 350, 'maxHeight': 350 }) + "' alt='marker' width='80'><br>" +
                            "<strong>" + place.name + '</strong><br>' +
                            "<strong>Place ID: </strong>" + place.place_id + "<br>" +
                            "<strong>Address: </strong>" + place.formatted_address +
                        "</div>");
                    infowindow.open(map, this);
                });
            }

            currentMarker = marker;
        }
    });

}

function drawMarkersByplaceIds(){
    for(var i=0; i<markers.length; i++){
        markers[i].setMap(null);
    }
    markers = [];

    $(".placeId").each(function(i,e){
        console.log(e);
        drawSingleMarker(e.name);
    });
}

function drawSingleMarker(placeid){
    service.getDetails(
        {
            placeId: placeid
        },
        function (place, status) {
            console.log("current draw placeid: " + placeid);

            var marker;
            var infowindow = new google.maps.InfoWindow();

            if (status === google.maps.places.PlacesServiceStatus.OK) {

                if (typeof(place.photos) == "undefined") {
                    marker = new google.maps.Marker({
                        map: map,
                        position: place.geometry.location,
                        title: place.name,
                        //这里控制 地图上marker的显示大小
                        icon: "../../static/img/search/not_found-small.png"
                    });

                    google.maps.event.addListener(marker, 'click', function () {
                        infowindow.setContent("<div id='" + place.place_id + "' style='width: 220px'>" +
                                                    "<img class='img' src='../../static/img/search/not_found.jpg' alt='marker' width='80'><br>" +
                                                    "<strong>" + place.name + '</strong><br>' +
                                                    "<strong>Place ID: </strong>" + place.place_id + "<br>" +
                                                    "<strong>Address: </strong>" + place.formatted_address +
                                              "</div>");
                        infowindow.open(map, this);
                    });

                } else {
                    marker = new google.maps.Marker({
                        map: map,
                        position: place.geometry.location,
                        title: place.name,
                        //这里控制 地图上marker的显示大小
                        icon: place.photos[0].getUrl({
                            'maxWidth': 30,
                            'maxHeight': 30
                        })
                    });

                    google.maps.event.addListener(marker, 'click', function () {
                        infowindow.setContent(
                        "<div id='" + place.place_id + "' style='width: 220px'>" +
                            "<img class='img' src='" + place.photos[0].getUrl({ 'maxWidth': 350, 'maxHeight': 350 }) + "' alt='marker' width='80'><br>" +
                            "<strong>" + place.name + '</strong><br>' +
                            "<strong>Place ID: </strong>" + place.place_id + "<br>" +
                            "<strong>Address: </strong>" + place.formatted_address +
                        "</div>");
                    infowindow.open(map, this);
                    });

                }

                markers.push(marker);
            }
        });
}

/*
* Quicksort, sort by a property, or by "get the function on which the sorting is based".
* @method Sort
* @static
* @param {array} arr Unsorted array
* @param {string | function}  Sorting based on prop
* @param {boolean} desc
* @return {array} Returns a new sorted array
*/
function Sort(arr, prop, desc){
    var props=[],
    ret=[],
    i=0,
    len=arr.length;
    if(typeof prop=='string') {
        for(; i<len; i++){
            var oI = arr[i];
            if(typeof(oI[prop]) == 'number'){
                (props[i] = new Number(oI && oI[prop] || ''))._obj = oI;
            } else if(typeof(oI[prop]) == 'string'){
                (props[i] = new String(oI && oI[prop] || ''))._obj = oI;
            } else{
                throw 'can only compare string or numeric attribute values';
            }
        }

        console.log("quickSort Step1 props :");
        console.log(props[i]);
    }
    else if(typeof prop=='function') {
        for(; i<len; i++){
            var oI = arr[i];
            if(typeof(oI[prop]) == 'number'){
                (props[i] = new Number(oI && oI[prop] || ''))._obj = oI;
            } else if(typeof(oI[prop]) == 'string'){
                (props[i] = new String(oI && oI[prop] || ''))._obj = oI;
            } else{
                throw 'can only compare string or numeric attribute values';
            }
        }
    }
    else {
        throw 'selected prop Parameter type error';
    }

    //props.sort();
    quickSort(props,0, props.length-1);
    console.log("quickSort Step2 props  :");
    console.log(props);

    for(i=0; i<len; i++) {
        ret[i] = props[i]._obj;
    }
    console.log("quickSort Step3 ret  :");
    console.log(ret);

    if(desc) ret.reverse();
    return ret;
};



function quickSort(arr, left, right){
   var len = arr.length,
   pivot,
   partitionIndex;


  if(left < right){
    pivot = right;
    partitionIndex = partition(arr, pivot, left, right);

   //sort left and right
   quickSort(arr, left, partitionIndex - 1);
   quickSort(arr, partitionIndex + 1, right);
  }
  return arr;
}

function partition(arr, pivot, left, right){
   var pivotValue = arr[pivot],
       partitionIndex = left;

   for(var i = left; i < right; i++){
    if(arr[i] < pivotValue){
      swap(arr, i, partitionIndex);
      partitionIndex++;
    }
  }
  swap(arr, right, partitionIndex);
  return partitionIndex;
}

function swap(arr, i, j){
   var temp = arr[i];
   arr[i] = arr[j];
   arr[j] = temp;
}
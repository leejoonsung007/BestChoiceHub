//Execute when initializing the page
$(document).ready(function () {

});

var selectedData = [];
var totalData = [];
var currentPage = 1;
var pageSize = 6;
var totalPage = 29;

var school_ids = [];


function ajax_getSchoolDataByLatlng(){
    navigator.geolocation.getCurrentPosition(function (position){
        var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

        req = $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/distance_computing/'+ pos.lat + ','+ pos.lng,
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            success: function (data) {
                console.log("ajax data:");
                console.log(data);

                totalData = data.result;
                totalPage = data.page_counte;
                drawSchoolCardsByPage(currentPage);



            }
        });

    } );
}

function drawSchoolCardsByPage(page){
    $("#loadgif").hide();
    var holder = $("#school-holder");
    holder.empty();
    //这里一定要在每次循环前初始化为空
    school_ids = [];
    selectedData = [];

    currentPage = page;

    for (var i = (currentPage-1)*pageSize; i < currentPage*pageSize; i++){
        if(i < totalData.length){
            selectedData.push(totalData[i]);
        }
    }

    console.log("ajax_getSchoolDataByLatlng -- selectedData: ");
    console.log(selectedData);

    $.each(selectedData, function(i,school){
        var img_src = "";
        if(null != school.photo_ref1){
            //低分辨率
            img_src = '"../../static/img/home/'+school.official_school_name+'.jpeg"'
        }else{
            img_src = '"../../static/img/search/not_found.png"';
        }
        school_ids.push(school.place_id);

        holder.append(
            '<div class="product-item col-xs-6 col-md-4">' +
                '<a target="_blank" href=\"http://localhost:5000/school/'+ school.official_school_name+'/'+school.roll_number+'\">' +
                    '<img style="height: 150px;"' +
                         'src=' + img_src +
                         'alt="sample school"/>' +
                '</a>'+

                '<h2 style="font-weight:bold"><a target="_blank" href=\"http://localhost:5000/school/'+ school.official_school_name+'/'+school.roll_number+'\">' +
                                                 school.official_school_name+'</a><br>' +

                                                '<a class="'+ school.place_id + '" href="javascript:void(0)"' +
                                                'onclick="showLocation(this)"> <span style="color: black;font-size: 14px; font-style: italic">☞ Show Location </span> </a>' +
                '</h2>' +

                '<p><span style="font-weight:bold;color: black">Address:</span>' + school.address +
                '</p>' +

            '</div>'
        );
    });// end -- each

    addCustomMarkers(school_ids);

}


//Gets the province and city of the current location and sends it to the server side
/*function geocodeLocation(position) {
    var geocoder = new google.maps.Geocoder;
    geocoder.geocode({'location': position}, function (results, status) {
        if (status === 'OK') {
            if (results[0]) {
                var addr = results[0].formatted_address;
                var value = addr.split(",");

                count = value.length;
                country = value[count - 1];
                city = value[count - 2];
                area = value[count - 3];

                position['country'] = country;
                position['city'] = city;
                position['area'] = area;

                console.log(position);

                //设置下拉选框对应到当前所属城市
                var myselect = document.getElementById("county");
                for(var i=0; i < myselect.options.length; i++){
                    if(city.toLowerCase().indexOf(myselect.options[i].text.toLowerCase()) != -1){
                        myselect.options[i].selected = true;
                        break;
                    }
                }


            } else {
                console.log('No results found');
            }

        } else {
            console.log('Geocoder failed due to: ' + status);
        }
    });
}*/



// GoogleMap intinazing elements
var markers = [];
var latlng ;
var map ;
var service ;

var school_ids = [];

function initMap() {

    latlng = new google.maps.LatLng(53.3498118, -6.2711979);
    map = new google.maps.Map(document.getElementById('mapholder'), {
        center: latlng,
        zoom: 12,
        gestureHandling: 'greedy'
    });
    service = new google.maps.places.PlacesService(map);

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {

            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            latlng = pos;

            //geocodeLocation(geocoder, pos);

            map.setCenter(pos);
            var marker = new google.maps.Marker({
                position: pos,
                map: map
            });



            /*//Add a marker clusterer to manage the markers.
            var markerCluster = new MarkerClusterer(map, markers,
                {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
*/
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        //if get user location failed


        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}

function addCustomMarkers(placeIds){
    /*if (markers.length == 6){
         for(var j=0; j < markers.length; j++){
            markers[j].setMap(null);
        }
    }*/
    for(var j=0; j < markers.length; j++){
        markers[j].setMap(null);
    }
    markers = [];

    placeIds.map(function (id, i) {
        service.getDetails({
            placeId: id
        }, function (place, status) {
            console.log(id);
            var marker;
            var infowindow = new google.maps.InfoWindow();
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                    console.log("addMarkers: placeID "+i+"  "+id);
                    if (typeof(place.photos) == "undefined") {
                        marker = new google.maps.Marker({
                            map: map,
                            position: place.geometry.location,
                            title: place.name,
                            // label: labels[i % labels.length],
                            icon: "../../static/img/search/not_found-small.png"
                        });

                        google.maps.event.addListener(marker, 'click', function () {
                            infowindow.setContent("<div id='" + place.place_id + "' style='width: 220px'><img class= 'img' src='" +
                                "../../static/img/search/not_found.jpg" + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                                '<strong>Place ID: </strong>' + place.place_id + '<br>' +
                                '<strong>Address: </strong>' + place.formatted_address + '</div>');
                            infowindow.open(map, this);
                        });

                    } else {
                        marker = new google.maps.Marker({
                            map: map,
                            position: place.geometry.location,
                            title: place.name,
                            //label: labels[i % labels.length],
                            icon: place.photos[0].getUrl({
                                'maxWidth': 30,
                                'maxHeight': 30
                            })
                        });

                        google.maps.event.addListener(marker, 'click', function () {
                            infowindow.setContent("<div id='" + place.place_id + "' style='width: 220px'><img class= 'img' src='" + place.photos[0].getUrl({
                                    'maxWidth': 350,
                                    'maxHeight': 350
                                }) + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                                '<strong>Place ID: </strong>' + place.place_id + '<br>' +
                                '<strong>Address: </strong>' + place.formatted_address + '</div>');
                            infowindow.open(map, this);
                        });

                    }
            }

            /*if(markers.length >= 0 && markers.length < 6){
                markers.push(marker);
            }else{
                markers[i] = marker;
            }*/
            markers.push(marker);

        });//--function (place, status) end


    });


}




var currentMarker = null;

function showLocation(obj) {
    //var removeObj = document.getElementById(obj.getAttributeNode("class").value)
    //removeObj.parentNode.removeChild(removeObj);

    var infowindow = new google.maps.InfoWindow();
    var service = new google.maps.places.PlacesService(map);

    if (currentMarker != null) {
        currentMarker.setMap(null);
        currentMarker = null;
    }

    service.getDetails({
        placeId: obj.getAttributeNode("class").value
    }, function (place, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            map.setCenter(place.geometry.location);

            var marker;
            if (typeof(place.photos) == "undefined") {
                marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location,
                    title: place.name,
                    // label: labels[i % labels.length],
                    icon: "../../static/img/search/not_found-big.png"
                });

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent("<div id='" + place.place_id + "' style='width: 220px'><img class= 'img' src='" +
                        "../../static/img/search/not_found.jpg" + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                        '<strong>Place ID: </strong>' + place.place_id + '<br>' +
                        '<strong>Address: </strong>' + place.formatted_address + '</div>');
                    infowindow.open(map, this);
                });

            } else {
                marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location,
                    title: place.name,
                    //label: labels[i % labels.length],
                    icon: place.photos[0].getUrl({
                        'maxWidth': 40,
                        'maxHeight': 40
                    })
                });

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent("<div id='" + place.place_id + "' style='width: 220px'><img class= 'img' src='" + place.photos[0].getUrl({
                            'maxWidth': 350,
                            'maxHeight': 350
                        }) + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                        '<strong>Place ID: </strong>' + place.place_id + '<br>' +
                        '<strong>Address: </strong>' + place.formatted_address + '</div>');
                    infowindow.open(map, this);
                });
            }


            currentMarker = marker;
        }
    });

}


// Automatically refresh once. If you have not logged in, create a new cookie: views are set to 1.
// Judge whether the views are the first browsing based on whether there is a value or not.
function autoRefresh() {
    if (getCookie("views") != 1) {
        document.cookie = "views = 1";
        if (getCookie("view") != 1)
            location.reload()
        else
            refresh();// If the browser does not allow cookies to be written, the url refresh method is used.
    } else {
        delCookie("views");
    }

}

function getCookie(name) {
    //Gets the value of the cookie with the specified name
    var arrStr = document.cookie.split("; ");
    for (var i = 0; i < arrStr.length; i++) {
        var temp = arrStr[i].split("=");
        if (temp[0] == name)
            return unescape(temp[1]);
    }
    return null;
}

function delCookie(name) {
    //To remove the cookie with the specified name, set its expiration time to a past time
    var date = new Date();
    date.setTime(date.getTime() - 10000);
    document.cookie = name + "=a; expires=" + date.toGMTString();
}

function refresh() {
    url = location.href; // Assign the address of the current page to the variable url
    // The split variable url delimiter is "#"
    if (url.indexOf("#") == -1) { // If there's no # after the url
        url += "#"; // add #
        self.location.replace(url); // refresh the page
    }
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
}
$(document).ready(function () {

    // Set carousel options
    $('.carousel').carousel({
        interval: 8000 // 8 seconds vs. default 5
    });

});

var markers = [];

var latlng = new google.maps.LatLng(53.3498118, -6.2711979);

var map = new google.maps.Map(document.getElementById('mapholder'), {
    center: latlng,
    zoom: 12,
    gestureHandling: 'greedy'
});

//Gets the province and city of the current location and sends it to the server side
function geocodeLocation(geocoder, position) {
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

                req = $.ajax({
                    type: 'POST',
                    url: 'http://localhost:5000',
                    data: JSON.stringify(position),
                    contentType: 'application/json; charset=UTF-8',
                    dataType: 'json',
                    success: function (data) {
                        // if (data.result == 'success'){
                            console.log(data.result)
                            // console.log(data.pagination)
                            console.log(data.schools);
                        // }

                     }
                });

                // req.done(function(data){
                //     $('#trying').fadeOut(1000).fadeIn(1000),
                //     $('#trying').html(data)
                //     console.log(JSON.stringify(data))
                // });


            } else {
                console.log('No results found');
            }

        } else {
            console.log('Geocoder failed due to: ' + status);
        }
    });
}


function initMap(placeID) {

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {

            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };


            var infowindow = new google.maps.InfoWindow();
            var service = new google.maps.places.PlacesService(map);
            var geocoder = new google.maps.Geocoder;

            geocodeLocation(geocoder, pos);

            map.setCenter(pos);
            var marker = new google.maps.Marker({
                position: pos,
                map: map
            });


            /*service.getDetails({
                placeId: 'ChIJleUXFNAIZ0gRhNzwSNpWkw0'
            }, function (place, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    var marker = new google.maps.Marker({
                        map: map,
                        position: place.geometry.location,
                        title: place.name,
                        icon: place.photos[0].getUrl({
                            'maxWidth': 40,
                            'maxHeight': 40
                        })
                    });
                    google.maps.event.addListener(marker, 'click', function () {
                        infowindow.setContent("<div style='width: 220px'><img class= 'img' src='" + place.photos[0].getUrl({
                                'maxWidth': 350,
                                'maxHeight': 350
                            }) + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                            'Place ID: ' + place.place_id + '<br>' +
                            place.formatted_address + '</div>');
                        infowindow.open(map, this);
                    });
                }
            });*/


            // Create an array of alphabetical characters used to label the markers.
            var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

            var locations = placeID; /*[
                "ChIJHYkHCdsIZ0gRXz4yLREmvHQ",
                "ChIJpzxxr9AIZ0gRa69sULj9zYs",
                "ChIJ-UioQdsIZ0gRwAHOnjq8sko",
                "ChIJh1EtkpEIZ0gR1lMjFQUd-zc",
                "ChIJZzaAiGMIZ0gRozqf8i7vMnU",
                "ChIJibOyH2IOZ0gRtWMz9SQQDas",
                "ChIJ6fclDJEOZ0gRzisvsLddjNo",
                "ChIJ07tFM9gIZ0gRd87tXEv6POw",
                "ChIJTcaPW4cOZ0gRVgqU3H63398",
                "ChIJt9cchZgOZ0gRwW78_VEIEXw",
                "ChIJn3rZp-wIZ0gRDC17B3XLZkw",
                "ChIJ_3kBDcMOZ0gRNFzZqN7YWmI",
                "ChIJA5XXN9IOZ0gR7HGnIVFQrI8",
                "ChIJXa4Sy7AOZ0gRJLi1wQFCeGM",
                "ChIJjXO-8JgOZ0gR1KHY3XocqDU",
                "ChIJ34uYDdUNZ0gRwBp3Fy-23Jo",
                "ChIJzZS7sB0MZ0gRnVtm8nw3UB8",
                "ChIJgTCQFoYOZ0gRq3gV0jEBcuo",
                "ChIJiRUcslMJZ0gRVqRmjJY1ZVE"
            ]*/


            locations.map(function (location, i) {


                service.getDetails({
                    placeId: location
                }, function (place, status) {
                    if (status === google.maps.places.PlacesServiceStatus.OK) {

                        var marker;
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
                });

                markers.push(marker);

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

        geocodeLocation(geocoder, latlng);


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
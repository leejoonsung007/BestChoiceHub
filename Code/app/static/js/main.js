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
    zoom: 14,
    gestureHandling: 'greedy'
});

function initMap() {

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };


            map.setCenter(pos);
            var marker = new google.maps.Marker({
                position: pos,
                map: map
            });


            var infowindow = new google.maps.InfoWindow();
            var service = new google.maps.places.PlacesService(map);

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

            var locations = [
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
            ]



            locations.map(function (location, i) {



                service.getDetails({
                    placeId: location
                }, function (place, status) {
                    if (status === google.maps.places.PlacesServiceStatus.OK) {

                        var marker;
                        if (typeof(place.photos) == "undefined"){
                            marker = new google.maps.Marker({
                                map: map,
                                position: place.geometry.location,
                                title: place.name,
                               // label: labels[i % labels.length],
                                icon: "../../static/img/search/not_found-small.png"
                            });

                            google.maps.event.addListener(marker, 'click', function () {
                                infowindow.setContent("<div id='" +place.place_id+ "' style='width: 220px'><img class= 'img' src='" +
                                    "../../static/img/search/not_found.png" + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                                    '<strong>Place ID: </strong>' + place.place_id + '<br>' +
                                    '<strong>Address: </strong>' + place.formatted_address + '</div>');
                                infowindow.open(map, this);
                            });


                        }else{
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
                                infowindow.setContent("<div id='" +place.place_id+ "' style='width: 220px'><img class= 'img' src='" + place.photos[0].getUrl({
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

            //Add a marker clusterer to manage the markers.
            var markerCluster = new MarkerClusterer(map, markers,
                {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
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

function showLocation(obj){
    //var removeObj = document.getElementById(obj.getAttributeNode("class").value)
    //removeObj.parentNode.removeChild(removeObj);

    var infowindow = new google.maps.InfoWindow();
    var service = new google.maps.places.PlacesService(map);

    if(currentMarker != null){
        currentMarker.setMap(null);
        currentMarker = null;
    }

    service.getDetails({
        placeId: obj.getAttributeNode("class").value
    }, function (place, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            map.setCenter(place.geometry.location);

            var marker;
            if (typeof(place.photos) == "undefined"){
                marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location,
                    title: place.name,
                    // label: labels[i % labels.length],
                    icon: "../../static/img/search/not_found-big.png"
                });

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent("<div id='" +place.place_id+ "' style='width: 220px'><img class= 'img' src='" +
                        "../../static/img/search/not_found.png" + "' alt='Smiley face' width='80'><br><strong>" + place.name + '</strong><br>' +
                        '<strong>Place ID: </strong>' + place.place_id + '<br>' +
                        '<strong>Address: </strong>' + place.formatted_address + '</div>');
                    infowindow.open(map, this);
                });

            }else {
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
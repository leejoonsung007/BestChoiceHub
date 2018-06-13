$( document ).ready(function() {

	// Set carousel options
	$('.carousel').carousel({
	  interval: 8000 // 8 seconds vs. default 5
	});



});

function getLocation()
{
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(showPosition,showError);
    }
    else{x.innerHTML="Geolocation is not supported by this browser.";}
}


function showError(error)
{
    switch(error.code)
    {
        case error.PERMISSION_DENIED:
            x.innerHTML="User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML="Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML="The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML="An unknown error occurred."
            break;
    }
}

function showPosition(position)
{
    lat = position.coords.latitude;
    lon = position.coords.longitude;
    latlon = new google.maps.LatLng(lat, lon)
    mapholder = document.getElementById('mapholder')

    var myOptions={
        center:latlon,
		zoom:14,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        mapTypeControl:false,
        navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}
    };
    var map=new google.maps.Map(document.getElementById("mapholder"),myOptions);
    var marker=new google.maps.Marker({position:latlon,map:map,title:"You are here!"});
}
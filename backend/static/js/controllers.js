'use strict';

/* Controllers */

function waitmessages()
{
	var securityquotes = [
        "Adventure is worthwhile.",
        "Life is Either a daring adventure or nothing at all",
        "For my part, I travel not to go anywhere, but to go. I travel for travel’s sake. The great affair is to move.",
        "Traveling – it leaves you speechless, then turns you into a storyteller",
        "We travel, some of us forever, to seek other places, other lives, other souls.",
        "A journey is best measured in friends, rather than miles.",
        "The gladdest moment in human life, me thinks, is a departure into unknown lands.",
        "I am not the same, having seen the moon shine on the other side of the world.",
        "The world is a book, and those who do not travel read only one page.",
        "You don’t have to be rich to travel well."
	]
	var quote = securityquotes[Math.floor(Math.random() * securityquotes.length)];
    return quote;
}

function travelPics()
{
    var pics = [
        "/static/img/patagonia.jpg",
        "/static/img/stone.jpg",
        "/static/img/budapest.jpg",
        "/static/img/singapore.jpg",
        "/static/img/brazil.jpg",
        "/static/img/india.jpg",
    ];
    var pic = pics[Math.floor(Math.random() * pics.length)];
    return pic;
}

function SearchController($scope, Search, $window, $timeout){

    $scope.position = '28.7041,77.1025';

    $scope.countries = [
        "Canada",
        "Turkey",
        "Italy",
        "Czech Republic",
        "Hungary",
        "Luxembourg",
        "France",
        "Slovakia",
        "Ireland",
        "Argentina",
        "Norway",
        "Bahrain",
        "Saudi Arabia",
        "Australia",
        "Singapore",
        "Iceland",
        "Czechia",
        "China",
        "Belgium",
        "Germany",
        "Hong Kong",
        "Taiwan",
        "Spain",
        "Netherlands",
        "Denmark",
        "Poland",
        "Finland",
        "Israel",
        "United States",
        "Morocco",
        "Sweden",
        "Croatia",
        "Thailand",
        "Switzerland",
        "Russia",
        "Brazil",
        "Portugal",
        "Estonia",
        "Mexico",
        "Egypt",
        "United Arab Emirates",
        "South Africa",
        "India",
        "United Kingdom",
        "Malaysia",
        "Austria",
        "Japan",
        "South Korea"
    ];
    $scope.countries.sort()

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){
          $scope.$apply(function(){
            $scope.position = position.coords.latitude + "," +  position.coords.longitude;
          });
        });
    }

    $scope.bymoney = function(money, country) {
		Search.post({money: money, location: $scope.position, country: country}, function(data) {
			$window.location = '/result/' + data.id;
		});
    }

    tick();

    function tick() {
        $scope.image = travelPics();
        var timer  = $timeout(tick, 3000);
    }


    var timer  = $timeout(tick, 3000);
    $scope.$on("$destroy", function() {
        if (timer) {
            $timeout.cancel(timer);
        }
    });

}

function TripController($scope, Trip)
{
    var trips = Trip.get({}, function(data){
        $scope.data = data;
    })
}

function ResultController($scope, $routeParams, $timeout, Result, Remove)
{
	var queryResults = Result.get({queue_id: $routeParams.queue_id}, function(data) {
        $scope.data = data;
    });

    function tick() {
        $scope.quote = waitmessages();

        var queryResults = Result.get({queue_id: $routeParams.queue_id}, function(data) {
            $scope.data = data;
            if ($scope.data.status=='success')
            {
                $timeout.cancel(timer);
            }
            else{
                var timer  = $timeout(tick, 3000);
            }
        });
    }

    tick();
    $scope.$on("$destroy", function() {
        if (timer) {
            $timeout.cancel(timer);
        }
    });

    $scope.removecity = function(id, key) {
        Remove.get({'id':id, 'number': key}, function(data){
            $scope.data = data;
        });
    }

}

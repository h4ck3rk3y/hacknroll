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
        "The gladdest moment in human life, me thinks, is a departure into unknown lands."
	]
	var quote = securityquotes[Math.floor(Math.random() * securityquotes.length)];
    return quote;
}

function SearchController($scope, Search, $window, $timeout){

    $scope.position = '1.3521,103.8198';

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){
          $scope.$apply(function(){
            $scope.position = position.coords.latitude + "," +  position.coords.longitude;
          });
        });
    }

    $scope.go_places = function(money) {
		Search.post({money: money, location: $scope.position}, function(data) {
			$window.location = '/result/' + data.id;
		});
    }
}

function ResultController($scope, $routeParams, $timeout, Result)
{
	var queryResults = Result.get({queue_id: $routeParams.queue_id}, function(data) {
        $scope.data = data;
    });

    function tick() {
        $scope.quote = waitmessages();
        var queryResults = Result.get({queue_id: $routeParams.queue_id}, function(data) {
            $scope.data = data;
            if ($scope.data.status!='inprocess')
            {
                $timeout.cancel(timer);
            }
            var timer  = $timeout(tick, 3000);
        });
    }

    var timer  = $timeout(tick, 3000);
    $scope.$on("$destroy", function() {
        if (timer) {
            $timeout.cancel(timer);
        }
    });
}

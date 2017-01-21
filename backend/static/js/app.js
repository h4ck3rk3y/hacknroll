'use strict';

angular.module('AngularFlask', ['angularFlaskServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/search.html',
			controller: SearchController
		})
		.when('/result/:queue_id', {
			templateUrl: '/static/partials/result.html',
			controller: ResultController
		})
		.when('/mytrips', {
			templateUrl: '/static/partials/trips.html',
			controller: TripController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
	.filter('clean_date', function() {
	return function(input) {
		if(input != undefined)
			return input.replace('GMT', '');
		else
			return '';
	}
});
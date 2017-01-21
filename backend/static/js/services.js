'use strict';

angular.module('angularFlaskServices', ['ngResource'])
	.factory('Search', function($resource){
		return $resource('/api/maketrip/', {}, {
			post: {
				method: 'POST',
			}
		})
	})
	.factory('Result', function($resource){
		return $resource('/api/result/:queue_id', {}, {
			query : {
				method: 'GET',
				params: {'queue_id': ''}
			}
		})
	})
;




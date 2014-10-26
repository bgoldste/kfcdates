

Ember.Application.initializer({
  name: 'userapp',
  initialize: function(container, application) {
  	
  }
});

App = Ember.Application.create();

App.ApplicationAdapter = DS.RESTAdapter.extend({
    host: 'http://kfc.fastfooddates.com'
});

//App.ApplicationAdapter = DS.FixtureAdapter.extend({});

App.ApplicationStore = DS.Store.extend({
  revision: 11,
  url: "http://kfc.fastfooddates.com"
});


App.set('deferredMap', Ember.RSVP.defer());
MapInitialize = function() {
	App.get('deferredMap').resolve("Map Loaded");	 
}
function OnMapUpdate(map, event, center, viewport) {
    if (event.eventType == "MARKER_CLICKED") {
    	//App.set('lastLocationPicked', event.eventSource);
    	map.appContext.controller.content.slot.set('locationLatitude', event.eventSource.position.lat());
    	map.appContext.controller.content.slot.set('locationLongitude', event.eventSource.position.lng());
    	map.appContext.controller.content.slot.set('address', event.eventSource.title);
    }
}


App.Router.map(function() {
  this.route('login');
  this.route('profile');
  this.route('setup');
  this.route('confirmation');
  this.route('dates');
  this.route('proposal');
  this.route('slots');
  this.route('date');
  this.route('waiting');
});

App.User = DS.Model.extend({  	
  	photoURL: DS.attr('string'),
  	username: DS.attr('', {defaultValue: ''}),
  	firstname: DS.attr('', {defaultValue: ''}),
  	lastname: DS.attr('', {defaultValue: ''}),
	facebookID: DS.attr('', {defaultValue: ''}),
	locationLatitude: DS.attr('', {defaultValue: ''}),
	locationLongitude: DS.attr('', {defaultValue: ''}),
	isBuyer: DS.attr('', {defaultValue: ''}),
	isRecipient: DS.attr('', {defaultValue: ''}),
	email: DS.attr('', {defaultValue: ''}),
	slots: DS.hasMany('slot', { async: true , inverse: 'buyer'}),
	proposals: DS.hasMany('proposals', { async: true, inverse: 'buyer' }),
	dates: DS.hasMany('date', { async: true, inverse: 'buyer' })
});

App.Meetup = DS.Model.extend({
	locationLatitude: DS.attr('', {defaultValue: ''}),
	locationLongitude: DS.attr('', {defaultValue: ''}),
	address: DS.attr('', {defaultValue: ''}),
	date: DS.attr('', {defaultValue: ''}),
	time: DS.attr('', {defaultValue: ''}),
	state: DS.attr('', {defaultValue: ''}),
	buyer: DS.hasMany('user', { async: true }),
	recipient: DS.hasMany('user', { async: true }),
	kfcAddress: function() {
		if (this.get('address'))
			return 'KFC - ' + this.get('address');
	}.property('address'),
	moment: function (key, value, previousValue) {
		 if (arguments.length > 1 && value) {
		  this.set('date', moment(value*1000).format("MM/DD/YYYY"));
		}
		if (moment(this.get('date'), ["MM/DD/YYYY"], true).isValid())
			return moment(this.get('date'), ["MM/DD/YYYY"]);
		else
			return '';
	}.property('date')
});

App.Slot = App.Meetup.extend({});
App.Proposal = App.Meetup.extend({});
App.Date = App.Meetup.extend({});

App.Date.reopenClass({
  FIXTURES: [
    { id: 55, locationLatitude: '61.4', locationLongitude: '120.2', address: 'kfc down the road', time: '11:30', date: '01/01/2015', state: 'booked', buyer: [1], recipient: [2] },
    { id: 44, locationLatitude: '61.4', locationLongitude: '120.2', address: 'kfc up the road', time: '12:30', date: '01/01/2015', state: 'booked', buyer: [1], recipient: [3] },
  ]
});


App.Proposal.reopenClass({
  FIXTURES: [
    { id: 66, locationLatitude: '61.4', locationLongitude: '120.2', address: 'kfc down the road', time: '11:30', date: '01/01/2015', state: 'proposed', buyer: [1] },
    { id: 77, locationLatitude: '61.4', locationLongitude: '120.2', address: 'kfc up the road', time: '12:30', date: '01/01/2015', state: 'proposed', buyer: [1] },
  ]
});

App.User.reopenClass({
  FIXTURES: [
    { id: 1, photoURL: "http://x.com/x.jpg", username: 'dioptre', firstname: 'Andy', lastname: 'G', facebookID: 'mrdioptre', locationLatitude: '61.4', locationLongitude: '120.2', isBuyer: true, isRecipient: false, email: 'dioptre@gmail.com', meetups: [55,44] },
    { id: 2, firstname: 'Shirley' , lastname: 'H'},
    { id: 3, firstname: 'Michelle' , lastname: 'W'}
  ]
});

App.IndexRoute = Ember.Route.extend({
  redirect: function() {
   	this.transitionTo('profile'); 
  }
});



App.ProfileRoute = Ember.Route.extend({
	model: function() {
		return Ember.RSVP.hash({
			users: this.store.find('user', {id: null})
		});
	},
	afterModel: function (model) {
		model.user = model.users.get('firstObject');
	}
});

App.ProfileController = Ember.ObjectController.extend({
	actions: {
		makeBuyer: function () {
			this.set('model.user.isBuyer', true);
			this.set('model.user.isRecipient', false);
		},
		makeRecipient: function() {
			this.set('model.user.isBuyer', false);
			this.set('model.user.isRecipient', true);
		}
	}
});


App.SetupRoute = Ember.Route.extend({
	model: function() {
		return Ember.RSVP.hash({
			users: this.store.find('user', {id: null}),
			slot: this.store.createRecord('slot'),
			dates: this.store.find('date')
		});
	},
	afterModel: function(model) {
		if (model.dates && model.dates.content && model.dates.content.length > 0)
			this.transitionTo('confirmation');
		model.user = model.users.get('firstObject');
	}
});

App.SetupView = Em.View.extend({
  didInsertElement: function(){
  	var _this = this;
	Ember.RSVP.allSettled([App.get('deferredMap')]).then(function (array) {
		Ember.run.later(_this, function () { 
			Ember.run.scheduleOnce('afterRender', this, function() {
				var setupMap = function (position) {
					var m = SetupMap('date-map'); 
					m.appContext = _this;
					if (position)
						m.setCenter({ lat: position.coords.latitude, lng: position.coords.longitude });
					m.setZoom(10);
					var foundLocations = function(results, status) {
						$.each(results, function (i,v) {
							AddMarker(m, v.geometry.location, false, v.vicinity, v.id);							
						});
					}
					var service = new google.maps.places.PlacesService(m);
  					service.nearbySearch({
  						location: new google.maps.LatLng(m.getCenter().lat(),m.getCenter().lng()), 
  						keyword: 'kfc',
  						radius: '15000',
    					types: ['store','food']
  					}, foundLocations);

				}
			    if (navigator.geolocation) {
					navigator.geolocation.getCurrentPosition(setupMap)
				}	
				else {
					setupMap(null);
				}

			    
			  });
		}, 750);

	});

  }
});

App.SetupController = Ember.ObjectController.extend({
	times: [
	  { label: '10:00', value: '1000' },
	  { label: '10:30', value: '1030' },
	  { label: '11:00', value: '1100' },
	  { label: '11:30', value: '1130' },
	  { label: '12:00', value: '1200' },
	  { label: '12:30', value: '1230' },
	  { label: '13:00', value: '1300' },
	  { label: '13:30', value: '1330' },
	  { label: '14:00', value: '1400' },
	  { label: '14:30', value: '1430' },
	  { label: '15:00', value: '1500' },
	  { label: '15:30', value: '1530' },
	  { label: '16:00', value: '1600' },
	  { label: '16:30', value: '1630' },
	  { label: '17:00', value: '1700' },
	  { label: '17:30', value: '1730' },
	  { label: '18:00', value: '1800' },
	  { label: '18:30', value: '1830' },
	  { label: '19:00', value: '1900' },
	  { label: '19:30', value: '1930' },
	  { label: '20:00', value: '2000' },
	  { label: '20:30', value: '2030' },
	  { label: '21:00', value: '2100' },
	  { label: '21:30', value: '2130' },
	  { label: '22:00', value: '2200' }
	],
	isDisabled: function () {
		return !(this.get('model.slot.locationLatitude') && this.get('model.slot.locationLongitude') && this.get('model.slot.time') && this.get('model.slot.date'))
	}.property('model.slot.locationLatitude','model.slot.locationLatitude','model.slot.date','model.slot.time'),
	actions: {
		invite: function () {
			this.get('model.slot').save();
			this.transitionToRoute('waiting');
		}
	}

});


App.ProposalRoute = Ember.Route.extend({
	model: function() {
		return Ember.RSVP.hash({
			proposals: this.store.find('proposal'),
			dates: this.store.find('date')
		});
	},
	afterModel: function(model) {
		if (model.dates && model.dates.content && model.dates.content.length > 0)
			this.transitionTo('confirmation');
	}
});

App.ProposalController = Ember.ObjectController.extend({
	actions: {
		acceptDate: function (id) {
			proposal = this.store.getById('proposal',id);
			proposal.set('state','accepted');
			proposal.save();
			this.transitionToRoute('confirmation'); 
		}
	}
});

App.WaitingRoute = Ember.Route.extend({
	model: function() {
		return this.store.find('date');
	},
	afterModel: function(model) {
		if (model && model.content && model.content.length > 0)
			this.transitionTo('confirmation'); 
		else {
			setTimeout("location.reload(true);", 30000);
		}
	}
});

App.ConfirmationRoute = Ember.Route.extend({
	model: function() {
		return Ember.RSVP.hash({
			dates: this.store.find('date')
		});
	},
	afterModel: function(model) {
		if (model.dates && model.dates.content && model.dates.content.length > 0)
			model.date = model.dates.get('firstObject');
		//else
		//	this.transitionTo('profile'); 
	}
});

App.ConfirmationController = Ember.ObjectController.extend({
	actions: {
		cancelDate: function (id) {
			kfc_date = this.get('model.date');
			kfc_date.deleteRecord();
			kfc_date.save();
			
			this.transitionTo('profile'); 
		}
	}
});

// App.ArticleController = Ember.ObjectController.extend({
// 	// Title: function (key, value, previousValue) {
// 		// // setter
// 		// if (arguments.length > 1) {
// 		  // var title = this.get('model');
// 		  // title.set('title', value);
// 		  // title.save();
// 		// }

// 		// // getter
// 		// return this.get('model.title');
// 	// }.property('model.title'),
// 	// actions: {

// 	// }
// });
// App.ArticleRoute = Ember.Route.extend({
// 	beforeModel: function() {
// 		// $.get('/articles.php', function(data) {
// 			// App.articlesController.set('content', data);
// 		// });
// //	    Ember.run.scheduleOnce('sync', App, afterRenderEvent);

// 	},
// 	model: function() {
// 		return  this.store.findAll('article');
// 	}
// });

//DS.RESTAdapter.reopen({
  //buildURL: function(klass, id) {
  //if (id)
	//return '/' + klass + 's.php?id=' + id;
	//else
	//return '/' + klass + 's.php';
    // var urlRoot = Ember.get(klass, 'url');
    // if (!urlRoot) { throw new Error('Ember.RESTAdapter requires a `url` property to be specified'); }

    // if (!Ember.isEmpty(id)) {
      // return urlRoot + "/" + id;
    // } else {
      // return urlRoot;
    // }
  //}
//});



// App.ApplicationSerializer = DS.RESTSerializer.extend({
    // primaryKey: 'id',
    // serializeId: function(id) {
        // return id.toString();
    // }
// });

// App.Article = DS.Model.extend({
//   	title: DS.attr('string'),
//   	partners_firstname: DS.attr('', {defaultValue: ''}),
// 	dob: DS.attr('', {defaultValue: ''}),
// 	gender: DS.attr('', {defaultValue: ''}),
// 	date_moment: function (key, value, previousValue) {
// 		 if (arguments.length > 1) {
// 		  this.set('date_date', value.format("DD/MM/YYYY"));
// 		}
// 		if (moment(this.get('date_date'), ["DD/MM/YYYY"], true).isValid())
// 			return moment(this.get('date_date'), ["DD/MM/YYYY"]);
// 		else
// 			return '';
// 	}.property('date_date')
// });
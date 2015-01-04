Anovelmous.Router.map(function() {
   this.resource('read', function() {
       this.route('live');
       this.route('chapter');
   });
   this.resource('about', {'path': '/about'});
   this.resource('sidebar', {'path': '/sidebar'});
});

Anovelmous.IndexRoute = Ember.Route.extend({
    beforeModel: function() {
        this.transitionTo('read.live');
    }
});

Anovelmous.ReadRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('live');
    }
});

Anovelmous.ReadLive = Ember.Route.extend({
    model: function() {
        return this.store.find('live');
    },
    renderTemplate: function(controller) {
        this.render('read/live', {controller: controller});
    }
});

Anovelmous.ReadChapterRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('chapter');
    }
});

Anovelmous.SidebarRoute = Ember.Route.extend({
    renderTemplate: function() {
        this.render({ outlet: 'sidebar' });
    }
});

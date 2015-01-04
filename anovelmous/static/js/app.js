window.Anovelmous = Ember.Application.create();

Ember.View.reopen({
    didInsertElement : function() {
        this._super();
        Ember.run.scheduleOnce('afterRender', this, this.afterRenderEvent);
    },
    afterRenderEvent : function() {
        $(document).foundation('offcanvas', 'reflow');
    }
});

Anovelmous.ApplicationAdapter = DS.FixtureAdapter.extend();

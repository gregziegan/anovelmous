Anovelmous.Live = DS.Model.extend({
    text: DS.attr('string')
});

Anovelmous.Live.reopenClass({
  FIXTURES: [
    {
        id: 1,
        text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ornare mi vel odio condimentum, eget ' +
        'fringilla erat ornare. Proin et posuere mauris. Nunc urna ligula, aliquet in hendrerit quis, aliquet vitae ' +
        'libero. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec id ' +
        'ante egestas, ornare ipsum placerat, tempus lorem. Nunc at eros vel mi venenatis fringilla vel sed lacus. ' +
        'Curabitur sodales erat eros, in iaculis nulla finibus ac. Pellentesque habitant morbi tristique senectus ' +
        'et netus et malesuada fames ac turpis egestas. Aliquam tincidunt lectus vitae faucibus posuere. Morbi ' +
        'maximus nisi sit amet nunc gravida, non sodales nulla gravida.'
    },
    {
        id: 2,
        text: 'It was the worst of times it was the best of times...'
    }
  ]
});


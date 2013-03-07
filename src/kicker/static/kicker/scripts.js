$(function() {
  var $times = $('time');

  $times.each(function(i, time) {
    $(time).html(moment($(time).html(), 'YYYY-MM-DDTHH:mm:ssZZ').fromNow());
  });
});

// custom javascript
console.log("The cake is a lie!");

function navHighlight() {
  $( 'a[href^="/' + location.pathname.split("/")[1] + '"]').parent().addClass('active');
}

$( document ).ready(function() {
  navHighlight();
});


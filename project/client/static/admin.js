// custom javascript
console.log("The cake is a lie!");

function navHighlight() {
  console.log("I MADE IT");
  $( 'a[href^="/' + location.pathname.split("/")[1] + '"]').parent().addClass('active');
  console.log(location.pathname);
  console.log(window.location.href);
}

$( document ).ready(function() {
  console.log('Is anyone out there?');
  navHighlight();
  console.log("I've made it this far");
});


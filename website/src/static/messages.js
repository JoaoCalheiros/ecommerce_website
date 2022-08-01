/* Make Flask flash messages close after 3.5 seconds */

$(document).ready(function() {
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 3500); });
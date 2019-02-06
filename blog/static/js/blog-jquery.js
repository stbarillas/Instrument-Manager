
$(document).ready( function() {

    $('td:contains("No Record")').css('color', 'red');
    $('td:contains("Not Required")').css('color', '#00A1E4');
    $('td:contains("minutes")').css('color', '#FD9F12');
    $('td:contains("minute")').css('color', '#FD9F12');
    $('td:contains("0 minutes")').css('color', 'red');
    $('td:contains("hours")').css('color', '#FD9F12');
    $('td:contains("hour")').css('color', '#FD9F12');
    $('td:contains("days")').css('color', '#FD9F12');
    $('td:contains("day")').css('color', '#FD9F12');
    $('td:contains("0 Days")').css('color', 'red');
    $('td:contains("weeks")').css('color', 'green');
    $('td:contains("week")').css('color', 'green');
    $('td:contains("months")').css('color', 'green');
    $('td:contains("month")').css('color', 'green');
    $('td:contains("year")').css('color', 'green');
    $('td:contains("years")').css('color', 'green');
});
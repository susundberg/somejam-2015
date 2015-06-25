(function() {

// Localize jQuery variable
var jQuery;

var link_tag = document.createElement('link');
  link_tag.setAttribute("type", "text/css");
  link_tag.setAttribute("rel", "stylesheet");
  link_tag.setAttribute("href", "https://cdn.rawgit.com/yahoo/pure-release/v0.6.0/pure-min.css");
  link_tag.onload = styleLoadHandler;
  (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(link_tag);

// From http://alexmarandon.com/articles/web_widget_jquery/
var script_tag = document.createElement('script');
  script_tag.setAttribute("type", "text/javascript");
  script_tag.setAttribute("src", "https://code.jquery.com/jquery-1.11.1.min.js");
  script_tag.onload = scriptLoadHandler;
  (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);

// Called once jQuery has loaded 
function scriptLoadHandler() {
    // Restore $ and window.jQuery to their previous values and store the
    // new jQuery in our local jQuery variable
    jQuery = window.jQuery.noConflict(true);
    // Call our main function
    main(); 
}

function styleLoadHandler() {
  
}

function main() { 
jQuery(document).ready(function($) { 
  var now = new Date().getTime();
  
  var api_key  = "key=AIzaSyD4q8fMwUE0IsaVJ4vLS2vbl1qHvDx0ERs";
  var base_url = "https://www.googleapis.com/calendar/v3/calendars/l7fs5ste4bllsanrtclmbnpvks%40group.calendar.google.com/events";
  
  filter_max   = new Date( now + 2*24*60*60*1000 );
  filter_min   = new Date( now );

  params = ["timeMin=" + encodeURIComponent(  filter_min.toISOString() ), "maxResults=4", "orderBy=startTime","singleEvents=true", api_key ]
  get_events_url = base_url + "?" + params.join("&")
  
  // We do not get the location specification on the 'list' so we need to get each event
  // by its id. This creates lots of queries .. 
  function event_get_location( event_id )
  {
     var params = [ api_key, "fields=description,location" ];
     var get_url = base_url + "/" + event_id + "/" +  "?" + params.join("&");
     $.getJSON( get_url, function( data ) { 
       var target_url = data["location"];
       // Make sure we dont get relative links .. 
       if ( target_url.slice(0,4) != "http" )
       {
         target_url = "http://" + target_url;
       }
       var elem = $("#" + event_id );   
       elem.attr("href",  target_url );
       elem.attr("title", data["description"]);
     } );
  }
  
  var current_day = Math.floor( now / 1000 / 60 / 60 / 24); 
  $.getJSON( get_events_url , function( data ) {
    var table_items = [];
    $.each( data["items"], function( key, val ) {

       var date_start = new Date( val.start.dateTime );
       var date_end   = new Date( val.end.dateTime );
       var event_start_date = Math.floor( date_start / 1000 / 60 / 60 / 24); 
       var str_desc = " "

       function pad2(number) { return (number < 10 ? '0' : '') + number };
       function dformat( d ) { return pad2(d.getHours()) + ":" + pad2(d.getMinutes()) };
       
       // Produce the date of the event if not today
       if ( event_start_date != current_day )
       {
         str_desc = pad2( date_start.getDate() ) + "." ;
       }
       
       var elems = [ "<a class='pure-button' id='"+val.id+"'> " + val.summary + "</a>" , str_desc, dformat(date_start),dformat(date_end) ];
       table_items.push( "<td>" + elems.join("</td><td>") + "</td>" );
       event_get_location( val.id );
    });
    $("#mistaapua").append("<table class='pure-table'> <tbody><tr>" + table_items.join("</tr><tr>") + "</tr></table>" );
   }); // get json
     
  }); // document ready
 } // function main
})(); // anom function, and call


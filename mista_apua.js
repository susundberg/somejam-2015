(function() {

// Localize jQuery variable
var jQuery;


function create_link_tag( url )
{
  var link_tag = document.createElement('link');
  link_tag.setAttribute("type", "text/css");
  link_tag.setAttribute("rel", "stylesheet");
  link_tag.setAttribute("href", url );
  return link_tag;
}

// From http://alexmarandon.com/articles/web_widget_jquery/
var script_tag = document.createElement('script');
  script_tag.setAttribute("type", "text/javascript");
  script_tag.setAttribute("src", "https://code.jquery.com/jquery-1.11.1.min.js");
  script_tag.onload = scriptLoadHandler;

var doc_head = (document.getElementsByTagName("head")[0] || document.documentElement);
doc_head.appendChild( create_link_tag( "https://cdn.rawgit.com/yahoo/pure-release/v0.6.0/pure-min.css" ) );
doc_head.appendChild( create_link_tag( "https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css" ) );
doc_head.appendChild(script_tag);

// Called once jQuery has loaded 
function scriptLoadHandler() {
    // Restore $ and window.jQuery to their previous values and store the
    // new jQuery in our local jQuery variable
    jQuery = window.jQuery.noConflict(true);
    // Call our main function
    main(); 
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
     var params = [ api_key, "fields=description,location,colorId,kind,transparency,visibility" ];
     var get_url = base_url + "/" + event_id + "/" +  "?" + params.join("&");
     $.getJSON( get_url, function( data ) { 
       var elem = $("#" + event_id );   
       console.log(JSON.stringify(data));
       var target_url = data["location"];
       if ( target_url ) // Avoid errors if somebody forgets to update the location
       {
          // Make sure we dont get relative links .. 
          if ( target_url.slice(0,4) != "http" )
          {
            target_url = "http://" + target_url;
          }
          elem.attr("href",  target_url );
       }
       elem.attr("title", data["description"]);
     } );
  }
  
  $.getJSON( get_events_url , function( data ) {
    var table_items = [];
    $.each( data["items"], function( key, val ) {

       var date_start = new Date( val.start.dateTime );
       var date_end   = new Date( val.end.dateTime );
       
       if ( date_start > now || now > date_end )
       {
         // skip all events that are not open right now
         return;
       }
     
       var elems = [ "<a class='pure-button' id='"+val.id+"' style='width:100%;'> " + val.summary + "</a>" , "<i class='fa fa-users'></i>" ];
       table_items.push( "<td style='border-left:none;'> " + elems.join("</td><td style='border-left:none;'>") + "</td>" );
       event_get_location( val.id );
    });
    $("#mistaapua").append("<table class='pure-table'> <tbody><tr>" + table_items.join("</tr><tr>") + "</tr></table>" );
   }); // get json
     
  }); // document ready
 } // function main
})(); // anom function, and call


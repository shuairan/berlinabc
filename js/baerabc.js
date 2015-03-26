var TILES_URL = "http://a.tile.thunderforest.com/transport/{z}/{x}/{y}.png";

var INITIAL_LOCATION = [52.518611, 13.408333];
var INITIAL_ZOOM = 12;
var ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> ' +
                  'contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">' +
                  'CC-BY-SA</a>. Tiles &copy; <a href="http://cartodb.com/attributions">' +
                  'CartoDB</a>';

var authors = ['katrin-roenicke', 'holgerklein'];
var authors_data = {
    'katrin-roenicke' : 'Katrin Rönicke',
    'holgerklein' : 'Holger Klein',
};

var map;
var groups = {};
var icons = {};
L.AwesomeMarkers.Icon.prototype.options.prefix = 'fa';
icons['holgerklein'] = L.AwesomeMarkers.icon({markerColor: 'darkpurple', icon: 'train'});
icons['katrin-roenicke'] = L.AwesomeMarkers.icon({markerColor: 'orange', icon: 'train'});
icons['both'] = L.AwesomeMarkers.icon({markerColor: 'darkgreen', icon: 'train'});


/*
 * prepare data
 */
$.each(authors, function( index, author ) {
    groups[author] = L.layerGroup();
});
groups['both'] = L.layerGroup();

/*
 * Create pop html code
 */
function getPopupHTML(station) {
    s = '<div class="popup">';
    s += '<h1><a href= ' + station['wikipedia_link'] + '>' + station['name'] + '</h1> </a>';
    
    for (var article in station["articles"]) {
        var data = station["articles"][article];
        s += '<div class="author-' + data['author'] + '">';
        s += '<h2><a href="' + data['link'] + '">' + data['title'] + '</a></h2>';
        s += '<span class="popup-authorinfo"><em>' + data['published'] + '</em> von <strong>' + authors_data[data['author']] + '</strong></span>';
        //s += '<div class="popup-summary">' + data['description'] + '</div>';
        s += '</div>';
    }
    
    s += '</div>';
    return s;
}

/*
 * Initialize map.
 */
function initMap() {
    var tiles = new L.TileLayer(TILES_URL, {attribution: ATTRIBUTION});
    map = new L.Map('map').addLayer(tiles).setView(INITIAL_LOCATION, INITIAL_ZOOM);
}

/*
 * Initialize layer controls.
 *
 * Controls which serve no purpose are disabled. For example, if
 * currently no markets are open then the corresponding radio
 * button is disabled.
 */
function initControls() {
    $.each(groups, function( index, group ) {
        var count = group.getLayers().length;
        var elem_id = '#'+index;
        if (count === 0) {
            // No markets today or all of today's markets currently open
            $(elem_id).attr('disabled', true);
        }
        else {
            $(elem_id).attr('checked', true);
        }
        
    });
    $("input[name='authors[]']").change(updateLayers);
}


/*
 * Update layer visibility according to layer control settings.
 */
function updateLayers(e) {
    var value = document.querySelector('[name="authors[]"]:checked').value;
    
    if (e) {
        author = $(this).val();
        if (this.checked) {
             map.addLayer(groups[author]);
        }
        else {
             map.removeLayer(groups[author]);
        }
    }
}

function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

/*
 * Create map markers from JSON article data.
 */
function initMarkers(json) {
    for (var station in json) {
        var stationData = json[station];
        //console.log(data);
        
        var authors = [];
        for (var article in stationData["articles"]) {
            var data = stationData["articles"][article];
            authors.push(data['author']);
        }
        
        authors = authors.filter(onlyUnique)
        var author = authors.length == 1 ? authors[0] : 'both';
        
        if (stationData['coordinates']) {
            var marker = L.marker(stationData['coordinates']);
            var popup = getPopupHTML(stationData)
            marker.bindPopup(popup);
        
            marker.setIcon(icons[author]);
            groups[author].addLayer(marker);
        }
    }
}


/*
 * Initialize legend.
 */
function initLegend() {
    var legend = L.control({position: 'bottomright'});
    legend.onAdd = function (m) {
        return L.DomUtil.get('legend');
    };
    legend.addTo(map);
}

$(document).ready(function() {
    initMap();
    initLegend();
    $.getJSON("markers.json", function(json) {
        initMarkers(json);
        initControls();
        $.each(groups, function( index, group ) {
            map.addLayer(group);
        });
        updateLayers();
    });
});

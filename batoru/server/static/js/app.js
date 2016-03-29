namespace = '/fight';

// the socket.io documentation recommends sending an explicit package upon connection
// this is specially important when using the global namespace
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
var id = 0;

// Status window
socket.on('fight status', function(msg) {
    $('#status').prepend($('<div/>').text(msg.data).html() + '<br>');
});

// Log window
socket.on('fight log', function(msg) {
    $('#log_text').prepend($('<small/>').text(msg.data).html() + '<br>');
});

// Battle figures
socket.on('fight front', function(json) {
    var player_window = JSON.parse(json.data);
    if ($( "#player" ).val() == player_window.name) {
        $('#player_window div.progress_holder').empty();
        $('#player_window div.progress_holder').prepend(
            $('<div/>').text(player_window.name).html()
            + '<br>'
            + '<div class="progress">'
            + '<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="'
            + player_window.hit_points
            + '" aria-valuemin="0" aria-valuemax="'
            + player_window.hit_points
            + '" style="width: 100%">'
            + '</div>'
            + '</div>'
        );
    } else {
        $('#opponent_window div.progress_holder').empty();
        $('#opponent_window div.progress_holder').prepend(
            $('<div/>').text(player_window.name).html()
            + '<br>'
            + '<div class="progress">'
            + '<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="'
            + player_window.hit_points
            + '" aria-valuemin="0" aria-valuemax="'
            + player_window.hit_points
            + '" style="width: 100%">'
            + '</div>'
            + '</div>'
        );
    }
});

// Battle events
socket.on('fight scroll', function(json) {
    var fight_scroll = JSON.parse(json.data);
    loser_hitpoints = fight_scroll.loser.hit_points;
    percent = 0;
    bar_class = '';
    old_class = '';

    count = Math.floor((Math.random() * 3));

    var images = [];
    images[0] = "bam";
    images[1] = "puff";
    images[2] = "splash";
    images[3] = "swooosh";

    $('#player_window img').each(function(){
        $(this).hide();
    });

    $('#opponent_window img').each(function(){
        $(this).hide();
    });

    if (fight_scroll.winner.name == $( "#player" ).val()) {
        max = $('#opponent_window .progress-bar').attr('aria-valuemax');
        divider = Math.round(max / 100);
        if ( loser_hitpoints > 0 ) {
            percent = Math.round(loser_hitpoints / divider);
        }
        if ( percent < 60 ) {
            bar_class = 'progress-bar-warning';
        }
        if ( percent < 30 ) {
            bar_class = 'progress-bar-danger';
            old_class = 'progress-bar-warning';
        }
        $('#opponent_window .progress-bar').addClass(bar_class).removeClass(old_class);
        $('#opponent_window .progress-bar').attr('aria-valuenow', loser_hitpoints);
        $('#opponent_window .progress-bar').width(percent + '%');

        $('#opponent_window img.'+images[count]).show();
    } else {
        max = $('#player_window .progress-bar').attr('aria-valuemax');
        divider = Math.round(max / 100);
        if ( loser_hitpoints > 0 ) {
            percent = Math.round(loser_hitpoints / divider);
        }
        if ( percent < 60 ) {
            bar_class = 'progress-bar-warning';
        }
        if ( percent < 30 ) {
            bar_class = 'progress-bar-danger';
            old_class = 'progress-bar-warning';
        }
        $('#player_window .progress-bar').addClass(bar_class).removeClass(old_class);
        $('#player_window .progress-bar').attr('aria-valuenow', loser_hitpoints);
        $('#player_window .progress-bar').width(percent + '%');

        $('#player_window img.'+images[count]).show();
    }
});

// Battle player list.
socket.on('fight players', function(msg) {
    $('#playerlist').empty()
    $('#playerlist').append($("<option></option>")
         .attr('value','monster')
         .text('monster'));
    $.each( msg.player, function( key, value ) {
      if (key != $( "#player" ).val()) {
          $('#playerlist').append($("<option></option>")
             .attr("value",value)
             .text(key));
      }
    });
});

// event handler for new connections
socket.on('connect', function() {
    socket.emit('my message', {data: 'I\'m connected!'});
    id = socket.id;
});

$( document ).ready(function() {

    $( "#fightbox" ).hide()

    $( "#join" ).click(function() {
        $( "#fightbox" ).show()
        $( "#joinbox" ).hide()
        $('#log_text').empty();
        $('#status').empty();
        $('#fightbox').prepend('<h2>' + $('<div/>').text($( "#player" ).val()).html() + '</h2>');

        socket.emit('join', {room: 'players', player: $( "#player" ).val(), player_room: id});
        return false;
    });

    $( "#fight" ).click(function() {
        // $('#log_text').empty();
        $opponent = $('#playerlist').find(":selected").text();
        socket.emit('fight', {room: id, data: $opponent, player: $( "#player" ).val()});
    });

    $( "#level" ).click(function() {
        // $('#log_text').empty();
        socket.emit('fight', {room: id, data: 'level', player: $( "#player" ).val()});
    });
});

$(document).idle({
    onIdle: function(){
      socket.emit('leave', {room: 'players', player: $( "#player" ).val(), player_room: id});
      $('#status').prepend($('<div/>').text('You are now marked as idle.').html() + '<br>');
    },
    onActive: function(){
      socket.emit('join', {room: 'players', player: $( "#player" ).val(), player_room: id});
    },
    idle: 60000
})
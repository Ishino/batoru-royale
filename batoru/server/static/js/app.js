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
            '<div class="margin-bottom">'
            + '<span class="badge">' + player_window.level + '</span> ' + $('<div/>').text(player_window.name).html()
            + '</div>'
            + '<div class="progress">'
            + '<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="'
            + player_window.hit_points
            + '" aria-valuemin="0" aria-valuemax="'
            + player_window.hit_points
            + '" style="width: 100%">'
            + '</div>'
            + '</div>'
            + '<div id="skill_points">Skill points: <span class="label label-info">' + player_window.skill_points + '</span></div>'
        );
    } else {
        $('#opponent_window div.progress_holder').empty();
        $('#opponent_window div.progress_holder').prepend(
            '<div class="margin-bottom">'
            + '<span class="badge">' + player_window.level + '</span> ' + $('<div/>').text(player_window.name).html()
            + '</div>'
            + '<div class="progress">'
            + '<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="'
            + player_window.hit_points
            + '" aria-valuemin="0" aria-valuemax="'
            + player_window.hit_points
            + '" style="width: 100%">'
            + '</div>'
            + '</div>'
            + '<div id="skill_points">Skill points: <span class="label label-info">' + player_window.skill_points + '</span></div>'
        );
    }
});

// Battle events
socket.on('fight scroll', function(json) {

    var fight_scroll = JSON.parse(json.data);

    var player = fight_scroll.winner
    var opponent = fight_scroll.loser

    if (fight_scroll.loser.name == $( "#player" ).val()) {
        player = fight_scroll.loser
        opponent = fight_scroll.winner
    }

    player_percent = 0;
    opponent_percent = 0;
    player_bar_class = '';
    player_bar_class = '';
    opponent_bar_class = '';
    opponent_bar_class = '';

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

    opponent_max = $('#opponent_window .progress-bar').attr('aria-valuemax');
    opponent_divider = Math.round(opponent_max / 100);
    if (opponent.hit_points > 0) {
        opponent_percent = Math.round(opponent.hit_points / opponent_divider);
    }
    if ( opponent_percent > 60 ) {
        opponent_bar_class = 'progress-bar-default';
    }
    if ( opponent_percent < 60 ) {
        opponent_bar_class = 'progress-bar-warning';
    }
    if ( opponent_percent < 30 ) {
        opponent_bar_class = 'progress-bar-danger';
    }

    $('#opponent_window .progress-bar').attr('class', "progress-bar progress-bar-striped active " + opponent_bar_class );
    $('#opponent_window .progress-bar').attr('aria-valuenow', opponent.hit_points);
    $('#opponent_window .progress-bar').width(opponent_percent + '%');
    $('#opponent_window #skill_points span').empty().prepend($('<div/>').text(opponent.skill_points).html());

    player_max = $('#player_window .progress-bar').attr('aria-valuemax');
    player_divider = Math.round(player_max / 100);
    if (player.hit_points > 0) {
        player_percent = Math.round(player.hit_points / player_divider);
    }
    if ( player_percent > 60 ) {
        player_bar_class = 'progress-bar-default';
    }
    if ( player_percent < 60 ) {
        player_bar_class = 'progress-bar-warning';
    }
    if ( player_percent < 30 ) {
        player_bar_class = 'progress-bar-danger';
    }

    $('#player_window .progress-bar').attr('class', "progress-bar progress-bar-striped active " + player_bar_class );
    $('#player_window .progress-bar').attr('aria-valuenow', player.hit_points);
    $('#player_window .progress-bar').width(player_percent + '%');
    $('#player_window #skill_points span').empty().prepend($('<div/>').text(player.skill_points).html());

    if (fight_scroll.winner.name == $( "#player" ).val()) {
        $('#opponent_window img.'+images[count]).show();
    } else {
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

    $( "#heal" ).click(function() {
        $opponent = $('#playerlist').find(":selected").text();
        socket.emit('command', {room: id, command: 'heal', player: $( "#player" ).val()});
    });

    $( "#boost" ).click(function() {
        $opponent = $('#playerlist').find(":selected").text();
        socket.emit('command', {room: id, command: 'boost', player: $( "#player" ).val()});
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
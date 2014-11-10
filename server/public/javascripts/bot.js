$(function() {
  var $canvas = $("#sonar-canvas");
  //$canvas.css('background-color', 'rgba(158, 167, 184, 0.2)');
  $canvas.css('border', '1px solid #333');

  canvas = document.getElementById("sonar-canvas");
  var canvas_width = canvas.width;
  var canvas_height = canvas.height;

  var ctx = canvas.getContext('2d');

  // Render sensor reference

  var sensor_ref = [canvas_width/2 - 5, canvas_height - 10];

  var pointHistory = [];

  function renderPoint(angle, distance) {
    var MAX_DISTANCE = 400;
    var MAX_LINE_LENGTH = canvas_height - 50;
    var PIXELS_PER_CM = 1.5;

    distance = distance * PIXELS_PER_CM;

    var radians = angle * (Math.PI/180);

    var y = distance * Math.sin(radians);
    var x = distance * Math.cos(radians);

    pointHistory.unshift([x, y]);
    renderPointHistory();

    // ctx.fillRect((sensor_ref[0] - x) * PIXELS_PER_CM, (sensor_ref[1] - y) * PIXELS_PER_CM, 10, 10);
    ctx.fillRect((sensor_ref[0] - x), (sensor_ref[1] - y), 4, 4);

  }

  function renderPointHistory() {
    var VISIBILITY_THRESHOLD = -1 * (1/15.0);
    ctx.clearRect(0, 0, canvas_width, canvas_height);
    ctx.fillStyle = "rgba(0, 0, 0, 1)";
    ctx.fillRect(canvas_width/2 - 5,canvas_height - 10, 10, 10);
    for(var i = 0; i < pointHistory.length; i++) {
      var point = pointHistory[i];
      var opacity = (VISIBILITY_THRESHOLD * i) + 1;
      ctx.fillStyle = "rgba(0, 0, 0, " + opacity + ")";
      ctx.fillRect((sensor_ref[0] - point[0]), (sensor_ref[1] - point[1]), 4, 4);
    }
  }

  var socket = io('http://localhost:3000');
  socket.on('event', function (data_raw) {
    console.log(data_raw);
    var data = $.parseJSON(data_raw);
    console.log(data);
    if(data.angle && data.distance) {
      renderPoint(data.angle, data.distance);
    }
  });

  renderPoint(0, 200);
  renderPoint(45, 200);
  renderPoint(90, 200);
  renderPoint(135, 200);
  renderPoint(180, 200);
  renderPoint(0, 100);
  renderPoint(45, 100);
  renderPoint(90, 100);
  renderPoint(135, 100);
  renderPoint(180, 100);
  renderPoint(0, 300);
  renderPoint(45, 300);
  renderPoint(90, 300);
  renderPoint(135, 300);
  renderPoint(180, 300);
});

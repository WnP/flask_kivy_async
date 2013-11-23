$(document).ready(
    function() {

      // init RGB values
      var r = 0;
      var g = 0;
      var b = 0;

      // async event from server
      rgba_event = new EventSource('/rgb_source');

      rgba_event.onmessage = function(message) {
        var data = JSON.parse(message.data);
        r = data.r;
        g = data.g;
        b = data.b;
        // use animate to smooth the signal
        $('body').animate({
          backgroundColor: 'rgb('+r+','+g+','+b+')',
        },1);
      };

      // AJAX send RGB values
      var sendRGB = function(red, green, blue) {
        $.getJSON($SCRIPT_ROOT + '/_send_rgb', {
          red: red,
          green: green,
          blue: blue,
        }, function(data) {
          var res = data.result;
        });
        return true;
      };

      // init sliders
      $('#rgba_sliders input').each(function(){
        $(this).slider({
          reversed: true,
          selection: 'after',
        });
      });

      // bind sliders
      $('#slider_red').on('slide', function() {
        r = $(this).slider('getValue');
        sendRGB(r, g, b);
      });

      $('#slider_green').on('slide', function() {
        g = $(this).slider('getValue');
        sendRGB(r, g, b);
      });

      $('#slider_blue').on('slide', function() {
        b = $(this).slider('getValue');
        sendRGB(r, g, b);
      });

    })

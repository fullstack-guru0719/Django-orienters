document.addEventListener("DOMContentLoaded", function() {

  // // The words, graph & PDF buttons
  var content_selectors = document.querySelectorAll('a.content_selector');
  for (let i = 0; i < content_selectors.length; i++) {
    content_selectors[i].addEventListener("click", function(event) {
      event.preventDefault();

      // // Reset the active cadence button
      for (let j = 0; j < content_selectors.length; j++) {
        var content_selector = content_selectors[j];
        if (content_selector.classList.contains('btn-active')) {
          content_selector.classList.remove('btn-active');
        }
      }

      // // Show the clicked button as active
      this.classList.add('btn-active');

      // event.preventDefault();

      // // Hide existing cadence detail
      var cds = document.querySelectorAll('.content');
      for (let j = 0; j < cds.length; j++) {
        var cd = cds[j];
        if (!cd.classList.contains('hide')) {
          cd.classList.add('hide');
        }
      }

      // // Reveal the detail for the clicked cadence
      var eyed = this.getAttribute('data-content-id');
      document.getElementById('content-' + eyed).classList.remove('hide');
    })
  };

  // // init graph
  // // Make sure the graph's element is as high as it's width.
  // // Already set via CSS but that KO-ed.
  var graph_element = document.getElementById('content-graph');
  var position_info = graph_element.getBoundingClientRect();
  // var height = position_info.height;
  var width = position_info.width;
  // console.log('BEFORE: height = ' + height);
  // console.log('BEFORE: width  = ' + width);
  // console.log('BEFORE: ' + graph_element.style.height);
  graph_element.style.height = width + 'px';
  // console.log('AFTER : ' + graph_element.style.height);

  var myChart = Highcharts.chart('content-graph', chart_options);

});

var drawlines = function(el, json, attr, yaxisleg, width, height) { 
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = width - margin.left - margin.right,
        height = height - margin.top - margin.bottom,
        yticks = 8; // Todo make yticks reponsive

    var svg = d3.select(el).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Add gradient to chart
    var gradient = amatyrlib.addGradient(svg, width, height);

    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    // Figure out xformat to be used given the domain and chart width
    var xextent = d3.extent(json, function(d) { return d.date; })
    xFormatter(xAxis, xextent);

    var yAxis = d3.svg.axis()
        .scale(y)
        .ticks(yticks)
        .orient("left");

    var colorscale2 = d3.scale.category20c();

    var line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.val); })
        .interpolate("basis")

    json.forEach(function(d) {
        d.val = d[attr];
    });

    x.domain(d3.extent(json, function(d) { return d.date; }));
    y.domain(d3.extent(json, function(d) { return d.val; }));

    var yrule = svg.selectAll("g.y")
        .data(y.ticks(yticks))
        .enter().append("g")
        .attr("class", "y axis")
      .append("svg:line")
        .attr("class", "yLine")
        .style("stroke", "#eee")
        .style("shape-rendering", "crispEdges")
        .attr("x1", 0)
        .attr("x2", width)
        .attr("y1", y)
        .attr("y2", y);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(yaxisleg);

    pathos = svg.append("path")
      .datum(json)
      .attr("class", "line")
      .attr("stroke", "darkred")
      .attr("d", line)
      .on("mouseover", function (d, i) {
          var pos = $(this).offset();
          $(tt).text(d.x + ': ' + d.y)
          .css({top: topOffset + pos.top, left: pos.left + leftOffset})
          .show();
      })
      .on("mouseout", function (x) {
          $(tt).hide();
      })


    /*
     * pathos.each(function(d, i) {
        console.log(d, i);
    });*/
}

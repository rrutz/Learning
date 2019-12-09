function plot(){

    document.getElementById("my_dataviz").innerHTML = '';

    var data = [
        {'x':0,'y':0, 'y2':1},
        {'x':1,'y':2, 'y2':1},
        {'x':2,'y':1, 'y2':1},
        {'x':3,'y':3, 'y2':1},
        {'x':4,'y':5, 'y2':1},
        {'x':5,'y':1, 'y2':1},
    ]

    var data2 = [
        {'x':0,'y':1},
        {'x':1,'y':1},
        {'x':2,'y':1},
        {'x':3,'y':1},
        {'x':4,'y':1},
        {'x':5,'y':1},
    ]
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = window.innerWidth/2. - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;
    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")"); // shift svg to right
                    
    var xScale = d3.scaleLinear()
        .domain([0, 5]) // input
        .range([0, width]); // pixmel mapping


    svg
        .append("g")
            .attr("transform", "translate(0," + height + ")") // just move the axis to the bottom
            .call(d3.axisBottom(xScale)); // scale axis

    var yScale = d3.scaleLinear()
        .domain( [0, 5])
        .range([ height, 0 ]);
    svg
        .append("g")
        .call(d3.axisLeft(yScale));

    var yScaleR = d3.scaleLinear()
        .domain( [0, 10])
        .range([ height, 0 ]);
    svg
        .append("g")
        .attr("transform",
                    "translate(" + width + ",0)")
        .call(d3.axisRight(yScaleR));


    // add the lines
    svg
        .append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "#69b3a2")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .curve(d3.curveBasis) // make the curve smooth
                .x(function(d) { return xScale(d.x); })  // loops through data
                .y(function(d) { return yScale(d.y); })
                )

    // create a tooltip
    var Tooltip = d3.select("#my_dataviz")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")

    // Three function that change the tooltip when user hover / move / leave a cell
    var mouseover = function(d) {
        Tooltip
        .style("opacity", 1)
    }
    var mousemove = function(d) {
        Tooltip
        .html("x:" + d.x + " y:" + d.y)
        .style("left", (d3.event.pageX+10) + "px")
        .style("top", (d3.event.pageY+10) + "px")
    }
    var mouseleave = function(d) {
        Tooltip
        .style("opacity", 0)
    }

    // add the points
    svg
        .selectAll("circle")
        .data(data)
        .enter()
            .append("circle")
                .attr("cx", function(d, i) {return xScale(d.x); } )
                .attr("cy", function(d) { return yScale(d.y) } )
                .attr("r", 5)
                .attr("fill", "#69b3a2")
                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave)
    // add the points
    svg
        .selectAll("plot2")
        .data(data2)
        .enter()
            .append("circle")
                .attr("cx", function(d, i) {return xScale(d.x); } )
                .attr("cy", function(d) { return yScaleR(d.y) } )
                .attr("r", 5)
                .attr("fill", "#69b3a2")
                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave)
}


window.addEventListener("resize", plot);
window.addEventListener("load", plot);

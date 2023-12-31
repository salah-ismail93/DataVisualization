<template>
    <div class="mx-auto max-w-5xl py-3">
        <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Choropleth Map: Mapping the Aggregated Concentration of Trees Across the USA</p>
        <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
            the choropleth maps effectively illustrate the aggregated concentration of trees in the USA at a state level.
            The use of white areas highlights states with missing information, maintaining transparency.
            The hover functionality enhances interactivity, providing users with additional insights into individual states.
            Overall, this visualization serves as a valuable tool for understanding the spatial patterns and relative abundance of trees
            across the United States.
        </p>
    </div>
    <div class="mx-auto max-w-7xl text-center">
        <div id="chart4Div3" class="flex flex-col items-center">
            <svg id="chart4_3" width="900" height="500"></svg>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'ChoroplethMap',
    data() {
        return {
            // Add your data properties here
        }
    },
    // Add your component logic here
    mounted() {
        this.drawChoroplethMap();
    },
    methods: {
        drawChoroplethMap() {
            var margin = { top: 200, right: 30, bottom: 50, left: 500 };
            // The svg
            var svg4 = d3.select("#chart4_3"),
                width = +svg4.attr("width") - margin.left - margin.right,
                height = +svg4.attr("height") - margin.top - margin.bottom;

            // Map and projection

            let projection4 = d3
                .geoAlbersUsa()
                .scale(1000)
                .translate([width, height]);

            // Data and color scale
            var data4 = new Map();
            let colorScale4 = d3
                .scaleThreshold()
                .domain([50000, 100000, 200000, 300000, 500000])
                .range(d3.schemeGreens[6]);

            var tooltipA3T4 = d3
                .select("#chart4Div3")
                .append("div")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("padding", "10px")
                //.style("min-width", "2px")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("font-size", "16px");

            // Load external data and boot
            Promise.all([
                d3.json("/geojsonUSA.json"),
                d3.csv("/abundance_map.csv")
            ]).then(([topo, data]) => {
                data.forEach(d => {
                    data4.set(d.state, +d.abundance);
                });

                ready4(null, topo); // Call ready4 with loaded topo data

                // ... (rest of your code remains mostly the same)
            }).catch(error => console.error("Error loading data:", error));

            function ready4(error, topo) {
                let mouseOver = function (e, d) {
                    d3.selectAll(".Country")
                        .transition()
                        .duration(200)
                        .style("opacity", 0.5)
                        .style("stroke", "transparent");
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .style("opacity", 1)
                        .style("stroke", "red");

                    tooltipA3T4.transition().duration(200).style("opacity", 1);
                    tooltipA3T4
                        .html(
                            "<span style='color:grey'>State: </span>" +
                            d.properties.NAME +
                            "<br>" +
                            "<span style='color:grey'>Total trees: </span>" +
                            d.total
                        )
                        .style("top", event.pageY + "px");
                };
                let mouseMove = function (e, d) {
                    tooltipA3T4
                        .style("left", event.pageX + 30 + "px")
                        .style("top", event.pageY + "px");
                };

                let mouseLeave = function (e, d) {
                    d3.selectAll(".Country")
                        .transition()
                        .duration(200)
                        .style("opacity", 1)
                        .style("stroke", "black");
                    d3.select(this).transition().duration(200).style("stroke", "black");

                    tooltipA3T4.transition().duration(200).style("opacity", 0);
                };

                let path = d3.geoPath().projection(projection4);
                let currentZoomState = null;
                let zoomIn = function (event, d) {
                    if (currentZoomState === d.id) {
                        // Reset to initial view
                        svg4.transition()
                            .duration(750)
                            .call(
                                zoom.transform,
                                d3.zoomIdentity
                            );
                        currentZoomState = null; // Reset the currently zoomed state
                    } else {
                        // Zoom to the clicked state
                        let bounds = path.bounds(d);
                        let dx = bounds[1][0] - bounds[0][0];
                        let dy = bounds[1][1] - bounds[0][1];
                        let x = (bounds[0][0] + bounds[1][0]) / 2;
                        let y = (bounds[0][1] + bounds[1][1]) / 2;
                        let scale = Math.max(1, Math.min(8, 0.9 / Math.max(dx / width, dy / height)));
                        let translate = [width / 2 - scale * x, height / 2 - scale * y];

                        svg4.transition()
                            .duration(750)
                            .call(
                                zoom.transform,
                                d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
                            );
                        currentZoomState = d.id; // Set the currently zoomed state
                    }
                };

                let mouseDotOver = function (e, d) {
                    d3.selectAll(".Country")
                        .transition()
                        .duration(200)
                        .style("opacity", 0.5)
                        .style("stroke", "transparent");
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .style("opacity", 1)
                        .style("stroke", "red");

                    tooltipA3T4.transition().duration(200).style("opacity", 1);

                    tooltipA3T4
                        .html(
                            "<span style='color:grey'>State: </span>" +
                            d.state +
                            "<br>" +
                            "<span style='color:grey'>Abundance: </span>" +
                            d.abundance
                        )
                        .style("top", event.pageY + "px");
                };

                let mouseDotLeave = function () {
                    d3.selectAll(".Country")
                        .transition()
                        .duration(200)
                        .style("opacity", 1)
                        .style("stroke", "black");
                    d3.select(this).transition().duration(200).style("stroke", "black");

                    tooltipA3T4.transition().duration(200).style("opacity", 0);
                };
                // Draw the map
                let world = svg4
                    .append("g")
                    .selectAll("path")
                    .data(topo.features)
                    .enter()
                    .append("path")
                    // draw each country
                    .attr("d", path)
                    // set the color of each country
                    .attr("fill", function (d) {
                        let abundance_value = data4.get(d.properties.NAME) || 0;
                        d.total = abundance_value;
                        let color_value = abundance_value != 0 ? colorScale4(d.total) : "white"
                        return color_value;
                    })
                    .style("stroke", "black")
                    .attr("class", function (d) {
                        return "Country";
                    })
                    .style("opacity", 1)
                    .on("click", zoomIn)
                    .on("mouseover", mouseOver)
                    .on("mousemove", mouseMove)
                    .on("mouseleave", mouseLeave);

                // Define the zoom behavior
                let zoomed = function (event) {
                    world.attr("transform", event.transform);
                    // Update circle positions and sizes on zoom
                    svg4.selectAll("circle")
                        .attr("cx", function (d) {
                            return event.transform.apply([projection4([+d.longitude, +d.latitude])[0], projection4([+d.longitude, +d.latitude])[1]])[0];
                        })
                        .attr("cy", function (d) {
                            return event.transform.apply([projection4([+d.longitude, +d.latitude])[0], projection4([+d.longitude, +d.latitude])[1]])[1];
                        })
                        .attr("r", 3);
                };
                let zoom = d3.zoom()
                    .scaleExtent([1, 8])
                    .on("zoom", zoomed);
                svg4.call(zoom);

                world.append("rect")
                    .attr("class", "background")
                    .attr("width", width)
                    .attr("height", height)
                    .attr("fill", "transparent")
                    .on("click", function () {
                        if (currentZoomState !== null) {
                            svg4.transition()
                                .duration(750)
                                .call(zoom.transform, d3.zoomIdentity);
                            currentZoomState = null;
                        }
                    });

                // Legend
                // Calculate the position for the legend
                const legendX = width + 400; 
                const legendY = height / 2  ;

                const x = d3.scaleLinear()
                    .domain([2.6, 75.1])
                    .rangeRound([600, 860]);

                const legend = svg4.append("g")
                    .attr("id", "choropleth_legend")
                    .attr("transform", `translate(${legendX}, ${legendY})`);

                const legend_entry = legend.selectAll("g.legend")
                    .data(colorScale4.range().map(function (d) {
                        d = colorScale4.invertExtent(d);
                        if (d[0] == null) d[0] = x.domain()[0];
                        if (d[1] == null) d[1] = x.domain()[1];
                        return d;
                    }))
                    .enter().append("g")
                    .attr("class", "legend_entry");

                const ls_w = 20,
                    ls_h = 20;

                legend_entry.append("rect")
                    .attr("x", 20)
                    .attr("y", function (d, i) {
                        return height - (i * ls_h) - 2 * ls_h;
                    })
                    .attr("width", ls_w)
                    .attr("height", ls_h)
                    .style("fill", function (d) {
                        return colorScale4(d[0]);
                    });

                legend_entry.append("text")
                    .attr("x", 50)
                    .attr("y", function (d, i) {
                        return height - (i * ls_h) - ls_h - 6;
                    })
                    .text(function (d, i) {
                        if (i === 0) return "< " + d[1] / 1000 + "k";
                        if (d[1] < d[0]) return "> " + d[0] / 1000 + "k";
                        return "from " + d[0] / 1000 + "k to " + d[1] / 1000 + "k";
                    });

                legend.append("text").attr("x", 15).attr("y", 100).text("Tree abundance");
            }

        }
    }
}
</script>

<style scoped>
/* Add your component styles here */
</style>

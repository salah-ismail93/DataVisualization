<template>
    <div class="mx-auto max-w-5xl py-3">
        <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Dot Density Map Illustrating the
            Distribution of Trees Across All States</p>
        <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
            the dot density map, where each green dot signifies a specific quantity of trees across U.S. states,
            provides a visually compelling representation of tree distribution. Despite its monochromatic use of green,
            the map remains effective for quick comprehension of regional patterns in tree density. The simplicity,
            coupled with the color choice, enhances its utility for environmental and forestry analysis.
            This green dot density map offers valuable insights into the concentration and distribution of trees,
            serving as a practical tool for informed conservation and land management decisions.
        </p>
    </div>
    <div class="mx-auto max-w-7xl text-center">
        <div id="chart4Div" class="flex flex-col items-center">
            <svg id="chart4" width="900" height="500"></svg>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'DotDensityMap',
    data() {
        return {
            // Add your data properties here
        }
    },
    // Add your component logic here
    mounted() {
        this.drawDotDensityMap();
    },
    methods: {
        drawDotDensityMap() {
            var margin = { top: 200, right: 30, bottom: 50, left: 500 };
            // The svg
            var svg4 = d3.select("#chart4"),
                width = +svg4.attr("width") - margin.left - margin.right,
                height = +svg4.attr("height") - margin.top - margin.bottom;

            // Map and projection

            let projection4 = d3
                .geoAlbersUsa()
                .scale(1000)
                .translate([width, height]);

            // Data and color scale
            var data4 = new Map();

            var tooltipA3T4 = d3
                .select("#chart4Div")
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
                d3.csv("/dotmap_alternative.csv")
            ]).then(([topo, data]) => {
                data.forEach(d => {
                    data4.set(d.city, +d.count);
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
                            "<span style='color:grey'>CENSUS AREA in mi2: </span>" +
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
                            "<span style='color:grey'>City: </span>" +
                            d.city +
                            "<br>" +
                            "<span style='color:grey'>Count: </span>" +
                            d.count
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
                        d.total = d.properties.CENSUSAREA;
                        return "#ffffff";
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

                d3.csv("/dotmap_alternative.csv").then((data) => {
                    svg4
                        .selectAll("dot")
                        .data(data)
                        .enter()
                        .append("circle")
                        .attr("cx", function (d) {
                            return projection4([+d.longitude, +d.latitude])[0];
                        })
                        .attr("cy", function (d) {
                            return projection4([+d.longitude, +d.latitude])[1];
                        })
                        .attr("r", 3)
                        .style("fill", "#2b8a3e")
                        .on("mouseover", mouseDotOver)
                        .on("mouseleave", mouseDotLeave)
                        .attr("stroke", "black")
                        .attr("stroke-width", 0.3)
                        .attr("fill-opacity", 0.8);
                });
            }

        }
    }
}
</script>

<style scoped>
/* Add your component styles here */
</style>

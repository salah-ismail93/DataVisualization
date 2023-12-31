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
    <div>
        <div id="dotmap"></div>
    </div>
</template>

<script>
import * as d3 from 'd3';
import * as topojson from 'topojson';

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
            // set the dimensions and margins of the graph
            var margin = { top: 60, right: 70, bottom: 70, left: 100 },
                width = 1435 - margin.left - margin.right,
                height = 700 - margin.top - margin.bottom;

            let projection = d3.geoAlbersUsa()
                .scale(width - 20)
                .translate([width / 2, height / 2]);

            let path = d3.geoPath().projection(projection);

            let tooltip = null;

            let mouseOver = function (event, d) {
                d3.selectAll(".Circle")
                    .transition()
                    .duration(200)
                    .style("opacity", 0.1)
                    .style("stroke", "none");
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style("stroke", "black")
                    .style("opacity", 0.5)
                    .style("stroke-width", "0.75px");
                if (!tooltip) {
                    tooltip = d3.select("body").append("div")
                        .attr("class", "tooltip")
                        .style("opacity", 0);
                }
                tooltip.html('<p>' + d.city + ' &rarr; ' + d.count + ' trees</p>')
                    .style("left", (event.pageX + 15) + "px")
                    .style("top", (event.pageY - 28) + "px")
                    .transition().duration(400)
                    .style("opacity", 1);
            }

            let mouseLeave = function () {
                d3.selectAll(".Circle")
                    .transition()
                    .duration(200)
                    .style("opacity", 0.5)
                    .style("stroke", "none");
                // Hide and remove the tooltip
                if (tooltip) {
                    tooltip.transition().duration(300)
                        .style("opacity", 0)
                        .remove();
                    tooltip = null; // Reset tooltip variable
                }
            }
            let mouseOver_states = function (event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style("stroke", d.properties.abundance != 0 ? "green" : "black")
                    .style("stroke-width", "2px");
                // Create the tooltip if it doesn't exist
                if (!tooltip) {
                    tooltip = d3.select("body").append("div")
                        .attr("class", "tooltip")
                        .style("opacity", 0);
                }
                tooltip.html(d.properties.name + ' &#40;' + d.properties.postal + '&#41;')
                    .style("left", (event.pageX + 15) + "px")
                    .style("top", (event.pageY - 28) + "px")
                    .transition().duration(400)
                    .style("opacity", 1);
            }

            let mouseLeave_states = function () {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style("stroke", "black")
                    .style("stroke-width", "0.75px");
                if (tooltip) {
                    tooltip.transition().duration(300)
                        .style("opacity", 0)
                        .remove();
                    tooltip = null; // Reset tooltip variable
                }
            }

            let svg = d3.select("#dotmap")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", `0 0 ${width} ${height}`);
            let zoomed = function (event) {
                world.attr("transform", event.transform);
                // Update circle positions and sizes on zoom
                svg.selectAll("circle")
                    .attr("cx", function (d) {
                        return event.transform.apply([projection([+d.longitude, +d.latitude])[0], projection([+d.longitude, +d.latitude])[1]])[0];
                    })
                    .attr("cy", function (d) {
                        return event.transform.apply([projection([+d.longitude, +d.latitude])[0], projection([+d.longitude, +d.latitude])[1]])[1];
                    })
                    .attr("r", 2);
            };

            let zoom = d3.zoom()
                .scaleExtent([1, 8])
                .on("zoom", zoomed);

            svg.call(zoom);

            let world = svg.append("g");

            let currentZoomState = null;

            let svgBackground = world.append("rect")
                .attr("class", "background")
                .attr("width", width)
                .attr("height", height)
                .attr("fill", "transparent")
                .on("click", function () {
                    if (currentZoomState !== null) {
                        svg.transition()
                            .duration(750)
                            .call(zoom.transform, d3.zoomIdentity);
                        currentZoomState = null;
                    }
                });

            let zoomIn = function (event, d) {
                if (currentZoomState === d.id) {
                    // Reset to initial view
                    svg.transition()
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

                    svg.transition()
                        .duration(750)
                        .call(
                            zoom.transform,
                            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
                        );
                    currentZoomState = d.id; // Set the currently zoomed state
                }
            };

            fetch("/choropleth.json")
                .then(response => response.json())
                .then(data => {
                    const data_features = topojson.feature(data, data.objects.states).features;

                    world.selectAll(".states")
                        .data(data_features)
                        .enter().append("path")
                        .attr("data-name", function (d) { return d.properties.name })

                        // add a class and styling
                        .attr("d", path)
                        .style("stroke", "black")
                        .attr("class", "Country")
                        .attr("id", function (d) { return d.id })
                        .style("opacity", 1)
                        .style("stroke-width", "0.75px")
                        .style("fill", "white")
                        .on("mouseover", mouseOver_states)
                        .on("mouseleave", mouseLeave_states)
                        .on("click", zoomIn);
                })
                .catch(error => {
                    console.error("Error fetching the data:", error);
                });
            d3.csv("/dotmap_alternative.csv").then(function (data) {
                svg.selectAll("circle")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("class", "Circle")
                    .attr("cx", function (d) {
                        return projection([+d.longitude, +d.latitude])[0];
                    })
                    .attr("cy", function (d) {
                        return projection([+d.longitude, +d.latitude])[1];
                    })
                    .attr("r", 2)
                    .style("fill", "rgb(34,139,34)")
                    .style("opacity", 0.5)
                    .on("mouseover", mouseOver)
                    .on("mouseleave", mouseLeave);
            });
        }
    }
}
</script>

<style scoped>
/* Add your component styles here */
</style>

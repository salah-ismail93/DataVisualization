<template>
    <div class="mx-auto max-w-5xl py-3">
        <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Dot Density Map Illustrating the
            Distribution of Trees Across All States</p>
        <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
            the dot density map, employing a distinct color for each of the top 10 tree species,
            offers a rich and detailed portrayal of their distribution across U.S. states.
            The use of a diverse color palette enhances the map's ability to convey information,
            allowing for a nuanced understanding of regional patterns in tree density.
            This visual representation, though more intricate, remains accessible for environmental and forestry analysis.
            By focusing on the top 10 tree species and assigning unique colors to each,
            the map becomes a valuable tool for informed conservation and land management decisions,
            providing insights into the concentration and distribution of these key species in the United States.
        </p>
    </div>
    <div>
        <div id="dotmapTop10"></div>
    </div>
</template>

<script>
import * as d3 from 'd3';
import * as topojson from 'topojson';

export default {
    name: 'DotDensityMapTop10',
    data() {
        return {
            // Add your data properties here
        }
    },
    // Add your component logic here
    mounted() {
        this.DotDensityMapTop10();
    },
    methods: {
        DotDensityMapTop10() {
            // set the dimensions and margins of the graph
            var margin = { top: 60, right: 70, bottom: 70, left: 100 },
                width = 1435 - margin.left - margin.right,
                height = 700 - margin.top - margin.bottom;

            let projection = d3.geoAlbersUsa()
                .scale(width - 20)
                .translate([width / 2, height / 2]);

            let path = d3.geoPath().projection(projection);

            const speciesColors = {
                "platanus_acerifolia": "#FF5733",       // Reddish-orange
                "prunus": "#8B0000",                    // Dark red
                "liquidambar_styraciflua": "#FFA500",   // Orange
                "acer_rubrum": "#FF0000",               // Pure red
                "gleditsia_triacanthos": "#00FF00",     // Green
                "lagerstroemia_indica": "#2101FF",      // Pure blue
                "pyrus_calleryana": "#00CED1",          // Blue-green
                "tilia_cordata": "#8A2BE2",             // Blue-violet
                "acer_platanoides": "#FFFF00",          // Yellow
                "fraxinus_pennsylvanica": "#FF00FF",    // Fuchsia
                "others": "#A9A9A9"                     // Dark gray
            };

            let tooltip = null;

            let mouseOver = function (event, d) {
                d3.selectAll('[class^="circle"]')
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
                tooltip.html(d.city + ' &rarr; ' +
                    d.count + ' trees of type <i>' + d.scientific_name + '</i>')
                    .style("left", (event.pageX + 15) + "px")
                    .style("top", (event.pageY - 28) + "px")
                    .transition().duration(400)
                    .style("opacity", 1);
            }

            let mouseLeave = function () {
                d3.selectAll('[class^="circle"]')
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

            let svg = d3.select("#dotmapTop10")
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

            var selectedColors = [];

            function handleLegendClick(scientificName) {

                // Check if the clicked color is already selected
                const index = selectedColors.indexOf(scientificName);

                // If selected, remove it; otherwise, add it
                if (index !== -1) {
                    selectedColors.splice(index, 1);
                } else {
                    selectedColors.push(scientificName);
                }

                // Update the visualization based on the selected colors
                updateVisualization(selectedColors);

                // Update the legend styles
                updateLegendStyles();
            }

            function updateVisualization(selectedColors) {

                Object.keys(speciesColors).forEach(scientific_name => {
                    const isClicked = selectedColors.includes(scientific_name);
                    const displayStyle = isClicked || selectedColors.length === 0 ? null : "none";
                    const circles = d3.selectAll(`.circle-${scientific_name}`);
                    const legendText = d3.selectAll(`.legend-text-${scientific_name}`);

                    circles.style("display", displayStyle);
                    legendText.style("font-weight", isClicked ? "bold" : "normal");

                });
            }

            function updateLegendStyles() {
                const keys = Object.keys(speciesColors);
                const isColorsEmpty = selectedColors.length === 0;
                const isColorsFull = selectedColors.length === Object.keys(speciesColors).length;

                keys.forEach(key => {
                    const color = speciesColors[key];
                    const isClicked = selectedColors.includes(key);

                    d3.selectAll(`.legend-rect-${key}`)
                        .style("fill", isClicked || isColorsEmpty ? color : "white")
                        .style("stroke", color);

                    d3.selectAll(`.legend-text-${key}`)
                        .style("font-weight", isClicked && !isColorsFull ? "bold" : "normal");
                });

                if (isColorsFull) selectedColors = [];
            }

            d3.csv("/dotmap2_alternative.csv").then(function (data) {
                svg.selectAll("circle")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("class", function (d) { return "circle-" + d.scientific_name.replace(/\s+/g, '_').toLowerCase(); })
                    .attr("cx", function (d) {
                        return projection([+d.longitude, +d.latitude])[0];
                    })
                    .attr("cy", function (d) {
                        return projection([+d.longitude, +d.latitude])[1];
                    })
                    .attr("r", 2)
                    .style("fill", function (d) {
                        return speciesColors[d.scientific_name.replace(/\s+/g, '_').toLowerCase()];
                    })
                    .style("opacity", 0.5)
                    .on("mouseover", mouseOver)
                    .on("mouseleave", mouseLeave);
            });

            var map_legend = svg.append("g")
                .attr("class", "legend")
                .attr("transform", "translate(80,220)");

            var keys = Object.keys(speciesColors); // Get keys from the dictionary

            keys.forEach(function (key, j) {
                var color = speciesColors[key]; // Get color value for the key

                map_legend.append("rect")
                    .attr("class", `legend-rect-${key}`)
                    .attr("x", width / 2 + 385) // 100
                    .attr("y", j * 30)
                    .attr("width", 20)
                    .attr("height", 20)
                    .attr("fill", color)
                    .on("click", () => handleLegendClick(key))
                    .style("cursor", "pointer");

                map_legend.append("text")
                    .attr("x", width / 2 + 415) // 85
                    .attr("y", j * 30 + 15)
                    .attr("class", "legend-text-" + key)
                    .text((key.charAt(0).toUpperCase() + key.slice(1)).replace(/_/g, ' ')) // Display the key associated with the color
                    .style("font-size", "12px");
            });
        }
    }
}
</script>

<style scoped>
/* Add your component styles here */
</style>

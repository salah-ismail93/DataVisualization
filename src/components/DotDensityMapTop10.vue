<template>
    <div class="mx-auto max-w-5xl py-3">
        <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Dot Density Map Illustrating the
            Distribution of Top 10 Trees Across All States</p>
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
    <div class="mx-auto max-w-7xl text-center">
        <div id="chart4Div2" class="flex flex-col items-center">
            <svg id="chart4_2" width="900" height="500"></svg>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

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
            var margin = { top: 200, right: 30, bottom: 50, left: 500 };
            // The svg
            var svg4 = d3.select("#chart4_2"),
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
                .select("#chart4Div2")
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
                d3.csv("/dotmap2_alternative.csv")
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

                const speciesColors = {
                    prunus: "#8B0000",
                    acer_rubrum: "#FF0000",
                    tilia_cordata: "#8A2BE2",
                    pyrus_calleryana: "#00CED1",
                    acer_platanoides: "#FFFF00",
                    platanus_acerifolia: "#FF5733",
                    lagerstroemia_indica: "#2101FF",
                    gleditsia_triacanthos: "#00FF00",
                    fraxinus_pennsylvanica: "#FF00FF",
                    liquidambar_styraciflua: "#FFA500",
                    others: "#A9A9A9",
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
                            d.count +
                            "<br>" +
                            "<span style='color:grey'>tree type: </span>" +
                            d.scientific_name
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
                        return "#dbf8cf";
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

                d3.csv("/dotmap2_alternative.csv").then((data) => {
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
                        .style("fill", function (d) {
                            return speciesColors[
                                d.scientific_name.replace(/\s+/g, "_").toLowerCase()
                            ];
                        })
                        .on("mouseover", mouseDotOver)
                        .on("mouseleave", mouseDotLeave)
                        .attr("stroke", "black")
                        .attr("stroke-width", 0.3)
                        .attr("fill-opacity", 0.8);
                });

                var map_legend = svg4
                    .append("g")
                    .attr("class", "legend")
                    .attr("transform", "translate(160,175)");

                var keys = Object.keys(speciesColors); // Get keys from the dictionary

                keys.forEach(function (key, j) {
                    var color = speciesColors[key]; // Get color value for the key

                    map_legend
                        .append("rect")
                        .attr("class", `legend-rect-${key}`)
                        .attr("x", width / 2 + 385) // 100
                        .attr("y", j * 30)
                        .attr("width", 20)
                        .attr("height", 20)
                        .attr("fill", color)
                        //.on("click", () => handleLegendClick(key))
                        .style("cursor", "pointer");

                    map_legend
                        .append("text")
                        .attr("x", width / 2 + 415) // 85
                        .attr("y", j * 30 + 15)
                        .attr("class", "legend-text-" + key)
                        .text((key.charAt(0).toUpperCase() + key.slice(1)).replace(/_/g, " ")) // Display the key associated with the color
                        .style("font-size", "12px");
                });
            }

        }
    }
}
</script>

<style scoped>
/* Add your component styles here */
</style>

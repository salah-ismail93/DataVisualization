<template>
    <div class="mx-auto max-w-5xl py-3">
        <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Green Canopy Chronicles: Mapping Tree Density Across the USA</p>
        <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
            "Explore the 'Green Canopy Chronicles,' an interactive choropleth map revealing the exact landscape of tree density across
            the United States. The legend guides your journey through shaded landscapes, while white areas highlight states where tree information is unavailable.
            Hover over states for instant insights, making this atlas a dynamic tool for understanding the intricate
            tapestry of America's arboreal richness."
        </p>
    </div>
    <div class="mx-auto max-w-7xl text-center">
        <div id="chart4Div4" class="flex flex-col items-center">
            <svg id="chart4_4" width="900" height="500"></svg>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'ChoroplethMapDensity',
    data() {
        return {
            // Add your data properties here
        }
    },
    // Add your component logic here
    mounted() {
        this.drawChoroplethMapDensity();
    },
    methods: {
        drawChoroplethMapDensity() {
            var margin = { top: 200, right: 30, bottom: 50, left: 500 };
            // The svg
            var svg4 = d3.select("#chart4_4"),
                width = +svg4.attr("width") - margin.left - margin.right,
                height = +svg4.attr("height") - margin.top - margin.bottom;

            // Map and projection

            let projection4 = d3
                .geoAlbersUsa()
                .scale(1000)
                .translate([width, height]);

            // Data and color scale
            var data4 = new Map();
            let colorScale5 = d3
                .scaleThreshold()
                .domain([5, 10, 15, 20, 25, 30])
                .range(d3.schemeGreens[7]);

            var tooltipA3T4 = d3
                .select("#chart4Div4")
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

                    let density = ((d.total / d.properties.CENSUSAREA) * 2.58998811).toFixed(3);
                    tooltipA3T4.transition().duration(200).style("opacity", 1);
                    tooltipA3T4
                        .html(
                            "<span style='color:grey'>State: </span>" +
                            d.properties.NAME +
                            "<br>" +
                            "<span style='color:grey'>Total trees density: </span>" +
                            density
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
                        let density = ((abundance_value / d.properties.CENSUSAREA) * 2.58998811).toFixed(3);
                        let color_value = density != 0 ? colorScale5(density) : "white"
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
                const legendX = width + 350; 
                const legendY = height / 2  ;

                const x = d3.scaleLinear()
                    .domain([2.6, 25])
                    .rangeRound([600, 860]);

                const legend = svg4.append("g")
                    .attr("id", "choropleth_legend_density")
                    .attr("transform", `translate(${legendX}, ${legendY})`);

                const legend_entry = legend.selectAll("g.legend")
                    .data(colorScale5.range().map(function (d) {
                        d = colorScale5.invertExtent(d);
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
                        return colorScale5(d[0]);
                    });

                legend_entry.append("text")
                    .attr("x", 50)
                    .attr("y", function (d, i) {
                        return height - (i * ls_h) - ls_h - 6;
                    })
                    .text(function (d, i) {
                        if (i === 0) return "< " + d[1];
                        if (d[1] < d[0]) return "> " + d[0];
                        return "from " + d[0]  + " to " + d[1] ;
                    });

                legend.append("text").attr("x", 15).attr("y", 75).text("Tree Density per m2");
            }

        }
    }
}
</script>

<style scoped>
/* Add your component styles here */
</style>

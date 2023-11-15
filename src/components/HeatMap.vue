<template>
    <!-- Heatmap -->
    <div class="bg-white px-6 lg:px-8 text-center">
        <div class="mx-auto max-w-5xl">
            <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl">Heatmap according to states</p>
            <div>
                <label for="stateSelect">Select State:</label>
                <select id="stateSelect"></select>
            </div>
            <div class="flex justify-center py-3 hidden" id="A1chart2">
                <div class="tooltip A1chart2Inner"></div>
                <!-- Heatmap container -->
                <div id="heatmap-container"></div>
            </div>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'HeatMap',
    mounted() {

        // Heatmap
        const heatmapMargin = { top: 10, right: 10, bottom: 30, left: 150 };
        const heatmapWidth = 800 - heatmapMargin.left - heatmapMargin.right;
        const heatmapHeight = 400 - heatmapMargin.top - heatmapMargin.bottom;

        // Create SVG element for Heatmap
        const heatmapSvg = d3.select('#heatmap-container')
            .append('svg')
            .attr('width', heatmapWidth + heatmapMargin.left + heatmapMargin.right)
            .attr('height', heatmapHeight + heatmapMargin.top + heatmapMargin.bottom)
            .append('g')
            .attr('transform', `translate(${heatmapMargin.left},${heatmapMargin.top})`);

        d3.csv('/species.csv').then((data) => {
            // Heatmap
            const states = Array.from(new Set(data.map((d) => d.state)));

            // Populate the state selection dropdown
            const stateSelect = d3.select('#stateSelect');
            stateSelect
                .selectAll('option')
                .data(states)
                .enter()
                .append('option')
                .text((d) => d);

            // Add change event listener to the state selection
            stateSelect.on('change', function () {
                const selectedState = this.value;
                const filteredData = data.filter((d) => d.state === selectedState);
                const aggregatedData = d3.rollup(
                    filteredData,
                    (v) => d3.sum(v, (d) => +d.count),
                    (d) => d.city
                );
                const topCities = Array.from(aggregatedData)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 5) // Limit to the first 5 cities
                    .map((d) => d[0]);

                const treeTypes = Array.from(new Set(filteredData.map((d) => d.common_name)))
                    .sort((a, b) => {
                        const countA = filteredData.filter((d) => d.common_name === a).reduce((sum, d) => sum + +d.count, 0);
                        const countB = filteredData.filter((d) => d.common_name === b).reduce((sum, d) => sum + +d.count, 0);
                        return countB - countA;
                    })
                    .slice(0, 5); // Limit to the first 5 tree types

                const heatmapData = filteredData.filter((d) => topCities.includes(d.city) && treeTypes.includes(d.common_name));
                drawHeatmap(heatmapData);
                document.getElementById('A1chart2').classList.remove('hidden');
            });


        });

        function drawHeatmap(data) {
            const cities = Array.from(new Set(data.map((d) => d.city))).slice(0, 5); // Limit to the first 5 cities
            const treeTypes = Array.from(new Set(data.map((d) => d.common_name))).slice(0, 5); // Limit to the first 5 tree types

            const xScale = d3.scaleBand().domain(cities).range([0, heatmapWidth]);
            const yScale = d3.scaleBand().domain(treeTypes).range([0, heatmapHeight]);

            const colorScale = d3.scaleSequential(d3.interpolateGreens).domain([1, d3.max(data, (d) => +d.count)]);

            const tooltip = d3.select("#A1chart2")
                .append("div")
                .attr("class", "tooltip");

            function mouseover(event, d) {
                const totalAmount = d.count;
                const treeType = d.common_name;
                const averageHeight = d.mean_h;
                tooltip
                    .html(`Tree Type: ${treeType}<br>Total Amount: ${totalAmount}<br>Canopy mean_h: ${averageHeight}`)
                    .style('opacity', 1);
                d3.select(this).attr('fill', '#0255ee');
            }

            function mousemove() {
                tooltip
                    .style('left', `${event.pageX + 40}px`)
                    .style('top', `${event.pageY + 5}px`);
            }

            function mouseleave() {
                tooltip.style('opacity', 0);
                d3.select(this).attr('fill', (d) => colorScale(+d.count));
            }



            heatmapSvg.selectAll('*').remove();

            heatmapSvg
                .selectAll('rect')
                .data(data)
                .enter()
                .append('rect')
                .attr('x', (d) => xScale(d.city))
                .attr('y', (d) => yScale(d.common_name))
                .attr('width', xScale.bandwidth())
                .attr('height', yScale.bandwidth())
                .attr('fill', (d) => colorScale(+d.count))
                .on('mouseover', mouseover)
                .on('mousemove', mousemove)
                .on('mouseleave', mouseleave);

            heatmapSvg.append('g').call(d3.axisBottom(xScale)).attr('transform', `translate(0,${heatmapHeight})`);
            heatmapSvg.append('g').call(d3.axisLeft(yScale));
        
        const legendWidth = 300, legendHeight = 20;

    // Append a defs (for definition) element to your SVG
const defs = heatmapSvg.append('defs');

// Append a linearGradient element to the defs and give it a unique id
const linearGradient = defs.append('linearGradient').attr('id', 'linear-gradient');

// Horizontal gradient
linearGradient
    .attr("x1", "0%")
    .attr("y1", "0%")
    .attr("x2", "100%")
    .attr("y2", "0%");

// Set the color for the start (0%)
linearGradient.append("stop") 
    .attr("offset", "0%")   
    .attr("stop-color", d3.interpolateGreens(0)); 

// Set the color for the end (100%)
linearGradient.append("stop") 
    .attr("offset", "100%")   
    .attr("stop-color", d3.interpolateGreens(1));

// Draw the rectangle and fill with gradient
heatmapSvg.append("rect")
    .attr("width", legendWidth)
    .attr("height", legendHeight)
    .style("fill", "url(#linear-gradient)")
    .attr("transform", `translate(${heatmapWidth - legendWidth}, ${heatmapHeight + 40})`);

// Create scale for legend axis
const legendScale = d3.scaleLinear()
    .domain([1, d3.max(data, (d) => +d.count)])
    .range([0, legendWidth]);

// Create legend axis
const legendAxis = d3.axisBottom(legendScale).ticks(5);
heatmapSvg.append("g")
    .attr("transform", `translate(${heatmapWidth - legendWidth}, ${heatmapHeight + 60})`)
    .call(legendAxis);

    }
}
}

</script>


<style>
.tooltip {
    opacity: 0;
    background-color: white;
    border: solid;
    border-width: 2px;
    border-radius: 5px;
    padding: 10px;
    position: absolute;
    z-index: 1080;
    display: block;
    margin: 0;
    font-family: var(--bs-font-sans-serif);
    font-style: normal;
    font-weight: 400;
    line-height: 1.5;
    text-align: left;
    text-align: start;
    text-decoration: none;
    text-shadow: none;
    text-transform: none;
    letter-spacing: normal;
    word-break: normal;
    word-spacing: normal;
    white-space: normal;
    line-break: auto;
    font-size: .875rem;
    word-wrap: break-word;
    opacity: 0;
}
</style>

<template>
    <div class="bg-white px-6 lg:px-8 text-center mt-8">
        <div class="mx-auto">
            <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
                Stacked Bar Chart Multiples
            </h3>
            <div>
                <label for="selectStateMultiples">Select City:</label>
                <select id="selectStateMultiples">
                </select>
            </div>
            <div class="flex flex-wrap justify-center py-3" id="A1chart5">
                <div class="tooltip A1chart5Inner"></div>
            </div>
        </div>
    </div>
</template>
  
<script>
import * as d3 from 'd3';

export default {
    name: 'StackedBarChartMultiples',
    mounted() {
        //----------- Third Chart --------------

        const margin = { top: 30, right: 0, bottom: 80, left: 110 };
        const width = 400 - margin.left - margin.right;
        const height = 500 - margin.top - margin.bottom;

        // Read the data
        d3.csv("/stacked_bar_chart_multiples.csv").then((data) => {
            const states = Array.from(new Set(data.map((d) => d.state)));

            // Populate the state selection dropdown
            const selectStateMultiples = d3.select('#selectStateMultiples');
            selectStateMultiples
                .selectAll('option')
                .data(states)
                .enter()
                .append('option')
                .text((d) => d);

            // Add change event listener to the state selection
            selectStateMultiples.on('change', function () {
                const selectedState = this.value;
                let citiesInState = data.filter((d) => d.state === selectedState);

                drawBarChartMultiple(citiesInState);

            });

        })
            .catch((err) => {
                console.error(err);
            });

        function drawBarChartMultiple(data) {
            // Group the data: I want to draw one line per group
            const sumstat = d3.group(data, (d) => d.scientific_name);
            const allKeys = Array.from(sumstat.keys());
            let svg = d3.select("#A1chart5");
            svg.selectAll('*').remove();
            // Add an svg element for each group. The will be one beside each other and will go on the next row when no more room available
            svg = d3
                .select("#A1chart5")
                .selectAll("mybar")
                .data(Array.from(sumstat))
                .enter()
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

            // Add X axis
            const x = d3
                .scaleLinear()
                .range([0, width])
                .domain([0, d3.max(data, (d) => +d.tree_count)]);

            svg
                .append("g")
                .attr("transform", `translate(0, ${height})`)
                .call(d3.axisBottom(x).ticks(3))
                .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");

            const y = d3
                .scaleBand()
                .domain(data.map((d) => d.city))
                .range([0, height])
                .padding(0.2);

            svg
                .append("g")
                .call(d3.axisLeft(y).ticks(5))
                .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");

            // Color palette
            const colorTitles = d3.scaleOrdinal()
                .domain(allKeys)
                .range(['#3c51ae', '#ffd43b', '#4daf4a', '#e41a1c', '#FFBCD9', '#adb5bd']);


            // Tooltip for all the bars
            const tooltip3 = d3
                .select("#A1chart5")
                .append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("padding", "10px");

            // Event handlers for mouseover, mousemove, and mouseleave
            const mouseover3 = function (event, d) {
                const totalAmount3 = d.tree_count;
                const treeType3 = d.scientific_name;
                tooltip3
                    .html("Tree Type: " + treeType3 + "<br>" + "Total Amount: " + totalAmount3)
                    .style("opacity", 1);
            };

            const mousemove3 = function (event) {
                tooltip3
                    .style("left", `${event.pageX + 20}px`)
                    .style("top", `${event.pageY + 10}px`);
            };

            const mouseleave3 = function () {
                tooltip3.style("opacity", 0);
            };

            // Create the bars
            svg
                .selectAll("mybar")
                .data((d) => d[1])
                .enter()
                .append("rect")
                // eslint-disable-next-line no-unused-vars
                .style("fill", (d, i) => colorTitles(d.scientific_name))
                // eslint-disable-next-line no-unused-vars
                .attr("x", (d, i) => x(0))
                // eslint-disable-next-line no-unused-vars
                .attr("y", (d, i) => y(d.city))
                .attr("height", y.bandwidth())
                // eslint-disable-next-line no-unused-vars
                .attr("width", (d, i) => width - (width - x(d.tree_count)))
                .on("mouseover", mouseover3)
                .on("mousemove", mousemove3)
                .on("mouseleave", mouseleave3);

            // Add titles
            svg
                .append("text")
                .attr("text-anchor", "start")
                .attr("y", -5)
                .attr("x", 0)
                .text((d) => d[0])
                .style("fill", (d) => colorTitles(d[0]));
        }

    }


}
</script>
  
<style>
.tooltip {
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
  
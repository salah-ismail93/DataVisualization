<template>
    <div>
        <label for="citySelect">Select City:</label>
        <select id="citySelect">
        </select>
    </div>
    <div class="flex justify-center py-3 hidden" id="A1chart1">
        <div class="tooltip A1chart1Inner"></div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'BarChart',
    mounted() {
        // Chart dimensions
        const margin = { top: 10, right: 100, bottom: 50, left: 100 };
        const width = 800 - margin.left - margin.right;
        const height = 1000 - margin.top - margin.bottom;
        // Create SVG element
        const svg = d3.select("#A1chart1")
            .append("svg")
            .attr("viewBox", `0 0 1000 1000`)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);
        // Define data URL
        const dataUrl = "/species.csv";

        // Load data
        d3.csv(dataUrl).then(function (data) {
            // Create a set of unique cities from the data
            const cities = new Set(data.map(d => d.city));

            // Populate the city selection dropdown
            const citySelect = d3.select("#citySelect");
            citySelect
                .selectAll("option")
                .data(Array.from(cities))
                .enter()
                .append("option")
                .text(city => city);
            // Initialize the chart with all data
            //drawChart(data);
            // Add change event listener to the city selection
            citySelect.on("change", function () {
                svg.selectAll("*").remove();
                const selectedCity = this.value;
                // Filter the data based on the selected city
                const filteredData = data.filter(d => d.city === selectedCity);
                console.log(filteredData);
                // Update the chart with filtered data
                // Use reduce to find the maximum count
                const maxCount = filteredData.reduce((max, entry) => {
                    const count = parseInt(entry.count, 10);
                    return count > max ? count : max;
                }, -1);
                console.log("Maximum count value:", maxCount);
                drawChart(filteredData, maxCount);
                document.getElementById("A1chart1").classList.remove("hidden");
            });
        }).catch(function (error) {
            console.error("Error loading data:", error);
        });
        // Function to draw the chart
        function drawChart(data, maxCount) {
            console.log(maxCount);
            // Create X scale
            const x = d3.scaleLinear()
                .domain([0, maxCount])
                .range([0, width]);
            // Create Y scale
            const y = d3.scaleBand()
                .range([0, height])
                .domain(data.map(d => d.common_name))
                .padding(0.1)
                .paddingOuter(0.2);
            // Append X axis
            svg.append("g")
                .attr("transform", `translate(0,${height})`)
                .call(d3.axisBottom(x))
                .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");
            // Append Y axis
            svg.append("g")
                .call(d3.axisLeft(y));
            // Create tooltip
            const tooltip = d3.select("#A1chart1")
                .append("div")
                .attr("class", "tooltip");
            // Mouse event functions
            function mouseover(event, d) {
                const totalAmount = d.count;
                const treeType = d.common_name;
                const averageHeight = d.mean_h;
                tooltip
                    .html(`Tree Type: ${treeType}<br>Total Amount: ${totalAmount}<br>Canopy mean_h: ${averageHeight}`)
                    .style("opacity", 1);
                d3.select(this).attr("fill", "#0e6efc");
            }
            function mousemove() {
                tooltip
                    .style("left", `${event.pageX + 40}px`)
                    .style("top", `${event.pageY + 5}px`);
            }
            function mouseleave() {
                tooltip.style("opacity", 0);
                d3.select(this).attr("fill", d => scolor(d.count));
            }
            // Color scales
            const scolor = d3.scaleSequential()
                .domain([0, d3.max(data, d => d.count)])
                .interpolator(d3.interpolateGreens);
            const scolor2 = d3.scaleSequential()
                .domain([300, 270])
                .interpolator(d3.interpolateGreys);
            // Create bars
            const bars = svg.selectAll(".bar")
                .data(data)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", x(0))
                .attr("y", d => y(d.common_name))
                .attr("width", 0)
                .attr("height", y.bandwidth())
                .attr("fill", d => scolor(d.count))
                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave);
            // Add count labels
            svg.selectAll(".label")
                .data(data)
                .enter()
                .append("text")
                .attr("class", "label")
                .text(d => d.count)
                .attr("x", d => x(d.count) + 15)
                .attr("y", d => y(d.common_name) + 10)
                .attr("text-anchor", "right")
                .attr("font-family", "sans-serif")
                .attr("font-size", "11px")
                .attr("fill", "black");
            // Animation
            bars.transition()
                .duration(800)
                .attr("x", () => x(0))
                .attr("width", d => width - (width - x(d.count)))
                .delay((d, i) => i * 100);
        }

    },

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

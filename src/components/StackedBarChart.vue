<template>
    <!-- Stacked Bar Chart -->
<div class="bg-white px-6 lg:px-8 text-center mt-8">
  <div class="mx-auto max-w-5xl">
    <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
      Stacked Bar Chart
    </h3>
    
    <div>
      <label for="stateSelectStacked">Select State:</label>
      <select id="stateSelectStacked"></select>
    </div>
    <div class="flex justify-center py-3 hidden" id="A1chart3">
      <div class="tooltip A1chart3Inner"></div>
      <div id="stacked-bar-chart-container"></div>
    </div>
  </div>
</div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'StackedBarChart',
    mounted() {
        // Stacked Bar chart
        const stackedMargin = { top: 10, right: 100, bottom: 50, left: 100 };
        const stackedWidth = 800 - stackedMargin.left - stackedMargin.right;
        const stackedHeight = 400 - stackedMargin.top - stackedMargin.bottom;

        // Create SVG element for Stacked Bar chart
        const stackedSvg = d3
            .select('#stacked-bar-chart-container')
            .append('svg')
            .attr('width', stackedWidth + stackedMargin.left + stackedMargin.right)
            .attr('height', stackedHeight + stackedMargin.top + stackedMargin.bottom)
            .append('g')
            .attr('transform', `translate(${stackedMargin.left},${stackedMargin.top})`);

        d3.csv('/species.csv').then((data) => {
            // Stacked Bar Chart - State Dropdown
            const statesS = Array.from(new Set(data.map((d) => d.state)));

            d3.select('#stateSelectStacked')
                .selectAll('option')
                .data(statesS) // Use the populated states from data()
                .enter()
                .append('option')
                .text((d) => d);

            // Add change event listener to the state selection
            d3.select('#stateSelectStacked').on('change', function () {
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

                // const treeTypes = Array.from(new Set(filteredData.map((d) => d.common_name)))
                //     .sort((a, b) => {
                //         const countA = filteredData.filter((d) => d.common_name === a).reduce((sum, d) => sum + +d.count, 0);
                //         const countB = filteredData.filter((d) => d.common_name === b).reduce((sum, d) => sum + +d.count, 0);
                //         return countB - countA;
                //     })
                //     .slice(0, 5); // Limit to the first 5 tree types

                // Add change event listener to the state selection
                d3.select('#stateSelectStacked').on('change', function () {
                    const selectedStateS = this.value;
                    const filteredData = data.filter((d) => d.state === selectedStateS);
                    const limitedData = filteredData.slice(0, 20);
                    const maxCount = d3.max(limitedData, (d) => +d.count);
                    drawStackedBarChart(limitedData, maxCount);
                });

                const treeTypeCounts = new Map();

                filteredData.forEach((d) => {
                    if (topCities.includes(d.city)) {
                        const treeType = d.common_name;
                        const count = +d.count;
                        if (treeTypeCounts.has(treeType)) {
                            treeTypeCounts.set(treeType, treeTypeCounts.get(treeType) + count);
                        } else {
                            treeTypeCounts.set(treeType, count);
                        }
                    }
                });

                const stackedData = Array.from(treeTypeCounts, ([treeType, count]) => ({ treeType, count }));
                drawStackedBarChart(stackedData);
                document.getElementById('A1chart3').classList.remove('hidden');
            });

            function drawStackedBarChart(data) {
                const x = d3.scaleLinear().domain([0, d3.max(data, (d) => +d.count)]).range([0, stackedWidth]);
                const y = d3
                    .scaleBand()
                    .range([0, stackedHeight])
                    .domain(data.map((d) => d.treeType))
                    .padding(0.1)
                    .paddingOuter(0.5);

                // Create a color scale for the tree types
                const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

                stackedSvg.selectAll('*').remove();

                stackedSvg
                    .append('g')
                    .selectAll('rect')
                    .data(data)
                    .enter()
                    .append('rect')
                    .attr('x', 0)
                    .attr('y', (d) => y(d.treeType))
                    .attr('width', (d) => x(d.count))
                    .attr('height', y.bandwidth())
                    .attr('fill', (d) => colorScale(d.treeType));

                // Update Y axis
                stackedSvg
                    .append('g')
                    .call(d3.axisLeft(y))
                    .selectAll('text')
                    .style('text-anchor', 'end')
                    .attr('dx', '-0.5em')
                    .attr('dy', '0.5em')
                    .attr('transform', 'rotate(-45)');

                stackedSvg.append('g').call(d3.axisLeft(y));
            }
        });
    },
};

</script>

<style></style>

<template>
  <!-- Bar Chart -->
  <div class="bg-white px-6 lg:px-8 py-22">
    <div class="mx-auto max-w-5xl text-center">
      <h2 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-4xl">Assignment 1 - Comparing Categories</h2>
    </div>
    <div class="mx-auto max-w-5xl">
      <div class="bg-white px-6 lg:px-8 text-center">
        <div class="mx-auto max-w-5xl">
          <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
            A new dataset containing information on 5.6 million trees from 63 major US cities has been compiled, including
            details on location, species, nativity, health, and more.
          </p>
          <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl">Abundance of Trees</p>
        </div>
      </div>
    </div>
    <BarChart/>
    <StackedBarChart/>
    <HeatMap/>
  </div>
</template>
<script>
import * as d3 from 'd3';
import BarChart from '../components/BarChart.vue';
import StackedBarChart from '../components/StackedBarChart.vue';
import HeatMap from '../components/Heatmap.vue';
export default {
  name: 'AssignmentOne',
  components: {
    BarChart,
    StackedBarChart,
    HeatMap,
  },
  /*mounted() {
    // Bar Chart
    const margin = { top: 10, right: 100, bottom: 50, left: 100 };
    const width = 800 - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;

    // Create SVG element for Bar Chart
    const svg = d3.select('#barchart-container')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Heatmap
    const heatmapMargin = { top: 10, right: 10, bottom: 30, left: 40 };
    const heatmapWidth = 800 - heatmapMargin.left - heatmapMargin.right;
    const heatmapHeight = 400 - heatmapMargin.top - heatmapMargin.bottom;

    // Create SVG element for Heatmap
    const heatmapSvg = d3.select('#heatmap-container')
      .append('svg')
      .attr('width', heatmapWidth + heatmapMargin.left + heatmapMargin.right)
      .attr('height', heatmapHeight + heatmapMargin.top + heatmapMargin.bottom)
      .append('g')
      .attr('transform', `translate(${heatmapMargin.left},${heatmapMargin.top})`);

    // Stacked Bar chart
    const stackedMargin = { top: 10, right: 100, bottom: 50, left: 100 };
    const stackedWidth = 800 - stackedMargin.left - stackedMargin.right;
    const stackedHeight = 400 - stackedMargin.top - stackedMargin.bottom;

    // Create SVG element for Stacked Bar chart
    const stackedSvg = d3.select('#stacked-bar-chart-container')
      .append('svg')
      .attr('width', stackedWidth + stackedMargin.left + stackedMargin.right)
      .attr('height', stackedHeight + stackedMargin.top + stackedMargin.bottom)
      .append('g')
      .attr('transform', `translate(${stackedMargin.left},${stackedMargin.top})`);

    // Load data
    d3.csv('/species.csv').then((data) => {
      // Stacked Bar Chart - State Dropdown
      const states = Array.from(new Set(data.map((d) => d.state)));
      const statesS = Array.from(new Set(data.map((d) => d.state)));

      d3.select('#stateSelectStacked')
        .selectAll('option')
        .data(statesS) // Use the populated states from data()
        .enter()
        .append('option')
        .text((d) => d);

      // Add change event listener to the state selection
      d3.select('#stateSelectStacked').on('change', function () {
        const selectedStateS = this.value;
        const filteredData = data.filter((d) => d.state === selectedStateS);
        const limitedData = filteredData.slice(0, 20);
        const maxCount = d3.max(limitedData, (d) => +d.count);
        drawStackedBarChart(limitedData, maxCount);
      });

      // Bar Chart
      const cities = Array.from(new Set(data.map((d) => d.city)));

      // Populate the city selection dropdown
      const citySelect = d3.select('#citySelect');
      citySelect
        .selectAll('option')
        .data(cities)
        .enter()
        .append('option')
        .text((d) => d);

      // Add change event listener to the city selection
      citySelect.on('change', function () {
        const selectedCity = this.value;
        const filteredData = data.filter((d) => d.city === selectedCity);
        const limitedData = filteredData.slice(0, 20);
        const maxCount = d3.max(limitedData, (d) => +d.count);

        drawBarChart(limitedData, maxCount);
        document.getElementById('A1chart1').classList.remove('hidden');
      });

      // Heatmap

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
        stackedSvg.append('g')
          .call(d3.axisLeft(y))
          .selectAll("text")
          .style("text-anchor", "end")
          .attr("dx", "-0.5em")
          .attr("dy", "0.5em")
          .attr("transform", "rotate(-45)");

        stackedSvg.append('g').call(d3.axisLeft(y));
      }

      function drawBarChart(data, maxCount) {
        const x = d3.scaleLinear().domain([0, maxCount]).range([0, width]);
        const y = d3
          .scaleBand()
          .range([0, height])
          .domain(data.map((d) => d.common_name))
          .padding(0.1)
          .paddingOuter(0.5);

        const tooltip = d3.select("#A1chart1")
          .append("div")
          .attr("class", "tooltip");

        function mouseover(event, d) {
          const totalAmount = d.count;
          const treeType = d.common_name;
          const averageHeight = d.mean_h;
          tooltip
            .html(`Tree Type: ${treeType}<br>Total Amount: ${totalAmount}<br>Canopy mean_h: ${averageHeight}`)
            .style('opacity', 1);
          d3.select(this).attr('fill', '#0e6efc');
        }

        function mousemove() {
          tooltip
            .style('left', `${event.pageX + 40}px`)
            .style('top', `${event.pageY + 5}px`);
        }

        function mouseleave() {
          tooltip.style('opacity', 0);
          d3.select(this).attr('fill', (d) => scolor(d.count));
        }

        const scolor = d3.scaleSequential()
          .domain([0, d3.max(data, d => d.count)])
          .interpolator(d3.interpolateGreens);

        svg.selectAll('*').remove();

        svg
          .append('g')
          .attr('transform', `translate(0,${height})`)
          .call(d3.axisBottom(x))
          .selectAll('text')
          .attr('transform', 'translate(-10,0)rotate(-45)')
          .style('text-anchor', 'end');

        svg.append('g').call(d3.axisLeft(y));

        const bars = svg
          .selectAll('.bar')
          .data(data)
          .enter()
          .append('rect')
          .attr('class', 'bar')
          .attr('x', x(0))
          .attr('y', (d) => y(d.common_name))
          .attr('width', 0)
          .attr('height', y.bandwidth())
          .attr('fill', 'steelblue')
          .on('mouseover', mouseover)
          .on('mousemove', mousemove)
          .on('mouseleave', mouseleave);

        bars
          .transition()
          .duration(800)
          .attr('x', 0)
          .attr('width', (d) => x(d.count))
          .delay((d, i) => i * 100);
      }

      function drawHeatmap(data) {
        const cities = Array.from(new Set(data.map((d) => d.city))).slice(0, 5); // Limit to the first 5 cities
        const treeTypes = Array.from(new Set(data.map((d) => d.common_name))).slice(0, 5); // Limit to the first 5 tree types

        const xScale = d3.scaleBand().domain(cities).range([0, heatmapWidth]);
        const yScale = d3.scaleBand().domain(treeTypes).range([0, heatmapHeight]);

        const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([0, d3.max(data, (d) => +d.count)]);

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
          d3.select(this).attr('fill', '#0e6efc');
        }

        function mousemove() {
          tooltip
            .style('left', `${event.pageX + 40}px`)
            .style('top', `${event.pageY + 5}px`);
        }

        function mouseleave() {
          tooltip.style('opacity', 0);
          d3.select(this).attr('fill', (d) => scolor(d.count));
        }

        const scolor = d3.scaleSequential()
          .domain([0, d3.max(data, d => d.count)])
          .interpolator(d3.interpolateGreens);

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
      }
    });
  },*/
};
</script>

<style>
/*.tooltip {
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
  font-size: 0.875rem;
  word-wrap: break-word;
}*/
</style>
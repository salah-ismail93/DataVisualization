<template>
  <div class="bg-white px-6 lg:px-8 text-center mt-8">
    <div class="mx-auto max-w-5xl">
      <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
        Bar Chart
      </h3>
      <div>
        <label for="citySelect">Select City:</label>
        <select id="citySelect">
        </select>
      </div>
      <div class="flex justify-center py-3" id="A1chart1">
        <div class="tooltip A1chart1Inner"></div>
        <!-- Bar chart container -->
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'BarChart',
  mounted() {
    // Bar Chart
    const margin = { top: 10, right: 50, bottom: 50, left: 150 };
    const width = 900 - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;

    // Create SVG element for Bar Chart
    const svg = d3.select('#A1chart1')
      .append('svg')
      .attr('width', width)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    d3.csv('/species.csv').then((data) => {
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
      });
    });

    function drawBarChart(data, maxCount) {
      const x = d3.scaleLinear().domain([0, maxCount]).range([0, width]);
      const y = d3
        .scaleBand()
        .range([0, height])
        .domain(data.map((d) => d.scientific_name))
        .padding(0.1)
        .paddingOuter(0.5);

      const tooltip = d3.select("#A1chart1")
        .append("div")
        .attr("class", "tooltip");

      function mouseover(event, d) {
        const totalAmount = d.count;
        const treeType = d.scientific_name;
        const averageHeight = d.mean_h;
        tooltip
          .html(`Tree Type: ${treeType}<br>Total Amount: ${totalAmount}<br>Canopy mean_h: ${averageHeight}`)
          .style('opacity', 1);
        d3.select(this).attr('fill', '#2222bb');
      }

      function mousemove() {
        tooltip
          .style('left', `${event.pageX + 40}px`)
          .style('top', `${event.pageY + 5}px`);
      }

      function mouseleave() {
        tooltip.style('opacity', 0);
        d3.select(this).attr('fill', 'steelblue');
      }


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
        .attr('y', (d) => y(d.scientific_name))
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

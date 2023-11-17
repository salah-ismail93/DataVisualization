<template>
    <div class="bg-white px-6 lg:px-8 text-center mt-8">
      <div class="mx-auto max-w-5xl">
        <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
          Waffle Chart
        </h3>
    <div class="waffle-chart-container">
      <div>
        <label for="WaffleStateSelect">Select State:</label>
        <select id="WaffleStateSelect" @change="updateChart">
          <option v-for="state in states" :key="state" :value="state">{{ state }}</option>
        </select>
      </div>
      <div id="waffle-chart"></div>
      <!-- Legend can be added here -->
    </div>
      </div>
    </div>
  </template>
  
  <script>
  import * as d3 from 'd3';
  
  export default {
    name: 'WaffleChart',
    data() {
      return {
        states: [], // Array to hold states
        selectedState: '', // Selected state
        data: [], // Your data
        chartSize: 20 // Size of the waffle chart (can be adjusted)
      };
    },
    mounted() {
      // Load your data here
      d3.csv('/species.csv').then((loadedData) => {
        this.data = loadedData;
        this.states = Array.from(new Set(this.data.map(d => d.state)));
        this.selectedState = this.states[0];
        this.drawChart();
        const states = Array.from(new Set(loadedData.map((d) => d.state)));

        d3.select("#WaffleStateSelect")
          .selectAll("option")
          .data(states)
          .enter()
          .append("option")
          .text((d) => d);


      });
    },
    methods: {
      drawChart() {
        // Clear the existing chart
        const chart = d3.select('#waffle-chart');
        chart.selectAll('*').remove();
  
        // Filter data based on the selected state
        const filteredData = this.data.filter(d => d.state === this.selectedState);
  
        // Logic to draw the waffle chart
        // Assuming 'neighborhood' and 'treeType' are fields in your data
        const neighborhoods = Array.from(new Set(filteredData.map(d => d.neighborhood)));
        const treeTypes = Array.from(new Set(filteredData.map(d => d.treeType)));
        const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(treeTypes);
  
        // Sample logic for waffle chart
        neighborhoods.forEach((neighborhood) => {
      const neighborhoodData = filteredData.filter(d => d.neighborhood === neighborhood);
      const waffles = chart.append('div').classed('waffle-neighborhood', true);

      // Adjust the width of each waffle dynamically
      const waffleWidth = 100 / this.chartSize - 2; // Adjust '2' based on margin/padding

      neighborhoodData.forEach(d => {
        waffles.append('div')
          .classed('waffle', true)
          .style('background-color', colorScale(d.treeType))
          .style('width', waffleWidth + '%') // Set the width dynamically
          .style('height', '20px'); // Adjust as needed
      });
    });
      },
      updateChart(event) {
        this.selectedState = event.target.value;
        this.drawChart();
      }
    }
  };
  </script>
  
  <style scoped>
  .waffle-chart-container {
    /* Styles for your container */
  }
  .waffle-neighborhood {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    margin-bottom: 10px;
  }
  .waffle {
    margin: 1px;
    /* Width and height are set dynamically in the script */
  }
  /* Additional styles */
  </style>
  
  
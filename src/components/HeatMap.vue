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
        <div ref="legend" id="chart_2_legend"></div>
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
  
      d3.csv('/public/new_estat_sdg_13_50.csv').then((data) => {
        // Heatmap
        const states = Array.from(new Set(data.map((d) => d.geo\TIME_PERIOD)));
  
        // Populate the state selection dropdown
        const stateSelect = d3.select('#stateSelect');
        stateSelect
          .selectAll('option')
          .data(states)
          .enter()
          .append('option')
          .text((d) => d);
  
        const selectedState = "New York"; // Initial selection
        const filteredData = data.filter((d) => d.geo\TIME_PERIOD === selectedState); // Filter data by selected state
  
        // Function to draw heatmap based on selected state
        let drawHeatmap = (data) => {
          // Your heatmap drawing logic goes here...
        };
  
        // Initial heatmap drawing
        drawHeatmap(filteredData);
  
        // Add change event listener to the state selection
        stateSelect.on('change', function () {
          const selectedState = this.value;
          const filteredData = data.filter((d) => d.geo\TIME_PERIOD === selectedState); // Filter data by selected state
          drawHeatmap(filteredData); // Redraw heatmap based on selected state
        });
      });
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
  }
  #chart_2_legend {
    margin-left: 30%;
    padding-bottom: 5px;
  }
  </style>
  
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
        <div id="waffle-chart">
          <canvas id="waffle-canvas" width="800" height="600"></canvas>
        </div>
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
      states: [],
      selectedState: '',
      data: [],
      cityDetails: [],
      canvasWidth: 800,
      canvasHeight: 600,
      squareSize: 10,
      squarePadding: 2,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      // Load the data from CSV
      d3.csv('/top_5_trees_per_city_with_others.csv').then((loadedData) => {
        this.data = loadedData;
        this.states = Array.from(new Set(this.data.map(d => d.state)));
        this.selectedState = this.states[0];
        this.processData();
        this.drawChart();
      });
    },
    processData() {
      // Filter the data for the selected state
      const filteredData = this.data.filter(d => d.state === this.selectedState);
      // Group by city
      this.cityDetails = d3.groups(filteredData, d => d.city);
    },
    drawChart() {
      const canvas = document.getElementById('waffle-canvas');
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
      
      // Create a color scale based on scientific_name
      const colorScale = d3.scaleOrdinal(d3.schemeCategory10)
        .domain(this.data.map(d => d.scientific_name));

      let yOffset = 0;
      this.cityDetails.forEach(([city, trees]) => {
        // Sort the trees by count, descending
        trees.sort((a, b) => b.count - a.count);

        let x = 0;
        let y = yOffset;
        trees.forEach(tree => {
          for (let i = 0; i < tree.count; i++) {
            ctx.fillStyle = colorScale(tree.scientific_name);
            ctx.fillRect(x * (this.squareSize + this.squarePadding), y, this.squareSize, this.squareSize);
            x++;
            if ((x * (this.squareSize + this.squarePadding)) >= this.canvasWidth) {
              x = 0;
              y += this.squareSize + this.squarePadding;
            }
          }
        });
        yOffset = y + this.squareSize + this.squarePadding; // Update yOffset for the next city
      });
    },
    updateChart(event) {
      this.selectedState = event.target.value;
      this.processData();
      this.drawChart();
    }
  }
};
</script>



<style scoped>
.waffle-chart-container {
  /* Styles for your container */
}
</style>

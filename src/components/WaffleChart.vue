<template>
  <div class="bg-white px-6 lg:px-8 text-center mt-8">
    <div class="mx-auto max-w-5xl">
      <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
        Waffle Chart
      </h3>
      <div>
        <label for="WaffleStateSelect">Select State:</label>
        <select id="WaffleStateSelect" v-model="selectedState" @change="updateChart">
          <option v-for="state in states" :key="state" :value="state">{{ state }}</option>
        </select>
      </div>
      <div class="waffle-chart-grid">
        <div class="waffle-chart-container" v-for="(details, cityIndex) in cityDetails" :key="cityIndex">
          <h4>{{ details.city }}</h4>
          <canvas :id="'waffle-canvas-' + cityIndex" class="waffle-canvas" :width="canvasSize" :height="canvasSize"></canvas>
          <div class="legend">
            <span v-for="(color, name) in details.legend" :key="name">
              <span class="color-box" :style="{ backgroundColor: color }">&nbsp;</span>
              <span class="tree-name">{{ name }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
  
    <!-- Content will be dynamically updated -->
 
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
      canvasSize: 300,
      squareSize: 10,
      squarePadding: 2,
      colorScale: d3.scaleOrdinal(d3.schemeCategory10),
    };
  },
  mounted() {
    this.loadData();

   
  },
  methods: {
    loadData() {
      d3.csv('/top_5_trees_per_city_with_others.csv').then((loadedData) => {
        this.data = loadedData;
        this.states = Array.from(new Set(this.data.map(d => d.state).sort()));
        this.selectedState = this.states[0];
        this.processData();
      });
    },
    processData() {
      const filteredData = this.data.filter(d => d.state === this.selectedState);
      const groupedByCity = d3.group(filteredData, d => d.city);

      this.cityDetails = Array.from(groupedByCity).map(([city, records]) => {
        const trees = records.sort((a, b) => b.count - a.count);
        const legend = trees.map((tree, index) => ({ name: tree.scientific_name, color: this.colorScale(index) }));

        return {
          city,
          trees,
          legend: Object.fromEntries(legend.map(item => [item.name, item.color])),
        };
      });

      this.$nextTick(() => {
        this.cityDetails.forEach((details, cityIndex) => {
          this.drawChart(details, cityIndex);
        });
      });
    },
    drawChart(details, cityIndex) {
      const canvas = document.getElementById('waffle-canvas-' + cityIndex);
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, this.canvasSize, this.canvasSize);

      const maxCount = Math.max(...details.trees.map(tree => tree.count));
      const scaleFactor = 150 / maxCount;
      let squares = [];

      //console.log("maxCount"+maxCount);
      //console.log("maxSquares"+this.maxSquares);
      //console.log("scaleFactor"+scaleFactor);
      
      let x = 0, y = 0;
      const maxPerRow = Math.floor(this.canvasSize / (this.squareSize + this.squarePadding));

      details.trees.forEach(tree => {
        const scaledCount = Math.round(tree.count * scaleFactor);
        console.log("scaleFactor"+scaledCount);
        ctx.fillStyle = details.legend[tree.scientific_name];
        for (let i = 0; i < scaledCount; i++) {
          squares.push({x:x,y:y,tree:tree});
          ctx.fillRect(x * (this.squareSize + this.squarePadding), y, this.squareSize, this.squareSize);
          x++;
          if (x >= maxPerRow) {
            x = 0;
            y += this.squareSize + this.squarePadding;
          }
        }
      });
      canvas.squares=squares;

    },
    updateChart() {
      this.processData();
    },
  
  }
};
</script>
<style scoped>
.waffle-chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.waffle-canvas {
  display: block;
  width: 100%;
  height: auto;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  
}

.color-box {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 5px;
  
}

.tree-name {
  margin-right: 15px;
}

.tooltip {
  display: none;
  position: absolute;
  padding: 8px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: none;
  z-index: 100;
}
</style>


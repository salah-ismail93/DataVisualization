<template>
  <div class="bg-white px-6 lg:px-8 text-center mt-8">
    <div class="mx-auto">
      <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
        Waffle Chart
      </h3>
      <div>
        <label for="selectStateWaffle">Select State:</label>
        <select id="selectStateWaffle">
        </select>
      </div>
      <div class="flex flex-wrap justify-center py-3 flex-column hidden" id="waffle-container">
        <div class="flex flex-wrap flex-row">
          <div class="flex-custom" v-for="(value, key, index) in cities" :key="index" :id="'A1chart5-' + (index + 1)">
            <h3 class="text-left">{{ key }}</h3>
          </div>
          <div id="chart_5_legend"></div>
        </div>
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
      cities: {},
      color_map: {
        'Acer platanoides': 0,
        'Acer saccharum': 1,
        'Acer rubrum': 2,
        'Acer saccharinum': 3,
        'Tilia cordata': 4,
        'Other': 5
      },
      color: null
    }
  },
  mounted() {

    let subgroups = ["Celtis australis", "Aesculus hippocastanum", "Carpinus betulus", "Tilia cordata", "Platanus x hispanica", "Other"]
    this.color = d3.scaleOrdinal()
      .domain(subgroups)
      .range(['#3c51ae', '#ffd43b', '#4daf4a', '#e41a1c', '#FFBCD9', '#adb5bd']);

    // Load the combined CSV file
    d3.csv('/stacked_bar_chart_multiples.csv').then((data) => {
      const states = Array.from(new Set(data.map((d) => d.state)));

      // Populate the state selection dropdown
      const selectStateWaffle = d3.select('#selectStateWaffle');
      selectStateWaffle
        .selectAll('option')
        .data(states)
        .enter()
        .append('option')
        .text((d) => d);

      document.getElementById('waffle-container').classList.add('hidden');
      const selectedState = "New Mexico";
      let citiesInState = data.filter((d) => d.state === selectedState);

      //drawBarChartMultiple(citiesInState);
      // Extract unique city names
      let uniqueCities = Array.from(new Set(citiesInState.map(d => d.city)));

      // Generate cities object with unique identifiers
      this.cities = {};
      uniqueCities.forEach((city, index) => {
        this.cities[city] = index + 1;
      });

      // Use the generated cities object
      // console.log(this.cities);

      // Group data by city
      let groupedData = d3.group(citiesInState, d => d.city);

      // Iterate over the cities and generate the waffle charts for each one
      setTimeout(() => {
        document.getElementById('waffle-container').classList.remove('hidden');
        groupedData.forEach((citiesData) => {
          this.generateWaffleChart(this.cities, citiesData);
        });
      }, 500);
      // Add change event listener to the state selection
      selectStateWaffle.on('change', (value) => {
        document.getElementById('waffle-container').classList.add('hidden');
        const selectedState = value.target.value;
        let citiesInState = data.filter((d) => d.state === selectedState);

        //drawBarChartMultiple(citiesInState);
        // Extract unique city names
        let uniqueCities = Array.from(new Set(citiesInState.map(d => d.city)));

        // Generate cities object with unique identifiers
        this.cities = {};
        uniqueCities.forEach((city, index) => {
          this.cities[city] = index + 1;
        });

        // Use the generated cities object
        // console.log(this.cities);

        // Group data by city
        let groupedData = d3.group(citiesInState, d => d.city);

        // Iterate over the cities and generate the waffle charts for each one
        setTimeout(() => {
          document.getElementById('waffle-container').classList.remove('hidden');
          groupedData.forEach((citiesData) => {
            this.generateWaffleChart(this.cities, citiesData);
          });
        }, 500);
      });

    }).catch((err) => {
      console.error(err);
    });

  },
  methods: {
    generateLegend() {
      const legendData = Object.keys(this.color_map);

      const legendContainer = d3.select('#chart_5_legend');
      legendContainer.selectAll('*').remove(); // Clear existing content

      const legend = legendContainer
        .append('svg')
        .attr('width', 200)
        .attr('height', 120)
        .selectAll('g')
        .data(legendData)
        .enter()
        .append('g')
        .attr('transform', (d, i) => `translate(0, ${i * 20})`);

      legend
        .append('rect')
        .attr('width', 18)
        .attr('height', 18)
        .style('fill', (d) => this.color(this.color_map[d]));

      legend
        .append('text')
        .attr('x', 24)
        .attr('y', 9)
        .attr('dy', '.35em')
        .text((d) => d);
    },

    // Create a function to generate the waffle chart for a given city
    generateWaffleChart(cities, data) {
      var total = 0;
      var widthWaffle,
        heightWaffle,
        widthSquares = 10,
        heightSquares = 10,
        squareSize = 10,
        squareValue = 0,
        gap = 1;

      let theData = [];

      // total
      total = d3.sum(data, function (d) {
        return d.tree_count;
      });

      // value of a square
      squareValue = total / (widthSquares * heightSquares);

      // remap data
      let color_map = this.color_map;
      data.forEach(function (d) {
        d.tree_count = +d.tree_count;
        d.units = Math.round(d.tree_count / squareValue);
        theData = theData.concat(
          Array(d.units + 1).join(1).split('').map(function () {
            return {
              squareValue: squareValue,
              units: d.units,
              abundance: d.tree_count,
              groupIndex: color_map[d.scientific_name],
              name: d.scientific_name,
              neigh: d.city
            };
          })
        );
      });

      if (theData.length < 100) {
        for (let i = 0; i < 100 - theData.length; i++) {
          theData = theData.slice(0, 1).concat(theData);
        }
      }

      theData = theData.slice(0, 100);

      widthWaffle = (squareSize * widthSquares) + widthSquares * gap + 25;
      heightWaffle = (squareSize * heightSquares) + heightSquares * gap + 25;

      // eslint-disable-next-line no-unused-vars
      let waffle = d3.select(`#A1chart5-${cities[data[0]['city']]}`);
      waffle.selectAll('svg').remove();
      let color = this.color;
      waffle
        .append("svg")
        .attr("viewBox", `0 0 ${widthWaffle} ${heightWaffle}`)
        .attr("width", widthWaffle * 2)
        .attr("height", heightWaffle * 2)
        .append("g")
        .attr("transform", `translate(${squareSize / 2},0)`)
        .selectAll("div")
        .data(theData)
        .enter()
        .append("rect")
        .attr("width", squareSize)
        .attr("height", squareSize)
        .attr("fill", function (d) {
          return color(d.groupIndex);
        })
        .attr("x", function (d, i) {
          let col = Math.floor(i / heightSquares);
          return (col * squareSize) + (col * gap);
        })
        .attr("y", function (d, i) {
          let row = i % heightSquares;
          return (heightSquares * squareSize) - ((row * squareSize) + (row * gap));
        })
        .append("title")
        .text(function (d) {
          return "Tree type: " + d.name + "; \nAbundance: " + d.abundance + "; \nPercentage: " + d.units + "%" + "\nCity: " + d.neigh;
        });

      this.generateLegend();
    }
  }
}

</script>

<style scoped>
.flex-custom {
  flex: 1 1 25%
}
</style>

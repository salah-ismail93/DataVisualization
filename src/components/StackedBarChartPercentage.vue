<template>
  <div class="bg-white px-6 lg:px-8 text-center mt-8">
    <div class="mx-auto max-w-5xl">
      <h3 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl">
        Stacked Bar Chart
      </h3>
      <div>
        <label for="selectStateStack100">Select State:</label>
        <select id="selectStateStack100"></select>
      </div>
      <div class="flex justify-center py-3" id="A1chart4">
        <div class="tooltip A1chart4Inner"></div>
        <div id="chart_4_legend100"></div>
      </div>
    </div>
  </div>
</template>
    
<script>
import * as d3 from "d3";

export default {
  name: "StackedBarChartPercentage",
  mounted() {
    // Chart dimensions
    const margin = { top: 10, right: 100, bottom: 50, left: 100 };
    const width = 800 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;

    var svg = d3.select("#A1chart4")
      .append("svg")
      .attr("viewBox", `0 0 1000 500`)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Parse the Data
    d3.csv("/stacked_bar_chart.csv").then(function (allData) {
      // Bar Chart
      const states = Array.from(new Set(allData.map((d) => d.state)));

      // Populate the state selection dropdown
      const selectStateStack100 = d3.select('#selectStateStack100');
      selectStateStack100
        .selectAll('option')
        .data(states)
        .enter()
        .append('option')
        .text((d) => d);

      // Add change event listener to the state selection
      selectStateStack100.on('change', function () {
        const selectedState = this.value;
        let citiesInState = allData.filter((d) => d.state === selectedState);

        if (citiesInState.length > 5) {
          // Sort the array based on the "total" property in descending order
          citiesInState.sort((a, b) => parseFloat(b.total) - parseFloat(a.total));

          // Get the first 5 objects
          let biggestCitiesInState = citiesInState.slice(0, 5);

          drawBarChart(allData, selectedState, biggestCitiesInState);
        } else {
          console.log("The number of objects is not greater than 5.");
          drawBarChart(allData, selectedState, citiesInState);
        }
      });


    }).catch((err) => {
      console.error(err)
    });

    function drawBarChart(allData, selectedState, biggestCitiesInState) {
      // List of treeNames = header of the csv files = soil condition here
      var treeNames = allData.columns.slice(2, -1);
      // List of citiesNames = species here = value of the first column called group -> I show them on the X axis
      var citiesNames = Array.from(new Set(biggestCitiesInState.filter(function (d) { return d.state === selectedState; }).map(function (d) { return d.city; })));

      // Calculate the total for each city
      var cityTotals = biggestCitiesInState.reduce((acc, city) => {
        acc[city.city] = d3.sum(treeNames, (tree) => +city[tree]);
        return acc;
      }, {});

      // Calculate percentages
      biggestCitiesInState.forEach((city) => {
        treeNames.forEach((tree) => {
          city[tree] = +city[tree] / cityTotals[city.city];
        });
      });

      // stack the data --> stack per subgroup
      var stackedData = d3.stack()
        .keys(treeNames)(biggestCitiesInState);

      // Update X axis to represent percentages
      var x = d3.scaleLinear()
        .domain([0, 1]) // 0% to 100%
        .range([0, width]);

      svg.selectAll('*').remove();

      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSizeOuter(0))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

      // Add Y axis
      var y = d3.scaleBand()
        .domain(citiesNames)
        .range([0, height])
        .padding([0.2]);
      svg.append("g")
        .call(d3.axisLeft(y));
      // color palette = one color per subgroup
      var color = d3.scaleOrdinal()
        .domain(treeNames)
        .range(['#3c51ae', '#ffd43b', '#4daf4a', '#e41a1c', '#FFBCD9', '#adb5bd']);

      // Create a tooltip
      var tooltip2 = d3.select("#A1chart4")
        .append("div")
        .attr("class", "tooltip");

      // Three functions that change the tooltip when the user hovers / moves / leaves a cell
      var mouseover2 = function (event, d) {
        var subgroupName = d3.select(this.parentNode).datum().key;
        var subgroupValue = d.data[subgroupName];
        tooltip2
          .html("Tree Type: " + subgroupName + "<br>" + "Percentage: " + ((subgroupValue * 100).toFixed(2)) + "%")
          .style("opacity", 1);
        d3.select(this).attr("fill", "#0e6efc");
      };

      var mousemove2 = function (event) {
        tooltip2
          .style('left', (event.pageX + 30) + 'px')
          .style('top', (event.pageY + 10) + 'px');
      };

      // Show the bars
      svg.append("g")
        .selectAll("g")
        // Enter the stack data = loop key per key = group per group
        .data(stackedData)
        .join("g")
        .attr("fill", function (d) {
          return color(d.key);
        })
        .selectAll("rect")
        // Enter a second time = loop subgroup per subgroup to add all rectangles
        .data(function (d) {
          return d;
        })
        .join("rect")
        .attr("x", function (d) {
          return x(d[0]);
        })
        .attr("y", function (d) {
          return y(d.data.city);
        })
        .attr("height", y.bandwidth())
        .attr("width", function (d) {
          return x(d[1]) - x(d[0]);
        })
        .on("mouseover", mouseover2)
        .on("mousemove", mousemove2)
        .on("mouseleave", function () {
          tooltip2.style("opacity", 0);
          d3.select(this).attr("fill", function () {
            return color;
          });
        });

      var color_map = {
        'Acer platanoides': 0,
        'Acer saccharum': 1,
        'Acer rubrum': 2,
        'Acer saccharinum': 3,
        'Tilia cordata': 4,
        'Other': 5
      }

      // Remove existing legend before updating
      d3.select("#chart_4_legend100 svg").remove();

      var legend = d3.select("#chart_4_legend100")
        .append("svg")
        .attr('width', 300)
        .attr('height', 200)
        .append('g')
        .attr("transform", `translate(50,0)`)
        .selectAll("div")
        .data(treeNames)
        .join("g")
        .attr('transform', function (d, i) { return "translate(0," + i * 30 + ")"; });

      legend.append("rect")
        .attr("width", 20)
        .attr("height", 20)
        .style("fill", function (d) { return color(color_map[d]); });

      legend.append("text")
        .attr("x", 25)
        .attr("y", 15)
        .text(function (d) { return d; });
    }

  },
};
</script>
    
<style></style>
    
<template>
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
  import * as d3 from "d3";
  
  export default {
    name: "StackedBarChart",
    mounted() {
      const margin = { top: 10, right: 100, bottom: 50, left: 100 };
      const width = 800 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;
  
      const svg = d3
        .select("#stacked-bar-chart-container")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
  
      d3.csv("/species.csv").then((data) => {
        const states = Array.from(new Set(data.map((d) => d.state)));
        d3.select("#stateSelectStacked")
          .selectAll("option")
          .data(states)
          .enter()
          .append("option")
          .text((d) => d);
  
        d3.select("#stateSelectStacked").on("change", function () {
          const selectedState = this.value;
          const filteredData = data.filter((d) => d.state === selectedState);
          const processedData = processDataForStackedChart(filteredData);
          drawStackedBarChart(processedData);
          document.getElementById("A1chart3").classList.remove("hidden");
        });
      });
  
      function processDataForStackedChart(rawData) {
        // Aggregate data by city and then tree type
        const cityTreeData = d3.rollups(
          rawData,
          (v) => d3.sum(v, (d) => +d.count),
          (d) => d.city,
          (d) => d.common_name
        );
  
        // Prepare data structure for stacked bar chart
        const topTrees = new Set();
        cityTreeData.forEach(([trees]) => {
          trees.sort((a, b) => b[1] - a[1]);
          trees.slice(0, 5).forEach(([tree]) => topTrees.add(tree));
        });
  
        const stackedData = cityTreeData.map(([city, trees]) => {
          const treeMap = new Map(trees);
          const treeData = { city };
          let otherCount = 0;
  
          topTrees.forEach((tree) => {
            treeData[tree] = treeMap.get(tree) || 0;
          });
  
          treeMap.forEach((count, tree) => {
            if (!topTrees.has(tree)) otherCount += count;
          });
  
          treeData["Other"] = otherCount;
          return treeData;
        });
  
        return {
          data: stackedData,
          keys: Array.from(topTrees).concat(["Other"]),
        };
      }
  
      function drawStackedBarChart({ data, keys }) {
        svg.selectAll("*").remove();
  
        const x = d3
          .scaleLinear()
          .domain([0, d3.max(data, (d) => d3.sum(keys, (key) => d[key]))])
          .range([0, width]);
  
        const y = d3
          .scaleBand()
          .domain(data.map((d) => d.city))
          .range([0, height])
          .padding(0.1);
  
        const color = d3.scaleOrdinal(d3.schemeCategory10);
  
        const stack = d3.stack().keys(keys);
        svg
          .append("g")
          .selectAll("g")
          .data(stack(data))
          .enter()
          .append("g")
          .attr("fill", (d) => color(d.key))
          .selectAll("rect")
          .data((d) => d)
          .enter()
          .append("rect")
          .attr("x", (d) => x(d[0]))
          .attr("y", (d) => y(d.data.city))
          .attr("width", (d) => x(d[1]) - x(d[0]))
          .attr("height", y.bandwidth());
  
        svg.append("g").call(d3.axisLeft(y));
  
        svg
          .append("g")
          .attr("transform", `translate(0,${height})`)
          .call(d3.axisBottom(x));
      }
    },
  };
  </script>
  
  <style></style>
  
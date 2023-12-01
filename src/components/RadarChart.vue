<template>
  <div class="mx-auto max-w-5xl py-3">
    <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Mean Montly Temperature</p>
    <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
      Radar chart visualizing USA states monthly temperature means for the desired years, with hover information for max,
      min, and mean temperatures.
    </p>
  </div>
  <div class="flex">
    <div id="state-selector">
      <label for="state-dropdown" style="margin-left: 10px;">Select State:</label>
      <select v-model="selectedState" class="selectpicker" id="state-dropdown" data-style="btn-primary"
        data-live-search="true">
        <option v-for="option in stateOptions" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>
    <div class="dropdown">
        <button class="btn btn-primary dropdown-toggle" type="button" id="year-dropdown-radar" data-toggle="dropdown"
          aria-haspopup="true" aria-expanded="false" style="margin-left: 8px;">
          Select Year
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="max-height: 250px; overflow-y: auto;">
          <form id="year-checkbox-form-radar" style="padding: 5px;">
            <div v-for="year in yearsOptions" :key="year">
              <div class="form-check-radar">
                <input class="form-check-radar-input" type="checkbox" :value="year" :id="'Radarcheck' + year"
                  v-model="selectedYears" />
                <label :for="'Radarcheck' + year" class="form-check-radar-label">{{ year }}</label>
              </div>
            </div>
          </form>
        </div>
      </div>
    <div class="flex justify-center py-3" id="A3chart2">
      <div class="tooltip A3chart2Inner"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'RadarChart',
  data() {
    return {
      yearsOptions: [],
      stateOptions: [],
      selectedState: 'Alabama',
      selectedYears: ['1895'],
    };
  },
  // Add your component logic here
  mounted() {
    this.drawRadarChart('Alabama', ['1895']);
    // Listen for changes in the dropdown selection
    document.getElementById("state-dropdown").addEventListener("change", (value) => {
      const selectedState = value.target.value;

      let svgA3T2 = d3.select("#A3chart2")
      svgA3T2.selectAll('svg').remove();

      // Select all checked checkboxes
      const checkedCheckboxes = document.querySelectorAll("#year-checkbox-form-radar input:checked");

      // Extract values of checked checkboxes
      const selectedYears = Array.from(checkedCheckboxes).map(checkbox => checkbox.value);

      this.drawRadarChart(selectedState, selectedYears);
    });
    // Add an event listener for changes in the year dropdown
    document.getElementById("year-checkbox-form-radar").addEventListener("change", () => {
      // Select all checked checkboxes
      let checkedCheckboxes = document.querySelectorAll('.form-check-radar-input:checked');
      if (checkedCheckboxes.length > 10) {
        alert('Maximum 10 checkboxes allowed!');
        // Uncheck the last checkbox
        event.target.checked = false;
      } else {
        const selectedState = document.getElementById("state-dropdown").value;
        // Extract values of checked checkboxes
        const selectedYears = Array.from(checkedCheckboxes).map(checkbox => checkbox.value);
    
        let svgA3T2 = d3.select("#A3chart2")
        svgA3T2.selectAll('svg').remove();
        this.drawRadarChart(selectedState, selectedYears);
      }
    });
  },
  methods: {
    drawRadarChart(selectedState, selectedYears) {
      // Set the dimensions and margins of the graph
      let margin = { top: 60, right: 40, bottom: 70, left: 60 },
        width = 1000 - margin.left - margin.right,
        height = 700 - margin.top - margin.bottom;

      //RadarChart
      function angleToCoordinate(angle, value) {
        let x = Math.cos(angle) * radialScale(value);
        let y = Math.sin(angle) * radialScale(value);
        return { "x": 300 + x, "y": 300 - y };
      }

      const features = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
      let colors = ["darkorange", "gray", "navy", "blue", "red", "green", "black", "yellow"];


      let svgA3T2 = d3.select("#A3chart2").append("svg")
        .attr("viewBox", `0 0 700 700`)
        .attr("width", width)
        .attr("height", height);

      let radialScale = d3.scaleLinear()
        .domain([-10, 30])
        .range([0, 250]);
      let ticks = [-10, 0, 10, 20, 30];
      ticks.forEach(t =>
        svgA3T2.append("circle")
          .attr("cx", 300)
          .attr("cy", 300)
          .attr("fill", "none")
          .attr("stroke", "gray")
          .attr("r", radialScale(t))
      );
      ticks.forEach(t =>
        svgA3T2.append("text")
          .attr("x", 305)
          .attr("y", 300 - radialScale(t))
          .text(t.toString())
      );


      for (var i = 0; i < features.length; i++) {
        let ft_name = features[i];
        let angle = (Math.PI / 2) + (2 * Math.PI * i / features.length);
        let line_coordinate = angleToCoordinate(angle, 30);
        let label_coordinate = angleToCoordinate(angle, 32);

        //draw axis line
        svgA3T2.append("line")
          .attr("x1", 300)
          .attr("y1", 300)
          .attr("x2", line_coordinate.x)
          .attr("y2", line_coordinate.y)
          .attr("stroke", "black");

        //draw axis label
        svgA3T2.append("text")
          .attr("x", label_coordinate.x)
          .attr("y", label_coordinate.y)
          .text(ft_name);
      }
      let line = d3.line()
        .x(d => d.x)
        .y(d => d.y);


      function getPathCoordinates(data_point) {
        let coordinates = [];
        for (var i = 0; i < features.length + 1; i++) {
          let ft_name = features[i % features.length];
          let angle = (Math.PI / 2) + (2 * Math.PI * i / features.length);
          coordinates.push(angleToCoordinate(angle, parseFloat(data_point[ft_name])));
        }
        return coordinates;
      }

      // ---------------------------//
      //       HIGHLIGHT GROUP      //
      // ---------------------------//

      // What to do when one group is hovered
      var highlight = function (e, d) {
        // reduce opacity of all groups
        d3.selectAll("path").style("opacity", .01)
        d3.selectAll(".circle-mean").style("opacity", .01)

        // expect the one that is hovered
        console.log(d)
        d3.select(`#Year${d}`).style("opacity", 1)
        d3.selectAll(`#mean${d}`).style("opacity", 1)
      }

      // And when it is not hovered anymore
      var noHighlight = function () {
        d3.selectAll("path").style("opacity", 1)
        d3.selectAll(".circle-mean").style("opacity", 1)
      }

      // ---------------------------//
      //     INTERACTIVE LEGEND     //
      // ---------------------------//


      // Add one dot in the legend for each name.
      var size = 20
      var moveX = 300
      // eslint-disable-next-line no-unused-vars
      var moveY = 50
      var xCircle = 390 + moveX
      // eslint-disable-next-line no-unused-vars
      var xLabel = 440 + moveX


      svgA3T2.selectAll("myrect")
        .data(selectedYears)
        .enter()
        .append("circle")
        .attr("cx", xCircle)
        .attr("cy", function (d, i) { return 10 + i * (size + 5) + 200 }) // 100 is where the first dot appears. 25 is the distance between dots
        .attr("r", 7)
        .style("fill", function (d, i) { return colors[i] })
        .on("mouseover", highlight)
        .on("mouseleave", noHighlight)

      // Add labels beside legend dots
      svgA3T2.selectAll("mylabels")
        .data(selectedYears)
        .enter()
        .append("text")
        .attr("x", xCircle + size * .8)
        .attr("y", function (d, i) { return i * (size + 5) + (size / 2) + 202 }) // 100 is where the first dot appears. 25 is the distance between dots
        .style("fill", function (d, i) { return colors[i] })
        .text(function (d) { return d })
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle")
        .on("mouseover", highlight)
        .on("mouseleave", noHighlight)




      d3.csv("/all_data_melted.csv",

        function (d) {
          return {
            year: d.year,
            month: d.month,
            mean: d.mean,
            state: d.state
          }
        }).then((data) => {
          // Bar Chart
          this.stateOptions = [...new Set(data.map((d) => d.state))];
          this.yearsOptions = [...new Set(data.map((d) => d.year))];
          if (selectedState && selectedYears) {
          data = data.filter(item => {
            // Specify the desired years and state
            const desiredYears = selectedYears;
            const desiredState = selectedState;

            // Check if the item's year and state match the desired values
            return desiredYears.includes(item.year) && item.state === desiredState;
          });
        }
          //Tooltip
          var tooltipA3T2 = d3.select("#A3chart2")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("font-size", "16px");

          let mouseoverA3T2_mean = function (e, d) {
            console.log(d)
            tooltipA3T2
              .transition()
              .duration(200)
              .style("opacity", 1)
            tooltipA3T2
              .html("<span style='color:grey'>Year: </span> " + d.year + "<br><span style='color:grey'>Month: </span> " + d.month + "<br><span style='color:grey'>Mean Temp (°C): </span>" + d.mean)
            d3.selectAll("path").style("opacity", .01)
            d3.selectAll(".circle-mean").style("opacity", .01)

            // expect the one that is hovered
            console.log(d)
            d3.select(`#Year${d.year}`).style("opacity", 1)
            d3.selectAll(`#mean${d.year}`).style("opacity", 1)
          }
          let mousemoveA3T2 = function () {
            tooltipA3T2
              .style('left', (event.pageX + 20) + 'px')
              .style('top', (event.pageY + 10) + 'px')

          }
          let mouseleaveA3T2 = function () {
            tooltipA3T2
              .transition()
              .duration(200)
              .style("opacity", 0);
            d3.selectAll("path").style("opacity", 1)
            d3.selectAll(".circle-mean").style("opacity", 1)
          }
          let count = 0
          for (i = 0; i < selectedYears.length; i++) {

            let temp_year = data.filter(function (row) {
              return row.year == selectedYears[i];
            });

            let dict = {}
            temp_year.forEach(function (d) {
              dict[d.month] = d.mean;
            });
            //console.log(dict);
            let color = colors[i];
            let coordinates = getPathCoordinates(dict);
            //draw the path element
            svgA3T2.append("path")
              .datum(coordinates)
              .attr("d", line)
              .attr("id", "Year" + selectedYears[i])
              .attr("stroke-width", 3)
              .attr("stroke", color)
              .attr("fill", "none")
              .attr("stroke-opacity", 1)
              .attr("opacity", 1);

            // eslint-disable-next-line no-unused-vars
            for (const [key, value] of Object.entries(dict)) {
              svgA3T2
                .append("circle")
                // it doubles line [*]

                .attr("id", function () { return "mean" + selectedYears[i] })
                .attr("class", "circle-mean")
                // full notation for the node    
                // [*] selection.classed() method for classes,
                // but you can omit this line because you wrote .selectAll(".datapoints") above
                .attr("fill", color)  // you must make big dots 
                // to be clickable for people
                .attr("stroke", "white")
                // .attr("stroke-width", "1")
                .attr("cx", function () {

                  let angle = (Math.PI / 2) + (2 * Math.PI * count / features.length);
                  return angleToCoordinate(angle, value).x

                })
                .attr("cy", function () {

                  let angle = (Math.PI / 2) + (2 * Math.PI * count / features.length);
                  return angleToCoordinate(angle, value).y

                })
                .attr("r", 3)

              count++
            }

          }

          d3.selectAll(".circle-mean").data(data)
            .on("mouseover", mouseoverA3T2_mean)
            .on("mousemove", mousemoveA3T2)
            .on("mouseleave", mouseleaveA3T2);
        }).catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style scoped></style>

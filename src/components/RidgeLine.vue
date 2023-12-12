<template>
  <div class="mx-auto max-w-5xl py-3">
    <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl text-center">Distribution of Max & Min temp for all
      months (ridgelines plot)</p>
    <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
      Yearly distribution of max and min temperatures, filtered by state, displayed with vertical ridge lines to emphasize
      heights.
    </p>
  </div>
  <div class="flex items-center justify-center">
    <div class="filtering mb-12">
      <div id="state-selector-ridge">
        <label for="state-dropdown-ridge" style="margin-left: 10px;">Select State:</label>
        <select v-model="ridgeSelectedState" class="selectpicker" id="state-dropdown-ridge" data-style="btn-primary"
          data-live-search="true">
          <option v-for="option in ridgeOptionsStates" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>
      <div class="dropdown">
        <button class="btn btn-primary dropdown-toggle" type="button" id="year-dropdown-ridge" data-toggle="dropdown"
          aria-haspopup="true" aria-expanded="false" style="margin-left: 8px;">
          Select Year
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" style="max-height: 250px; overflow-y: auto;">
          <form id="year-checkbox-form-ridge" style="padding: 5px;">
            <div v-for="year in ridgeOptionsYears" :key="year">
              <div class="form-check-ridge">
                <input class="form-check-ridge-input" type="checkbox" :value="year" :id="'Ridgecheck' + year"
                  v-model="ridgeSelectedYear" />
                <label :for="'Ridgecheck' + year" class="form-check-ridge-label">{{ year }}</label>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div class="flex items-center justify-center loading-chart">
    <div v-if="!isLoading3" id="A3chart3">
      <div class="tooltip A3chart3Inner"></div>
      <div id="chart_3_legend"></div>
    </div>
    <div v-if="isLoading3">
      <div class="border-t-transparent border-solid animate-spin rounded-full border-blue-400 border-8 h-32 w-32"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'RidgeLine',
  data() {
    return {
      ridgeSelectedState: [],
      ridgeSelectedYear: [],
      ridgeOptionsStates: [],
      ridgeOptionsYears: [],
      isLoading3: true
    }
  },
  // Component properties and methods here
  mounted() {
    function filterDataByYearsAndStates(data, state, years) {
      return data.filter(function (d) {
        return d.state === state &&
          years.includes(d.year.toString());
      });
    }
    let drawRidgeLine = (selectedState, selectedYears) => {
      if (selectedState && selectedYears.length > 0) {
        const margin = { top: 80, right: 30, bottom: 50, left: 50 },
          width = 1000 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

        d3.select("#A3chart3").select('svg').remove();
        // append the svg object to the body of the page
        const svg = d3.select("#A3chart3")
          .append("svg")
          .attr("width", width + 100 + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform",
            `translate(${margin.left},${margin.top})`);

        d3.csv("/all_data_melted.csv").then((fullData) => {
          this.ridgeOptionsStates = [...new Set(fullData.map((d) => d.state))];
          this.ridgeOptionsYears = [...new Set(fullData.map((d) => d.year))];

          // Convert string data to numbers
          let data = filterDataByYearsAndStates(fullData, selectedState, selectedYears)
          data.forEach(function (d) {
            d.year = +d.year;
            d.min = +d.min;
            d.max = +d.max;
          });

          // Get the unique years from your data
          var years = Array.from(new Set(data.map(d => d.year)));

          // Define the categories for minimum and maximum temperatures
          var categories = ["min", "max"];

          // Create a color scale using a suitable color scheme for temperature
          var minTemperatureColors = {};
          var maxTemperatureColors = {};

          years.forEach(year => {
            var blueStart = d3.color("lightblue");
            var blueEnd = d3.color("darkblue");
            var redStart = d3.color("lightsalmon");
            var redEnd = d3.color("darkred");

            var blueGradient = d3.scaleLinear().domain([0, 1]).range([blueStart, blueEnd]);
            var redGradient = d3.scaleLinear().domain([0, 1]).range([redStart, redEnd]);

            minTemperatureColors[year] = blueGradient(years.indexOf(year) / (years.length)).toString();
            maxTemperatureColors[year] = redGradient(years.indexOf(year) / (years.length)).toString();
          });
          function getColor(temperatureType, year) {
            if (temperatureType === "min") {
              return minTemperatureColors[year];
            } else if (temperatureType === "max") {
              return maxTemperatureColors[year];
            }
          }
          var gap = 0
          for (var i = 0; i < years.length; i++) {
            gap = gap + 15
            svg.append("circle").attr("cx", width - gap).attr("cy", 0).attr("r", 6).style("fill", minTemperatureColors[years[i]])
            svg.append("circle").attr("cx", width - gap).attr("cy", 30).attr("r", 6).style("fill", maxTemperatureColors[years[i]])
          }

          svg.append("text").attr("x", width - gap).attr("y", -15).text("Min").style("font-size", "10px").attr("alignment-baseline", "left")
          svg.append("text").attr("x", width - gap).attr("y", 18).text("Max").style("font-size", "10px").attr("alignment-baseline", "left")

          function createArrayWithIntervals(maxNumber, interval) {
            const result = [];
            maxNumber = Math.ceil(maxNumber / interval) * interval;
            for (let i = 0; i <= maxNumber; i += interval) {
              result.push(i);
            }
            return result;
          }
          // Add X axis for temperature values
          let maxRange = Math.ceil(d3.max(data).max / 10) * 10 + 10;
          var x = d3.scaleLinear()
            .domain([-20, 40]) // Adjust the domain based on your data range
            .range([0, width - 200]);

          var xAxis = svg.append("g")
            .attr("class", "xAxis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickValues(createArrayWithIntervals(maxRange, 10)));

          // Add X axis label
          svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width - 200)
            .attr("y", height + 40)
            .text("Max & Min Montly Temperature (°C)");
          // Compute kernel density estimation for each column (year and temperature type)
          function kernelDensityEstimator(kernel, X) {
            return function (V) {
              return X.map(function (x) {
                return [x, d3.mean(V, function (v) { return kernel(x - v); })];
              });
            };
          }
          function kernelEpanechnikov(k) {
            return function (v) {
              return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
            };
          }
          // Compute kernel density estimation for each column (year and temperature type)
          var kde = kernelDensityEstimator(kernelEpanechnikov(1), x.ticks(10)); // Adjust ticks based on your data
          var allDensity = [];

          for (let i = 0; i < years.length; i++) {
            var year = years[i];
            for (var j = 0; j < categories.length; j++) {
              var key = categories[j];
              var density = kde(data.filter(d => d.year === year).map(d => d[key]));
              allDensity.push({ key: key, year: year, density: density });
            }
          }

          // Create a Y scale for densities
          const y = d3.scaleLinear()
            .domain([0, 1])
            .range([height, 0]);


          // Create the Y axis for names
          const yName = d3.scaleBand()
            .domain(years)
            .range([0, height])
            .paddingInner(1)
          svg.append("g")
            .call(d3.axisLeft(yName).tickSize(0))
            .select(".domain").remove()

          function rgbToHex(rgb) {
            // Extract the RGB values using a regular expression
            const rgbArray = rgb.match(/\d+/g);

            // Convert each RGB value to its hexadecimal representation
            const hexArray = rgbArray.map(value => {
              const hex = parseInt(value, 10).toString(16);
              return hex.length === 1 ? '0' + hex : hex; // Ensure two digits
            });

            // Concatenate the hexadecimal values and prepend the #
            const hexColor = '#' + hexArray.join('');

            return hexColor;
          }

          // Add areas for Ridgeline plot
          var myCurves = svg.selectAll(".myCurves")
            .data(allDensity)
            .enter()
            .append("path")
            .attr("class", "myCurves")
            .attr("transform", function (d) {
              return "translate(0," + (yName(d.year) - height) + ")";
            })
            .attr("fill", function (d) {
              return getColor(d.key, d.year); // Color based on temperature type (minimum or maximum)
            })
            .attr("fill-opacity", "0.5")
            .attr("stroke", function (d) {
              const hexColor = rgbToHex(getColor(d.key, d.year));
              return hexColor; // Color based on temperature type (minimum or maximum)
            })
            .datum(function (d) {
              return d.density;
            })
            .attr("stroke-width", 2)
            .attr("d", d3.line()
              .curve(d3.curveBasis)
              .x(function (d) {
                return x(d[0]);
              })
              .y(function (d) {
                return y(d[1]);
              })
            );
          this.isLoading3 = false;
        }).catch(function (error) {
          console.log("Error loading the data: " + error);
        });
      }
    }
    drawRidgeLine('Alabama', ['1895', '1896', '1897']);
    // Listen for changes in the dropdown selection
    document.getElementById("state-dropdown-ridge").addEventListener("change", (value) => {
      const selectedState = value.target.value;

      let svgA3T3 = d3.select("#A3chart3")
      svgA3T3.selectAll('svg').remove();

      // Select all checked checkboxes
      const checkedCheckboxes = document.querySelectorAll("#year-checkbox-form-ridge input:checked");

      // Extract values of checked checkboxes
      const selectedYears = Array.from(checkedCheckboxes).map(checkbox => checkbox.value);

      drawRidgeLine(selectedState, selectedYears);
      scrollToDiv();
    });
    // Add an event listener for changes in the year dropdown
    document.getElementById("year-checkbox-form-ridge").addEventListener("change", () => {
      // Select all checked checkboxes
      let checkedCheckboxes = document.querySelectorAll('.form-check-ridge-input:checked');
      if (checkedCheckboxes.length > 10) {
        alert('Maximum 10 checkboxes allowed!');
        // Uncheck the last checkbox
        event.target.checked = false;
      } else {
        const selectedState = document.getElementById("state-dropdown-ridge").value;
        // Extract values of checked checkboxes
        const selectedYears = Array.from(checkedCheckboxes).map(checkbox => checkbox.value);

        let svgA3T3 = d3.select("#A3chart3")
        svgA3T3.selectAll('svg').remove();
        drawRidgeLine(selectedState, selectedYears);
        scrollToDiv();
      }
    });

    function scrollToDiv() {
      // Access the target div using its id
      const targetDiv = document.getElementById('A3chart3');

      if (targetDiv) {
        // Scroll to the target div
        targetDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }
}
</script>

<style scoped>
.ridgeline {
  /* Your component styles here */
}
</style>

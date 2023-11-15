<template>
  <!-- Bar Chart -->
  <div class="bg-white px-6 lg:px-8 py-22">
    <div class="mx-auto max-w-5xl text-center">
      <h2 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-4xl">Assignment 1 - Comparing Categories</h2>
    </div>
    <div class="mx-auto max-w-5xl">
      <div class="bg-white px-6 lg:px-8 text-center">
        <div class="mx-auto max-w-5xl">
          <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
            A new dataset containing information on 5.6 million trees from 63 major US cities has been compiled, including
            details on location, species, nativity, health, and more.
          </p>
          <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl">Abundance of Trees</p>
        </div>
      </div>
    </div>
    <BarChart />
    <StackedBarChart />
    <HeatMap />
  </div>
</template>
<script>
import BarChart from '../components/BarChart.vue';
import StackedBarChart from '../components/StackedBarChart.vue';
import HeatMap from '../components/heatmap.vue';
export default {
  name: 'AssignmentOne',
  components: {
    BarChart,
    StackedBarChart,
    HeatMap,
  },
  mounted() {


  },
};
</script>

<style>
/*.tooltip {
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
  font-size: 0.875rem;
  word-wrap: break-word;
}*/
</style>
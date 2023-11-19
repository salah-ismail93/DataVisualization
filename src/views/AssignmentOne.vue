<template>
  <!-- Bar Chart -->
  <div class="bg-white px-6 lg:px-8 py-22 main">
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
  </div>

  <div>
    <div class="sm:hidden">
      <label for="tabs" class="sr-only">
        Select a tab
      </label>
      <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
      <select id="tabs" name="tabs" v-model="selectedTab"
        class="block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
        <option v-for="tab in tabs" :key="tab.name" :value="tab.name">
          {{ tab.name }}
        </option>
      </select>
    </div>
    <div class="hidden sm:block">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <a v-for="tab in tabs" :key="tab.name" :href="tab.href" :class="{
            'border-indigo-500 text-indigo-600': tab.current,
            'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700': !tab.current,
            'whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium': true,
          }" :aria-current="tab.current ? 'page' : undefined" @click.prevent="selectTab(tab)">
            {{ tab.name }}
          </a>
        </nav>
      </div>
    </div>
    <!-- Your tab content goes here -->
    <div v-show="selectedTab === 'Bar Chart'">
      <!-- Content for BarChart Tab -->
      <BarChart />
    </div>
    <div v-show="selectedTab === 'Stacked Bar Chart'">
      <!-- Content for StackedBarChart Tab -->
      <StackedBarChart />
    </div>
    <div v-show="selectedTab === 'Stacked Bar Chart Percentage'">
      <!-- Content for StackedBarChartPercentage Tab -->
      <StackedBarChartPercentage />
    </div>
    <div v-show="selectedTab === 'Heat Map'">
      <!-- Content for HeatMap Tab -->
      <HeatMap />
    </div>
    <div v-show="selectedTab === 'Waffle Chart'">
      <!-- Content for WaffleChart Tab -->
      <WaffleChart />
    </div>
  </div>
</template>
<script>
import BarChart from '../components/BarChart.vue';
import StackedBarChart from '../components/StackedBarChart.vue';
import StackedBarChartPercentage from '../components/StackedBarChartPercentage.vue';
import HeatMap from '../components/HeatMap.vue';
import WaffleChart from '../components/WaffleChart.vue';
export default {
  name: 'AssignmentOne',
  components: {
    BarChart,
    StackedBarChart,
    StackedBarChartPercentage,
    HeatMap,
    WaffleChart,
  },
  data() {
    return {
      tabs: [
        { name: 'Bar Chart', href: '#', current: true },
        { name: 'Stacked Bar Chart', href: '#', current: false },
        { name: 'Stacked Bar Chart Percentage', href: '#', current: false },
        { name: 'Heat Map', href: '#', current: false },
        { name: 'Waffle Chart', href: '#', current: false },
      ],
      selectedTab: 'BarChart',
    };
  },
  methods: {
    selectTab(tab) {
      this.tabs.forEach((t) => {
        t.current = t.name === tab.name;
        this.selectedTab = tab.name;
      });
    },
  },
  mounted() {


  },
};
</script>

<style>

</style>
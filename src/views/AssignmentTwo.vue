<template>
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
        <div v-show="selectedTab === 'Alluvial'">
            <!-- Content for Alluvial Tab -->
            <AlluvialChart />
        </div>
        <div v-show="selectedTab === 'Chart2'">
            <!-- Content for Chart2 Tab -->
            <p>Chart2</p>
        </div>
        <div v-show="selectedTab === 'Chart3'">
            <!-- Content for Chart3 Tab -->
            <p>Chart3</p>
        </div>
        <div v-show="selectedTab === 'Chart4'">
            <!-- Content for Billing Tab -->
            <p>Chart4</p>
        </div>
    </div>
</template>
  
<script>
import  AlluvialChart  from "../components/AlluvialChart.vue";  // Import the AlluvialChart component

export default {
    name: 'AssignmentTwo',
    components: {
        AlluvialChart, // Import the AlluvialChart component
    },
    data() {
        return {
            tabs: [
                { name: 'Alluvial', href: '#', current: true },
                { name: 'Chart2', href: '#', current: false },
                { name: 'Chart3', href: '#', current: false },
                { name: 'Chart4', href: '#', current: false },
            ],
            selectedTab: 'Alluvial',
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
};
</script>
 
<style>
</style>

<template>
    <!--  About the team and project  -->
    <div class="bg-white px-6 lg:px-8 py-32">
        <div class="mx-auto max-w-5xl text-center">
            <h2 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Assignment 2 - Flux (Sankey or alluvial
                Diagram)
            </h2>

        </div>
    </div>

    <!-- The charts are here -->
    <div class="bg-white px-6 lg:px-8 text-center">
        <div class="mx-auto max-w-5xl">
            <p class="mt-4 text-base leading-7 text-indigo-600 sm:text-2xl">The relationship between states , cities and the
                tree species by the top 10 trees</p>
            <p class="mx-auto mt-6 max-w-2xl text-base leading-8 text-gray-600 text-center">
                An alluvial diagram depicting the interplay between states, cities in them and the species of the top 10
                tree types.
            </p>

            <div class="flex justify-center py-3" id="alluvial-container"></div>

        </div>

    </div>
</template>

<script>
export default {
    name: "AlluvialChart",
    mounted() {
        // Load D3.js and D3 scale chromatic
        const script1 = document.createElement('script');
        script1.src = 'https://d3js.org/d3.v5.min.js';
        document.head.appendChild(script1);

        const script2 = document.createElement('script');
        script2.src = "https://cdnjs.cloudflare.com/ajax/libs/d3-sankey/0.12.3/d3-sankey.min.js";
        document.head.appendChild(script2);

        setTimeout(() => {
            // Set up the SVG container size
            const width = 1000; // Set your preferred width
            const height = 500; // Set your preferred height
            // Load CSV data
            // eslint-disable-next-line no-undef
            d3.csv("sankey.csv").then(function (data) {
                // eslint-disable-next-line no-undef
                var nodeColorScale = d3.scaleOrdinal(d3.schemeCategory10);
                // Set up the SVG container
                // eslint-disable-next-line no-undef
                const svg = d3.select("#alluvial-container")
                    .append("svg")
                    .attr("width", 2000) // Set your preferred width
                    .attr("height", 1000); // Set your preferred height

                // Create a D3 sankey layout
                // eslint-disable-next-line no-undef
                const sankey = d3.sankey()
                    .nodeWidth(15)
                    .nodePadding(10)
                    .extent([[0, 0], [width, height]]);

                const nodesData = [...new Set(data.flatMap(d => [d.source, d.target]))];
                const nodes = nodesData.map((name, index) => ({ name, id: index }));

                const { nodes: sankeyNodes, links } = sankey({
                    nodes,
                    links: data.map(d => ({ source: nodesData.indexOf(d.source), target: nodesData.indexOf(d.target), value: +d.value }))
                });

                // Draw links
                svg.append("g")
                    .selectAll("path")
                    .data(links)
                    .enter()
                    .append("path")
                    .attr("class", "link")
                    // eslint-disable-next-line no-undef
                    .attr("d", d3.sankeyLinkHorizontal())
                    .attr("stroke", d => nodeColorScale(d.source.name))
                    .attr("stroke", "#000")
                    .attr("stroke-opacity", 0.2)
                    .style("fill", "none")
                    .attr("stroke-width", function (d) { return d.width; });

                // Draw nodes
                svg.append("g")
                    .selectAll("rect")
                    .data(sankeyNodes)
                    .enter()
                    .append("rect")
                    .attr("x", d => d.x0)
                    .attr("y", d => d.y0)
                    .attr("height", d => d.y1 - d.y0)
                    .attr("width", d => d.x1 - d.x0)
                    .attr("fill", d => nodeColorScale(d.name));


                // Add labels to nodes
                svg.append("g")
                    .selectAll("text")
                    .data(sankeyNodes)
                    .enter()
                    .append("text")
                    .attr("x", d => (d.x0 < width / 2) ? d.x1 + 6 : d.x0 - 6)
                    .attr("y", d => (d.y1 + d.y0) / 2)
                    .attr("dy", "0.35em")
                    .attr("text-anchor", d => (d.x0 < width / 2) ? "start" : "end")
                    .text(d => d.name)
                    .style("fill", function(d) { return d.color; })
                    .style("font-size", "10px");
            });
        }, 1000);

    },
};
</script>

<style>
.link {
    fill: none;
    stroke: #000;
    stroke-opacity: .2;
}
path.link:hover {
  stroke-opacity: 0.5;
}
</style>

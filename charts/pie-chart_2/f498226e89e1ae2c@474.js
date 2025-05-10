function _1(d3,data,md){return(
""
)}

function _chart(d3,data)
{
  // Specify the chart’s dimensions.
  const width = 928;
  const height = Math.min(width, 500);

  // Create the color scale.
  const color = d3.scaleOrdinal()
      .domain(data.map(d => d.name))
      .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse())

  // Create the pie layout and arc generator.
  const pie = d3.pie()
      .sort(null)
      .value(d => d.value);

  const arc = d3.arc()
      .innerRadius(0)
      .outerRadius(Math.min(width, height) / 2 - 1);

  const labelRadius = arc.outerRadius()() * 0.8;

  // A separate arc generator for labels.
  const arcLabel = d3.arc()
      .innerRadius(labelRadius)
      .outerRadius(labelRadius);

  const arcs = pie(data);

  // Create the SVG container.
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;text-align: center");

  // Add a sector path for each value.
  svg.append("g")
      .attr("stroke", "white")
    .selectAll()
    .data(arcs)
    .join("path")
      .attr("fill", d => color(d.data.name))
      .attr("d", arc)
    .append("title")
      .text(d => `${d.data.name}: ${d.data.value.toLocaleString("en-US")}`);

  // Create a new arc generator to place a label close to the edge.
  // The label shows the value if there is enough room.
  svg.append("g")
      .attr("text-anchor", "middle")
    .selectAll()
    .data(arcs)
    .join("text")
      .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
      .call(text => text.append("tspan")
          .attr("y", "-0.4em")
          .attr("font-weight", "bold")
          .text(d => d.data.name))
      .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
          .attr("x", 0)
          .attr("y", "0.7em")
          .attr("fill-opacity", 0.7)
          .attr("text-align","center")
          .text(d => d.data.value.toLocaleString("en-US")));

  return svg.node();
}


function _data(FileAttachment){return(
FileAttachment("population-by-age.csv").csv({typed: true})
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["population-by-age.csv", {url: new URL("https://raw.githubusercontent.com/AndoniAranguren/HerramientasDeVisualizacionSteam/main/data/genres.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["d3","data","md"], _1);
  main.variable(observer("chart")).define("chart", ["d3","data"], _chart);
  main.variable(observer("data")).define("data", ["FileAttachment"], _data);
  return main;
}

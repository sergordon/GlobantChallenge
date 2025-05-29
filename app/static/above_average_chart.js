
window.renderAboveAvgChart = function(data) {
  const chartDiv = document.getElementById("above-avg-chart");
  chartDiv.innerHTML = "";

  if (!Array.isArray(data) || data.length === 0) {
    chartDiv.innerHTML = "No data to display.";
    return;
  }

  data.sort((a, b) => b.Hired - a.Hired);
  const departments = data.map(d => d.Department).reverse();
  const hires = data.map(d => d.Hired).reverse();

  const trace = {
    x: hires,
    y: departments,
    type: "bar",
    orientation: "h",
    text: hires.map(h => `${h} hires`),
    textposition: "auto",
    textfont: { color: "white" },
    hoverinfo: "x+y",
    marker: {
      color: "rgba(25, 81, 86, 0.6)",
      line: { color: "rgba(58, 71, 80, 1.0)", width: 1 }
    }
  };

  const layout = {
    title: "Hires in departments above average",
    xaxis: { title: "Total Hires" },
    yaxis: { title: "Department", automargin: true },
    margin: { l: 150, r: 50, t: 50, b: 50 },
    height: Math.max(400, departments.length * 30)
  };

  Plotly.newPlot("above-avg-chart", [trace], layout);
};


window.renderQuarterlyChart = function(data) {
  const container = document.getElementById("stacked-quarterly-chart");
  container.innerHTML = "";

  if (!Array.isArray(data) || data.length === 0) {
    container.innerHTML = "No data to display.";
    return;
  }

  const departments = [...new Set(data.map(d => d.Department))].sort();

  const dropdown = document.createElement("select");
  dropdown.id = "dept-select";
  dropdown.style.marginBottom = "1em";

  departments.forEach(dept => {
    const opt = document.createElement("option");
    opt.value = dept;
    opt.textContent = dept;
    dropdown.appendChild(opt);
  });

  container.appendChild(dropdown);

  const chartDiv = document.createElement("div");
  chartDiv.id = "stacked-chart";
  container.appendChild(chartDiv);

  function drawStackedChart(dept) {
    const filtered = data.filter(d => d.Department === dept);
    const jobs = [...new Set(filtered.map(d => d.Job))].sort();
    const quarterColors = ["#cce5ff", "#99ccff", "#66b3ff", "#3399ff"];

    const traces = ["Q1", "Q2", "Q3", "Q4"].map((quarter, i) => ({
      x: jobs,
      y: jobs.map(job => {
        const match = filtered.find(d => d.Job === job);
        return match ? match[quarter] : 0;
      }),
      name: quarter,
      type: "bar",
      marker: { color: quarterColors[i] }
    }));

    const layout = {
      barmode: "stack",
      title: `Quarterly Hires (Stacked) - ${dept}`,
      xaxis: { title: "Job Titles", tickangle: -45 },
      yaxis: { title: "Number of Hires" },
      margin: { b: 150 }
    };

    Plotly.newPlot("stacked-chart", traces, layout);
  }

  drawStackedChart(departments[0]);

  dropdown.addEventListener("change", e => {
    drawStackedChart(e.target.value);
  });
};

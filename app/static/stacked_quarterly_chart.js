document.addEventListener("DOMContentLoaded", function () {
    const endpoint = "/report/quarterly-hiring";
    const params = "?datefrom=2021-01-01&dateto=2021-12-31";
  
    fetch(endpoint + params)
      .then(res => res.json())
      .then(data => {
        if (!data || data.length === 0) {
          document.getElementById("stacked-quarterly-chart").innerHTML = "No data to display.";
          return;
        }

        // Get unique sorted departments
        const departments = [...new Set(data.map(d => d.Department))].sort();
        
        // Create dropdown
        const dropdown = document.createElement("select");
        dropdown.id = "dept-select";
        dropdown.style.marginBottom = "1em";
        departments.forEach(dept => {
          const opt = document.createElement("option");
          opt.value = dept;
          opt.textContent = dept;
          dropdown.appendChild(opt);
        });

        const container = document.getElementById("stacked-quarterly-chart");
        container.innerHTML = "";
        container.appendChild(dropdown);
  
        const chartDiv = document.createElement("div");
        chartDiv.id = "stacked-chart";
        container.appendChild(chartDiv);
  
        function drawStackedChart(dept) {
          const filtered = data.filter(d => d.Department === dept);
          const jobs = [...new Set(filtered.map(d => d.Job))].sort();
  
          const quarterColors = ["#cce5ff", "#99ccff", "#66b3ff", "#3399ff"];

          const traces = ["Q1", "Q2", "Q3", "Q4"].map((quarter, i) => {
            return {
              x: jobs,
              y: jobs.map(job => {
                const match = filtered.find(d => d.Job === job);
                return match ? match[quarter] : 0;
              }),
              name: quarter,
              type: "bar",
              marker: {
                color: quarterColors[i]
              }
            };
          });

  
          const layout = {
            barmode: "stack",
            title: `Quarterly Hires (Stacked) - ${dept}`,
            xaxis: { title: "Job Titles", tickangle: -45 },
            yaxis: { title: "Number of Hires" },
            margin: { b: 150 }
          };
  
          Plotly.newPlot("stacked-chart", traces, layout);
        }
  
        // Initial chart
        drawStackedChart(departments[0]);
  
        dropdown.addEventListener("change", e => {
          drawStackedChart(e.target.value);
        });
      })
      .catch(err => {
        console.error("Chart error:", err);
        document.getElementById("stacked-quarterly-chart").innerHTML = "Failed to load chart.";
      });
  });
  
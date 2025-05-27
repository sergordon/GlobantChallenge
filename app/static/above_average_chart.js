document.addEventListener("DOMContentLoaded", function () {
    console.log("Fetching above-average chart data...");
  
    const endpoint = "/report/above-average-hiring";
    const params = "?datefrom=2021-01-01&dateto=2021-12-31";
  
    fetch(endpoint + params)
      .then(res => res.json())
      .then(data => {
        console.log("Above-average data:", data);
  
        if (!data || data.length === 0) {
          document.getElementById("chart-above").innerHTML = "No data to display.";
          return;
        }
        
        // Step 1: Sort data by Hired descending
        data.sort((a, b) => b.Hired - a.Hired);

        // Step 2: Extract chart inputs
        const departments = data.map(d => d.Department).reverse();
        const hires = data.map(d => d.Hired).reverse();

        // Step 3: Define trace with labels
        const trace = {
        x: hires,
        y: departments,
        type: "bar",
        orientation: "h",
        text: hires.map(h => `${h} hires`), // label with units
        textposition: "auto",
        textfont: {
            color: "white"
          },
        hoverinfo: "x+y",
        marker: {
            color: "rgba(25, 81, 86, 0.6)",
            line: {
            color: "rgba(58, 71, 80, 1.0)",
            width: 1
            }
        }
        };

        // Step 4: Define layout
        const layout = {
        title: "Hires in departments above average",
        xaxis: { title: "Total Hires" },
        yaxis: {
            title: "Department",
            automargin: true
        },
        margin: {
            l: 150,
            r: 50,
            t: 50,
            b: 50
        },
        height: Math.max(400, departments.length * 30)
        };
  
        Plotly.newPlot("chart-above", [trace], layout);
        })
        .catch(error => {
            console.error("Error loading chart:", error);
            document.getElementById("chart-above").innerHTML = "Error loading chart.";
        });
  });
  
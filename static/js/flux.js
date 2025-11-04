const form = document.getElementById('flux-panel');
let maChart;
let gridVisible = true;

document.getElementById('submit_formula').addEventListener('click', async (e) => {
  e.preventDefault();


  const payload = {
    ticker: form.ticker.value || '',
    interval: form.interval.value || '',
    moving_average: form.moving_average.value || '',
    formula_1: form.formula_1.value || '',
    formula_2: form.formula_2.value || '',
    window: form.window.value || null
  };

  try {
    const response = await fetch('/engine', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    const errorDiv = document.getElementById('engine-error');

    if (data.error) {
      errorDiv.textContent = data.error;
      return;
    } else {
      errorDiv.textContent = '';
    }

    if (maChart) maChart.destroy();
    if (typeof alphabetaChart !== 'undefined' && alphabetaChart) {
      alphabetaChart.destroy();
    }

    const ctx = document.getElementById('engine-canvas').getContext('2d');
    maChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          //FORMULA PLOT
          {
            label: 'Formula 1',
            data: data.value_1,
            borderColor: '#ff3b30',
            borderWidth: 0.5,
            pointRadius: 0,
            backgroundColor: '#ff3b30',
            tension: 0.4
          },
          {
            label: 'Formula 2',
            data: data.value_2,
            borderColor: '#007AFF',
            backgroundColor: '#007AFF',
            pointRadius: 0,
            tension: 0.4,
            borderWidth: 0.5
          },

          //MOVING AVERAGE PLOT
          {
            label: `${payload.moving_average.toUpperCase()} of Close Price`,
            data: data.ma_type,
            borderColor: '#34C759',
            backgroundColor: '#34C759',
            pointRadius: 0,
            tension: 0.4,
            borderWidth: 0.5
          },

          
          //BOLLINGER BAND PLOT
          {
          label: 'MIDDLE BAND',
          data:data.marw,
          pointRadius: 0,
          tension: 0.4,
          borderWidth:0.5,
          borderColor: '#B0B0B0',
          backgroundColor: '#B0B0B0'
          },
          {
            label:'UPPER BAND',
            data: data.bb_upper,
            pointRadius:0,
            tension:0.4,
            borderWidth:0.5,
            borderColor: '#9B5DE5',
            backgroundColor: '#9B5DE5'
          },
          {
            label: 'LOWER BAND',
            data: data.bb_lower,
            pointRadius: 0,
            tension: 0.4,
            borderWidth: 0.5,
            borderColor: '#00BBF9',
            backgroundColor: '#00BBF9'
          },

          

          // PRICE PLOT===
          {
            label: 'Closing Price',
            data: data.close,
            borderColor: '#FFD60A',
            backgroundColor: '#FFD60A',
            pointRadius: 0,
            tension: 0.4,
            borderWidth: 0.5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f0f0f',
            titleColor: '#fff',
            bodyColor: '#ddd'
          },
          zoom: {
            pan: { enabled: true, mode: 'xy' },
            zoom: {
              wheel: { enabled: true },
              pinch: { enabled: true },
              drag: { enabled: true },
              mode: 'xy'
            }
          }
        },
        scales: {
          x: { ticks: { color: '#bbb' }, grid: { color: 'rgba(255,255,255,0.1)' } },
          y: { ticks: { color: '#bbb' }, grid: { color: 'rgba(255,255,255,0.1)' } }
        }
      }
    });

  } catch (err) {
    document.getElementById('engine-error').textContent = 'Something went wrong.';
    console.error(err);
  }
});

// === Button Actions ===
document.getElementById('resetZoom').addEventListener("click", () => {
  if (maChart) maChart.resetZoom();
});

document.getElementById("toggleGrid").addEventListener("click", () => {
  gridVisible = !gridVisible;
  if (maChart) {
    maChart.options.scales.x.grid.color = gridVisible ? "rgba(255,255,255,0.05)" : "transparent";
    maChart.options.scales.y.grid.color = gridVisible ? "rgba(255,255,255,0.05)" : "transparent";
    maChart.update();
  }
});

document.getElementById("downloadChart").addEventListener("click", () => {
  const canvas = document.getElementById("engine-canvas");
  const link = document.createElement("a");
  link.download = "chart.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
});

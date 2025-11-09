const rwForm = document.getElementById('rw-panel');
let rwChart;
let gridVisible_6 = true;

document.getElementById('submit_rw').addEventListener('click', async (e) => {
    e.preventDefault();

    const payload = {
        ticker: rwForm.ticker_rw.value,
        interval: rwForm.interval_rw.value,
        th_rw: rwForm.th_rw.value,
        nos_rw: rwForm.nos_rw.value,
        drift_rw: rwForm.drift_rw.value,
        volatility_rw: rwForm.volatility_rw.value
    };


    try {
        const response = await fetch('/rw_engine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const errorDiv = document.getElementById('forecast-error_rw');


        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        } else {
            errorDiv.textContent = ''
        }

        if (maChart) maChart.destroy();
        if (alphabetaChart) alphabetaChart.destroy();
        if (oscillatorChart) oscillatorChart.destroy();
        if (vwmChart) vwmChart.destroy();
        if (vnrChart) vnrChart.destroy();
        if (rwChart) rwChart.destroy();

        const ctx = document.getElementById('forecast-canvas').getContext('2d');

        const labels = data.labels;
        const sims = data.simulations;


        const datasets = sims.map((sim, i) => ({
            data: sim,
            borderColor: `hsl(${(i * 40) % 360}, 70%, 60%)`,
            borderWidth: 1,
            tension: 0,
            pointRadius: 0,
            fill: false
        }));

        //MEAN LINE
        const meanPath = Array.from({ length: labels.length }, (_, j) =>
            sims.reduce((sum, sim) => sum + sim[j], 0) / sims.length
        );

        datasets.push({
            label: 'Average Path',
            data: meanPath,
            borderColor: 'white',
            borderWidth: 2,
            tension: 0,
            pointRadius: 0
        });

        rwChart = new Chart(ctx, {
            type: 'line',
            data: { labels, datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#0f0f0f',
                        titleColor: '#fff'
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
        document.getElementById('forecast-error_rw').textContent = 'Something went wrong,';
        console.error(err);
    }
});

//WILL ADD BUTTONS HERE
document.getElementById('resetZoom').addEventListener("click", () => {
  if (rwChart) rwChart.resetZoom();
});

document.getElementById("toggleGrid").addEventListener("click", () => {
  gridVisible = !gridVisible;
  if (rwChart) {
    rwChart.options.scales.x.grid.color = gridVisible_6 ? "rgba(255,255,255,0.1)" : "transparent";
    rwChart.options.scales.y.grid.color = gridVisible_6 ? "rgba(255,255,255,0.1)" : "transparent";
    rwChart.update();
  }
});

document.getElementById("downloadChart").addEventListener("click", () => {
  const canvas = document.getElementById("engine-canvas");
  const link = document.createElement("a");
  link.download = "main_chart.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
});

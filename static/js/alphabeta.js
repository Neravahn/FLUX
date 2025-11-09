const alphabetaform = document.getElementById('alphabeta-panel');
let alphabetaChart;
let gridVisible_2 = true;

document.getElementById('submit_alphabeta').addEventListener('click', async (e) => {
    e.preventDefault();



    const payload = {
        ticker_alphabeta: alphabetaform.ticker_alphabeta.value,
        benchmark: alphabetaform.benchmark.value,
        interval: alphabetaform.interval_alphabeta.value

    };

    try {
        const response = await fetch('/alphabeta_engine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const errorDiv = document.getElementById('engine-error_alphabeta');

        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        } else {
            errorDiv.textContent = '';

        }


        // DESTROY PREVIOUS CHART BEFORE DEPLOYING NEW ONE
        if (maChart) maChart.destroy();
        if (alphabetaChart) alphabetaChart.destroy();
        if (oscillatorChart) oscillatorChart.destroy();
        if (vwmChart) vwmChart.destroy();
        if (vnrChart) vnrChart.destroy();
        if (rwChart) rwChart.destroy();

        const ctx = document.getElementById('engine-canvas').getContext('2d');
        alphabetaChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Actual Returns',
                        data: data.actual_points,
                        borderColor: '#ff3b30',
                        pointRadius: 1,
                        backgroundColor: '#ff3b30'

                    },
                    {
                        label: `Regression Line (B = ${data.beta.toFixed(2)}, a = ${data.alpha.toFixed(4)})`,
                        data: data.regression_line,
                        borderColor: '#007aff',
                        backgroundColor: '#007aff',
                        pointRadius: 1
                    },

                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true },
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
                    x: { title: { display: true, text: 'Benchmark' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    y: { title: { display: true, text: 'Stock Returns' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
    } catch (err) {
        document.getElementById('engine-error_alphabeta').textContent = 'Something went wrong.';
        console.error(err);
    }
});

// BUTTON ACTIONS HAHAHAH
document.getElementById('resetZoom').addEventListener("click", () => {
    if (alphabetaChart) alphabetaChart.resetZoom();
});

document.getElementById("toggleGrid").addEventListener("click", () => {
    gridVisible = !gridVisible;
    if (alphabetaChart) {
        alphabetaChart.options.scales.x.grid.color = gridVisible_2 ? "rgba(255,255,255,0.1)" : "transparent";
        alphabetaChart.options.scales.y.grid.color = gridVisible_2 ? "rgba(255,255,255,0.1)" : "transparent";
        alphabetaChart.update();
    }
});

document.getElementById("downloadChart").addEventListener("click", () => {
    const canvas = document.getElementById("engine-canvas");
    const link = document.createElement("a");
    link.download = "main_chart.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
});

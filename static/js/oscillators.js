const oscillatorForm = document.getElementById('oscillator-panel')
let oscillatorChart;
let gridVisible_3 = true;

document.getElementById('submit_oscillator').addEventListener('click', async (e) => {
    e.preventDefault();


    const payload = {
        ticker_oscillator: oscillatorForm.ticker_oscillator.value,
        interval_oscillator: oscillatorForm.interval_oscillator.value,
        select_oscillator: oscillatorForm.select_oscillator.value,
        //OPTIONAL TUNING PART
        period: oscillatorForm.period_oscillator.value,
        fast: oscillatorForm.fast_oscillator.value,
        slow: oscillatorForm.slow_oscillator.value,
        signal: oscillatorForm.signal_oscillator.value

    };


    try {
        const response = await fetch('/oscillator_engine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const errorDiv = document.getElementById('engine-error_oscillator');


        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        } else {
            errorDiv.textContent = '';
        }


        // DESTROY PREVIOUS CAHRT BEFOR DEPLOYING NEW ONE
        if (maChart) maChart.destroy();
        if (alphabetaChart) alphabetaChart.destroy();
        if (oscillatorChart) oscillatorChart.destroy();
        if (vwmChart) vwmChart.destroy();
        if (vnrChart) vnrChart.destroy();
        if (rwChart) rwChart.destroy();

        const ctx = document.getElementById('engine-canvas').getContext('2d');
        oscillatorChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,

                datasets: [

                    //OSCILLATORS PLOT ONLY
                    {
                        label: `${payload.select_oscillator.toUpperCase()}`,
                        data: data.oscillator,
                        borderColor: 'red',
                        backgroundColor: 'red',
                        pointRadius: 0,
                        tension: 0.4,
                        borderWidth: 0.5

                    },
                    {
                        label: 'Signal',
                        data: data.oscillator_signal,
                        borderColor: 'green',
                        backgroundColor: 'green',
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
                    x: { ticks: { color: '#bbb' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    y: { ticks: { color: '#bbb' }, grid: { color: 'rgba(255,255,255,0.1)' } }

                }
            }
        });

    } catch (err) {
        document.getElementById('engine-error_oscillator').textContent = 'Something went wrong.';
        console.error(err);

    }
});

// BUTTON ACTIONS
document.getElementById('resetZoom').addEventListener("click", () => {
    if (oscillatorChart) oscillatorChart.resetZoom();
});

document.getElementById("toggleGrid").addEventListener("click", () => {
    gridVisible = !gridVisible;
    if (oscillatorChart) {
        oscillatorChart.options.scales.x.grid.color = gridVisible_3 ? "rgba(255,255,255,0.1)" : "transparent";
        oscillatorChart.options.scales.y.grid.color = gridVisibl_3 ? "rgba(255,255,255,0.1)" : "transparent";
        oscillatorChart.update();
    }
});

document.getElementById("downloadChart").addEventListener("click", () => {
    const canvas = document.getElementById("engine-canvas");
    const link = document.createElement("a");
    link.download = "main_chart.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
});

const vwmForm = document.getElementById('vwm-panel');
let vwmChart;
let gridVisible_4 = true;

document.getElementById('submit_vwm').addEventListener('click', async (e) => {
    e.preventDefault();
    

    const payload = {
        ticker : vwmForm.ticker_vwm.value,
        interval: vwmForm.interval_vwm.value,
        vwm: vwmForm.vwm.value,
        period: vwmForm.period_vwm.value
    };


    try {
        const response = await fetch('/vwm_engine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const errorDiv = document.getElementById('engine-error_vwm');


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

        const ctx = document.getElementById('engine-canvas').getContext('2d');
        vwmChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'VWM',
                        data: data.vwm,
                        borderColor: '#007aff',
                        borderWidth: 0.5,
                        backgroundColor: '#007aff',
                        tension: 0.4,
                        pointRadius: 0
                    },
                    {
                        labels: 'VWM-SIGNAL',
                        data: data.vwm_ma,
                        borderColor: '#34c759',
                        borderWidth: '0.5',
                        baclgroundColor: '#34c759',
                        tension: 0.5,
                        pointRadius: 0
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false},
                    tooltip: {
                        backgroundColor: '#0f0f0f',
                        titleColor: '#fff',
                        bodyColor: '#ddd'
                    },

                    zoom: {
                        pan: { enabled: true, mode: 'xy'},
                        zoom: {
                            wheel: {enabled: true},
                            pinch: {enabled: true},
                            drag: {enabled: true},
                            mode: 'xy'
                        }
                    }
                },

                scales : {
                    x: { ticks : {color: '#bbb'}, grid: {color: 'rgba(255, 255, 255, 0.1'}},
                    y: { ticks : {color: '#bbb'}, grid: {color: 'rgba(255, 255, 255, 0.1'}}
                }
            }
        });

    } catch (err) {
        document.getElementById('engine-error_vwm').textContent = 'Something went wrong.';
        console.error(err)
    }

});

//DDING BUTTON ACTIONS

document.getElementById('resetZoom').addEventListener('click', () => {
    if (vwmChart) vwmChart.resetZoom();
});

document.getElementById('downloadChart').addEventListener('click', () => {
    const canvas = document.getElementById('engine-canvas');
    const link = document.createElement('a');
    link.download = 'vwm.png';
    link.href = canvas.toDataUrl('image.png');
    link.click();
});
const vnrForm = document.getElementById('vnr-panel');
let vnrChart;
let gridVisible_5;



document.getElementById('submit_vnr').addEventListener('click', async (e) => {
    e.preventDefault();


    const payload = {
        ticker: vnrForm.ticker_vnr.value,
        interval: vnrForm.interval_vnr.value,
        window: vnrForm.window_vnr.value,
        vnr: vnrForm.vnr.value,
        confidence: vnrForm.confidence.value,
        risk_free: vnrForm.risk_free.value
    };



    try {
        const response = await fetch('/vnr_engine', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const errorDiv = document.getElementById('engine-error_vnr');


        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        } else {
            errorDiv.textContent =''
        }

        //DESTROY PREVIOUS CAHRT BEFORE DEPLOYING NEW ONE

        if (oscillatorChart) oscillatorChart.destroy();
        if (maChart) maChart.destroy();
        if (alphabetaChart) alphabetaChart.destroy();
        if (vnrChart) vnrChart.destroy();
        if (vwmChart) vwmChart.destroy();


        //CREATING NEW CHART
        const ctx = document.getElementById('engine-canvas').getContext('2d');
        vnrChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: `${payload.vnr.toUpperCase()}`,
                        data: data.vnr,
                        borderWidth: 0.5,
                        pointRadius: 0,
                        backgroundColor: 'red',
                        borderColor: 'red',
                        tension: 0.4
                        
                    },
                    {
                        label : 'UPPER BAND',
                        data: data.upper,
                        pointRadius:0,
                        borderColor: '#9b5de5',
                        backgroundColor: '#9b5de5',
                        tension: 0.4,
                        borderWidth: 0.5
                        
                    },
                    {
                        label: 'LOWER BAND',
                        data: data.lower,
                        pointRadius: 0,
                        borderColor: '#00bbf9',
                        tension: 0.4,
                        borderWidth: 0.5,
                        backgroundColor: '#00bbf9'
                        
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: true},
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

                scales: {
                    x: {ticks: {color: '#bbb'}, grid: {color: 'rgba(255,255,255,0.1'}},
                    y: {ticks: {color: '#bbb'}, grid: {color: 'rgba(255,255,255,0.1'} }
                }
            }

        });

    }catch (err) {
        document.getElementById('engine-error_vnr').textContent = 'Something went wrong,';
        console.error(err);
    }
});

//=====BUTTON ACTIONS=======

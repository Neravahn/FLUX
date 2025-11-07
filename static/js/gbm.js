const gbmForm = document.getElementById('gbm-panel');
let gbmChart;
let gridVisible_5 = true;

document.getElementById('submit_gbm').addEventListener('click', async (e) => {
    e.preventDefault();

    const payload = {
        ticker : gbmForm.ticker_gbm.value,
        interval: gbmForm.interval_gbm.value,
        th_gbm: gbmForm.th_gbm.value,
        nos_gbm: gbmForm.nos_gbm.value
    };

    try {
        const response = await fetch('/gbm_engine', {
            method : 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const errorDiv = document.getElementById('forecast-error_gbm');

        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        } else { 
            errorDiv.textContent = ''
        }

        if (gbmChart) gbmChart.destroy();

        const ctx = document.getElementById('forecast-canvas').getContext('2d');

        const labels = data.labels;
        const sims = data.simulations;


        

        const datasets = sims.map((sim, i) => ({
            label: `Sim ${i+1}`,
            data: sim,
            borderColor: `hsl(${(i*40) % 360}, 70%, 60%)`,
            borderWidth:1,
            tension:0.,
            pointRadius: 0,
            fill:false
        }));

        //MEAN LINE
        const meanPath = Array.from({length: labels.length}, (_, j) =>
        sims.reduce((sum, sim) => sum+sim[j], 0)/sims.length
    );

        datasets.push ({
            labell:'Average Path',
            data: meanPath,
            borderColor: 'white',
            borderWidth: 2,
            tension: 0,
            pointRadius: 0
        });

        gbmChart = new Chart(ctx, {
            type: 'line',
            data: {labels,datasets},
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display:false},
                    tooltip: {
                        backgroundColor: '#0f0f0f',
                        titleColot: '#fff',
                        bodyColor: '#ddd'
                    },

                    zoom: {
                        pan: { enabled: true, mode:'xy'},
                        zoom: {
                            wheel: {enabled:true},
                            pinch: {enabled:true},
                            drag: {enabled:true},
                            mode:'xy'
                        }
                    }
                },

                scales: {
                    x: { ticks: { color: '#bbb'},grid: { color: 'rgba(255,255,255,0.1)'}},
                    y: { ticks: { color: '#bbb' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });


    }catch (err) {
        document.getElementById('forecast-error_gbm').textContent = 'Something went wrong.';
        console.error(err);
    }
});

//WILL ADD BUTTON ACTIONS HERE

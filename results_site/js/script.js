// Global State
let currentData = [];
let sortState = {
    key: 'channel',
    direction: 'asc' // 'asc' or 'desc'
};
let myChart = null; // Chart.js instance

document.addEventListener('DOMContentLoaded', () => {
    console.log('Script loaded');
    if (window.resultsData) {
        console.log('Data found:', window.resultsData);
        window.allData = window.resultsData;
        
        // Initialize
        populateFilters(window.allData);
        populateMetricOptions(window.allData);
        applyFilters(); // This will also sort and render
    } else {
        console.error('No data found in window.resultsData. Check data.js loading.');
    }
});

// --- Populating Filters ---
function populateFilters(data) {
    const channels = new Set();
    const bits = new Set();
    const eps = new Set();
    const alphas = new Set();
    const betas = new Set();
    const decLRs = new Set();
    const decSteps = new Set();
    const epochs = new Set();

    data.forEach(row => {
        if (row.channel) channels.add(row.channel.replace(/_hf\d+$/, ''));
        if (row.bits !== undefined) bits.add(row.bits);
        if (row.eps !== undefined) eps.add(row.eps);
        if (row.alpha !== undefined) alphas.add(row.alpha);
        if (row.beta !== undefined) betas.add(row.beta);
        if (row.decoder_lr !== undefined) decLRs.add(row.decoder_lr);
        if (row.decoder_steps !== undefined) decSteps.add(row.decoder_steps);
        if (row.Epochs !== undefined) epochs.add(row.Epochs);
    });

    populateSelect('filter-channel', Array.from(channels).sort());
    populateSelect('filter-bits', Array.from(bits).sort((a,b) => a-b));
    populateSelect('filter-eps', Array.from(eps).sort((a,b) => a-b));
    populateSelect('filter-alpha', Array.from(alphas).sort((a,b) => a-b));
    populateSelect('filter-beta', Array.from(betas).sort((a,b) => a-b));
    populateSelect('filter-declr', Array.from(decLRs).sort());
    populateSelect('filter-decsteps', Array.from(decSteps).sort((a,b) => a-b));
    populateSelect('filter-epochs', Array.from(epochs).sort((a,b) => a-b));
}

function populateSelect(id, values) {
    const select = document.getElementById(id);
    // Keep the first "All" option
    select.innerHTML = '<option value="all">All</option>';
    
    values.forEach(val => {
        const option = document.createElement('option');
        option.value = val;
        option.textContent = val;
        select.appendChild(option);
    });
}

function populateMetricOptions(data) {
    const select = document.getElementById('metric-select');
    const availableAttacks = new Set();
    
    // Scan all data to find all possible attacks
    data.forEach(row => {
        if (row.metrics) {
            Object.keys(row.metrics).forEach(attack => {
                availableAttacks.add(attack);
            });
        }
    });
    
    // Sort and add to select
    Array.from(availableAttacks).sort().forEach(attack => {
        const option = document.createElement('option');
        option.value = attack;
        option.textContent = attack;
        select.appendChild(option);
    });
}

// --- Filtering Logic ---
function applyFilters() {
    const searchText = document.getElementById('search-text').value.toLowerCase();
    const filterChannel = document.getElementById('filter-channel').value;
    const filterBits = document.getElementById('filter-bits').value;
    const filterEps = document.getElementById('filter-eps').value;
    const filterAlpha = document.getElementById('filter-alpha').value;
    const filterBeta = document.getElementById('filter-beta').value;
    const filterDecLR = document.getElementById('filter-declr').value;
    const filterDecSteps = document.getElementById('filter-decsteps').value;
    const filterEpochs = document.getElementById('filter-epochs').value;
    const filterEval = document.getElementById('filter-eval').value;

    currentData = window.allData.filter(row => {
        // Text Search
        const matchText = (
            row.run_name.toLowerCase().includes(searchText) ||
            (row.channel && row.channel.toLowerCase().includes(searchText))
        );
        if (!matchText) return false;

        // Dropdowns
        if (filterChannel !== 'all') {
            const rowChannel = row.channel ? String(row.channel).replace(/_hf\d+$/, '') : '';
            if (rowChannel !== filterChannel) return false;
        }
        if (filterBits !== 'all' && String(row.bits) !== filterBits) return false;
        if (filterEps !== 'all' && String(row.eps) !== filterEps) return false;
        if (filterAlpha !== 'all' && String(row.alpha) !== filterAlpha) return false;
        if (filterBeta !== 'all' && String(row.beta) !== filterBeta) return false;
        if (filterDecLR !== 'all' && String(row.decoder_lr) !== filterDecLR) return false;
        if (filterDecSteps !== 'all' && String(row.decoder_steps) !== filterDecSteps) return false;
        if (filterEpochs !== 'all' && String(row.Epochs) !== filterEpochs) return false;
        
        // Eval Stats Available
        if (filterEval !== 'all') {
            const hasEval = row.eval_exists === true;
            if (filterEval === 'yes' && !hasEval) return false;
            if (filterEval === 'no' && hasEval) return false;
        }

        return true;
    });

    // Update UI count
    const countDiv = document.getElementById('row-count');
    if (countDiv) {
        countDiv.textContent = `Showing ${currentData.length} of ${window.allData.length} runs`;
    }

    // Re-sort and render
    executeSort();
}

function resetFilters() {
    document.getElementById('search-text').value = '';
    document.getElementById('filter-channel').value = 'all';
    document.getElementById('filter-bits').value = 'all';
    document.getElementById('filter-eps').value = 'all';
    document.getElementById('filter-alpha').value = 'all';
    document.getElementById('filter-beta').value = 'all';
    document.getElementById('filter-declr').value = 'all';
    document.getElementById('filter-decsteps').value = 'all';
    document.getElementById('filter-epochs').value = 'all';
    document.getElementById('filter-eval').value = 'all';
    applyFilters();
}

function exportCSV() {
    if (!currentData || currentData.length === 0) {
        alert("No data to export.");
        return;
    }

    // 1. Collect all unique attack names from the current filtered data
    const attackNames = new Set();
    currentData.forEach(row => {
        if (row.metrics) {
            Object.keys(row.metrics).forEach(attack => attackNames.add(attack));
        }
    });
    const sortedAttacks = Array.from(attackNames).sort();

    // 2. Define headers
    // Standard headers
    const headers = [
        "Date", "Time", "bits", "eps", "alpha", "beta", 
        "mask_reg", "logit_reg", "decoder_lr", "decoder_steps", 
        "batch_size", "Epochs", "channel"
    ];
    
    // Dynamic headers for metrics (ber, snr, lsd for each attack)
    sortedAttacks.forEach(attack => {
        headers.push(`eval_${attack}_ber`);
        headers.push(`eval_${attack}_snr`);
        headers.push(`eval_${attack}_lsd`);
    });

    // 3. Build CSV rows
    const csvRows = [];
    csvRows.push(headers.join(",")); // Header row

    const valOrEmpty = (v) => (v !== undefined && v !== null) ? v : "";

    currentData.forEach(row => {
        const rowData = [];
        
        // Standard fields
        rowData.push(valOrEmpty(row.Date));
        rowData.push(valOrEmpty(row.Time));
        rowData.push(valOrEmpty(row.bits));
        rowData.push(valOrEmpty(row.eps));
        rowData.push(valOrEmpty(row.alpha));
        rowData.push(valOrEmpty(row.beta));
        rowData.push(valOrEmpty(row.mask_reg));
        rowData.push(valOrEmpty(row.logit_reg));
        rowData.push(valOrEmpty(row.decoder_lr));
        rowData.push(valOrEmpty(row.decoder_steps));
        rowData.push(valOrEmpty(row.batch_size));
        rowData.push(valOrEmpty(row.Epochs));
        rowData.push(valOrEmpty(row.channel));

        // Dynamic metric fields
        sortedAttacks.forEach(attack => {
            if (row.metrics && row.metrics[attack]) {
                const m = row.metrics[attack];
                rowData.push(m.ber !== null && m.ber !== undefined ? m.ber : "");
                rowData.push(m.snr !== null && m.snr !== undefined ? m.snr : "");
                rowData.push(m.lsd !== null && m.lsd !== undefined ? m.lsd : "");
            } else {
                rowData.push("", "", "");
            }
        });

        // Escape fields if necessary (simple CSV escaping: quotes around fields with commas)
        const escapedRow = rowData.map(val => {
            const strVal = String(val);
            if (strVal.includes(",") || strVal.includes("\n") || strVal.includes('"')) {
                return `"${strVal.replace(/"/g, '""')}"`;
            }
            return strVal;
        });

        csvRows.push(escapedRow.join(","));
    });

    // 4. Trigger download
    const csvString = csvRows.join("\n");
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'filtered_results.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// --- Sorting Logic ---
function handleSort(key) {
    if (sortState.key === key) {
        // Toggle direction
        sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
    } else {
        sortState.key = key;
        sortState.direction = 'desc'; // Default to desc for new columns usually better for numbers
        if (key === 'channel') sortState.direction = 'asc'; // Text usually asc
    }
    
    updateSortIcons(key);
    executeSort();
}

function executeSort() {
    const key = sortState.key;
    const dir = sortState.direction === 'asc' ? 1 : -1;

    currentData.sort((a, b) => {
        // Helper to get comparable value
        const getVal = (row, k) => {
            let val = row[k];
            // Normalize channel for sorting (remove _hfX suffix)
            if (k === 'channel' && val) {
                val = val.replace(/_hf\d+$/, '');
            }
            return val;
        };

        let valA = getVal(a, key);
        let valB = getVal(b, key);

        // Primary Sort Comparison
        let comparison = 0;

        // Handle numeric strings or numbers
        const isNumA = !isNaN(parseFloat(valA)) && isFinite(valA);
        const isNumB = !isNaN(parseFloat(valB)) && isFinite(valB);

        if (isNumA && isNumB) {
            valA = parseFloat(valA);
            valB = parseFloat(valB);
            comparison = (valA - valB) * dir;
        } else {
            // Fallback to string
            if (valA === undefined || valA === null) valA = "";
            if (valB === undefined || valB === null) valB = "";
            valA = String(valA).toLowerCase();
            valB = String(valB).toLowerCase();

            if (valA < valB) comparison = -1 * dir;
            else if (valA > valB) comparison = 1 * dir;
            else comparison = 0;
        }

        // Secondary Sort logic
        if (comparison === 0) {
            // Secondary sort is ALWAYS Date+Time Descending (Newest first)
            // UNLESS we are explicitly sorting by Date or Time themselves
            if (key !== 'Date' && key !== 'Time') {
                 if (a.Date !== b.Date) {
                     return a.Date < b.Date ? 1 : -1; // Descending Date (bigger date first)
                 }
                 if (a.Time !== b.Time) {
                     return a.Time < b.Time ? 1 : -1; // Descending Time (bigger time first)
                 }
            } else if (key === 'Date') {
                // If sorting by Date, tie-break with Time in same direction
                if (a.Time !== b.Time) {
                     let timeCmp = 0;
                     if (a.Time < b.Time) timeCmp = -1;
                     else if (a.Time > b.Time) timeCmp = 1;
                     return timeCmp * dir;
                 }
            }
        }
        
        return comparison;
    });

    renderTable(currentData);
}

function updateSortIcons(activeKey) {
    // Remove classes from all headers
    document.querySelectorAll('th').forEach(th => {
        th.classList.remove('asc', 'desc');
        if (th.getAttribute('data-sort') === activeKey) {
            th.classList.add(sortState.direction);
        }
    });
}


// --- Rendering ---
function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="12" style="text-align:center; padding: 20px;">No matching results found</td></tr>';
        return;
    }

    data.forEach(row => {
        const tr = document.createElement('tr');

        // Date/Time
        const dateCell = `<td>${row.Date}<br><span style="color:#888">${row.Time}</span></td>`;
        
        // Config columns
        const bitsCell = `<td>${row.bits}</td>`;
        const epsCell = `<td>${row.eps}</td>`;
        const alphaCell = `<td>${row.alpha}</td>`;
        const betaCell = `<td>${row.beta}</td>`;
        const maskRegCell = `<td>${row.mask_reg !== undefined ? row.mask_reg : '-'}</td>`;
        const logitRegCell = `<td>${row.logit_reg !== undefined ? row.logit_reg : '-'}</td>`;
        const decLRCell = `<td>${row.decoder_lr}</td>`;
        const decStepsCell = `<td>${row.decoder_steps}</td>`;

        // Channel
        let channelClass = '';
        let displayChannel = row.channel;
        
        // Remove suffix like _hf0, _hf1, etc.
        if (displayChannel) {
            displayChannel = displayChannel.replace(/_hf\d+$/, '');
        }

        if (row.channel.startsWith('none')) channelClass = 'channel-none';
        else if (row.channel.startsWith('noise_only')) channelClass = 'channel-noise';
        else if (row.channel === 'full') channelClass = 'channel-full';
        else if (row.channel.startsWith('full_hf')) channelClass = 'channel-full-hf0';
        
        const channelCell = `<td><span class="channel-badge ${channelClass}">${displayChannel}</span></td>`;

        const epochsCell = `<td>${row.Epochs}</td>`;
        
        // Checkpoints
        const encBadge = row.enc_checkpoint ? '<span class="badge badge-yes">Enc</span>' : '<span class="badge badge-no">Enc</span>';
        const decBadge = row.dec_checkpoint ? '<span class="badge badge-yes">Dec</span>' : '<span class="badge badge-no">Dec</span>';
        const ckptCell = `<td>${encBadge} ${decBadge}</td>`;
        
        // Metrics
        let metricsHtml = '';
        if (row.metrics && Object.keys(row.metrics).length > 0) {
            metricsHtml += `<button class="show-stats-btn" onclick="toggleStats(this)">Show Evaluation Stats</button>
                            <div class="stats-content" style="display: none;">`;
            
            // Custom sort: Identity first, then alphabetical
            const attacks = Object.keys(row.metrics).sort((a, b) => {
                if (a.toLowerCase() === 'identity') return -1;
                if (b.toLowerCase() === 'identity') return 1;
                return a.localeCompare(b);
            });

            attacks.forEach(attack => {
                const m = row.metrics[attack];
                const ber = m.ber !== null ? m.ber.toFixed(3) : '-';
                const snr = m.snr !== null ? m.snr.toFixed(1) : '-';
                const lsd = m.lsd !== null ? m.lsd.toFixed(2) : '-';
                
                metricsHtml += `<div class="metric-group">
                    <span class="metric-name">${attack}:</span>
                    <div class="metric-grid">
                        <span>BER: ${ber}</span>
                        <span>SNR: ${snr}</span>
                        <span>LSD: ${lsd}</span>
                    </div>
                </div>`;
            });
            metricsHtml += `</div>`;
        } else {
            metricsHtml = '<span style="color:#ccc">No eval data</span>';
        }
        const metricsCell = `<td>${metricsHtml}</td>`;

        // Plot
        let plotCell = '<td>-</td>';
        if (row.plot_url) {
            plotCell = `<td><a class="plot-link" href="${row.plot_url}" target="_self">View Plot</a></td>`;
        }

        tr.innerHTML = dateCell + bitsCell + epsCell + alphaCell + betaCell + maskRegCell + logitRegCell + decLRCell + decStepsCell + channelCell + epochsCell + ckptCell + metricsCell + plotCell;
        tbody.appendChild(tr);
    });

    // Ensure icons are correct after render (if we just loaded)
    updateSortIcons(sortState.key);
}

function toggleStats(btn) {
    const content = btn.nextElementSibling;
    if (content.style.display === "none") {
        content.style.display = "block";
        btn.textContent = "Hide Evaluation Stats";
    } else {
        content.style.display = "none";
        btn.textContent = "Show Evaluation Stats";
    }
}

// --- Chart Generation ---
function generateChart() {
    const metricSelect = document.getElementById('metric-select');
    const attackName = metricSelect.value;
    
    if (!attackName) {
        alert('Please select an attack first.');
        return;
    }

    // Filter to only entries with evaluation stats
    const dataForChart = currentData.filter(row => row.eval_exists === true);

    if (dataForChart.length === 0) {
        alert('No data with evaluation stats found in current selection.');
        return;
    }

    const xAxisSelect = document.getElementById('xaxis-select');
    const xAxisKey = xAxisSelect.value; // "" (Date-Time) or "eps", "beta", etc.

    const ctx = document.getElementById('comparisonChart').getContext('2d');
    const chartWrapper = document.querySelector('.chart-wrapper');
    const hideBtn = document.getElementById('hide-chart-btn');
    
    chartWrapper.style.display = 'block';
    hideBtn.style.display = 'inline-block';

    if (myChart) {
        myChart.destroy();
    }

    // Generate Labels (X-Axis)
    const labels = dataForChart.map(row => {
        if (xAxisKey) {
            // Use selected parameter
            let val = row[xAxisKey];
            if (val === undefined || val === null) return 'N/A';
            return val;
        } else {
            // Default: Date-Time
            return `${row.Date}-${row.Time}`;
        }
    });

    const berValues = dataForChart.map(row => {
        if (row.metrics && row.metrics[attackName]) {
            const val = row.metrics[attackName]['ber'];
            return val !== undefined && val !== null ? val : null;
        }
        return null;
    });

    const snrValues = dataForChart.map(row => {
        if (row.metrics && row.metrics[attackName]) {
            const val = row.metrics[attackName]['snr'];
            return val !== undefined && val !== null ? val : null;
        }
        return null;
    });

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels, 
            datasets: [
                {
                    label: `${attackName} BER`,
                    data: berValues,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: false,
                    tension: 0.1,
                    yAxisID: 'y'
                },
                {
                    label: `${attackName} SNR`,
                    data: snrValues,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: false,
                    tension: 0.1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'BER'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'SNR (dB)'
                    },
                    grid: {
                        drawOnChartArea: false // only want the grid lines for one axis to show up
                    }
                },
                x: {
                    ticks: {
                        autoSkip: true,
                        maxRotation: 45,
                        minRotation: 0
                    },
                    title: {
                        display: true,
                        text: xAxisKey ? xAxisSelect.options[xAxisSelect.selectedIndex].text : 'Runs (Sorted)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: (context) => {
                             const idx = context[0].dataIndex;
                             const row = dataForChart[idx];
                             return row.run_name;
                        },
                        label: (context) => {
                             const val = context.raw !== null ? context.raw : 'N/A';
                             return `${context.dataset.label}: ${val}`;
                        },
                        afterLabel: (context) => {
                            // Only show detailed info once per tooltip
                            if (context.datasetIndex === 0) {
                                const idx = context.dataIndex;
                                const row = dataForChart[idx];
                                return [
                                    `Channel: ${row.channel}`,
                                    `Bits: ${row.bits}, Eps: ${row.eps}`,
                                    `Alpha: ${row.alpha}, Beta: ${row.beta}`,
                                    `MaskReg: ${row.mask_reg}, LogitReg: ${row.logit_reg}`
                                ];
                            }
                            return null;
                        }
                    }
                },
                legend: {
                    position: 'top',
                }
            }
        }
    });
}

function hideChart() {
    const chartWrapper = document.querySelector('.chart-wrapper');
    const hideBtn = document.getElementById('hide-chart-btn');
    
    chartWrapper.style.display = 'none';
    hideBtn.style.display = 'none';
    
    if (myChart) {
        myChart.destroy();
        myChart = null;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Script loaded');
    if (window.resultsData) {
        console.log('Data found:', window.resultsData);
        renderTable(window.resultsData);
        window.allData = window.resultsData; // Store for sorting/filtering
    } else {
        console.error('No data found in window.resultsData. Check data.js loading.');
    }
});

function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    data.forEach(row => {
        const tr = document.createElement('tr');

        // Date/Time
        const dateCell = `<td>${row.Date}<br><span style="color:#888">${row.Time}</span></td>`;
        
        // Config columns
        const bitsCell = `<td>${row.bits}</td>`;
        const epsCell = `<td>${row.eps}</td>`;
        const alphaCell = `<td>${row.alpha}</td>`;
        const betaCell = `<td>${row.beta}</td>`;

        // Channel
        let channelClass = '';
        if (row.channel === 'none') channelClass = 'channel-none';
        else if (row.channel === 'noise_only') channelClass = 'channel-noise';
        else if (row.channel === 'full') channelClass = 'channel-full';
        
        const channelCell = `<td><span class="channel-badge ${channelClass}">${row.channel}</span></td>`;

        const epochsCell = `<td>${row.Epochs}</td>`;

        // Checkpoints
        const encBadge = row.enc_checkpoint ? '<span class="badge badge-yes">Enc</span>' : '<span class="badge badge-no">Enc</span>';
        const decBadge = row.dec_checkpoint ? '<span class="badge badge-yes">Dec</span>' : '<span class="badge badge-no">Dec</span>';
        const ckptCell = `<td>${encBadge} ${decBadge}</td>`;

        // Metrics
        let metricsHtml = '';
        if (row.metrics && Object.keys(row.metrics).length > 0) {
            // Sort attacks alphabetically
            const attacks = Object.keys(row.metrics).sort();
            attacks.forEach(attack => {
                const m = row.metrics[attack];
                const ber = m.ber !== null ? m.ber.toFixed(3) : '-';
                const snr = m.snr !== null ? m.snr.toFixed(1) : '-';
                const lsd = m.lsd !== null ? m.lsd.toFixed(2) : '-';
                
                metricsHtml += `<div class="metric-group">
                    <span class="metric-name">${attack}:</span>
                    <span class="metric-values">BER:${ber} SNR:${snr} LSD:${lsd}</span>
                </div>`;
            });
        } else {
            metricsHtml = '<span style="color:#ccc">No eval data</span>';
        }
        const metricsCell = `<td>${metricsHtml}</td>`;

        // Plot
        let plotCell = '<td>-</td>';
        if (row.plot_url) {
            plotCell = `<td><a class="plot-link" href="${row.plot_url}" target="_self">View Plot</a></td>`;
        }

        tr.innerHTML = dateCell + bitsCell + epsCell + alphaCell + betaCell + channelCell + epochsCell + ckptCell + metricsCell + plotCell;
        tbody.appendChild(tr);
    });
}

// Filtering
function filterTable() {
    const query = document.getElementById('search').value.toLowerCase();
    if (!window.allData) return;

    const filtered = window.allData.filter(row => {
        // Search in run_name, channel, or stringified metrics
        return row.run_name.toLowerCase().includes(query) || 
               (row.channel && row.channel.toLowerCase().includes(query));
    });
    renderTable(filtered);
}

// Sorting (Basic implementation)
let sortDir = 1; // 1 = asc, -1 = desc
function sortTable(key) {
    if (!window.allData) return;
    
    sortDir *= -1;
    
    window.allData.sort((a, b) => {
        let valA = a[key];
        let valB = b[key];
        
        // Handle potential nulls
        if (valA === undefined) valA = "";
        if (valB === undefined) valB = "";

        if (valA < valB) return -1 * sortDir;
        if (valA > valB) return 1 * sortDir;
        return 0;
    });
    
    renderTable(window.allData);
}


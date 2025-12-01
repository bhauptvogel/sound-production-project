// Global State
let currentData = [];
let sortState = {
    key: 'Date',
    direction: 'desc' // 'asc' or 'desc'
};

document.addEventListener('DOMContentLoaded', () => {
    console.log('Script loaded');
    if (window.resultsData) {
        console.log('Data found:', window.resultsData);
        window.allData = window.resultsData;
        
        // Initialize
        populateFilters(window.allData);
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

    data.forEach(row => {
        if (row.channel) channels.add(row.channel);
        if (row.bits !== undefined) bits.add(row.bits);
        if (row.eps !== undefined) eps.add(row.eps);
        if (row.alpha !== undefined) alphas.add(row.alpha);
        if (row.beta !== undefined) betas.add(row.beta);
    });

    populateSelect('filter-channel', Array.from(channels).sort());
    populateSelect('filter-bits', Array.from(bits).sort((a,b) => a-b));
    populateSelect('filter-eps', Array.from(eps).sort((a,b) => a-b));
    populateSelect('filter-alpha', Array.from(alphas).sort((a,b) => a-b));
    populateSelect('filter-beta', Array.from(betas).sort((a,b) => a-b));
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

// --- Filtering Logic ---
function applyFilters() {
    const searchText = document.getElementById('search-text').value.toLowerCase();
    const filterChannel = document.getElementById('filter-channel').value;
    const filterBits = document.getElementById('filter-bits').value;
    const filterEps = document.getElementById('filter-eps').value;
    const filterAlpha = document.getElementById('filter-alpha').value;
    const filterBeta = document.getElementById('filter-beta').value;

    currentData = window.allData.filter(row => {
        // Text Search
        const matchText = (
            row.run_name.toLowerCase().includes(searchText) ||
            (row.channel && row.channel.toLowerCase().includes(searchText))
        );
        if (!matchText) return false;

        // Dropdowns
        if (filterChannel !== 'all' && String(row.channel) !== filterChannel) return false;
        if (filterBits !== 'all' && String(row.bits) !== filterBits) return false;
        if (filterEps !== 'all' && String(row.eps) !== filterEps) return false;
        if (filterAlpha !== 'all' && String(row.alpha) !== filterAlpha) return false;
        if (filterBeta !== 'all' && String(row.beta) !== filterBeta) return false;

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
    applyFilters();
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
        let valA = a[key];
        let valB = b[key];

        // Handle Dates specially if needed, but usually string comparison YYYYMMDD works
        if (key === 'Date') {
            // Secondary sort by Time
            if (valA === valB) {
                return a['Time'] < b['Time'] ? -1 * dir : 1 * dir;
            }
        }

        // Handle numeric strings or numbers
        // If both are numbers, subtract. If strings, localeCompare.
        const isNumA = !isNaN(parseFloat(valA)) && isFinite(valA);
        const isNumB = !isNaN(parseFloat(valB)) && isFinite(valB);

        if (isNumA && isNumB) {
            valA = parseFloat(valA);
            valB = parseFloat(valB);
            return (valA - valB) * dir;
        }
        
        // Fallback to string
        if (valA === undefined || valA === null) valA = "";
        if (valB === undefined || valB === null) valB = "";
        valA = String(valA).toLowerCase();
        valB = String(valB).toLowerCase();

        if (valA < valB) return -1 * dir;
        if (valA > valB) return 1 * dir;
        return 0;
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
        const decLRCell = `<td>${row.decoder_lr}</td>`;
        const decStepsCell = `<td>${row.decoder_steps}</td>`;

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

        tr.innerHTML = dateCell + bitsCell + epsCell + alphaCell + betaCell + decLRCell + decStepsCell + channelCell + epochsCell + ckptCell + metricsCell + plotCell;
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

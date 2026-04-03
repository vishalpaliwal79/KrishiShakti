// KrishiShakti Control Panel — Full Automation

let autoAIInterval = null;
let currentMode    = 'auto';

function toast(msg, type = 'success') {
    const el = document.createElement('div');
    el.className = `ctrl-toast ctrl-toast-${type}`;
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.classList.add('show'), 10);
    setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 300); }, 3500);
}

async function apiFetch(url, options = {}) {
    try {
        const res  = await fetch(url, options);
        const text = await res.text();
        try { return { ok: res.ok, status: res.status, data: JSON.parse(text) }; }
        catch { return { ok: false, status: res.status, data: { error: `Server error ${res.status}` } }; }
    } catch (e) { return { ok: false, status: 0, data: { error: e.message } }; }
}

document.addEventListener('DOMContentLoaded', () => {
    const u = JSON.parse(localStorage.getItem('krishishakti_user') || sessionStorage.getItem('krishishakti_user') || '{}');
    document.getElementById('user-initial').textContent = (u.name || 'U')[0].toUpperCase();
    refreshAllData();
    setInterval(refreshAllData, 5000);
    startAutoAI();
});

async function refreshAllData() {
    console.log('Refreshing all dashboard data...');
    // Execute multiple loads in parallel to speed up UI synchronization
    await Promise.all([
        loadSystemMode(),
        loadDevices(),
        loadSensors(),
        loadActivity(),
        loadIrrigationHistory()
    ]);
}

async function loadSystemMode() {
    const { ok, data } = await apiFetch('/api/system/mode');
    if (ok) applyMode(data.mode);
}

async function setSystemMode(mode) {
    const { ok, data } = await apiFetch('/api/system/mode', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode })
    });
    if (ok && data.success) {
        toast(`Switched to ${mode.toUpperCase()} mode`, 'info');
        await refreshAllData(); // Full refresh ensures correct toggle state
    } else {
        toast(`Mode switch failed: ${data.error || 'Unknown'}`, 'error');
    }
}

function applyMode(mode) {
    currentMode = mode;
    const isAuto = mode === 'auto';
    document.getElementById('auto-banner').style.display   = isAuto  ? 'flex' : 'none';
    document.getElementById('manual-banner').style.display = !isAuto ? 'flex' : 'none';
    document.getElementById('btn-auto').classList.toggle('active', isAuto);
    document.getElementById('btn-manual').classList.toggle('active', !isAuto);
    
    // Disable/Enable toggles globally based on mode
    ['pump','fan'].forEach(dev => {
        const toggle = document.getElementById(`toggle-${dev}`);
        if (toggle) toggle.disabled = isAuto;
    });
}

async function loadSensors() {
    const { ok, data } = await apiFetch('/api/sensors');
    if (ok) updateSensorStrip(data);
}

function updateSensorStrip(d) {
    const temp  = d.dht22?.temperature || 0;
    const hum   = d.dht22?.humidity    || 0;
    const moist = d.tds?.value         || 0;
    const tank  = d.fc28?.value        || 0;
    const air   = d.mq135?.value       || 0;
    
    document.getElementById('s-temp').textContent  = temp  ? parseFloat(temp).toFixed(1) + '°C' : '--°C';
    document.getElementById('s-hum').textContent   = hum   ? parseFloat(hum).toFixed(1)  + '%'  : '--%';
    document.getElementById('s-moist').textContent = (moist !== undefined) ? parseFloat(moist).toFixed(1) + '%' : '--%';
    document.getElementById('s-tank').textContent  = (tank !== undefined)  ? parseFloat(tank).toFixed(1)  + ' cm' : '-- cm';
    
    // Air Quality Status Display
    const airText = document.getElementById('s-air');
    if (airText) {
        const isLeak = (air > 100);
        airText.textContent = isLeak ? "DETECTION!" : "NORMAL";
        airText.style.color = isLeak ? "#ef4444" : "#10b981";
        airText.style.fontWeight = "bold";
    }
    
    // Update Arduino Connection Status
    const hwText = document.getElementById('hw-state-text');
    const hwDot  = document.getElementById('hw-dot');
    const badge  = document.getElementById('hw-status-badge');
    
    if (hwText && d.arduino_status) {
        hwText.textContent = `Arduino: ${d.arduino_status}`;
        const color = d.arduino_color === 'green' ? '#10b981' : 
                     d.arduino_color === 'red' ? '#ef4444' : '#6b7280';
        if (hwDot) hwDot.style.backgroundColor = color;
        // Optionally update badge class if needed, but color on dot is usually enough
    }
}

async function loadDevices() {
    const { ok, data } = await apiFetch('/api/devices');
    if (ok) renderDevices(data);
}

function renderDevices(devices) {
    ['pump','fan'].forEach(dev => {
        const d = devices[dev]; if (!d) return;
        const toggle = document.getElementById(`toggle-${dev}`);
        const label  = document.getElementById(`label-${dev}`);
        const detail = document.getElementById(`detail-${dev}`);
        const card   = document.getElementById(`card-${dev}`);
        if (!toggle || !card) return;
        
        toggle.checked = d.on;
        toggle.disabled = (currentMode === 'auto');
        label.textContent = d.on ? 'ON' : 'OFF';
        label.style.color = d.on ? '#10b981' : '#6b7280';
        
        card.classList.toggle('active-device', d.on);
        
        if (dev === 'pump')    detail.textContent = `Duration: ${d.duration_min || '--'} min`;
        if (dev === 'fan')     detail.textContent = `Speed: ${d.speed || 'off'}`;
    });
}

async function toggleDevice(device, on) {
    if (currentMode === 'auto') {
        toast('Switch to Manual mode to control devices', 'info');
        const t = document.getElementById(`toggle-${device}`); if (t) t.checked = !on;
        return;
    }
    const toggle = document.getElementById(`toggle-${device}`);
    const label  = document.getElementById(`label-${device}`);
    const originalOn = !on; // Save state for retry if needed
    
    toggle.disabled = true; label.textContent = '...';
    const { ok, data } = await apiFetch('/api/control-device', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device, on, mode: 'manual' })
    });
    
    toggle.disabled = false;
    if (ok && data.success) {
        toast(`${device} turned ${on ? 'ON' : 'OFF'}`, 'success');
        await refreshAllData(); // Centralized Refresh
    } else {
        toggle.checked = originalOn;
        label.textContent = originalOn ? 'ON' : 'OFF';
        toast(`Failed: ${data.error || 'Unknown'}`, 'error');
    }
}

// per-device switchMode removed in favor of global system mode.

async function runAI() {
    const btn = document.querySelector('.btn-ai-run');
    if (btn) { btn.textContent = 'Thinking...'; btn.disabled = true; }
    const { ok, data } = await apiFetch('/api/ai-decision');
    if (btn) { btn.textContent = 'Run AI Now'; btn.disabled = false; }
    if (!ok) {
        document.getElementById('ai-explanation').innerHTML = `<div class="ai-reason">Error: ${data.error || 'Server error'}</div>`;
        return;
    }
    renderAIDecision(data);
    await refreshAllData(); // Synchronize devices and logs after AI run
}

function renderAIDecision(d) {
    const warning = document.getElementById('sensor-warning');
    const explBox = document.getElementById('ai-explanation');
    explBox.innerHTML = ''; // Start clean
    
    if (!d.valid) {
        if (warning) warning.style.display = 'block';
        explBox.innerHTML = (d.explanation || []).map(r => `<div class="ai-reason">${r}</div>`).join('');
        document.getElementById('conf-fill').style.width = '0%';
        document.getElementById('conf-pct').textContent  = '0%';
        document.getElementById('env-state-text').textContent = 'Waiting';
        document.getElementById('ai-meta').textContent = 'Sensor data invalid - decisions paused';
        return;
    }
    if (warning) warning.style.display = 'none';
    const conf = d.confidence || 85;
    document.getElementById('conf-fill').style.width = conf + '%';
    document.getElementById('conf-pct').textContent  = conf + '%';
    document.getElementById('conf-fill').style.background =
        conf >= 85 ? 'linear-gradient(90deg,#10b981,#059669)'
      : conf >= 65 ? 'linear-gradient(90deg,#f59e0b,#d97706)'
                   : 'linear-gradient(90deg,#ef4444,#dc2626)';
    explBox.innerHTML = (d.explanation || []).length
        ? d.explanation.map(r => `<div class="ai-reason">${r}</div>`).join('')
        : '<div class="ai-reason">All systems nominal</div>';
    const ts = d.timestamp ? new Date(d.timestamp).toLocaleTimeString() : '--';
    const i  = d.inputs || {};
    document.getElementById('ai-meta').textContent =
        `Last run: ${ts}  moisture ${(i.moisture||0).toFixed(0)}%  temp ${(i.temperature||0).toFixed(1)}C  humidity ${(i.humidity||0).toFixed(0)}%`;
    const state = d.env_state || 'Normal';
    document.getElementById('env-state-badge').className = 'env-state-badge ' + state.toLowerCase().replace(/ /g,'-');
    document.getElementById('env-state-text').textContent = state;
}

function toggleAutoAI(cb) {
    if (cb.checked) startAutoAI();
    else { clearInterval(autoAIInterval); autoAIInterval = null; }
}

function startAutoAI() {
    clearInterval(autoAIInterval);
    runAI();
    autoAIInterval = setInterval(runAI, 8000);
}

// injectDemo removed to ensure only real sensor data is used.

async function loadActivity() {
    const { ok, data: logs } = await apiFetch('/api/activity?limit=15');
    const el = document.getElementById('activity-list');
    if (!ok || !logs.length) { el.innerHTML = '<div style="color:#888;padding:16px;text-align:center">No activity yet</div>'; return; }
    el.innerHTML = logs.map(l => {
        const ts  = new Date(l.timestamp).toLocaleTimeString();
        const cls = l.category === 'warning' ? 'activity-warn' : l.category === 'system' ? 'activity-sys' : 'activity-ai';
        return `<div class="activity-item ${cls}"><span class="activity-time">${ts}</span><span class="activity-msg">${l.message}</span></div>`;
    }).join('');
}


async function loadIrrigationHistory() {
    const { ok, data: logs } = await apiFetch('/api/irrigation/history?limit=20');
    const tbody = document.getElementById('irr-tbody');
    if (!ok || !logs.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#888">No irrigation events yet</td></tr>'; return; }
    tbody.innerHTML = [...logs].reverse().map(l => `<tr>
        <td>${new Date(l.timestamp).toLocaleString()}</td>
        <td><span class="badge-${l.action||'start'}">${(l.action||'--').toUpperCase()}</span></td>
        <td><span class="badge-${l.mode||'auto'}">${(l.mode||'auto').toUpperCase()}</span></td>
        <td>${l.moisture!=null?l.moisture.toFixed(1)+'%':'--'}</td>
        <td>${l.duration_min!=null?l.duration_min+' min':'--'}</td>
    </tr>`).join('');
}

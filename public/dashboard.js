let ws;
let dataPoints = 0;
let startTime = Date.now();

// Initialize WebSocket connection
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        updateConnectionStatus(true);
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateDashboard(data);
        dataPoints++;
    };
    
    ws.onclose = () => {
        console.log('WebSocket disconnected');
        updateConnectionStatus(false);
        setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

function updateConnectionStatus(connected) {
    const statusDot = document.getElementById('connection-status');
    if (connected) {
        statusDot.className = 'status-dot connected';
    } else {
        statusDot.className = 'status-dot';
        statusDot.style.background = '#ef4444';
    }
}

function updateDashboard(data) {
    console.log('updateDashboard called with data:', data);
    
    // Check if data is valid
    if (!data || !data.mq135 || !data.dht22 || !data.pms5003 || !data.fc28) {
        console.error('Invalid data structure:', data);
        return;
    }
    
    // Update welcome user name
    const user = JSON.parse(localStorage.getItem('krishishakti_user') || sessionStorage.getItem('krishishakti_user') || '{}');
    document.getElementById('welcome-user').textContent = user.name || 'User';
    
    // Update location if available from sensor data
    if (data.location && data.location.city && data.location.country) {
        document.getElementById('location-text').textContent = `${data.location.city}, ${data.location.country}`;
    }
    
    // Update MQ-135 (Air Quality)
    const mq135Value = data.mq135.value;
    console.log('MQ-135 value:', mq135Value);
    document.getElementById('mq135-value').textContent = mq135Value.toFixed(1);
    const mq135Progress = Math.min((mq135Value / 500) * 100, 100);
    document.getElementById('mq135-progress').style.width = mq135Progress + '%';
    updateStatus('mq135-status', mq135Value, [0, 100, 200, 400]);
    
    // Update PMS5003 (Particulate Matter)
    const pm25Value = data.pms5003.pm25;
    const pm10Value = data.pms5003.pm10;
    console.log('PM2.5 value:', pm25Value, 'PM10 value:', pm10Value);
    document.getElementById('pm25-value').textContent = pm25Value.toFixed(1);
    document.getElementById('pm10-value').textContent = pm10Value.toFixed(1);
    updateStatus('pms-status', pm25Value, [0, 12, 35, 55]);
    
    // Update DHT22 (Temperature & Humidity)
    const tempValue = data.dht22.temperature;
    const humidityValue = data.dht22.humidity;
    console.log('Temperature:', tempValue, 'Humidity:', humidityValue);
    document.getElementById('temp-value').textContent = tempValue.toFixed(1);
    document.getElementById('humidity-value').textContent = humidityValue.toFixed(1);
    updateStatus('dht-status', humidityValue, [30, 60, 70, 80]);
    
    // Update FC-28 (Water Tank Level)
    const fc28Value = data.fc28.value;
    console.log('Water level:', fc28Value);
    document.getElementById('fc28-value').textContent = fc28Value.toFixed(1);
    document.getElementById('water-fill').style.height = fc28Value + '%';
    updateStatus('fc28-status', fc28Value, [0, 30, 60, 80]);
    
    // Update quick stats
    document.getElementById('quick-air').textContent = data.mq135.value < 100 ? 'Good' : data.mq135.value < 200 ? 'Moderate' : 'Poor';
    document.getElementById('quick-temp').textContent = data.dht22.temperature.toFixed(1) + '°C';
    document.getElementById('quick-water').textContent = data.fc28.value.toFixed(0) + '%';
    
    // Update last update time
    const updateTime = new Date(data.timestamp);
    document.getElementById('last-update').textContent = updateTime.toLocaleTimeString();
    
    // Update system info
    document.getElementById('data-points').textContent = dataPoints;
}

function updateStatus(elementId, value, thresholds) {
    const element = document.getElementById(elementId);
    const [good, moderate, poor, danger] = thresholds;
    
    element.classList.remove('good', 'warning', 'danger');
    
    if (value <= moderate) {
        element.classList.add('good');
        element.querySelector('span:last-child').textContent = 'Excellent';
    } else if (value <= poor) {
        element.classList.add('warning');
        element.querySelector('span:last-child').textContent = 'Moderate';
    } else if (value <= danger) {
        element.classList.add('warning');
        element.querySelector('span:last-child').textContent = 'Poor';
    } else {
        element.classList.add('danger');
        element.querySelector('span:last-child').textContent = 'Critical';
    }
}

// Update uptime
setInterval(() => {
    const uptime = Math.floor((Date.now() - startTime) / 1000);
    const hours = Math.floor(uptime / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    const seconds = uptime % 60;
    document.getElementById('uptime').textContent = 
        `${hours}h ${minutes}m ${seconds}s`;
}, 1000);

// Fetch historical data from Google Sheets or local storage
function loadHistoricalData() {
    fetch('/api/sheets/data?limit=20')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                document.getElementById('data-source-badge').textContent = 
                    '☁️ Data from Google Sheets';
                document.getElementById('data-source-badge').style.background = '#10b981';
                updateHistoryTable(data);
            } else {
                // Try local storage
                fetch('/api/history')
                    .then(response => response.json())
                    .then(localData => {
                        if (localData && localData.length > 0) {
                            document.getElementById('data-source-badge').textContent = 
                                '💾 Data from Local Storage';
                            document.getElementById('data-source-badge').style.background = '#3b82f6';
                            updateHistoryTable(localData.slice(-20));
                        } else {
                            document.getElementById('data-source-badge').textContent = 
                                '⚠️ No data yet - Start simulator!';
                            document.getElementById('data-source-badge').style.background = '#f59e0b';
                        }
                    });
            }
        })
        .catch(error => {
            console.error('Error fetching from Google Sheets, trying local storage...');
            // Fallback to local storage
            fetch('/api/history')
                .then(response => response.json())
                .then(localData => {
                    if (localData && localData.length > 0) {
                        document.getElementById('data-source-badge').textContent = 
                            '💾 Data from Local Storage';
                        document.getElementById('data-source-badge').style.background = '#3b82f6';
                        updateHistoryTable(localData.slice(-20));
                    } else {
                        document.getElementById('data-source-badge').textContent = 
                            '⚠️ No data available';
                        document.getElementById('data-source-badge').style.background = '#f59e0b';
                    }
                })
                .catch(err => {
                    document.getElementById('data-source-badge').textContent = 
                        '❌ Error loading data';
                    document.getElementById('data-source-badge').style.background = '#ef4444';
                });
        });
}

function updateHistoryTable(data) {
    const tbody = document.getElementById('history-body');
    tbody.innerHTML = '';
    
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 20px;">No data available yet. Start the simulator!</td></tr>';
        return;
    }
    
    // Reverse to show newest first
    const reversedData = [...data].reverse();
    reversedData.forEach(row => {
        const time = new Date(row.timestamp).toLocaleTimeString();
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${time}</td>
            <td>${(row.mq135 || 0).toFixed(1)}</td>
            <td>${(row.temperature || 0).toFixed(1)}°C</td>
            <td>${(row.humidity || 0).toFixed(1)}%</td>
            <td>${(row.pm25 || 0).toFixed(1)}</td>
            <td>${(row.pm10 || 0).toFixed(1)}</td>
            <td>${(row.fc28 || 0).toFixed(1)}%</td>
        `;
        tbody.appendChild(tr);
    });
}

// Fetch initial data
console.log('Fetching initial sensor data...');
fetch('/api/sensors')
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Initial data received:', data);
        updateDashboard(data);
    })
    .catch(error => {
        console.error('Error fetching initial data:', error);
        // Try again after 2 seconds
        setTimeout(() => {
            console.log('Retrying initial fetch...');
            fetch('/api/sensors')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(err => console.error('Retry failed:', err));
        }, 2000);
    });

// Load historical data
loadHistoricalData();

// Refresh historical data every 10 seconds
setInterval(loadHistoricalData, 10000);

// Connect WebSocket
connectWebSocket();


// Detect and display location
function detectLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                try {
                    // Use reverse geocoding to get city name
                    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
                    const data = await response.json();
                    
                    const city = data.address.city || data.address.town || data.address.village || data.address.state;
                    const country = data.address.country;
                    
                    document.getElementById('location-text').textContent = `${city}, ${country}`;
                    
                    // Store location for later use
                    localStorage.setItem('user_location', JSON.stringify({
                        city: city,
                        country: country,
                        lat: lat,
                        lon: lon,
                        timestamp: new Date().toISOString()
                    }));
                } catch (error) {
                    console.error('Error getting location name:', error);
                    document.getElementById('location-text').textContent = `Lat: ${lat.toFixed(2)}, Lon: ${lon.toFixed(2)}`;
                }
            },
            (error) => {
                console.error('Geolocation error:', error);
                // Try to get location from IP
                getLocationFromIP();
            }
        );
    } else {
        // Geolocation not supported, try IP-based location
        getLocationFromIP();
    }
}

async function getLocationFromIP() {
    try {
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        
        const city = data.city;
        const country = data.country_name;
        
        document.getElementById('location-text').textContent = `${city}, ${country}`;
        
        localStorage.setItem('user_location', JSON.stringify({
            city: city,
            country: country,
            lat: data.latitude,
            lon: data.longitude,
            timestamp: new Date().toISOString()
        }));
    } catch (error) {
        console.error('Error getting IP location:', error);
        document.getElementById('location-text').textContent = 'Location unavailable';
    }
}

// Check if we have cached location (less than 24 hours old)
function loadCachedLocation() {
    const cached = localStorage.getItem('user_location');
    if (cached) {
        const location = JSON.parse(cached);
        const cacheAge = Date.now() - new Date(location.timestamp).getTime();
        
        // If cache is less than 24 hours old, use it
        if (cacheAge < 24 * 60 * 60 * 1000) {
            document.getElementById('location-text').textContent = `${location.city}, ${location.country}`;
            return true;
        }
    }
    return false;
}

// Initialize location detection
if (!loadCachedLocation()) {
    detectLocation();
}

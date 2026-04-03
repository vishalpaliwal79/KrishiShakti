// Agriculture AI JavaScript - Simplified Upload Version

let currentImage = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('=== AGRICULTURE PAGE LOADED ===');
    loadUserInfo();
    loadLocation();
    updateHealthScore();
    setupImageUpload();
    connectToSensorData();
    console.log('=== INITIALIZATION COMPLETE ===');
});

// Load user info
function loadUserInfo() {
    const user = JSON.parse(localStorage.getItem('airwater_user') || sessionStorage.getItem('airwater_user') || '{}');
    document.getElementById('welcome-user').textContent = user.name || 'User';
}

// Load location
function loadLocation() {
    const cached = localStorage.getItem('user_location');
    if (cached) {
        const location = JSON.parse(cached);
        document.getElementById('location-text').textContent = `${location.city}, ${location.country}`;
    } else {
        detectLocation();
    }
}

async function detectLocation() {
    try {
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        const city = data.city;
        const country = data.country_name;
        
        document.getElementById('location-text').textContent = `${city}, ${country}`;
        
        localStorage.setItem('user_location', JSON.stringify({
            city: city,
            country: country,
            timestamp: new Date().toISOString()
        }));
    } catch (error) {
        console.error('Error getting location:', error);
        document.getElementById('location-text').textContent = 'Location unavailable';
    }
}

// Image upload handling - SIMPLE VERSION
function setupImageUpload() {
    console.log('=== SETTING UP IMAGE UPLOAD ===');
    
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('crop-image');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resetBtn = document.getElementById('reset-btn');
    
    console.log('Elements:', {
        uploadBtn: uploadBtn ? 'Found' : 'NOT FOUND',
        fileInput: fileInput ? 'Found' : 'NOT FOUND',
        analyzeBtn: analyzeBtn ? 'Found' : 'NOT FOUND',
        resetBtn: resetBtn ? 'Found' : 'NOT FOUND'
    });
    
    if (!uploadBtn || !fileInput) {
        console.error('CRITICAL: Upload button or file input not found!');
        alert('Upload system error. Please refresh the page.');
        return;
    }
    
    // Upload button click
    uploadBtn.onclick = function() {
        console.log('>>> UPLOAD BUTTON CLICKED <<<');
        fileInput.click();
    };
    
    // File input change
    fileInput.onchange = function(e) {
        console.log('>>> FILE INPUT CHANGED <<<');
        const file = e.target.files[0];
        
        if (!file) {
            console.log('No file selected');
            return;
        }
        
        console.log('File details:', {
            name: file.name,
            type: file.type,
            size: file.size + ' bytes (' + (file.size / 1024).toFixed(2) + ' KB)'
        });
        
        // Validate
        if (!file.type.match('image.*')) {
            console.error('Not an image file!');
            alert('Please select an image file (JPG, PNG, GIF)');
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) {
            console.error('File too large!');
            alert('File must be smaller than 10MB');
            return;
        }
        
        console.log('File validation passed, loading preview...');
        loadImagePreview(file);
    };
    
    // Analyze button
    if (analyzeBtn) {
        analyzeBtn.onclick = function() {
            console.log('>>> ANALYZE BUTTON CLICKED <<<');
            analyzeCrop();
        };
    }
    
    // Reset button
    if (resetBtn) {
        resetBtn.onclick = function() {
            console.log('>>> RESET BUTTON CLICKED <<<');
            resetUpload();
        };
    }
    
    console.log('=== IMAGE UPLOAD SETUP COMPLETE ===');
}

function loadImagePreview(file) {
    console.log('Loading image preview for:', file.name);
    currentImage = file;
    
    const reader = new FileReader();
    
    reader.onload = function(e) {
        console.log('FileReader onload triggered');
        
        const previewImg = document.getElementById('preview-img');
        const uploadSection = document.querySelector('.simple-upload-section');
        const previewSection = document.getElementById('image-preview');
        const analysisSection = document.getElementById('analysis-result');
        
        if (!previewImg || !uploadSection || !previewSection) {
            console.error('Preview elements not found!');
            return;
        }
        
        console.log('Setting image source...');
        previewImg.src = e.target.result;
        
        console.log('Hiding upload section...');
        uploadSection.style.display = 'none';
        
        console.log('Showing preview section...');
        previewSection.style.display = 'block';
        
        if (analysisSection) {
            analysisSection.style.display = 'none';
        }
        
        console.log('✓ IMAGE PREVIEW DISPLAYED SUCCESSFULLY');
    };
    
    reader.onerror = function(error) {
        console.error('FileReader error:', error);
        alert('Error loading image. Please try again.');
    };
    
    console.log('Starting FileReader...');
    reader.readAsDataURL(file);
}

function resetUpload() {
    console.log('Resetting upload...');
    
    currentImage = null;
    
    const fileInput = document.getElementById('crop-image');
    const uploadSection = document.querySelector('.simple-upload-section');
    const previewSection = document.getElementById('image-preview');
    const analysisSection = document.getElementById('analysis-result');
    const previewImg = document.getElementById('preview-img');
    
    if (fileInput) fileInput.value = '';
    if (previewImg) previewImg.src = '';
    if (uploadSection) uploadSection.style.display = 'block';
    if (previewSection) previewSection.style.display = 'none';
    if (analysisSection) analysisSection.style.display = 'none';
    
    console.log('✓ Upload reset complete');
}

// AI Analysis - Real API Call
async function analyzeCrop() {
    if (!currentImage) {
        alert('Please upload an image first');
        return;
    }
    
    console.log('Starting AI analysis...');
    
    // Show loading state
    const analyzeBtn = document.getElementById('analyze-btn');
    const originalText = analyzeBtn.textContent;
    analyzeBtn.textContent = '🔄 Analyzing with AI...';
    analyzeBtn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('image', currentImage);
        
        const response = await fetch('/api/predict-disease', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const result = await response.json();
        if (!result.success) throw new Error(result.message || 'Analysis failed');
        
        if (result.mode === 'demo') showDemoModeBanner(result.message);
        
        displayAnalysisResult({
            name: result.disease,
            icon: result.is_healthy ? '✅' : '⚠️',
            confidence: result.confidence,
            severity: result.is_healthy ? 'None' : 'Moderate',
            description: result.is_healthy
                ? 'Your crop appears healthy with no visible signs of disease or pest damage.'
                : `Disease detected: ${result.disease}. Immediate action recommended.`,
            recommendations: result.recommendations || []
        });
        
    } catch (error) {
        console.error('Error during analysis:', error);
        alert('Error analyzing image: ' + error.message + '\n\nPlease try again.');
    } finally {
        analyzeBtn.textContent = originalText;
        analyzeBtn.disabled = false;
    }
}

function showDemoModeBanner(message) {
    if (document.getElementById('demo-mode-banner')) return;
    const banner = document.createElement('div');
    banner.id = 'demo-mode-banner';
    banner.style.cssText = `background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; margin: 15px 0; border-radius: 12px; font-size: 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);`;
    banner.innerHTML = `<span style="font-size: 24px;">🤖</span><div style="flex: 1;"><strong>Demo Mode Active</strong><br><span style="font-size: 13px; opacity: 0.95;">${message || 'Using simulated AI results.'}</span></div><button onclick="this.parentElement.remove()" style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 6px 12px; border-radius: 6px; cursor: pointer;">Got it</button>`;
    const aiSection = document.querySelector('.ai-section');
    aiSection.insertBefore(banner, aiSection.firstChild);
}

function displayAnalysisResult(result) {
    const analysisSection = document.getElementById('analysis-result');
    
    // Build detailed analysis sections
    let detailedAnalysisHTML = '';
    if (result.detailed_analysis) {
        detailedAnalysisHTML = `
            <div class="detailed-analysis">
                <h4>📋 Detailed Analysis</h4>
                <div class="analysis-grid">
                    ${Object.entries(result.detailed_analysis).map(([key, value]) => `
                        <div class="analysis-item">
                            <strong>${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong>
                            <span>${value}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    // Build treatment schedule if available
    let treatmentHTML = '';
    if (result.treatment_schedule) {
        treatmentHTML = `
            <div class="treatment-schedule">
                <h4>📅 Treatment Schedule</h4>
                <ul class="timeline">
                    ${result.treatment_schedule.map(step => `<li>${step}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build preventive measures
    let preventiveHTML = '';
    if (result.preventive_measures) {
        preventiveHTML = `
            <div class="preventive-measures">
                <h4>🛡️ Preventive Measures</h4>
                <ul>
                    ${result.preventive_measures.map(measure => `<li>${measure}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build warning signs if available
    let warningHTML = '';
    if (result.warning_signs) {
        warningHTML = `
            <div class="warning-signs">
                <h4>⚠️ Warning Signs to Watch</h4>
                <ul class="warning-list">
                    ${result.warning_signs.map(sign => `<li>${sign}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build natural remedies if available
    let naturalHTML = '';
    if (result.natural_remedies) {
        naturalHTML = `
            <div class="natural-remedies">
                <h4>🌿 Natural Remedies</h4>
                <ul>
                    ${result.natural_remedies.map(remedy => `<li>${remedy}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build chemical options if available
    let chemicalHTML = '';
    if (result.chemical_options) {
        chemicalHTML = `
            <div class="chemical-options">
                <h4>💊 Chemical Treatment Options</h4>
                <ul>
                    ${result.chemical_options.map(option => `<li>${option}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build fertilizer guide if available
    let fertilizerHTML = '';
    if (result.fertilizer_guide) {
        fertilizerHTML = `
            <div class="fertilizer-guide">
                <h4>🌿 Fertilizer Application Guide</h4>
                <ul>
                    ${result.fertilizer_guide.map(guide => `<li>${guide}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build application method if available
    let applicationHTML = '';
    if (result.application_method) {
        applicationHTML = `
            <div class="application-method">
                <h4>📝 Application Method</h4>
                <ul>
                    ${result.application_method.map(method => `<li>${method}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build beneficial insects if available
    let insectsHTML = '';
    if (result.beneficial_insects) {
        insectsHTML = `
            <div class="beneficial-insects">
                <h4>🐞 Beneficial Insects</h4>
                <ul>
                    ${result.beneficial_insects.map(insect => `<li>${insect}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build recovery timeline if available
    let recoveryHTML = '';
    if (result.recovery_timeline) {
        recoveryHTML = `
            <div class="recovery-timeline">
                <h4>⏱️ Recovery Timeline</h4>
                <ul class="timeline">
                    ${result.recovery_timeline.map(step => `<li>${step}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build next steps if available
    let nextStepsHTML = '';
    if (result.next_steps) {
        nextStepsHTML = `
            <div class="next-steps">
                <h4>👣 Next Steps</h4>
                <ul>
                    ${result.next_steps.map(step => `<li>${step}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Build cost estimate if available
    let costHTML = '';
    if (result.cost_estimate) {
        costHTML = `
            <div class="cost-estimate">
                <h4>💰 Cost Estimate</h4>
                <div class="cost-grid">
                    ${Object.entries(result.cost_estimate).map(([key, value]) => `
                        <div class="cost-item">
                            <span class="cost-label">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                            <span class="cost-value">${value}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    const html = `
        <div class="result-header">
            <h3>Analysis Results</h3>
            <div class="result-meta">
                <span class="confidence">${result.confidence}% Confidence</span>
                ${result.severity ? `<span class="severity severity-${result.severity.toLowerCase()}">${result.severity}</span>` : ''}
            </div>
        </div>
        <div class="disease-info">
            <div class="disease-status">
                <span class="status-icon">${result.icon}</span>
                <span class="disease-name">${result.name}</span>
            </div>
            <p class="disease-description">${result.description}</p>
        </div>
        
        ${detailedAnalysisHTML}
        
        <div class="recommendations">
            <h4>💡 Immediate Recommendations</h4>
            <ul>
                ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>
        
        ${treatmentHTML}
        ${naturalHTML}
        ${chemicalHTML}
        ${fertilizerHTML}
        ${applicationHTML}
        ${preventiveHTML}
        ${insectsHTML}
        ${warningHTML}
        ${recoveryHTML}
        ${nextStepsHTML}
        ${costHTML}
    `;
    
    analysisSection.innerHTML = html;
    analysisSection.style.display = 'block';
    analysisSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Rest of the functions (health score, sensor data, etc.)
function updateHealthScore(score = 85) {
    document.getElementById('health-score').textContent = Math.round(score);
    const circle = document.getElementById('health-progress');
    const circumference = 2 * Math.PI * 90;
    const offset = circumference - (score / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    
    if (score >= 80) {
        circle.style.stroke = '#10b981';
    } else if (score >= 60) {
        circle.style.stroke = '#f59e0b';
    } else {
        circle.style.stroke = '#ef4444';
    }
}

function connectToSensorData() {
    fetchSensorData();
    fetchAIRecommendations();
    setInterval(fetchSensorData, 5000);
    setInterval(fetchAIRecommendations, 10000);
}

async function fetchSensorData() {
    try {
        const response = await fetch('/api/sensors');
        const data = await response.json();
        updateHealthScoreFromSensors(data);
    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

async function fetchAIRecommendations() {
    try {
        const response = await fetch('/api/agriculture/recommendations');
        const data = await response.json();
        updateAIRecommendations(data);
    } catch (error) {
        console.error('Error fetching AI recommendations:', error);
    }
}

function updateHealthScoreFromSensors(data) {
    let score = 100;
    
    const airQuality = data.mq135?.value || 0;
    if (airQuality > 200) score -= 20;
    else if (airQuality > 100) score -= 10;
    
    const temp = data.dht22?.temperature || 0;
    if (temp > 0) {
        if (temp < 15 || temp > 35) score -= 15;
        else if (temp < 20 || temp > 30) score -= 5;
    }
    
    const humidity = data.dht22?.humidity || 0;
    if (humidity > 0) {
        if (humidity < 40 || humidity > 80) score -= 10;
        else if (humidity < 50 || humidity > 70) score -= 5;
    }
    
    const tds = data.tds?.value || 0;
    if (tds > 500) score -= 15;
    else if (tds > 300) score -= 5;
    
    updateHealthScore(Math.max(0, score));
    
    const moisture = data.fc28?.value || 0;
    document.getElementById('current-moisture').textContent = moisture.toFixed(0) + '%';
}

function updateAIRecommendations(data) {
    // Update irrigation, fertilizer, pest, weather tabs
    // (keeping existing implementation)
    if (data.ai_insights && data.ai_insights.length > 0) {
        const insightsHTML = data.ai_insights.map(insight => {
            const icons = {
                'success': '✅',
                'warning': '⚠️',
                'alert': '🚨',
                'info': '💡'
            };
            return `
                <div class="insight-item ${insight.type}">
                    <span class="insight-icon">${icons[insight.type]}</span>
                    <div class="insight-content">
                        <strong>${insight.title}</strong>
                        <p>${insight.message}</p>
                    </div>
                </div>
            `;
        }).join('');
        document.getElementById('ai-insights').innerHTML = insightsHTML;
    }
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

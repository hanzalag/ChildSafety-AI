// AegisYouth AI Client-Side Application Manager

let insightsChartInstance = null;
let currentDashboardData = null; // Stores latest metrics for CSV export

document.addEventListener("DOMContentLoaded", () => {
    let sessionUuid = localStorage.getItem("aegis_session_uuid");
    if (!sessionUuid) {
        sessionUuid = 'sess_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        localStorage.setItem("aegis_session_uuid", sessionUuid);
    }

    const sessionBadge = document.getElementById("session-badge");
    if (sessionBadge) {
        sessionBadge.innerText = `Session: ${sessionUuid.substring(0, 10)}...`;
    }

    window.AegisSession = sessionUuid;
});

// Helper Function: Format UTC ISO Timestamps cleanly into local Date & Time
function formatDateTime(isoString) {
    if (!isoString) return "N/A";
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
}

// SafeChat Sentinel Handler
async function analyzeSentinelMessage() {
    const textInput = document.getElementById("sentinel-input");
    const resultBox = document.getElementById("sentinel-result");
    if (!textInput || !resultBox) return;

    const text = textInput.value.trim();
    if (!text) {
        alert("Please enter a message to analyze.");
        return;
    }

    resultBox.innerHTML = `<p style="color: var(--text-muted);">Running advanced AI psycholinguistic sentiment & safety analysis...</p>`;
    resultBox.classList.add("active");

    try {
        const response = await fetch("/api/sentinel/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, session_uuid: window.AegisSession })
        });

        if (!response.ok) throw new Error("Server analysis failed.");
        const data = await response.json();

        const badgeClass = data.is_safe ? "badge-safe" : "badge-danger";
        const statusText = data.is_safe ? "Safe & Positive" : `Risk Detected: ${data.threat_category}`;

        resultBox.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4>Detailed AI Sentiment & Safety Report</h4>
                <span class="badge ${badgeClass}">${statusText}</span>
            </div>
            <p><strong>Precision Confidence Score:</strong> ${(data.confidence_score * 100).toFixed(1)}%</p>
            <p style="margin-top: 0.5rem;"><strong>Detailed AI Feedback:</strong> ${data.ai_feedback}</p>
            ${!data.is_safe ? `<div style="margin-top: 1rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-left: 3px solid var(--success); border-radius: 4px;"><p><strong>Reframed Alternative:</strong> ${data.reframed_text}</p></div>` : ''}
        `;
    } catch (err) {
        resultBox.innerHTML = `<p style="color: var(--danger);">Error connecting to AI moderation service.</p>`;
    }
}

// SafeCompanion Guard Handler
async function auditCompanionInteraction() {
    const promptInput = document.getElementById("companion-prompt");
    const responseInput = document.getElementById("companion-response");
    const resultBox = document.getElementById("companion-result");
    if (!promptInput || !responseInput || !resultBox) return;

    const promptText = promptInput.value.trim();
    const responseText = responseInput.value.trim();

    if (!promptText || !responseText) {
        alert("Please provide both a user prompt and companion response.");
        return;
    }

    resultBox.innerHTML = `<p style="color: var(--text-muted);">Auditing AI companion interaction...</p>`;
    resultBox.classList.add("active");

    try {
        const res = await fetch("/api/companion/audit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_uuid: window.AegisSession,
                companion_prompt: promptText,
                companion_response: responseText
            })
        });

        if (!res.ok) throw new Error("Audit service failed.");
        const data = await res.json();

        let badgeClass = "badge-safe";
        if (data.safety_rating === "Caution") badgeClass = "badge-caution";
        if (data.safety_rating === "Blocked") badgeClass = "badge-danger";

        resultBox.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4>Safety Audit Report</h4>
                <span class="badge ${badgeClass}">Rating: ${data.safety_rating}</span>
            </div>
            <p><strong>Boundary Violation Detected:</strong> ${data.boundary_violation_detected ? 'Yes ⚠️' : 'No ✅'}</p>
            <p style="margin-top: 0.5rem;"><strong>Audit Breakdown:</strong> ${data.audit_notes}</p>
            ${data.safety_rating !== 'Safe' ? `<div style="margin-top: 1rem; padding: 0.75rem; background: rgba(245, 158, 11, 0.1); border-left: 3px solid var(--warning); border-radius: 4px;"><p><strong>Recommended Safe Response:</strong> ${data.safe_response}</p></div>` : ''}
        `;
    } catch (err) {
        resultBox.innerHTML = `<p style="color: var(--danger);">Error connecting to AI audit service.</p>`;
    }
}

// Media Detective Computer Vision Handler
async function analyzeImageContent() {
    const fileInput = document.getElementById("detective-image-file");
    const resultBox = document.getElementById("detective-result");
    if (!fileInput || !resultBox) return;

    if (fileInput.files.length === 0) {
        alert("Please select an image file to analyze.");
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);
    formData.append("session_uuid", window.AegisSession);

    resultBox.innerHTML = `<p style="color: var(--text-muted);">Running Computer Vision & Deepfake AI Forensics on image...</p>`;
    resultBox.classList.add("active");

    try {
        const res = await fetch("/api/detector/analyze-image", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("Image analysis failed.");
        const data = await res.json();

        const badgeClass = data.is_harmful ? "badge-danger" : "badge-safe";
        const indicatorsHtml = (data.indicators || []).map(ind => `<li>${ind}</li>`).join("");

        resultBox.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4>Computer Vision Forensic Report</h4>
                <span class="badge ${badgeClass}">${data.threat_category}</span>
            </div>
            <p><strong>Precision Confidence Score:</strong> ${(data.confidence_score * 100).toFixed(1)}%</p>
            <p style="margin-top: 0.5rem;"><strong>AI Forensic Feedback:</strong> ${data.ai_feedback}</p>
            <p style="margin-top: 0.5rem;"><strong>Child Impact Assessment:</strong> ${data.child_impact_assessment}</p>
            ${indicatorsHtml ? `<div style="margin-top: 0.75rem;"><strong>Detected Visual Indicators:</strong><ul style="margin-left: 1.5rem; color: var(--text-muted);">${indicatorsHtml}</ul></div>` : ''}
            <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(6, 182, 212, 0.1); border-left: 3px solid var(--accent); border-radius: 4px;">
                <p><strong>Educational Guidance:</strong> ${data.educational_guidance}</p>
            </div>
        `;
    } catch (err) {
        resultBox.innerHTML = `<p style="color: var(--danger);">Error executing computer vision analysis.</p>`;
    }
}

// Dashboard Real-Time Metrics & Interactive Chart Loader
async function loadDashboardMetrics() {
    if (!window.AegisSession) return;

    try {
        const res = await fetch(`/api/dashboard/metrics?session_uuid=${window.AegisSession}`);
        if (!res.ok) throw new Error("Failed to load metrics.");
        const data = await res.json();
        currentDashboardData = data; // Cache data for CSV Export

        // Update Stat Cards
        const statScanned = document.getElementById("stat-scanned");
        const statThreats = document.getElementById("stat-threats");
        const statAudits = document.getElementById("stat-audits");
        const statSafety = document.getElementById("stat-safety");

        if (statScanned) statScanned.innerText = data.total_messages_scanned;
        if (statThreats) statThreats.innerText = data.threats_mitigated;
        if (statAudits) statAudits.innerText = data.companion_audits_count;
        if (statSafety) statSafety.innerText = data.safety_score_percentage + "%";

        // Update Moderations Table
        const modTable = document.getElementById("recent-moderations-body");
        if (modTable) {
            if (data.recent_moderations.length === 0) {
                modTable.innerHTML = `<tr><td colspan="3" style="text-align: center; color: var(--text-muted); padding: 1rem;">No scans recorded yet. Try SafeChat Sentinel!</td></tr>`;
            } else {
                modTable.innerHTML = data.recent_moderations.map(m => `
                    <tr>
                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border-color);">${m.input_text}</td>
                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border-color);"><span class="badge ${m.is_safe ? 'badge-safe' : 'badge-danger'}">${m.is_safe ? 'Safe' : m.threat_category}</span></td>
                        <td style="padding: 0.75rem; border-bottom: 1px solid var(--border-color); color: var(--text-muted); font-size: 0.85rem;">${formatDateTime(m.created_at)}</td>
                    </tr>
                `).join("");
            }
        }

        renderDashboardChart(data.safe_messages_count, data.threats_mitigated, data.companion_audits_count);

    } catch (err) {
        console.error("Dashboard auto-sync error:", err);
    }
}

// Render Interactive Insight Chart
function renderDashboardChart(safeCount, threatCount, auditCount) {
    const ctx = document.getElementById('safetyInsightsChart');
    if (!ctx) return;

    if (insightsChartInstance) {
        insightsChartInstance.data.datasets[0].data = [safeCount, threatCount, auditCount];
        insightsChartInstance.update('none');
        return;
    }

    insightsChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Safe Interactions', 'Mitigated Threats', 'Companion Audits'],
            datasets: [{
                label: 'Activity Volume',
                data: [safeCount, threatCount, auditCount],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(239, 68, 68, 0.7)',
                    'rgba(245, 158, 11, 0.7)'
                ],
                borderColor: [
                    '#10b981',
                    '#ef4444',
                    '#f59e0b'
                ],
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#94a3b8', stepSize: 1 },
                    grid: { color: '#334155' }
                },
                x: {
                    ticks: { color: '#f8fafc' },
                    grid: { display: false }
                }
            }
        }
    });
}

// Export Dashboard Activity as CSV
function exportDashboardCSV() {
    if (!currentDashboardData || !currentDashboardData.recent_moderations || currentDashboardData.recent_moderations.length === 0) {
        alert("No moderation activity available to export yet.");
        return;
    }

    let csvContent = "data:text/csv;charset=utf-8,ID,Message Snippet,Is Safe,Threat Category,Timestamp\n";

    currentDashboardData.recent_moderations.forEach(log => {
        const cleanSnippet = `"${log.input_text.replace(/"/g, '""')}"`;
        const row = `${log.id},${cleanSnippet},${log.is_safe},${log.threat_category},${formatDateTime(log.created_at)}`;
        csvContent += row + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `AegisYouth_Safety_Log_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
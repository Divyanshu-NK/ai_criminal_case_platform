// SPA View Management
function switchView(viewName) {
    document.getElementById('dashboard-view').classList.add('view-hidden');
    document.getElementById('workspace-view').classList.add('view-hidden');
    
    // Hide/Show sidebar links
    const workspaceNavs = document.querySelectorAll('.workspace-nav');
    const workspaceGroups = document.querySelectorAll('.workspace-nav-group');
    
    if (viewName === 'dashboard') {
        document.getElementById('dashboard-view').classList.remove('view-hidden');
        workspaceNavs.forEach(nav => nav.classList.add('view-hidden'));
        workspaceGroups.forEach(grp => grp.classList.add('view-hidden'));
        
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        document.querySelector('[data-target="dashboard-view"]').classList.add('active');
    } else if (viewName === 'workspace') {
        document.getElementById('workspace-view').classList.remove('view-hidden');
        workspaceNavs.forEach(nav => nav.classList.remove('view-hidden'));
        workspaceGroups.forEach(grp => grp.classList.remove('view-hidden'));
    }
}

// Tab Management
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    
    document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
    document.querySelector(`[data-target="${tabId}"]`).classList.add('active');
}

// Global state to hold latest context
let currentContext = null;

// Submission Handler
document.addEventListener("DOMContentLoaded", () => {
    const analyzeBtn = document.getElementById("analyze-btn");
    const scenarioInput = document.getElementById("scenario-input");

    analyzeBtn.addEventListener("click", async () => {
        const text = scenarioInput.value.trim();
        if (!text) return;

        // Transition to workspace
        switchView('workspace');
        switchTab('overview');
        
        // Reset traces
        document.querySelectorAll('.trace-status').forEach(el => {
            el.textContent = "Running";
            el.classList.remove("done");
        });
        
        document.getElementById('overview-summary').textContent = "Processing analysis... This may take a minute as agents collaborate.";

        analyzeBtn.disabled = true;
        
        try {
            const response = await fetch("/api/v1/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ scenario: text, task_type: "analysis" })
            });

            if (!response.ok) {
                document.getElementById('overview-summary').textContent = "Error during analysis.";
                return;
            }

            const data = await response.json();
            currentContext = data;
            
            // Mark all traces as done (since we don't have SSE yet, they finish simultaneously in MVP)
            document.querySelectorAll('.trace-status').forEach(el => {
                el.textContent = "✓";
                el.classList.add("done");
            });

            populateWorkspace(data);

        } catch (err) {
            document.getElementById('overview-summary').textContent = "Connection error.";
        } finally {
            analyzeBtn.disabled = false;
        }
    });
});

function populateWorkspace(data) {
    // 1. Overview
    if (data.report && data.report.summary) {
        document.getElementById('overview-summary').innerHTML = `<p>${data.report.summary}</p><br><p><strong>Conclusion:</strong> ${data.report.conclusion}</p>`;
    } else {
        document.getElementById('overview-summary').textContent = "Analysis complete.";
    }

    // 2. Facts
    const factsList = document.getElementById('facts-list');
    factsList.innerHTML = '';
    (data.facts || []).forEach(f => {
        const li = document.createElement('li');
        li.className = "has-icon legal-text";
        li.textContent = f.description;
        factsList.appendChild(li);
    });

    // 3. Offences & Validation
    const offencesTbody = document.getElementById('offences-tbody');
    offencesTbody.innerHTML = '';
    const validationMap = data.validation || {};
    
    (data.offences || []).forEach(offence => {
        const tr = document.createElement('tr');
        
        // Find if any potential section is validated
        let valResult = "Review";
        let badgeClass = "badge-medium";
        
        offence.potential_sections.forEach(sec => {
            if (validationMap[sec]) {
                if (validationMap[sec].is_satisfied) {
                    valResult = "Strong";
                    badgeClass = "badge-strong";
                } else {
                    valResult = "Insufficient";
                    badgeClass = "badge-weak";
                }
            }
        });

        tr.innerHTML = `
            <td style="font-weight: 500;">${offence.name}</td>
            <td style="color: var(--text-secondary);">${offence.potential_sections.join(", ")}</td>
            <td><span class="badge ${badgeClass}">${valResult}</span></td>
        `;
        
        tr.addEventListener('click', () => showOffenceDetails(offence, validationMap));
        offencesTbody.appendChild(tr);
    });

    // 4. Laws
    const lawsContainer = document.getElementById('laws-container');
    lawsContainer.innerHTML = '';
    (data.laws || []).forEach(law => {
        const card = document.createElement('div');
        card.className = "details-card legal-text";
        card.innerHTML = `
            <h3>${law.act_name} § ${law.section}</h3>
            <p>${law.text}</p>
        `;
        lawsContainer.appendChild(card);
    });

    // 5. Evidence
    const evAvailable = document.getElementById('evidence-available');
    evAvailable.innerHTML = '';
    (data.evidence || []).forEach(ev => {
        const li = document.createElement('li');
        li.className = "has-icon";
        li.innerHTML = `<strong>${ev.type}:</strong> ${ev.description}`;
        evAvailable.appendChild(li);
    });

    const evMissing = document.getElementById('evidence-missing');
    evMissing.innerHTML = '';
    (data.missing_evidence || []).forEach(ev => {
        const li = document.createElement('li');
        li.className = "missing-icon";
        li.innerHTML = `<strong>Missing:</strong> ${ev.description} - <span style="color:var(--text-secondary)">${ev.reason}</span>`;
        evMissing.appendChild(li);
    });

    // 6. Precedents
    const precList = document.getElementById('precedents-list');
    precList.innerHTML = '';
    (data.similar_cases || []).forEach(prec => {
        const div = document.createElement('div');
        div.className = "precedent-item legal-text";
        div.innerHTML = `
            <div class="precedent-header">
                <span class="precedent-title">${prec.case_name} (${prec.year})</span>
                <span class="precedent-court">${prec.court}</span>
            </div>
            <div style="margin-bottom: 8px;"><strong>Relevance:</strong> ${prec.relevance}</div>
            <p>${prec.summary}</p>
        `;
        precList.appendChild(div);
    });

    // 7. Strategy
    const prosList = document.getElementById('strategy-pros');
    prosList.innerHTML = '';
    if (data.strategy && data.strategy.prosecution_arguments) {
        data.strategy.prosecution_arguments.forEach(arg => {
            const li = document.createElement('li');
            li.textContent = arg;
            prosList.appendChild(li);
        });
    }

    const defList = document.getElementById('strategy-def');
    defList.innerHTML = '';
    if (data.strategy && data.strategy.defense_arguments) {
        data.strategy.defense_arguments.forEach(arg => {
            const li = document.createElement('li');
            li.textContent = arg;
            defList.appendChild(li);
        });
    }
}

function showOffenceDetails(offence, validationMap) {
    const detailsDiv = document.getElementById('offences-details');
    detailsDiv.classList.remove('view-hidden');
    
    let html = `<h3>${offence.name}</h3>`;
    html += `<p style="margin-bottom: 16px;">${offence.description}</p>`;
    
    offence.potential_sections.forEach(sec => {
        const val = validationMap[sec];
        if (val) {
            html += `<div class="details-section">
                <h4>Validation for ${sec}</h4>
                <p style="margin-bottom: 8px;">${val.reasoning}</p>
            `;
            if (val.missing_ingredients && val.missing_ingredients.length > 0) {
                html += `<ul class="clean-list">`;
                val.missing_ingredients.forEach(ing => {
                    html += `<li class="missing-icon">${ing}</li>`;
                });
                html += `</ul>`;
            }
            html += `</div>`;
        }
    });
    
    detailsDiv.innerHTML = html;
}

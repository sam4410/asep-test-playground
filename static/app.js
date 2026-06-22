// ASEP Client-Side Control Panel Application

let selectedRunId = null;
let pollingInterval = null;

// Initial Setup
document.addEventListener("DOMContentLoaded", () => {
    loadHistoricalRuns();
    
    // Bind form submission
    const form = document.getElementById("new-run-form");
    form.addEventListener("submit", handleStartRun);
    
    // Bind approval buttons
    const approveBtn = document.getElementById("btn-approve");
    approveBtn.addEventListener("click", handleApproveTask);
});

// Fetch all historical runs
async function loadHistoricalRuns() {
    try {
        const response = await fetch("/api/v1/runs");
        if (!response.ok) throw new Error("Failed to fetch runs");
        
        const runs = await response.json();
        const runsList = document.getElementById("runs-list");
        
        if (runs.length === 0) {
            runsList.innerHTML = `<div class="empty-state">No historical runs found.</div>`;
            return;
        }
        
        runsList.innerHTML = "";
        runs.forEach(run => {
            const runItem = document.createElement("div");
            runItem.className = `run-item ${selectedRunId === run.id ? 'active' : ''}`;
            runItem.dataset.runId = run.id;
            
            const dateStr = run.created_at ? new Date(run.created_at).toLocaleString() : "Unknown date";
            const statusClass = getStatusBadgeClass(run.status);
            
            runItem.innerHTML = `
                <div class="run-item-header">
                    <span class="run-item-id">${run.id.substring(0, 8)}...</span>
                    <span class="badge ${statusClass}">${run.status}</span>
                </div>
                <div class="run-item-goal">${run.goal}</div>
                <div class="run-item-date">${dateStr}</div>
            `;
            
            runItem.addEventListener("click", () => selectRun(run.id));
            runsList.appendChild(runItem);
        });
        
        // Auto-select first run if none selected
        if (!selectedRunId && runs.length > 0) {
            selectRun(runs[0].id);
        }
    } catch (err) {
        console.error(err);
        document.getElementById("runs-list").innerHTML = `<div class="empty-state text-danger">Error loading runs</div>`;
    }
}

// Select a specific run to inspect
function selectRun(runId) {
    selectedRunId = runId;
    
    // Update active highlight in runs list
    document.querySelectorAll(".run-item").forEach(item => {
        if (item.dataset.runId === runId) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
    
    // Reset/Start Polling
    if (pollingInterval) clearInterval(pollingInterval);
    pollRunData(); // Poll immediately
    pollingInterval = setInterval(pollRunData, 2000);
}

// Start a new execution goal run
async function handleStartRun(e) {
    e.preventDefault();
    const input = document.getElementById("requirement-input");
    const startBtn = document.getElementById("start-btn");
    const requirement = input.value.trim();
    
    if (!requirement) return;
    
    try {
        startBtn.disabled = true;
        startBtn.textContent = "Planning...";
        
        const response = await fetch("/api/v1/runs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ requirement })
        });
        
        if (!response.ok) throw new Error("Failed to start run");
        const data = await response.json();
        
        input.value = "";
        
        // Reload runs list and select the new run
        await loadHistoricalRuns();
        selectRun(data.run_id);
    } catch (err) {
        console.error(err);
        alert("Error starting run: " + err.message);
    } finally {
        startBtn.disabled = false;
        startBtn.textContent = "Execute Goal";
    }
}

// Poll selected run details, tasks, memory, and events
async function pollRunData() {
    if (!selectedRunId) return;
    
    try {
        const [runRes, tasksRes, memoryRes, eventsRes] = await Promise.all([
            fetch(`/api/v1/runs/${selectedRunId}`),
            fetch(`/api/v1/runs/${selectedRunId}/tasks`),
            fetch(`/api/v1/runs/${selectedRunId}/memory`),
            fetch(`/api/v1/runs/${selectedRunId}/events`)
        ]);
        
        if (!runRes.ok || !tasksRes.ok || !memoryRes.ok || !eventsRes.ok) {
            throw new Error("Failed to poll run details");
        }
        
        const run = await runRes.json();
        const tasks = await tasksRes.json();
        const memory = await memoryRes.json();
        const events = await eventsRes.json();
        
        // Update header & status card
        document.getElementById("selected-run-goal").textContent = run.goal;
        document.getElementById("selected-run-id").textContent = `Run ID: ${run.id}`;
        
        const statusBadge = document.getElementById("selected-run-status");
        statusBadge.textContent = run.status;
        statusBadge.className = `run-badge badge ${getStatusBadgeClass(run.status)}`;
        
        // Render sub-sections
        renderTasks(tasks);
        renderEvents(events);
        renderMemory(memory);
        
        // Check for pending approval tasks
        checkApprovalGate(tasks);
        
        // If run is completed, stop polling
        if (run.status === "DONE" || run.status === "FAILED") {
            clearInterval(pollingInterval);
            // Refresh runs list to show updated status
            loadHistoricalRuns();
        }
    } catch (err) {
        console.error("Polling error:", err);
    }
}

// Render the task queue sequence
function renderTasks(tasks) {
    const list = document.getElementById("tasks-list");
    if (tasks.length === 0) {
        list.innerHTML = `<div class="empty-state">No tasks created.</div>`;
        return;
    }
    
    list.innerHTML = "";
    tasks.forEach(task => {
        const node = document.createElement("div");
        node.className = "task-node";
        
        let dotColor = "var(--status-pending)";
        if (task.status === "RUNNING") dotColor = "var(--status-running)";
        else if (task.status === "DONE") dotColor = "var(--status-done)";
        else if (task.status === "PENDING_APPROVAL") dotColor = "var(--status-approval)";
        else if (task.status === "FAILED") dotColor = "var(--status-failed)";
        else if (task.status === "BLOCKED") dotColor = "var(--status-blocked)";
        
        const badgeClass = getStatusBadgeClass(task.status);
        
        node.innerHTML = `
            <div class="task-node-status-dot" style="background-color: ${dotColor}; box-shadow: 0 0 8px ${dotColor}"></div>
            <div class="task-node-info">
                <div class="task-node-header">
                    <span class="task-node-title">${task.title}</span>
                    <span class="task-node-owner">${task.owner}</span>
                </div>
                <div class="task-node-desc">${task.description}</div>
            </div>
            <span class="badge ${badgeClass}" style="margin-left: 12px; font-size: 8px;">${task.status}</span>
        `;
        list.appendChild(node);
    });
}

// Render recent events
function renderEvents(events) {
    const log = document.getElementById("events-log");
    if (events.length === 0) {
        log.innerHTML = `<div class="empty-state">No events logged yet.</div>`;
        return;
    }
    
    log.innerHTML = "";
    events.forEach(e => {
        const line = document.createElement("div");
        line.className = "event-line";
        
        const dateStr = e.created_at ? new Date(e.created_at).toLocaleTimeString() : "";
        
        line.innerHTML = `
            <span class="event-time">[${dateStr}]</span>
            <span class="event-type">${e.type}</span>
            <span class="event-source">(${e.source})</span>
        `;
        log.appendChild(line);
    });
}

// Render shared memory records
function renderMemory(memory) {
    const list = document.getElementById("memory-list");
    if (memory.length === 0) {
        list.innerHTML = `<div class="empty-state">No shared memory entries.</div>`;
        return;
    }
    
    list.innerHTML = "";
    memory.forEach(mem => {
        const card = document.createElement("div");
        card.className = "memory-card";
        
        let valueText = "";
        try {
            valueText = typeof mem.value === 'object' ? JSON.stringify(mem.value, null, 2) : mem.value;
        } catch (e) {
            valueText = mem.value;
        }
        
        card.innerHTML = `
            <div class="memory-card-header">
                <span class="memory-card-key">${mem.key}</span>
                <span class="memory-card-type">${mem.type}</span>
            </div>
            <pre class="memory-card-val"><code>${valueText}</code></pre>
        `;
        list.appendChild(card);
    });
}

// Check if there is an approval gate pending review
async function checkApprovalGate(tasks) {
    const approvalTask = tasks.find(t => t.status === "PENDING_APPROVAL");
    const box = document.getElementById("approval-box");
    
    if (!approvalTask) {
        box.style.display = "none";
        return;
    }
    
    // Prevent reloading patch if already showing for this task
    if (box.dataset.taskId === approvalTask.id && box.style.display !== "none") {
        return;
    }
    
    box.dataset.taskId = approvalTask.id;
    document.getElementById("approval-task-id").textContent = approvalTask.id;
    
    try {
        const res = await fetch(`/api/v1/tasks/${approvalTask.id}/patch`);
        if (!res.ok) throw new Error("Patch file not found");
        const patchData = await res.json();
        
        document.getElementById("approval-file-path").textContent = patchData.path;
        
        // Highlight patch content lines
        const highlighted = colorizeDiff(patchData.content);
        document.getElementById("patch-content-area").innerHTML = highlighted;
        
        box.style.display = "flex";
    } catch (e) {
        console.error("Error fetching approval patch:", e);
        box.style.display = "none";
    }
}

// Colorize unified diff formatting
function colorizeDiff(text) {
    const lines = text.split("\n");
    return lines.map(line => {
        const escaped = escapeHtml(line);
        if (line.startsWith("+") && !line.startsWith("+++")) {
            return `<span class="diff-added">${escaped}</span>`;
        } else if (line.startsWith("-") && !line.startsWith("---")) {
            return `<span class="diff-removed">${escaped}</span>`;
        } else if (line.startsWith("@@")) {
            return `<span class="diff-location">${escaped}</span>`;
        } else if (line.startsWith("---") || line.startsWith("+++")) {
            return `<span class="diff-header">${escaped}</span>`;
        }
        return escaped;
    }).join("\n");
}

// Helper to escape HTML tags
function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Action: Approve proposed patch
async function handleApproveTask() {
    const box = document.getElementById("approval-box");
    const taskId = box.dataset.taskId;
    const approveBtn = document.getElementById("btn-approve");
    
    if (!taskId) return;
    
    try {
        approveBtn.disabled = true;
        approveBtn.textContent = "Applying...";
        
        const response = await fetch(`/api/v1/tasks/${taskId}/approve`, {
            method: "POST"
        });
        
        if (!response.ok) throw new Error("Failed to approve task");
        
        box.style.display = "none";
        alert("Patch applied successfully! Resuming tasks execution loop.");
        
        // Re-enable polling immediately
        if (pollingInterval) clearInterval(pollingInterval);
        pollRunData();
        pollingInterval = setInterval(pollRunData, 2000);
        
    } catch (err) {
        console.error(err);
        alert("Approval failed: " + err.message);
    } finally {
        approveBtn.disabled = false;
        approveBtn.textContent = "Approve & Apply Patch";
    }
}

// Helper to map status to badge class
function getStatusBadgeClass(status) {
    switch (status) {
        case "PENDING": return "badge-pending";
        case "PLANNED": return "badge-planned";
        case "RUNNING": return "badge-running";
        case "PENDING_APPROVAL": return "badge-approval";
        case "DONE": return "badge-done";
        case "FAILED": return "badge-failed";
        case "BLOCKED": return "badge-blocked";
        default: return "badge-pending";
    }
}

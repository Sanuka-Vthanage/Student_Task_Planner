const BACKEND_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
  ? window.location.origin
  : "https://student-task-planner-api.onrender.com"; 

function showDashboard() {
  document.getElementById("splashPage").style.display = "none";
  document.getElementById("app").style.display = "flex";
  document.getElementById("dashboardPage").style.display = "block";
  document.getElementById("tasksPage").style.display = "none";
  loadTasks();
}

function showTasks() {
  document.getElementById("dashboardPage").style.display = "none";
  document.getElementById("tasksPage").style.display = "block";
  loadTasks();
}

function logout() {
  location.reload();
}

async function loadTasks() {
  let tasks;
  try {
    const res = await fetch(`${BACKEND_URL}/tasks`);
    if (!res.ok) throw new Error("Failed to load tasks");
    tasks = await res.json();
  } catch (err) {
    console.error(err);
    const totalEl = document.getElementById("totalTasks");
    const pendingEl = document.getElementById("pendingTasks");
    if (totalEl) totalEl.textContent = "-";
    if (pendingEl) pendingEl.textContent = "-";
    const list = document.getElementById("taskList");
    if (list) list.innerHTML = "<li style='color:#dc2626'>Could not connect to server. Is the backend running?</li>";
    return;
  }

  const list = document.getElementById("taskList");
  if (!list) return;
  list.innerHTML = "";

  tasks.forEach(task => {
    const li = document.createElement("li");
    li.className = task.completed ? "completed-task" : "";
    
    // Create task text
    const text = document.createElement("span");
    text.textContent = task.title;
    text.style.cursor = "pointer";
    text.onclick = () => toggleTask(task.id);
    
    // Create delete button
    const delBtn = document.createElement("button");
    delBtn.textContent = "❌";
    delBtn.style.float = "right";
    delBtn.onclick = (e) => {
        e.stopPropagation();
        deleteTask(task.id);
    };

    li.appendChild(text);
    li.appendChild(delBtn);
    list.appendChild(li);
  });

  // Calculate Pending vs Done
  const pendingCount = tasks.filter(t => t.completed === 0).length;
  document.getElementById("totalTasks").textContent = tasks.length;
  document.getElementById("pendingTasks").textContent = pendingCount;
}

async function addTask() {
  const input = document.getElementById("taskInput");
  if (!input.value) return;

  await fetch(`${BACKEND_URL}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: input.value })
  });

  input.value = "";
  loadTasks();
}

async function toggleTask(id) {
  await fetch(`${BACKEND_URL}/toggle/${id}`, { method: "POST" });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${BACKEND_URL}/delete/${id}`, { method: "DELETE" });
  loadTasks();
}

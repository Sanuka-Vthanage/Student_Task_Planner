const BACKEND_URL = "https://YOUR-BACKEND-URL.onrender.com";

function showDashboard() {
  splashPage.style.display = "none";
  app.style.display = "flex";
  dashboardPage.style.display = "block";
  tasksPage.style.display = "none";
  loadTasks();
}

function showTasks() {
  dashboardPage.style.display = "none";
  tasksPage.style.display = "block";
  loadTasks();
}

function logout() {
  location.reload();
}

// -------- API --------

async function loadTasks() {
  const res = await fetch(`${BACKEND_URL}/tasks`);
  const tasks = await res.json();

  const list = document.getElementById("taskList");
  list.innerHTML = "";

  tasks.forEach(task => {
    const li = document.createElement("li");
    li.textContent = task.title;
    list.appendChild(li);
  });

  document.getElementById("totalTasks").textContent = tasks.length;
  document.getElementById("pendingTasks").textContent = tasks.length;
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

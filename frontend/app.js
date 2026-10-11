const views = document.querySelectorAll(".view");
const navButtons = document.querySelectorAll("[data-route]");
const fileInput = document.getElementById("file-input");
const dropzone = document.getElementById("dropzone");
const preview = document.getElementById("preview");
const dropCopy = document.getElementById("drop-copy");
const analyzeBtn = document.getElementById("analyze-btn");
const cameraBtn = document.getElementById("camera-btn");
const camera = document.getElementById("camera");
const canvas = document.getElementById("camera-canvas");
const statusEl = document.getElementById("status");
const resultPanel = document.getElementById("result-panel");
const serving = document.getElementById("serving");
const GOAL = 2000;

let selectedFile = null;
let lastResult = null;
let mealType = "Lunch";
let cameraStream = null;

function show(route) {
  views.forEach((view) => view.classList.toggle("active", view.id === `view-${route}`));
  if (route === "dashboard") refreshDashboard();
  if (route === "how") loadModelInfo();
}

navButtons.forEach((btn) => {
  btn.addEventListener("click", () => show(btn.dataset.route));
});

function setFile(file) {
  selectedFile = file;
  const url = URL.createObjectURL(file);
  preview.src = url;
  preview.hidden = false;
  dropCopy.hidden = true;
  analyzeBtn.disabled = false;
  resultPanel.hidden = true;
  statusEl.textContent = "Looks tasty. Hit Analyze Food.";
}

fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) setFile(file);
});

["dragenter", "dragover"].forEach((name) => {
  dropzone.addEventListener(name, (event) => {
    event.preventDefault();
    dropzone.classList.add("hot");
  });
});
["dragleave", "drop"].forEach((name) => {
  dropzone.addEventListener(name, (event) => {
    event.preventDefault();
    dropzone.classList.remove("hot");
  });
});
dropzone.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (file) setFile(file);
});

cameraBtn.addEventListener("click", async () => {
  if (cameraStream) {
    const context = canvas.getContext("2d");
    canvas.width = camera.videoWidth;
    canvas.height = camera.videoHeight;
    context.drawImage(camera, 0, 0);
    canvas.toBlob((blob) => {
      setFile(new File([blob], "capture.jpg", { type: "image/jpeg" }));
      camera.hidden = true;
      cameraStream.getTracks().forEach((track) => track.stop());
      cameraStream = null;
      cameraBtn.textContent = "Use camera";
    }, "image/jpeg", 0.92);
    return;
  }
  cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
  camera.srcObject = cameraStream;
  camera.hidden = false;
  await camera.play();
  cameraBtn.textContent = "Capture frame";
});

document.getElementById("meal-types").addEventListener("click", (event) => {
  const btn = event.target.closest("button");
  if (!btn) return;
  mealType = btn.dataset.meal;
  document.querySelectorAll("#meal-types button").forEach((el) => el.classList.toggle("on", el === btn));
});
document.querySelector('#meal-types [data-meal="Lunch"]').classList.add("on");

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  analyzeBtn.disabled = true;
  statusEl.textContent = "Preprocessing image and running the Vision Transformer…";
  const body = new FormData();
  body.append("image", selectedFile);
  try {
    const response = await fetch("/api/analyze", { method: "POST", body });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analyze failed");
    lastResult = data;
    renderResult();
    statusEl.textContent = data.vision_check
      ? "Low ViT confidence — OpenRouter vision confirmed the dish."
      : "Model prediction ready.";
  } catch (error) {
    statusEl.textContent = error.message;
  } finally {
    analyzeBtn.disabled = false;
  }
});

serving.addEventListener("input", renderResult);

function scaledNutrition() {
  const food = lastResult.nutrition;
  const multiplier = Number(serving.value);
  return {
    multiplier,
    calories: (food.calories * multiplier).toFixed(0),
    protein: (food.protein * multiplier).toFixed(1),
    carbs: (food.carbs * multiplier).toFixed(1),
    fat: (food.fat * multiplier).toFixed(1),
    fiber: (food.fiber * multiplier).toFixed(1),
  };
}

function renderResult() {
  if (!lastResult) return;
  resultPanel.hidden = false;
  const food = lastResult.nutrition;
  const pred = lastResult.prediction;
  const macros = scaledNutrition();
  document.getElementById("result-name").textContent = food.display_name;
  document.getElementById("result-category").textContent = `${food.category} · ${food.serving}`;
  document.getElementById("insight").textContent =
    lastResult.insight || "Add an OpenRouter API key to generate a short nutrition note.";
  document.getElementById("serving-label").textContent = `${macros.multiplier.toFixed(2)}×`;
  const pct = Math.round(pred.confidence * 100);
  document.getElementById("confidence-label").textContent = `${pct}%`;
  document.getElementById("ring-path").setAttribute("stroke-dasharray", `${pct}, 100`);
  document.getElementById("macros").innerHTML = [
    ["Calories", macros.calories, "kcal"],
    ["Protein", macros.protein, "g"],
    ["Carbs", macros.carbs, "g"],
    ["Fat", macros.fat, "g"],
  ]
    .map(([label, value, unit]) => `<div class="macro"><b>${value}</b><span>${label} ${unit}</span></div>`)
    .join("");
  document.getElementById("alts").innerHTML = (pred.top_predictions || [])
    .slice(1)
    .map((item) => `<li>Also considered: ${item.class_name.replaceAll("_", " ")} (${Math.round(item.confidence * 100)}%)</li>`)
    .join("");
}

document.getElementById("log-btn").addEventListener("click", async () => {
  if (!lastResult) return;
  const payload = {
    food_class: lastResult.prediction.food_class,
    meal_type: mealType,
    serving_multiplier: Number(serving.value),
    confidence: lastResult.prediction.confidence,
    insight: lastResult.insight,
    image_path: lastResult.image_path,
  };
  const response = await fetch("/api/log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    statusEl.textContent = data.error || "Could not save meal.";
    return;
  }
  statusEl.textContent = "Added to today’s log.";
  show("dashboard");
});

async function refreshDashboard() {
  const response = await fetch("/api/dashboard");
  const data = await response.json();
  const totals = data.totals;
  const calories = Math.round(totals.calories);
  document.getElementById("cal-total").textContent = calories;
  document.getElementById("cal-left").textContent = Math.max(0, GOAL - calories);
  document.getElementById("cal-fill").style.width = `${Math.min(100, (calories / GOAL) * 100)}%`;
  document.getElementById("dash-macros").innerHTML = [
    ["Protein", totals.protein, 120],
    ["Carbs", totals.carbs, 250],
    ["Fat", totals.fat, 70],
  ]
    .map(
      ([label, value, goal]) =>
        `<div class="macro"><b>${Number(value).toFixed(0)}g</b><span>${label} / ${goal}g</span>
         <div class="goal-bar"><span style="width:${Math.min(100, (value / goal) * 100)}%"></span></div></div>`
    )
    .join("");
  const byMeal = data.by_meal_type || {};
  document.getElementById("by-meal").innerHTML = ["Breakfast", "Lunch", "Dinner", "Snack"]
    .map((name) => `<div><span>${name}</span><strong>${Math.round(byMeal[name] || 0)} kcal</strong></div>`)
    .join("");
  const list = document.getElementById("meal-list");
  if (!data.meals.length) {
    list.innerHTML = "<p class='muted'>No meals yet. Snap a photo to start the log.</p>";
    return;
  }
  list.innerHTML = data.meals
    .map(
      (meal) => `<article>
        <div>
          <strong>${meal.food_name}</strong>
          <div class="muted">${meal.meal_type} · ${Math.round(meal.calories)} kcal · ${Math.round((meal.confidence || 0) * 100)}%</div>
        </div>
        <button data-id="${meal.id}">Remove</button>
      </article>`
    )
    .join("");
  list.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await fetch(`/api/log/${btn.dataset.id}`, { method: "DELETE" });
      refreshDashboard();
    });
  });
}

async function loadModelInfo() {
  try {
    const response = await fetch("/api/model");
    const data = await response.json();
    document.getElementById("model-status").textContent =
      `Live model: ${data.architecture}. Source: ${data.source}. OpenRouter ${data.openrouter_enabled ? "connected" : "not configured"}.`;
  } catch {
    document.getElementById("model-status").textContent = "Start the Flask server to load the model.";
  }
}

show("home");

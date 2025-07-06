console.log("Dashboard Admin JS Loaded!");

// Sidebar toggle untuk mobile
const sideMenu = document.querySelector("aside");
const menuBtn = document.getElementById("menu-btn");
const closeBtn = document.getElementById("close-btn");

if (menuBtn && sideMenu) {
  menuBtn.addEventListener("click", () => {
    sideMenu.classList.add("show");
  });
}

if (closeBtn && sideMenu) {
  closeBtn.addEventListener("click", () => {
    sideMenu.classList.remove("show");
  });
}

// Sidebar hide/show toggle untuk desktop
const sidebarToggle = document.getElementById("sidebar-toggle");
const container = document.querySelector(".container");

if (sidebarToggle && container && sideMenu) {
  sidebarToggle.addEventListener("click", () => {
    container.classList.toggle("sidebar-hidden");
    sideMenu.classList.toggle("hidden");
    
    // Update icon based on state
    const icon = sidebarToggle.querySelector("span");
    if (sideMenu.classList.contains("hidden")) {
      icon.textContent = "menu";
    } else {
      icon.textContent = "menu_open";
    }
  });
}

// Dark mode toggle
const darkMode = document.querySelector(".dark-mode");
if (darkMode) {
  darkMode.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode-variables");
    darkMode.querySelector("span:nth-child(1)").classList.toggle("active");
    darkMode.querySelector("span:nth-child(2)").classList.toggle("active");
  });
}

// Close sidebar when clicking outside (for mobile)
document.addEventListener("click", (e) => {
  if (window.innerWidth <= 992) {
    const sidebar = document.querySelector("aside");
    const menuBtn = document.getElementById("menu-btn");
    const closeBtn = document.getElementById("close-btn");

    if (sidebar && sidebar.classList.contains("show")) {
      if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove("show");
      }
    }
  }
});

// SPA navigation
const menuLinks = document.querySelectorAll(".menu-link");
const contentSections = document.querySelectorAll(".content-section");

menuLinks.forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();

    menuLinks.forEach((link) => link.classList.remove("active"));
    link.classList.add("active");

    contentSections.forEach((sec) => sec.classList.remove("active"));
    const targetId = link.getAttribute("data-target");
    document.getElementById(targetId).classList.add("active");
  });
});

// -------------------------
// Visualisasi Chart Logic
// -------------------------

let mainChart;

const updateChartBtn = document.getElementById("updateChart");
if (updateChartBtn) {
  updateChartBtn.addEventListener("click", () => {
    const ctx = document.getElementById("mainChart").getContext("2d");
    const chartType = document.getElementById("chartType").value;
    const groupBy = document.getElementById("groupBy").value;
    const metric = document.getElementById("metric").value;

    if (mainChart) mainChart.destroy();

    // TODO: Implement real data fetching from API
    console.log(`Chart Updated: ${chartType} by ${groupBy} - ${metric}`);
  });
}

// -------------------------
// Prediksi Harga Logic
// -------------------------

const predictionForm = document.getElementById("predictionForm");
if (predictionForm) {
  const resultContainer = document.getElementById("predictionResult");

  predictionForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const land = predictionForm.land_area.value;
    const building = predictionForm.building_area.value;

    if (!land || !building) return;

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ land_area: land, building_area: building }),
      });

      const data = await response.json();

      resultContainer.innerHTML = `
        <div class="alert alert-success">
          <strong>Hasil Prediksi:</strong> Rp ${parseInt(
            data.prediction
          ).toLocaleString()}
        </div>
      `;
    } catch (err) {
      console.error(err);
      resultContainer.innerHTML = `
        <div class="alert alert-danger">
          Terjadi kesalahan memproses prediksi.
        </div>
      `;
    }
  });
}

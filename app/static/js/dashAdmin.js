console.log("Dashboard Admin JS Loaded!");

const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const darkMode = document.querySelector('.dark-mode');

menuBtn.addEventListener('click', () => {
  sideMenu.classList.add('show');
});

closeBtn.addEventListener('click', () => {
  sideMenu.classList.remove('show');
});

darkMode.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode-variables');
  darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
  darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
});

// Single Page Navigation
const menuLinks = document.querySelectorAll('.menu-link');
const contentSections = document.querySelectorAll('.content-section');

menuLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    menuLinks.forEach(link => link.classList.remove('active'));
    link.classList.add('active');
    contentSections.forEach(sec => sec.classList.remove('active'));
    const target = link.getAttribute('data-target');
    document.getElementById(target).classList.add('active');
  });
});

// Prediction Functions
function openPredictionPage() {
  window.open('/admin/prediction', '_blank');
}

async function trainModels() {
  const btn = event.target;
  const originalText = btn.innerHTML;
  
  // Show loading
  btn.innerHTML = '<span class="material-icons-sharp">hourglass_empty</span> Training...';
  btn.disabled = true;
  
  try {
    const response = await fetch('/api/train-models', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    const result = await response.json();
    
    if (result.success) {
      alert('Models berhasil ditraining!');
      loadModelStatus(); // Refresh status
    } else {
      alert('Error: ' + (result.error || 'Unknown error'));
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Terjadi kesalahan saat training models');
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
}

async function loadModelStatus() {
  const statusDiv = document.getElementById('modelStatus');
  
  try {
    const response = await fetch('/api/model-performance');
    const result = await response.json();
    
    let statusHTML = '<h3>Status Model</h3>';
    
    if (result.models_loaded) {
      statusHTML += '<div class="model-list">';
      Object.keys(result.performance_data).forEach(modelName => {
        statusHTML += `
          <div class="model-status-item status-success">
            <span class="material-icons-sharp">check_circle</span>
            <span>${modelName} - Ready</span>
          </div>
        `;
      });
      statusHTML += '</div>';
    } else {
      statusHTML += `
        <div class="model-status-item status-error">
          <span class="material-icons-sharp">error</span>
          <span>No models loaded. Please train models first.</span>
        </div>
      `;
    }
    
    statusDiv.innerHTML = statusHTML;
  } catch (error) {
    console.error('Error loading model status:', error);
    statusDiv.innerHTML = `
      <h3>Status Model</h3>
      <div class="model-status-item status-error">
        <span class="material-icons-sharp">error</span>
        <span>Error loading model status</span>
      </div>
    `;
  }
}

// Load model status when prediksi section is activated
document.addEventListener('DOMContentLoaded', function() {
  // Initial load of model status
  setTimeout(loadModelStatus, 1000);
  
  // Reload status when prediksi section is shown
  const prediksiLink = document.querySelector('[data-target="prediksi"]');
  if (prediksiLink) {
    prediksiLink.addEventListener('click', function() {
      setTimeout(loadModelStatus, 500);
    });
  }
});

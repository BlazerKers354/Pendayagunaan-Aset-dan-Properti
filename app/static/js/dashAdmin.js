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

// CRUD Properties Management
let currentPropertiesPage = 1;
let currentProperties = [];
let totalPropertiesPages = 1;

// Property Modal Functions
function openAddPropertyModal() {
  document.getElementById('modalTitle').textContent = 'Tambah Properti Baru';
  document.getElementById('propertyForm').reset();
  document.getElementById('propertyId').value = '';
  document.getElementById('propertyModal').style.display = 'block';
  toggleBuildingFields();
}

function openEditPropertyModal(propertyId) {
  document.getElementById('modalTitle').textContent = 'Edit Properti';
  // Load property data and populate form
  loadPropertyForEdit(propertyId);
  document.getElementById('propertyModal').style.display = 'block';
}

function closePropertyModal() {
  document.getElementById('propertyModal').style.display = 'none';
}

// Toggle building-specific fields based on property type
function toggleBuildingFields() {
  const propertyType = document.getElementById('property_type').value;
  const buildingFields = document.querySelectorAll('.building-fields');
  const buildingField = document.querySelectorAll('.building-field');
  
  if (propertyType === 'tanah_bangunan') {
    buildingFields.forEach(field => field.classList.add('show'));
    buildingField.forEach(field => field.classList.add('show'));
  } else {
    buildingFields.forEach(field => field.classList.remove('show'));
    buildingField.forEach(field => field.classList.remove('show'));
  }
}

// Load properties with filters and pagination
async function loadProperties(page = 1) {
  const loadingDiv = document.getElementById('loadingProperties');
  const tableBody = document.getElementById('propertiesTableBody');
  const noDataDiv = document.getElementById('noProperties');
  
  loadingDiv.style.display = 'block';
  tableBody.style.display = 'none';
  noDataDiv.style.display = 'none';
  
  try {
    const propertyType = document.getElementById('filterPropertyType').value;
    const status = document.getElementById('filterStatus').value;
    
    const params = new URLSearchParams({
      page: page,
      per_page: 10
    });
    
    if (propertyType) params.append('property_type', propertyType);
    if (status) params.append('status', status);
    
    const response = await fetch(`/api/admin/properties?${params}`);
    const data = await response.json();
    
    console.log('API Response:', data); // Debug log
    console.log('Properties received:', data.properties); // Debug log
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    currentProperties = data.properties;
    currentPropertiesPage = data.page;
    totalPropertiesPages = data.total_pages;
    
    displayProperties(data.properties);
    generatePropertiesPagination(data.total_pages, data.page);
    
    loadingDiv.style.display = 'none';
    
  } catch (error) {
    console.error('Error loading properties:', error);
    loadingDiv.style.display = 'none';
    noDataDiv.style.display = 'block';
  }
}

// Display properties in table
function displayProperties(properties) {
  const tableBody = document.getElementById('propertiesTableBody');
  
  console.log('displayProperties called with:', properties); // Debug
  console.log('Properties length:', properties.length); // Debug
  
  if (properties.length === 0) {
    document.getElementById('noProperties').style.display = 'block';
    tableBody.style.display = 'none';
    return;
  }
  
  tableBody.innerHTML = '';
  
  properties.forEach(property => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${property.id}</td>
      <td>${property.title}</td>
      <td>${property.location}</td>
      <td><span class="property-type-badge">${property.property_type === 'tanah' ? 'Tanah' : 'Tanah + Bangunan'}</span></td>
      <td>Rp ${property.price.toLocaleString()}</td>
      <td>${property.land_area.toLocaleString()} m²</td>
      <td><span class="status-badge ${property.status}">${property.status === 'aktif' ? 'Aktif' : 'Tidak Aktif'}</span></td>
      <td>
        <div class="action-buttons">
          <button onclick="openEditPropertyModal(${property.id})" class="edit-btn">
            <span class="material-icons-sharp">edit</span>
            Edit
          </button>
          <button onclick="deleteProperty(${property.id})" class="delete-btn">
            <span class="material-icons-sharp">delete</span>
            Hapus
          </button>
        </div>
      </td>
    `;
    tableBody.appendChild(row);
  });
  
  tableBody.style.display = 'table-row-group';
}

// Generate pagination for properties
function generatePropertiesPagination(totalPages, currentPage) {
  const pagination = document.getElementById('propertiesPagination');
  
  if (totalPages <= 1) {
    pagination.innerHTML = '';
    return;
  }
  
  let paginationHTML = '';
  
  // Previous button
  paginationHTML += `
    <button onclick="loadProperties(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
      <span class="material-icons-sharp">chevron_left</span>
    </button>
  `;
  
  // Page numbers
  const startPage = Math.max(1, currentPage - 2);
  const endPage = Math.min(totalPages, currentPage + 2);
  
  for (let i = startPage; i <= endPage; i++) {
    paginationHTML += `
      <button onclick="loadProperties(${i})" ${currentPage === i ? 'class="active"' : ''}>
        ${i}
      </button>
    `;
  }
  
  // Next button
  paginationHTML += `
    <button onclick="loadProperties(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
      <span class="material-icons-sharp">chevron_right</span>
    </button>
  `;
  
  pagination.innerHTML = paginationHTML;
}

// Filter properties
function filterProperties() {
  loadProperties(1);
}

// Property form submission
document.addEventListener('DOMContentLoaded', function() {
  const propertyForm = document.getElementById('propertyForm');
  if (propertyForm) {
    propertyForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const formData = new FormData(this);
      const data = Object.fromEntries(formData);
      
      const isEdit = data.property_id && data.property_id !== '';
      const url = isEdit ? `/api/admin/properties/${data.property_id}` : '/api/admin/properties';
      const method = isEdit ? 'PUT' : 'POST';
      
      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.error) {
          alert('Error: ' + result.error);
          return;
        }
        
        alert(isEdit ? 'Properti berhasil diupdate!' : 'Properti berhasil ditambahkan!');
        closePropertyModal();
        loadProperties(currentPropertiesPage);
        
      } catch (error) {
        console.error('Error saving property:', error);
        alert('Terjadi kesalahan saat menyimpan properti');
      }
    });
  }
  
  // Load properties when manajemen-aset section is activated
  const manajemenLink = document.querySelector('[data-target="manajemen-aset"]');
  if (manajemenLink) {
    manajemenLink.addEventListener('click', function() {
      setTimeout(() => {
        loadProperties(1);
      }, 100);
    });
  }
  
  // Close modal when clicking outside
  window.addEventListener('click', function(event) {
    const modal = document.getElementById('propertyModal');
    if (event.target === modal) {
      closePropertyModal();
    }
  });
});

// Load property for editing
async function loadPropertyForEdit(propertyId) {
  try {
    const response = await fetch(`/api/admin/properties/${propertyId}`);
    const property = await response.json();
    
    if (property.error) {
      alert('Error loading property: ' + property.error);
      return;
    }
    
    // Populate form with property data
    document.getElementById('propertyId').value = property.id;
    document.getElementById('title').value = property.title;
    document.getElementById('property_type').value = property.property_type;
    document.getElementById('location').value = property.location;
    document.getElementById('price').value = property.price;
    document.getElementById('land_area').value = property.land_area;
    document.getElementById('building_area').value = property.building_area || '';
    document.getElementById('bedrooms').value = property.bedrooms || '';
    document.getElementById('bathrooms').value = property.bathrooms || '';
    document.getElementById('floors').value = property.floors || 1;
    document.getElementById('certificate').value = property.certificate || '';
    document.getElementById('condition_property').value = property.condition_property || '';
    document.getElementById('facing').value = property.facing || '';
    document.getElementById('water_source').value = property.water_source || '';
    document.getElementById('internet').value = property.internet || 'Tidak';
    document.getElementById('hook').value = property.hook || 'Tidak';
    document.getElementById('power').value = property.power || '';
    document.getElementById('dining_room').value = property.dining_room || '';
    document.getElementById('living_room').value = property.living_room || '';
    document.getElementById('furnished').value = property.furnished || '';
    document.getElementById('road_width').value = property.road_width || '';
    document.getElementById('status').value = property.status;
    document.getElementById('description').value = property.description || '';
    
    toggleBuildingFields();
    
  } catch (error) {
    console.error('Error loading property for edit:', error);
    alert('Terjadi kesalahan saat memuat data properti');
  }
}

// Delete property
async function deleteProperty(propertyId) {
  if (!confirm('Apakah Anda yakin ingin menghapus properti ini?')) {
    return;
  }
  
  try {
    console.log('Attempting to delete property ID:', propertyId); // Debug
    console.log('Current properties:', currentProperties); // Debug
    
    // Find the property in currentProperties to get its type
    const property = currentProperties.find(p => p.id === propertyId);
    if (!property) {
      console.error('Property not found in currentProperties:', propertyId); // Debug
      alert('Property not found');
      return;
    }
    
    const propertyType = property.property_type;
    console.log('Property type:', propertyType); // Debug
    console.log('Delete URL:', `/api/admin/property/${propertyType}/${propertyId}`); // Debug
    
    const response = await fetch(`/api/admin/property/${propertyType}/${propertyId}`, {
      method: 'DELETE'
    });
    
    console.log('Delete response status:', response.status); // Debug
    
    const result = await response.json();
    console.log('Delete response result:', result); // Debug
    
    if (!response.ok || result.error) {
      console.error('Delete failed:', result.error); // Debug
      alert('Error: ' + (result.error || 'Failed to delete property'));
      return;
    }
    
    alert('Properti berhasil dihapus!');
    loadProperties(currentPropertiesPage);
    
  } catch (error) {
    console.error('Error deleting property:', error);
    alert('Terjadi kesalahan saat menghapus properti');
  }
}

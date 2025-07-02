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

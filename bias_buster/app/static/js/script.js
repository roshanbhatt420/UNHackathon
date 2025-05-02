// Global JS for navigation and scroll animations
document.addEventListener('DOMContentLoaded', () => {
  // Sticky navigation bar
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('sticky');
    } else {
      navbar.classList.remove('sticky');
    }
  });

  // Intersection Observer for fade-in sections
  const faders = document.querySelectorAll('.fade-in-section');
  const appearOptions = {
    threshold: 0.1
  };

  const appearOnScroll = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('appear');
        observer.unobserve(entry.target);
      }
    });
  }, appearOptions);

  faders.forEach(fader => {
    appearOnScroll.observe(fader);
  });
  const navLinks = document.querySelectorAll('.nav-link');
  
  // Get current page path (handles all cases)
  const currentPath = window.location.pathname;
  
  // Check each link
  navLinks.forEach(link => {
    // Get absolute path of the link
    const linkPath = new URL(link.href, window.location.href).pathname;
    
    // Remove active class first (clean slate)
    link.classList.remove('active');
    
    // Special case for home page
    const isHomePage = (currentPath === '/' || currentPath === '/index.html');
    const isHomeLink = (linkPath === '/' || linkPath.endsWith('/index.html'));
    
    // Set active class if matches
    if ((linkPath === currentPath) || (isHomePage && isHomeLink)) {
      link.classList.add('active');
    }
  });


  // Mobile menu functionality
// Mobile menu functionality - Unique variable names
const fairalyzeMobileBtn = document.querySelector('.mobile-menu-btn');
const fairalyzeNavMenu = document.querySelector('.nav-links');
const fairalyzeNavbar = document.getElementById('navbar');

// Toggle mobile menu
fairalyzeMobileBtn.addEventListener('click', function() {
  document.body.classList.toggle('fairalyze-nav-active');
});

// Close menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(fairalyzeNavLink => {
  fairalyzeNavLink.addEventListener('click', () => {
    document.body.classList.remove('fairalyze-nav-active');
  });
});

// Sticky navbar functionality
window.addEventListener('scroll', function() {
  if (window.scrollY > 50) {
    fairalyzeNavbar.classList.add('sticky');
  } else {
    fairalyzeNavbar.classList.remove('sticky');
  }
});
});


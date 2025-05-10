// Global JS for navigation and scroll animations
document.addEventListener('DOMContentLoaded', () => {
  // Sticky navigation bar
  const navbar = document.getElementById('navbar');
  
  // Single scroll event handler for sticky navbar
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

  // Active nav link highlighting
  const navLinks = document.querySelectorAll('.nav-link');
  const currentPath = window.location.pathname;
  
  navLinks.forEach(link => {
    const linkPath = new URL(link.href, window.location.href).pathname;
    link.classList.remove('active');
    
    const isHomePage = (currentPath === '/' || currentPath === '/index.html');
    const isHomeLink = (linkPath === '/' || linkPath.endsWith('/index.html'));
    
    if ((linkPath === currentPath) || (isHomePage && isHomeLink)) {
      link.classList.add('active');
    }
  });

  // Mobile menu functionality
  const fairalyzeMobileBtn = document.querySelector('.mobile-menu-btn');
  
  fairalyzeMobileBtn.addEventListener('click', () => {
    document.body.classList.toggle('fairalyze-nav-active');
  });

  // Close menu when clicking on a link
  document.querySelectorAll('.nav-link').forEach(navLink => {
    navLink.addEventListener('click', () => {
      document.body.classList.remove('fairalyze-nav-active');
    });
  });

  // Form submission handling
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', () => {
      const resultSection = document.getElementById('result-section');
      if (resultSection) {
        resultSection.style.display = 'none';
      }
    });
  }

  // Format markdown tables
  const markdownTables = document.querySelectorAll('.markdown-content table');
  markdownTables.forEach(table => {
    table.classList.add('styled-table');
  });

  // Format markdown content
  formatMarkdownContent();
});

// Markdown content formatting function
function formatMarkdownContent() {
    const markdownContent = document.querySelector('.markdown-content');
    if (markdownContent) {
        // Ensure proper spacing
        markdownContent.innerHTML = markdownContent.innerHTML
            .replace(/\n\n/g, '<br><br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
}
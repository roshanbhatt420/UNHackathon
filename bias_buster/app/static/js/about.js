document.addEventListener('DOMContentLoaded', () => {
  // Hover effect
  const cards = document.querySelectorAll('.team-card');

  cards.forEach(card => {
    card.addEventListener('mouseenter', () => card.classList.add('scale-up'));
    card.addEventListener('mouseleave', () => card.classList.remove('scale-up'));
  });

  // Scroll animation for the entire team section
  const teamSection = document.querySelector('#team');
  if (teamSection) {
    const options = { root: null, threshold: 0.1 };
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Add class to start fade/slide animation
          entry.target.classList.add('fade-in');
          obs.unobserve(entry.target);
        }
      });
    }, options);
    observer.observe(teamSection);
  }
});

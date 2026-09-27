const menuBtn = document.getElementById('menu-btn');
const navLinks = document.getElementById('nav-links');

menuBtn.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

document.addEventListener('DOMContentLoaded', function() {
  // Use event delegation for filter button
  document.body.addEventListener('click', function(e) {
    const filterBtn = e.target.closest('.filter-btn');
    const modal = document.getElementById('filterModal');
    const closeModal = document.getElementById('closeFilterModal');
    if (filterBtn && modal && closeModal) {
      console.log('Filter button clicked');
      modal.style.display = 'flex';
      document.body.classList.add('body-modal-open');
      setTimeout(() => modal.classList.add('show'), 10);
    }
    if (e.target === closeModal || e.target === modal) {
      modal.classList.remove('show');
      setTimeout(() => {
        modal.style.display = 'none';
        document.body.classList.remove('body-modal-open');
      }, 400);
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('trailNameSearchInput');

  if (input) {
    const searchUrl = input.getAttribute('data-search-url');

    input.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        const query = input.value;
        if (query !== "" && searchUrl) {
          const url = new URL(searchUrl, window.location.origin);
          url.searchParams.append("trailName", query);
          window.location.href = url.toString(); // Redirect
        }
      }
    });
  }
});

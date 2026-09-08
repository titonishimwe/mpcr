/**
 * MPCR (Movement for Christ in Rwanda) - Main Interactive Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // Hero background slideshow
  const heroSlides = document.querySelectorAll('.hero-slide');
  if (heroSlides.length > 1) {
    let currentSlide = 0;
    window.setInterval(() => {
      heroSlides[currentSlide].classList.remove('is-active');
      currentSlide = (currentSlide + 1) % heroSlides.length;
      heroSlides[currentSlide].classList.add('is-active');
    }, 5000);
  }

  // Team member slider — one page of cards at a time when there are more than fit
  const teamSlider = document.querySelector('[data-team-slider]');
  if (teamSlider) {
    const viewport = teamSlider.querySelector('[data-team-viewport]');
    const track = teamSlider.querySelector('[data-team-track]');
    const prevBtn = teamSlider.querySelector('[data-team-prev]');
    const nextBtn = teamSlider.querySelector('[data-team-next]');
    const cards = Array.from(track.children);
    let index = 0;

    const visibleCount = () => {
      const width = viewport.clientWidth;
      if (width <= 768) return 1;
      if (width <= 1024) return 2;
      return 3;
    };

    const update = () => {
      const visible = visibleCount();
      const maxIndex = Math.max(0, cards.length - visible);
      index = Math.min(index, maxIndex);
      const canSlide = cards.length > visible;
      teamSlider.classList.toggle('is-static', !canSlide);

      if (!canSlide || cards.length === 0) {
        track.style.transform = 'translateX(0)';
        prevBtn.hidden = true;
        nextBtn.hidden = true;
        return;
      }

      const gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 0;
      const cardWidth = cards[0].getBoundingClientRect().width + gap;
      track.style.transform = `translateX(-${index * cardWidth}px)`;
      prevBtn.hidden = index <= 0;
      nextBtn.hidden = index >= maxIndex;
    };

    prevBtn.addEventListener('click', () => {
      index = Math.max(0, index - 1);
      update();
    });

    nextBtn.addEventListener('click', () => {
      const maxIndex = Math.max(0, cards.length - visibleCount());
      index = Math.min(maxIndex, index + 1);
      update();
    });

    let touchStartX = 0;
    viewport.addEventListener('touchstart', (event) => {
      touchStartX = event.changedTouches[0].clientX;
    }, { passive: true });

    viewport.addEventListener('touchend', (event) => {
      const delta = event.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) < 40) return;
      if (delta < 0) nextBtn.click();
      else prevBtn.click();
    }, { passive: true });

    window.addEventListener('resize', update);
    update();
  }

  // 1. Mobile Menu Navigation Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('show');
      const isExpanded = navMenu.classList.contains('show');
      mobileToggle.setAttribute('aria-expanded', isExpanded);
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
        navMenu.classList.remove('show');
        mobileToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 2. Lightbox Modal for Gallery Photos
  const modalOverlay = document.getElementById('galleryModal');
  const modalImg = document.getElementById('modalImage');
  const modalTitle = document.getElementById('modalTitle');
  const modalCaption = document.getElementById('modalCaption');
  const modalLocation = document.getElementById('modalLocation');
  const modalClose = document.getElementById('modalClose');

  const galleryItems = document.querySelectorAll('.gallery-item');
  if (galleryItems.length > 0 && modalOverlay) {
    galleryItems.forEach(item => {
      item.addEventListener('click', () => {
        const imgSrc = item.getAttribute('data-img');
        const title = item.getAttribute('data-title') || '';
        const caption = item.getAttribute('data-caption') || '';
        const loc = item.getAttribute('data-location') || '';

        if (modalImg) modalImg.src = imgSrc;
        if (modalTitle) modalTitle.textContent = title;
        if (modalCaption) modalCaption.textContent = caption;
        if (modalLocation) modalLocation.textContent = loc;

        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
      });
    });

    const closeModal = () => {
      modalOverlay.classList.remove('active');
      document.body.style.overflow = '';
    };

    if (modalClose) {
      modalClose.addEventListener('click', closeModal);
    }

    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        closeModal();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
        closeModal();
      }
    });
  }

  // 3. Auto-dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
      });
    }, 6000);
  }
});

/**
 * LuxeMart - Main JavaScript
 * Handles: Dark Mode, Cart, Animations, Chatbot, Search, Toast Notifications
 */

// ============ DARK MODE ============
const ThemeManager = {
  init() {
    const saved = localStorage.getItem('luxe-theme') || 'light';
    this.apply(saved);
    document.getElementById('themeToggle')?.addEventListener('click', () => this.toggle());
  },
  apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('luxe-theme', theme);
  },
  toggle() {
    const current = document.documentElement.getAttribute('data-theme');
    this.apply(current === 'dark' ? 'light' : 'dark');
  }
};

// ============ NAVBAR ============
const NavbarManager = {
  init() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });

    // Mobile menu
    const btn = document.getElementById('mobileMenuBtn');
    const menu = document.getElementById('mobileMenu');
    const closeBtn = document.getElementById('mobileMenuClose');

    btn?.addEventListener('click', () => {
      menu?.classList.add('open');
      document.body.style.overflow = 'hidden';
    });

    const closeMenu = () => {
      menu?.classList.remove('open');
      document.body.style.overflow = '';
    };

    closeBtn?.addEventListener('click', closeMenu);
    menu?.addEventListener('click', (e) => { if (e.target === menu) closeMenu(); });
  }
};

// ============ HERO SLIDER ============
const HeroSlider = {
  current: 0,
  slides: [],
  dots: [],
  interval: null,

  init() {
    this.slides = [...document.querySelectorAll('.hero-slide')];
    this.dots = [...document.querySelectorAll('.hero-dot')];
    if (this.slides.length < 2) return;

    this.dots.forEach((dot, i) => dot.addEventListener('click', () => this.goTo(i)));

    this.start();
    document.querySelector('.hero-section')?.addEventListener('mouseenter', () => this.pause());
    document.querySelector('.hero-section')?.addEventListener('mouseleave', () => this.start());
  },

  goTo(index) {
    this.slides[this.current]?.classList.remove('active');
    this.dots[this.current]?.classList.remove('active');
    this.current = (index + this.slides.length) % this.slides.length;
    this.slides[this.current]?.classList.add('active');
    this.dots[this.current]?.classList.add('active');
  },

  next() { this.goTo(this.current + 1); },
  start() { this.interval = setInterval(() => this.next(), 5000); },
  pause() { clearInterval(this.interval); }
};

// ============ SCROLL ANIMATIONS ============
const ScrollAnimator = {
  init() {
    const observer = new IntersectionObserver(
      (entries) => entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      }),
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );
    document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));
  }
};

// ============ TOAST NOTIFICATIONS ============
const Toast = {
  container: null,

  init() {
    this.container = document.getElementById('alertContainer');
  },

  show(message, type = 'success', duration = 4000) {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'alert-container';
      this.container.id = 'alertContainer';
      document.body.appendChild(this.container);
    }

    const icons = { success: 'bi-check-circle-fill', error: 'bi-x-circle-fill', warning: 'bi-exclamation-triangle-fill', info: 'bi-info-circle-fill' };
    const titles = { success: 'Success', error: 'Error', warning: 'Warning', info: 'Info' };

    const toast = document.createElement('div');
    toast.className = `alert-toast toast-${type}`;
    toast.innerHTML = `
      <div class="toast-icon"><i class="bi ${icons[type] || icons.info}"></i></div>
      <div class="toast-body">
        <div class="toast-title">${titles[type] || 'Notice'}</div>
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close" onclick="this.closest('.alert-toast').remove()">
        <i class="bi bi-x"></i>
      </button>
    `;

    this.container.appendChild(toast);
    setTimeout(() => toast.remove(), duration);
  }
};

// ============ CART ============
const CartManager = {
  sidebarOpen: false,

  init() {
    document.getElementById('cartToggleBtn')?.addEventListener('click', () => this.open());
    document.getElementById('cartOverlay')?.addEventListener('click', () => this.close());
    document.getElementById('cartCloseBtn')?.addEventListener('click', () => this.close());

    // Add to cart buttons
    document.querySelectorAll('[data-add-cart]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const productId = btn.dataset.addCart;
        const form = btn.closest('form') || document.querySelector(`#addCartForm-${productId}`);
        if (form) {
          this.addToCart(form);
        }
      });
    });
  },

  async addToCart(form) {
    const formData = new FormData(form);
    const url = form.action;

    try {
      const res = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') }
      });
      const data = await res.json();
      if (data.success) {
        this.updateCount(data.cart_count);
        Toast.show(data.message, 'success');
      }
    } catch (e) {
      Toast.show('Failed to add to cart. Please try again.', 'error');
    }
  },

  updateCount(count) {
    document.querySelectorAll('.cart-count-badge').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
      el.animate([{transform: 'scale(1.5)'}, {transform: 'scale(1)'}], {duration: 300, easing: 'cubic-bezier(0.34,1.56,0.64,1)'});
    });
  },

  open() {
    document.getElementById('cartSidebar')?.classList.add('open');
    document.getElementById('cartOverlay')?.classList.add('open');
    document.body.style.overflow = 'hidden';
  },

  close() {
    document.getElementById('cartSidebar')?.classList.remove('open');
    document.getElementById('cartOverlay')?.classList.remove('open');
    document.body.style.overflow = '';
  }
};

// ============ WISHLIST ============
const WishlistManager = {
  init() {
    document.querySelectorAll('[data-wishlist]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const productId = btn.dataset.wishlist;
        try {
          const res = await fetch(`/wishlist/toggle/${productId}/`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') }
          });
          const data = await res.json();
          btn.classList.toggle('wishlisted', data.added);
          Toast.show(data.message, data.added ? 'success' : 'info');
          // Update count
          document.querySelectorAll('.wishlist-count-badge').forEach(el => {
            el.textContent = data.count;
          });
        } catch (e) {
          Toast.show('Please login to use wishlist', 'warning');
        }
      });
    });
  }
};

// ============ NEWSLETTER ============
const NewsletterManager = {
  init() {
    document.querySelectorAll('.newsletter-form').forEach(form => {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = form.querySelector('input[type="email"]').value;
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        btn.textContent = 'Subscribing...';
        btn.disabled = true;

        try {
          const formData = new FormData();
          formData.append('email', email);
          formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

          const res = await fetch('/users/newsletter/subscribe/', {
            method: 'POST',
            body: formData
          });
          const data = await res.json();
          Toast.show(data.message, data.success ? 'success' : 'info');
          if (data.success) form.reset();
        } catch (e) {
          Toast.show('Something went wrong. Please try again.', 'error');
        } finally {
          btn.textContent = originalText;
          btn.disabled = false;
        }
      });
    });
  }
};

// ============ CHATBOT ============
const Chatbot = {
  isOpen: false,
  responses: {
    default: "I'm here to help! Ask me about products, orders, or shipping.",
    hello: "Hello! Welcome to LuxeMart! 👋 How can I help you today?",
    order: "To track your order, visit the Order Tracking page or check your email for updates.",
    shipping: "We offer free shipping on orders over $75! Standard shipping takes 3-5 business days.",
    return: "We have a 30-day hassle-free return policy. Visit your account to initiate a return.",
    payment: "We accept Visa, Mastercard, American Express, and PayPal.",
    discount: "Sign up for our newsletter to get 10% off your first order! 🎉",
    help: "I can help with: orders, shipping, returns, payments, or product info. What do you need?",
  },

  init() {
    document.getElementById('chatbotBtn')?.addEventListener('click', () => this.toggle());
    document.getElementById('chatClose')?.addEventListener('click', () => this.close());
    document.getElementById('chatSendBtn')?.addEventListener('click', () => this.sendMessage());
    document.getElementById('chatInput')?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });
  },

  toggle() {
    this.isOpen ? this.close() : this.open();
  },

  open() {
    document.getElementById('chatbotWindow')?.classList.add('open');
    this.isOpen = true;
    document.getElementById('chatInput')?.focus();
  },

  close() {
    document.getElementById('chatbotWindow')?.classList.remove('open');
    this.isOpen = false;
  },

  sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input?.value.trim();
    if (!text) return;

    this.addMessage(text, 'user');
    input.value = '';

    setTimeout(() => {
      const response = this.getResponse(text.toLowerCase());
      this.addMessage(response, 'bot');
    }, 600);
  },

  getResponse(text) {
    for (const [key, val] of Object.entries(this.responses)) {
      if (key !== 'default' && text.includes(key)) return val;
    }
    return this.responses.default;
  },

  addMessage(text, sender) {
    const messages = document.getElementById('chatMessages');
    if (!messages) return;
    const div = document.createElement('div');
    div.className = `chat-msg ${sender}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }
};

// ============ PRODUCT IMAGE ZOOM ============
const ImageZoom = {
  init() {
    const mainImg = document.getElementById('productMainImage');
    if (!mainImg) return;

    mainImg.addEventListener('mousemove', (e) => {
      const rect = mainImg.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      mainImg.style.transformOrigin = `${x}% ${y}%`;
    });

    mainImg.addEventListener('mouseenter', () => {
      mainImg.style.transform = 'scale(1.4)';
    });

    mainImg.addEventListener('mouseleave', () => {
      mainImg.style.transform = 'scale(1)';
      mainImg.style.transformOrigin = 'center';
    });

    // Thumbnail switching
    document.querySelectorAll('.product-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        mainImg.src = thumb.dataset.full || thumb.src;
        document.querySelectorAll('.product-thumb').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
      });
    });
  }
};

// ============ QUANTITY CONTROL ============
const QuantityControl = {
  init() {
    document.querySelectorAll('.qty-minus').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.nextElementSibling;
        const min = parseInt(input?.min || 1);
        if (input && parseInt(input.value) > min) {
          input.value = parseInt(input.value) - 1;
          input.dispatchEvent(new Event('change'));
        }
      });
    });

    document.querySelectorAll('.qty-plus').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.previousElementSibling;
        const max = parseInt(input?.max || 99);
        if (input && parseInt(input.value) < max) {
          input.value = parseInt(input.value) + 1;
          input.dispatchEvent(new Event('change'));
        }
      });
    });
  }
};

// ============ PRICE RANGE SLIDER ============
const PriceRange = {
  init() {
    const minInput = document.getElementById('minPrice');
    const maxInput = document.getElementById('maxPrice');
    if (!minInput || !maxInput) return;

    const updateDisplay = () => {
      const minEl = document.getElementById('minPriceDisplay');
      const maxEl = document.getElementById('maxPriceDisplay');
      if (minEl) minEl.textContent = `$${minInput.value}`;
      if (maxEl) maxEl.textContent = `$${maxInput.value}`;
    };

    minInput.addEventListener('input', updateDisplay);
    maxInput.addEventListener('input', updateDisplay);
    updateDisplay();
  }
};

// ============ COUPON VALIDATION ============
const CouponManager = {
  init() {
    document.getElementById('applyCouponBtn')?.addEventListener('click', async () => {
      const code = document.getElementById('couponInput')?.value.trim().toUpperCase();
      if (!code) return;

      const formData = new FormData();
      formData.append('code', code);
      formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

      try {
        const res = await fetch('/validate-coupon/', { method: 'POST', body: formData });
        const data = await res.json();
        const msgEl = document.getElementById('couponMessage');
        if (msgEl) {
          msgEl.textContent = data.message;
          msgEl.className = `coupon-message ${data.valid ? 'valid' : 'invalid'}`;
        }
        if (data.valid) {
          document.getElementById('couponCodeHidden').value = code;
          Toast.show(data.message, 'success');
        }
      } catch (e) {
        Toast.show('Error validating coupon', 'error');
      }
    });
  }
};

// ============ SEARCH ============
const SearchManager = {
  init() {
    const searchInput = document.getElementById('navSearchInput');
    if (!searchInput) return;

    let timeout;
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        window.location.href = `/search/?q=${encodeURIComponent(searchInput.value)}`;
      }
    });
  }
};

// ============ STRIPE CHECKOUT ============
const StripeCheckout = {
  stripe: null,
  elements: null,
  card: null,

  async init() {
    const stripeKey = document.getElementById('stripePublicKey')?.value;
    if (!stripeKey || !window.Stripe) return;

    this.stripe = Stripe(stripeKey);
    this.elements = this.stripe.elements();

    this.card = this.elements.create('card', {
      style: {
        base: {
          fontFamily: '"DM Sans", sans-serif',
          fontSize: '16px',
          color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(),
          '::placeholder': { color: '#9a9a94' }
        }
      }
    });

    const cardContainer = document.getElementById('card-element');
    if (cardContainer) this.card.mount('#card-element');

    document.getElementById('checkoutForm')?.addEventListener('submit', (e) => this.handleSubmit(e));
  },

  async handleSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('submitOrderBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-arrow-repeat spin"></i> Processing...';

    try {
      const res = await fetch('/orders/create-payment-intent/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ payment_method: 'stripe' })
      });
      const { client_secret, error } = await res.json();

      if (error) throw new Error(error);

      const { paymentIntent, error: stripeError } = await this.stripe.confirmCardPayment(client_secret, {
        payment_method: { card: this.card }
      });

      if (stripeError) throw new Error(stripeError.message);

      if (paymentIntent.status === 'succeeded') {
        document.getElementById('paymentIntentId').value = paymentIntent.id;
        e.target.submit();
      }
    } catch (err) {
      Toast.show(err.message, 'error');
      btn.disabled = false;
      btn.innerHTML = 'Place Order';
    }
  }
};

// ============ UTILITY ============
function getCookie(name) {
  let value = `; ${document.cookie}`;
  let parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Number counter animation
function animateCounter(el) {
  const target = parseInt(el.dataset.target || el.textContent);
  const suffix = el.dataset.suffix || '';
  let current = 0;
  const increment = target / 60;
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      el.textContent = target.toLocaleString() + suffix;
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(current).toLocaleString() + suffix;
    }
  }, 16);
}

// Expose dismissMessage globally for inline usage
window.dismissAlert = (btn) => btn.closest('.alert-toast')?.remove();

// ============ INIT ALL ============
document.addEventListener('DOMContentLoaded', () => {
  ThemeManager.init();
  NavbarManager.init();
  HeroSlider.init();
  ScrollAnimator.init();
  Toast.init();
  CartManager.init();
  WishlistManager.init();
  NewsletterManager.init();
  Chatbot.init();
  ImageZoom.init();
  QuantityControl.init();
  PriceRange.init();
  CouponManager.init();
  SearchManager.init();
  StripeCheckout.init();

  // Animate counters
  document.querySelectorAll('.counter-animate').forEach(el => {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        animateCounter(el);
        observer.disconnect();
      }
    });
    observer.observe(el);
  });

  // Show Django messages as toasts
  document.querySelectorAll('.django-message').forEach(msg => {
    const type = msg.dataset.type || 'info';
    setTimeout(() => Toast.show(msg.textContent, type), 200);
  });
});

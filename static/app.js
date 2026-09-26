const rupees = n => `₹${n.toLocaleString('en-IN')}`;

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Request failed');
  return data;
}

function renderCart(cart) {
  document.getElementById('cart-count').textContent =
    cart.items.reduce((n, item) => n + item.qty, 0);
  document.getElementById('cart-items').innerHTML = cart.items
    .map(item => `<li>${item.name} × ${item.qty} — ${rupees(item.line_total)}</li>`)
    .join('') || '<li class="empty">Your cart is empty</li>';
  document.getElementById('subtotal').textContent = rupees(cart.subtotal);
  document.getElementById('discount').textContent = `${cart.discount_percent}%`;
  document.getElementById('total').textContent = rupees(cart.total);
}

async function loadProducts() {
  const products = await api('/api/products');
  document.getElementById('product-list').innerHTML = products.map(p => `
    <article class="product">
      <h3>${p.name}</h3>
      <p class="price">${rupees(p.price)}</p>
      <button data-add="${p.id}">Add to cart</button>
    </article>`).join('');
}

document.addEventListener('click', async event => {
  const id = event.target.dataset.add;
  if (id) renderCart(await api('/api/cart/add', { product_id: id }));
});

document.getElementById('coupon-form').addEventListener('submit', async event => {
  event.preventDefault();
  const message = document.getElementById('coupon-message');
  const code = document.getElementById('coupon-input').value;
  try {
    renderCart(await api('/api/cart/coupon', { code }));
    message.textContent = `Coupon ${code.toUpperCase()} applied`;
  } catch (err) {
    message.textContent = err.message;
  }
});

document.getElementById('checkout').addEventListener('click', () => {
  document.getElementById('checkout-message').textContent = 'Order placed! (demo)';
});

// Highlight "verified buyer" while preserving the surrounding parentheses.
const VERIFIED = /\((verified buyer)\)/g;

document.getElementById('load-reviews').addEventListener('click', async () => {
  const reviews = await api('/api/reviews');
  document.getElementById('review-list').innerHTML = reviews.map(r => `
    <li><strong>${r.author}</strong> ${'★'.repeat(r.rating)}<br>
      ${r.text.replace(VERIFIED, '(<mark>$1</mark>)')}</li>`).join('');
});

(async () => {
  await loadProducts();
  renderCart(await api('/api/cart'));
})();

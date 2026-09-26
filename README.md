# Demo Shop

A tiny storefront used as the target app for [show-dont-tell](https://github.com/yeah-ssh/show-dont-tell), an AI ticket-resolver agent built on TrueForge. Bug reports for this app are filed in Linear, and the agent reproduces them in a browser, records video proof and opens PRs here.

Standard library only; no install needed.

```bash
python3 server.py --port 5000     # http://127.0.0.1:5000
python3 -m pytest tests/           # unit tests (needs pytest)
```

## Layout
- `server.py`: static file server + JSON API (`/api/products`, `/api/cart`, `/api/cart/add`, `/api/cart/coupon`, `/api/cart/reset`, `/api/reviews`, `/healthz`)
- `cart.py`: cart and coupon logic
- `static/`: frontend (`index.html`, `styles.css`, `app.js`)
- `tests/`: pytest unit tests

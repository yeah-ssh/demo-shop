"""Demo Shop server: static frontend + small JSON API. Standard library only.

Usage: python3 server.py [--port 5000]
"""

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from cart import PRODUCTS, Cart, CouponError

STATIC_DIR = Path(__file__).parent / "static"
REVIEWS = [
    {"author": "Priya", "rating": 5, "text": "Best mug for late-night deploys. (verified buyer)"},
    {"author": "Arjun", "rating": 4, "text": "Tee fits well, washes fine. (verified buyer)"},
    {"author": "Meera", "rating": 5, "text": "Stickers are now on every laptop in the office."},
]

cart = Cart()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format, *args):  # keep repro output quiet
        pass

    def _json(self, status: int, payload) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        if self.path == "/api/products":
            return self._json(200, list(PRODUCTS.values()))
        if self.path == "/api/cart":
            return self._json(200, cart.to_dict())
        if self.path == "/api/reviews":
            return self._json(200, REVIEWS)
        if self.path == "/healthz":
            return self._json(200, {"ok": True})
        return super().do_GET()

    def do_POST(self):
        global cart
        data = self._body()
        try:
            if self.path == "/api/cart/add":
                cart.add(data["product_id"], int(data.get("qty", 1)))
            elif self.path == "/api/cart/remove":
                cart.remove(data["product_id"])
            elif self.path == "/api/cart/coupon":
                cart.apply_coupon(data.get("code", ""))
            elif self.path == "/api/cart/reset":
                cart = Cart()
            else:
                return self._json(404, {"error": "not found"})
        except CouponError as e:
            return self._json(400, {"error": str(e)})
        except (KeyError, ValueError) as e:
            return self._json(400, {"error": f"bad request: {e}"})
        return self._json(200, cart.to_dict())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Demo Shop on http://{args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

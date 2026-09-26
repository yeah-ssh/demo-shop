"""Cart and coupon logic for Demo Shop."""

from dataclasses import dataclass, field

PRODUCTS = {
    "mug": {"id": "mug", "name": "Forge Mug", "price": 450},
    "tee": {"id": "tee", "name": "Agent Tee", "price": 900},
    "cap": {"id": "cap", "name": "Sandbox Cap", "price": 600},
    "sticker": {"id": "sticker", "name": "Sticker Pack", "price": 150},
}

COUPONS = {
    "SAVE10": 10,
    "WELCOME20": 20,
}


class CouponError(ValueError):
    pass


@dataclass
class Cart:
    items: dict = field(default_factory=dict)
    discount_percent: int = 0
    applied_coupons: list = field(default_factory=list)

    def add(self, product_id: str, qty: int = 1) -> None:
        if product_id not in PRODUCTS:
            raise KeyError(product_id)
        if qty < 1:
            raise ValueError("qty must be >= 1")
        self.items[product_id] = self.items.get(product_id, 0) + qty

    def remove(self, product_id: str) -> None:
        self.items.pop(product_id, None)

    def subtotal(self) -> int:
        return sum(PRODUCTS[pid]["price"] * qty for pid, qty in self.items.items())

    def apply_coupon(self, code: str) -> int:
        code = code.strip().upper()
        if code not in COUPONS:
            raise CouponError(f"Unknown coupon: {code}")
        self.discount_percent += COUPONS[code]
        self.applied_coupons.append(code)
        return self.discount_percent

    def total(self) -> int:
        pct = min(self.discount_percent, 100)
        return round(self.subtotal() * (100 - pct) / 100)

    def to_dict(self) -> dict:
        return {
            "items": [
                {**PRODUCTS[pid], "qty": qty, "line_total": PRODUCTS[pid]["price"] * qty}
                for pid, qty in self.items.items()
            ],
            "subtotal": self.subtotal(),
            "discount_percent": self.discount_percent,
            "applied_coupons": list(self.applied_coupons),
            "total": self.total(),
        }

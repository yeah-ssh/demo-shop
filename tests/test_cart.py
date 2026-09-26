import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cart import Cart, CouponError  # noqa: E402


def test_subtotal_sums_line_items():
    cart = Cart()
    cart.add("mug", 2)
    cart.add("sticker")
    assert cart.subtotal() == 2 * 450 + 150


def test_coupon_applies_discount():
    cart = Cart()
    cart.add("tee")
    cart.apply_coupon("save10")
    assert cart.total() == 810


def test_coupon_cannot_be_applied_twice():
    cart = Cart()
    cart.add("tee")
    cart.apply_coupon("save10")
    cart.apply_coupon(" SAVE10 ")
    assert cart.discount_percent == 10
    assert cart.applied_coupons == ["SAVE10"]
    assert cart.total() == 810


def test_unknown_coupon_rejected():
    cart = Cart()
    with pytest.raises(CouponError):
        cart.apply_coupon("FREESTUFF")


def test_remove_item():
    cart = Cart()
    cart.add("cap")
    cart.remove("cap")
    assert cart.subtotal() == 0

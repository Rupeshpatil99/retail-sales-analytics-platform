"""Product data model for the retail sales analytics platform."""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Product:
    """Represents a single product in inventory.

    Attributes:
        product_id: Unique identifier for the product.
        name: Display name of the product.
        category: Product category (e.g. Electronics, Furniture).
        price: Unit price in the store's base currency.
        quantity: Current stock quantity on hand.
    """

    product_id: str
    name: str
    category: str
    price: float
    quantity: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert the product to a plain dictionary for JSON storage."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Product":
        """Build a Product instance from a dictionary (e.g. loaded from JSON).

        Args:
            data: A dictionary with keys product_id, name, category, price, quantity.

        Returns:
            A new Product instance.
        """
        return Product(
            product_id=str(data["product_id"]),
            name=str(data["name"]),
            category=str(data["category"]),
            price=float(data["price"]),
            quantity=int(data["quantity"]),
        )

    def total_value(self) -> float:
        """Return the total stock value (price * quantity) for this product."""
        return round(self.price * self.quantity, 2)

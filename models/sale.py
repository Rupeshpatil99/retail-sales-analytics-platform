"""Sale data model for the retail sales analytics platform."""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class SaleItem:
    """A single line item within a sale.

    Attributes:
        product_id: The id of the product purchased.
        product_name: The name of the product at time of sale.
        quantity: Number of units purchased.
        unit_price: Price per unit at time of sale.
    """

    product_id: str
    product_name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        """Return quantity * unit_price for this line item."""
        return round(self.quantity * self.unit_price, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the line item to a plain dictionary for JSON storage."""
        return asdict(self)


@dataclass
class Sale:
    """Represents a completed sale (bill) for a customer.

    Attributes:
        sale_id: Unique identifier for the sale.
        customer_id: The id of the customer who made the purchase.
        items: List of SaleItem line items included in this sale.
        timestamp: ISO-formatted date/time the sale was recorded.
    """

    sale_id: str
    customer_id: str
    items: List[SaleItem] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    @property
    def total_amount(self) -> float:
        """Return the total bill amount across all line items."""
        return round(sum(item.subtotal for item in self.items), 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the sale to a plain dictionary for JSON storage."""
        return {
            "sale_id": self.sale_id,
            "customer_id": self.customer_id,
            "items": [item.to_dict() for item in self.items],
            "timestamp": self.timestamp,
            "total_amount": self.total_amount,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Sale":
        """Build a Sale instance from a dictionary (e.g. loaded from JSON).

        Args:
            data: A dictionary with keys sale_id, customer_id, items, timestamp.

        Returns:
            A new Sale instance.
        """
        items = [
            SaleItem(
                product_id=str(i["product_id"]),
                product_name=str(i["product_name"]),
                quantity=int(i["quantity"]),
                unit_price=float(i["unit_price"]),
            )
            for i in data.get("items", [])
        ]
        return Sale(
            sale_id=str(data["sale_id"]),
            customer_id=str(data["customer_id"]),
            items=items,
            timestamp=str(data.get("timestamp", "")),
        )

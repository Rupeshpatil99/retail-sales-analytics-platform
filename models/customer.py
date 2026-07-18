"""Customer data model for the retail sales analytics platform."""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Customer:
    """Represents a customer record.

    Attributes:
        customer_id: Unique identifier for the customer.
        name: Full name of the customer.
        email: Contact email address.
        phone: Contact phone number.
    """

    customer_id: str
    name: str
    email: str
    phone: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the customer to a plain dictionary for JSON storage."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Customer":
        """Build a Customer instance from a dictionary (e.g. loaded from JSON).

        Args:
            data: A dictionary with keys customer_id, name, email, phone.

        Returns:
            A new Customer instance.
        """
        return Customer(
            customer_id=str(data["customer_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            phone=str(data["phone"]),
        )

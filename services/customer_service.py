"""Customer management service - CRUD operations for customers."""

from typing import List, Optional

from models.customer import Customer
from utils.file_handler import load_json, save_json
from utils.validator import (
    validate_non_empty_string,
    validate_email,
    validate_phone,
    ValidationError,
)
from utils.logger import get_logger

logger = get_logger(__name__)

CUSTOMERS_FILE = "data/customers.json"


class CustomerNotFoundError(Exception):
    """Raised when a customer lookup fails."""


class CustomerService:
    """Handles all customer CRUD operations and persistence."""

    def __init__(self, file_path: str = CUSTOMERS_FILE) -> None:
        """Initialize the service and load existing customers from disk.

        Args:
            file_path: Path to the JSON file used for persistence.
        """
        self.file_path = file_path
        self._customers: List[Customer] = self._load_customers()

    def _load_customers(self) -> List[Customer]:
        raw = load_json(self.file_path)
        return [Customer.from_dict(item) for item in raw]

    def _persist(self) -> None:
        save_json(self.file_path, [c.to_dict() for c in self._customers])

    def _find_customer(self, customer_id: str) -> Optional[Customer]:
        return next((c for c in self._customers if c.customer_id == customer_id), None)

    def add_customer(self, customer_id: str, name: str, email: str, phone: str) -> Customer:
        """Validate input and add a new customer.

        Raises:
            ValidationError: If any field is invalid or the id already exists.
        """
        customer_id = validate_non_empty_string(customer_id, "Customer ID")
        name = validate_non_empty_string(name, "Customer name")
        email = validate_email(email)
        phone = validate_phone(phone)

        if self._find_customer(customer_id) is not None:
            raise ValidationError(f"Customer ID '{customer_id}' already exists.")

        customer = Customer(customer_id, name, email, phone)
        self._customers.append(customer)
        self._persist()
        logger.info("Added customer: %s", customer_id)
        return customer

    def get_customer(self, customer_id: str) -> Customer:
        """Return a customer by id.

        Raises:
            CustomerNotFoundError: If no customer with that id exists.
        """
        customer = self._find_customer(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer '{customer_id}' not found.")
        return customer

    def list_customers(self) -> List[Customer]:
        """Return all customers."""
        return list(self._customers)

    def update_customer(self, customer_id: str, **fields) -> Customer:
        """Update one or more fields of an existing customer.

        Raises:
            CustomerNotFoundError: If the customer does not exist.
            ValidationError: If a provided field value is invalid.
        """
        customer = self.get_customer(customer_id)

        if "name" in fields:
            customer.name = validate_non_empty_string(fields["name"], "Customer name")
        if "email" in fields:
            customer.email = validate_email(fields["email"])
        if "phone" in fields:
            customer.phone = validate_phone(fields["phone"])

        self._persist()
        logger.info("Updated customer: %s", customer_id)
        return customer

    def delete_customer(self, customer_id: str) -> None:
        """Remove a customer record.

        Raises:
            CustomerNotFoundError: If the customer does not exist.
        """
        customer = self.get_customer(customer_id)
        self._customers.remove(customer)
        self._persist()
        logger.info("Deleted customer: %s", customer_id)

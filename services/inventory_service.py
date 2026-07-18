"""Inventory management service - CRUD operations for products."""

from typing import List, Optional

from models.product import Product
from utils.file_handler import load_json, save_json
from utils.validator import (
    validate_non_empty_string,
    validate_positive_number,
    validate_non_negative_int,
    ValidationError,
)
from utils.logger import get_logger

logger = get_logger(__name__)

PRODUCTS_FILE = "data/products.json"


class ProductNotFoundError(Exception):
    """Raised when a product lookup fails."""


class InsufficientStockError(Exception):
    """Raised when there isn't enough stock to fulfil a request."""


class InventoryService:
    """Handles all product/inventory CRUD operations and persistence."""

    def __init__(self, file_path: str = PRODUCTS_FILE) -> None:
        """Initialize the service and load existing products from disk.

        Args:
            file_path: Path to the JSON file used for persistence.
        """
        self.file_path = file_path
        self._products: List[Product] = self._load_products()

    def _load_products(self) -> List[Product]:
        raw = load_json(self.file_path)
        return [Product.from_dict(item) for item in raw]

    def _persist(self) -> None:
        save_json(self.file_path, [p.to_dict() for p in self._products])

    def _find_product(self, product_id: str) -> Optional[Product]:
        return next((p for p in self._products if p.product_id == product_id), None)

    def add_product(
        self, product_id: str, name: str, category: str, price: float, quantity: int
    ) -> Product:
        """Validate input and add a new product to inventory.

        Raises:
            ValidationError: If any field is invalid or the id already exists.
        """
        product_id = validate_non_empty_string(product_id, "Product ID")
        name = validate_non_empty_string(name, "Product name")
        category = validate_non_empty_string(category, "Category")
        price = validate_positive_number(price, "Price")
        quantity = validate_non_negative_int(quantity, "Quantity")

        if self._find_product(product_id) is not None:
            raise ValidationError(f"Product ID '{product_id}' already exists.")

        product = Product(product_id, name, category, price, quantity)
        self._products.append(product)
        self._persist()
        logger.info("Added product: %s", product_id)
        return product

    def get_product(self, product_id: str) -> Product:
        """Return a product by id.

        Raises:
            ProductNotFoundError: If no product with that id exists.
        """
        product = self._find_product(product_id)
        if product is None:
            raise ProductNotFoundError(f"Product '{product_id}' not found.")
        return product

    def list_products(self) -> List[Product]:
        """Return all products currently in inventory."""
        return list(self._products)

    def update_product(self, product_id: str, **fields) -> Product:
        """Update one or more fields of an existing product.

        Args:
            product_id: The id of the product to update.
            **fields: Any of name, category, price, quantity to change.

        Raises:
            ProductNotFoundError: If the product does not exist.
            ValidationError: If a provided field value is invalid.
        """
        product = self.get_product(product_id)

        if "name" in fields:
            product.name = validate_non_empty_string(fields["name"], "Product name")
        if "category" in fields:
            product.category = validate_non_empty_string(fields["category"], "Category")
        if "price" in fields:
            product.price = validate_positive_number(fields["price"], "Price")
        if "quantity" in fields:
            product.quantity = validate_non_negative_int(fields["quantity"], "Quantity")

        self._persist()
        logger.info("Updated product: %s", product_id)
        return product

    def delete_product(self, product_id: str) -> None:
        """Remove a product from inventory.

        Raises:
            ProductNotFoundError: If the product does not exist.
        """
        product = self.get_product(product_id)
        self._products.remove(product)
        self._persist()
        logger.info("Deleted product: %s", product_id)

    def reduce_stock(self, product_id: str, quantity: int) -> None:
        """Reduce stock for a product, typically called when a sale is made.

        Raises:
            ProductNotFoundError: If the product does not exist.
            InsufficientStockError: If not enough stock is available.
        """
        product = self.get_product(product_id)
        if product.quantity < quantity:
            raise InsufficientStockError(
                f"Not enough stock for '{product.name}'. "
                f"Available: {product.quantity}, requested: {quantity}."
            )
        product.quantity -= quantity
        self._persist()
        logger.info("Reduced stock for %s by %d", product_id, quantity)

    def total_inventory_value(self) -> float:
        """Return the total value of all stock currently on hand."""
        return round(sum(p.total_value() for p in self._products), 2)

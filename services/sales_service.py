"""Sales and billing service - creates sales, updates inventory, generates bills."""

import uuid
from typing import List, Dict

from models.sale import Sale, SaleItem
from services.inventory_service import InventoryService, ProductNotFoundError, InsufficientStockError
from services.customer_service import CustomerService, CustomerNotFoundError
from utils.file_handler import load_json, save_json
from utils.validator import validate_non_negative_int, ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

SALES_FILE = "data/sales.json"


class SalesService:
    """Handles creating sales (bills), updating inventory, and sales reporting."""

    def __init__(
        self,
        inventory_service: InventoryService,
        customer_service: CustomerService,
        file_path: str = SALES_FILE,
    ) -> None:
        """Initialize the sales service and load existing sales from disk.

        Args:
            inventory_service: Shared InventoryService instance used to check
                and reduce stock.
            customer_service: Shared CustomerService instance used to verify
                customers exist.
            file_path: Path to the JSON file used for persistence.
        """
        self.inventory_service = inventory_service
        self.customer_service = customer_service
        self.file_path = file_path
        self._sales: List[Sale] = self._load_sales()

    def _load_sales(self) -> List[Sale]:
        raw = load_json(self.file_path)
        return [Sale.from_dict(item) for item in raw]

    def _persist(self) -> None:
        save_json(self.file_path, [s.to_dict() for s in self._sales])

    def create_sale(self, customer_id: str, cart: Dict[str, int]) -> Sale:
        """Create a new sale (bill) for a customer.

        Validates the whole cart before changing any inventory state, so a
        failure partway through never leaves stock partially deducted.

        Args:
            customer_id: The id of the customer making the purchase.
            cart: A mapping of product_id -> quantity requested.

        Returns:
            The created Sale, including the computed total.

        Raises:
            CustomerNotFoundError: If the customer does not exist.
            ProductNotFoundError: If any product in the cart does not exist.
            InsufficientStockError: If stock is insufficient for any item.
            ValidationError: If the cart is empty or quantities are invalid.
        """
        if not cart:
            raise ValidationError("Cart cannot be empty.")

        self.customer_service.get_customer(customer_id)

        items: List[SaleItem] = []

        for product_id, quantity in cart.items():
            quantity = validate_non_negative_int(quantity, "Quantity")
            if quantity == 0:
                continue
            product = self.inventory_service.get_product(product_id)
            if product.quantity < quantity:
                raise InsufficientStockError(
                    f"Not enough stock for '{product.name}'. "
                    f"Available: {product.quantity}, requested: {quantity}."
                )
            items.append(SaleItem(product.product_id, product.name, quantity, product.price))

        if not items:
            raise ValidationError("Cart must contain at least one valid item.")

        for item in items:
            self.inventory_service.reduce_stock(item.product_id, item.quantity)

        sale = Sale(sale_id=str(uuid.uuid4())[:8], customer_id=customer_id, items=items)
        self._sales.append(sale)
        self._persist()
        logger.info(
            "Created sale %s for customer %s, total: %.2f",
            sale.sale_id, customer_id, sale.total_amount,
        )
        return sale

    def list_sales(self) -> List[Sale]:
        """Return all recorded sales."""
        return list(self._sales)

    def get_sale(self, sale_id: str) -> Sale:
        """Return a sale by id.

        Raises:
            ValueError: If no sale with that id exists.
        """
        sale = next((s for s in self._sales if s.sale_id == sale_id), None)
        if sale is None:
            raise ValueError(f"Sale '{sale_id}' not found.")
        return sale

    def total_revenue(self) -> float:
        """Return the sum of all sale totals ever recorded."""
        return round(sum(s.total_amount for s in self._sales), 2)

    def sales_by_customer(self, customer_id: str) -> List[Sale]:
        """Return all sales made by a specific customer."""
        return [s for s in self._sales if s.customer_id == customer_id]

    def print_bill(self, sale: Sale) -> str:
        """Generate a formatted receipt string for a sale.

        Args:
            sale: The sale to format.

        Returns:
            A human-readable receipt as a multi-line string.
        """
        customer = self.customer_service.get_customer(sale.customer_id)
        lines = [
            "=" * 40,
            "           SALES RECEIPT",
            "=" * 40,
            f"Sale ID   : {sale.sale_id}",
            f"Customer  : {customer.name}",
            f"Date      : {sale.timestamp}",
            "-" * 40,
        ]
        for item in sale.items:
            lines.append(
                f"{item.product_name[:20]:<20} x{item.quantity:<3} "
                f"@ {item.unit_price:>8.2f} = {item.subtotal:>10.2f}"
            )
        lines.append("-" * 40)
        lines.append(f"{'TOTAL':<30}{sale.total_amount:>10.2f}")
        lines.append("=" * 40)
        return "\n".join(lines)

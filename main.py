"""
Retail Sales Analytics Platform
--------------------------------
A command-line inventory, customer, and sales management system built
with clean OOP, type hints, input validation, and logging.

Run it with:  python main.py
"""

from services.inventory_service import (
    InventoryService,
    ProductNotFoundError,
    InsufficientStockError,
)
from services.customer_service import CustomerService, CustomerNotFoundError
from services.sales_service import SalesService
from utils.validator import ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)


def print_menu() -> None:
    """Print the main menu options."""
    print("\n" + "=" * 45)
    print(" RETAIL SALES ANALYTICS PLATFORM")
    print("=" * 45)
    print("1. Add product")
    print("2. List products")
    print("3. Add customer")
    print("4. List customers")
    print("5. Create sale")
    print("6. View sales report")
    print("7. Exit")


def handle_add_product(inventory: InventoryService) -> None:
    """Prompt for product details and add it to inventory."""
    try:
        product_id = input("Product ID: ")
        name = input("Name: ")
        category = input("Category: ")
        price = input("Price: ")
        quantity = input("Quantity: ")
        product = inventory.add_product(product_id, name, category, price, quantity)
        print(f"Added: {product.name} ({product.product_id})")
    except ValidationError as e:
        print(f"Input error: {e}")


def handle_list_products(inventory: InventoryService) -> None:
    """Print a table of all products in inventory."""
    products = inventory.list_products()
    if not products:
        print("No products in inventory yet.")
        return
    print(f"\n{'ID':<8}{'Name':<20}{'Category':<15}{'Price':>10}{'Qty':>8}")
    for p in products:
        print(f"{p.product_id:<8}{p.name:<20}{p.category:<15}{p.price:>10.2f}{p.quantity:>8}")
    print(f"\nTotal inventory value: {inventory.total_inventory_value():.2f}")


def handle_add_customer(customers: CustomerService) -> None:
    """Prompt for customer details and add a new customer."""
    try:
        customer_id = input("Customer ID: ")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        customer = customers.add_customer(customer_id, name, email, phone)
        print(f"Added: {customer.name} ({customer.customer_id})")
    except ValidationError as e:
        print(f"Input error: {e}")


def handle_list_customers(customers: CustomerService) -> None:
    """Print a table of all customers."""
    all_customers = customers.list_customers()
    if not all_customers:
        print("No customers yet.")
        return
    print(f"\n{'ID':<8}{'Name':<20}{'Email':<25}{'Phone':<15}")
    for c in all_customers:
        print(f"{c.customer_id:<8}{c.name:<20}{c.email:<25}{c.phone:<15}")


def handle_create_sale(sales: SalesService) -> None:
    """Prompt for a customer and cart items, then create a sale and print the bill."""
    try:
        customer_id = input("Customer ID: ")
        cart = {}
        print("Enter product IDs and quantities. Leave Product ID blank to finish.")
        while True:
            product_id = input("Product ID: ").strip()
            if not product_id:
                break
            quantity = input("Quantity: ").strip()
            cart[product_id] = quantity

        sale = sales.create_sale(customer_id, cart)
        print("\n" + sales.print_bill(sale))
    except (ValidationError, CustomerNotFoundError, ProductNotFoundError, InsufficientStockError) as e:
        print(f"Could not complete sale: {e}")


def handle_sales_report(sales: SalesService) -> None:
    """Print a summary table of all recorded sales."""
    all_sales = sales.list_sales()
    if not all_sales:
        print("No sales recorded yet.")
        return
    print(f"\n{'Sale ID':<10}{'Customer':<12}{'Date':<22}{'Total':>10}")
    for s in all_sales:
        print(f"{s.sale_id:<10}{s.customer_id:<12}{s.timestamp:<22}{s.total_amount:>10.2f}")
    print(f"\nTotal revenue: {sales.total_revenue():.2f}")


def main() -> None:
    """Run the interactive CLI menu loop."""
    inventory = InventoryService()
    customers = CustomerService()
    sales = SalesService(inventory, customers)

    actions = {
        "1": lambda: handle_add_product(inventory),
        "2": lambda: handle_list_products(inventory),
        "3": lambda: handle_add_customer(customers),
        "4": lambda: handle_list_customers(customers),
        "5": lambda: handle_create_sale(sales),
        "6": lambda: handle_sales_report(sales),
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "7":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue

        try:
            action()
        except Exception as e:  # safety net so the CLI never crashes outright
            logger.exception("Unexpected error")
            print(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()

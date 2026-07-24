# Retail Sales Analytics Platform

A command-line retail management system for handling inventory,
customers, and sales — built with clean, industry-standard Python
architecture: layered OOP design, type hints, docstrings, input
validation, custom exceptions, and logging.

## Features

- **Inventory management** — add, view, update, and delete products with stock tracking
- **Customer management** — add, view, update, and delete customer records with email/phone validation
- **Sales & billing** — create multi-item sales, auto-generate receipts, and automatically deduct stock
- **Validation layer** — every input is validated before it touches business logic or storage
- **Custom exceptions** — `ProductNotFoundError`, `InsufficientStockError`, `CustomerNotFoundError`, `ValidationError` for precise error handling
- **Logging** — every action (add, update, delete, sale) is logged to `logs/app.log` with timestamps
- **JSON persistence** — no database required; all data is stored in human-readable JSON files
- **Fully typed** — every function signature uses Python type hints
- **Documented** — every module, class, and public method has a docstring

## Project structure

```
retail-sales-analytics-platform/
│
├── main.py                    # CLI entry point
├── requirements.txt
├── README.md
│
├── data/                      # JSON data storage
│   ├── products.json
│   ├── customers.json
│   └── sales.json
│
├── models/                    # Data classes (Product, Customer, Sale)
│   ├── product.py
│   ├── customer.py
│   └── sale.py
│
├── services/                  # Business logic (CRUD + billing)
│   ├── inventory_service.py
│   ├── customer_service.py
│   └── sales_service.py
│
├── utils/                     # Shared helpers
│   ├── file_handler.py        # JSON read/write
│   ├── validator.py           # Input validation
│   └── logger.py              # Centralized logging
│
└── logs/
    └── app.log                # Runtime log file
```

## Architecture

The project follows a layered design so each part has a single
responsibility:

- **Models** — plain data structures (`dataclasses`) with no business logic
- **Services** — all business rules: validation, CRUD, stock deduction, billing
- **Utils** — cross-cutting concerns shared by every service (file I/O, validation, logging)
- **main.py** — a thin CLI layer that only handles user input/output and delegates everything else to services

This separation means the services could be reused behind a REST API
or a different UI without changing any business logic.

## Getting started

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd retail-sales-analytics-platform
   ```

2. No external dependencies are required — this project uses only the
   Python standard library (`dataclasses`, `json`, `logging`, `uuid`, `re`).
   Requires Python 3.9+.

3. Run it:
   ```
   python main.py
   ```

## Usage example

```
=============================================
 RETAIL SALES ANALYTICS PLATFORM
=============================================
1. Add product
2. List products
3. Add customer
4. List customers
5. Create sale
6. View sales report
7. Exit
Choose an option: 5
Customer ID: C001
Enter product IDs and quantities. Leave Product ID blank to finish.
Product ID: P001
Quantity: 2
Product ID:

========================================
           SALES RECEIPT
========================================
Sale ID   : 2387e249
Customer  : Amit Sharma
Date      : 2026-07-17T08:04:12
----------------------------------------
Wireless Mouse       x2   @   799.00 =    1598.00
----------------------------------------
TOTAL                            1598.00
========================================
```

## Error handling

The platform validates every input and raises specific, catchable
exceptions instead of generic errors:

| Exception | Raised when |
|---|---|
| `ValidationError` | Input fails a format/type/range check |
| `ProductNotFoundError` | A product id doesn't exist |
| `CustomerNotFoundError` | A customer id doesn't exist |
| `InsufficientStockError` | A sale requests more stock than is available |


## Roadmap / possible extensions

- Add unit tests with `pytest` for each service
- Replace JSON storage with SQLite for larger datasets
- Add a REST API layer (FastAPI) on top of the existing services
- Containerize with Docker
- Add a CI pipeline (GitHub Actions) to run tests on every push
- Add sales analytics: revenue by category, top customers, monthly trends

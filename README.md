# Walandoo Backend API

## Overview
This is the backend API for the Walandoo demo e-commerce app, built with Django REST Framework and PostgreSQL. It provides endpoints for products, stock, customers, shopping carts, orders, and shipments, with user authentication and strict per-customer data access.

## Authentication
- All endpoints (except registration and login) require authentication via TokenAuth.
- Obtain a token by POSTing to `/api/token-auth/` with your username and password.
- Include the token in the `Authorization` header: `Authorization: Token <your-token>`

## Permissions & Data Access
- **Customers** can only access their own profile, orders, and shipments.
- **Order and Shipment Endpoints**:
  - List and detail endpoints only return data for the authenticated user's customer record.
  - Attempting to access another user's order or shipment returns a 404 Not Found.
- **Products and Stock** are read-only and public.

## API Endpoints
- `/api/products/` (GET): List all products
- `/api/products/{id}/` (GET): Retrieve product details
- `/api/stock/` (GET): List all stock
- `/api/stock/{product_id}/` (GET): Retrieve stock for a product
- `/api/customers/{id}/` (GET/PUT/DELETE): Retrieve/update/delete your customer profile
- `/api/carts/` (GET/POST): List or create your shopping cart
- `/api/carts/{id}/` (GET/PUT/DELETE): Retrieve/update/delete your cart
- `/api/orders/` (GET/POST): List or create your orders (only your own)
- `/api/orders/{id}/` (GET/PUT/DELETE): Retrieve/update/delete your order (only your own)
- `/api/shipments/` (GET/POST): List or create your shipments (only your own)
- `/api/shipments/{id}/` (GET/PUT/DELETE): Retrieve/update/delete your shipment (only your own)
- `/api/register/` (POST): Register a new user
- `/api/profile/` (GET/PUT): Get or update your user profile
- `/api/openapi.yaml` (GET): Download the OpenAPI spec

## Example: Orders & Shipments
- **List Orders**: `GET /api/orders/` returns only your orders.
- **Retrieve Order**: `GET /api/orders/{id}/` returns 404 if the order does not belong to you.
- **List Shipments**: `GET /api/shipments/` returns only your shipments.
- **Retrieve Shipment**: `GET /api/shipments/{id}/` returns 404 if the shipment does not belong to you.

## Error Responses
- `401 Unauthorized`: If not authenticated.
- `404 Not Found`: If you try to access another user's order or shipment.

## Running Tests
- Run all tests with: `pytest api/tests.py --disable-warnings -v`
- Tests include model, API, registration, profile, and permission checks for customer, order, and shipment access.

## OpenAPI Spec
- The full OpenAPI spec is available at `/api/openapi.yaml`.
- It documents all endpoints, request/response schemas, and permission notes.

---

## Project Structure

```
walandoo/
├── backend/   # Django REST API backend
└── README.md
```

---

## Backend

- **Framework:** Django, Django REST Framework
- **Database:** PostgreSQL

### Setup

1. Create and activate a virtual environment:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your PostgreSQL credentials in `backend/walandoo/settings.py`.

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

---

## Development Notes

- The backend communicates with clients via RESTful API endpoints.
- Update CORS settings in Django if accessing the API from a different domain during development.
- Environment variables and secrets should be stored in `.env` files (excluded from version control).

---

## License

This project is for demonstration and educational purposes.

## API Usage Examples

### List Your Orders
```
GET /api/orders/
Authorization: Token <your-token>

Response:
[
  {
    "id": 1,
    "customer": 5,
    "total": 100.0,
    "status": "pending",
    ...
  }
]
```

### Retrieve Your Order
```
GET /api/orders/1/
Authorization: Token <your-token>

Response:
{
  "id": 1,
  "customer": 5,
  "total": 100.0,
  "status": "pending",
  ...
}
```

### Attempt to Retrieve Another User's Order
```
GET /api/orders/9999/
Authorization: Token <your-token>

Response:
404 Not Found
```

### List Your Shipments
```
GET /api/shipments/
Authorization: Token <your-token>

Response:
[
  {
    "id": 1,
    "order": 1,
    "tracking_number": "TRACK123",
    "carrier": "UPS",
    "status": "in transit",
    ...
  }
]
```

### Attempt to Retrieve Another User's Shipment
```
GET /api/shipments/9999/
Authorization: Token <your-token>

Response:
404 Not Found
```

---

## Release Notes

### 2025-05-27
- **Per-customer access control**: Orders and shipments endpoints now only return data for the authenticated customer. Attempting to access another user's order or shipment returns 404.
- **Comprehensive tests**: Added tests to ensure users cannot access or list other users' orders or shipments.
- **OpenAPI and README updates**: Documentation now clearly describes access control and error responses for these endpoints.
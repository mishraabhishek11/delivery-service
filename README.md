# 🚚 Delivery Service – FastAPI Service

A lightweight **FastAPI application** for managing **delivery orders**, backed by a SQLite database, with order creation, filtered/paginated listing and daily order statistics.

This project demonstrates **REST API design**, request validation with Pydantic/SQLModel, and database persistence.

---

## 🚀 Features

### 📦 Orders

- Create an order via `POST /orders/`
- New orders start with status `preparing`
- List orders via `GET /orders/`

### 📋 Listing & Filtering

- Filter by `status` (`preparing`, `picked_up`, `in_transit`, `delivered`)
- Filter by creation date with `created_at` (`YYYY-MM-DD`)
- Paginate with `skip` and `limit` (default 10, max 100)

### 📊 Daily Statistics

- `GET /stats/daily` returns the total number of orders created on a date, broken down by status
- Defaults to today when `summary_date` is omitted

### ✅ Validation & Docs

- Request bodies and query parameters are validated by Pydantic/SQLModel
- Auto-generated interactive docs (Swagger UI / ReDoc)

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Framework:** FastAPI
- **ORM / Validation:** SQLModel (SQLAlchemy + Pydantic)
- **Server:** Uvicorn
- **Database:** SQLite (`deliveryservice.db`, created automatically on startup)

---

## 📂 Project Structure

```
delivery-service/
├─ README.md
├─ requirements.txt
├─ main.py            # FastAPI app, lifespan (table creation) and router registration
├─ database.py        # SQLite engine, table creation and session dependency
├─ models.py          # OrderStatus enum, Order table, create/update schemas
└─ routes/
   ├─ __init__.py
   ├─ orders.py       # /orders endpoints
   └─ stats.py        # /stats endpoints
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <repository-url>
```

### 2️⃣ Navigate to the project folder

```bash
cd delivery-service
```

### 3️⃣ Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Start the server

```bash
uvicorn main:app --reload
```

### 6️⃣ Open in browser

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧑‍💻 Usage

### Endpoints

| Method | Path           | Description                                                         |
| ------ | -------------- | ------------------------------------------------------------------- |
| POST   | `/orders/`     | Create an order                                                     |
| GET    | `/orders/`     | List orders (optional `status`, `created_at`, `skip`, `limit`)      |
| GET    | `/stats/daily` | Order counts for a day, grouped by status (optional `summary_date`) |

### Create an order

```bash
curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Asha", "delivery_address": "12 MG Road, Pune", "items": "2x Pizza, 1x Coke"}'
```

Response:

```json
{
  "id": 1,
  "customer_name": "Asha",
  "delivery_address": "12 MG Road, Pune",
  "items": "2x Pizza, 1x Coke",
  "status": "preparing",
  "created_at": "2026-10-07T10:30:00.000000",
  "updated_at": "2026-10-07T10:30:00.000000"
}
```

### List orders

```bash
curl "http://localhost:8000/orders/?status=preparing&limit=10"
```

### Daily statistics

```bash
curl "http://localhost:8000/stats/daily?summary_date=2026-10-07"
```

Response:

```json
{
  "date": "2026-10-07",
  "total_orders": 3,
  "by_status": {
    "preparing": 2,
    "picked_up": 1,
    "in_transit": 0,
    "delivered": 0
  }
}
```

---

## 🗄️ Data Model

| Field              | Type     | Notes                                                         |
| ------------------ | -------- | ------------------------------------------------------------- |
| `id`               | int      | Primary key, auto-generated                                   |
| `customer_name`    | str      |                                                               |
| `delivery_address` | str      |                                                               |
| `items`            | str      | Free-text list of items                                       |
| `status`           | enum     | `preparing` (default), `picked_up`, `in_transit`, `delivered` |
| `created_at`       | datetime | Set automatically (local time)                                |
| `updated_at`       | datetime | Set automatically on creation                                 |

Tables are created automatically on application startup. There is no migration tooling yet, so schema changes require recreating `deliveryservice.db`.

---

## 🚧 Known Issues / Work in Progress

The following are present in the current code and are not yet fixed:

- `GET /health` is not registered: in `main.py`, `app.get(...)` is called without being applied as a decorator to `health_check`.
- `GET /orders/` rejects `skip=0` because `skip` is declared with `ge=1`; it should be `ge=0`.
- `GET /orders/?created_at=...` fails because the string is passed straight to `datetime.combine`; the parameter should be typed as `date`.
- `OrderUpdate` and `StatusLog` schemas exist, but no endpoints use them yet (no get/update/delete order, no status history).

---

## 🔮 Future Enhancements

- Get, update (status / address) and cancel order endpoints
- Status change history using `StatusLog`
- Database migrations (e.g. Alembic)
- Unit and integration tests
- Consistent error response shape
- Authentication
- Docker support

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat(scope): add your message"`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

Abhishek Mishra  
GitHub: [https://github.com/mishraabhishek11](https://github.com/mishraabhishek11)

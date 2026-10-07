from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application.
    This function is called when the application starts and stops.
    It creates the database tables when the application starts.
    """
    create_tables()
    print("Tables created")
    yield
    print("Application shutdown")


app = FastAPI(title="Delivery Service", description="A simple delivery service API",
              version="0.1.0", lifespan=lifespan)


app.include_router(orders_router)
app.include_router(stats_router)

app.get("/health", tags=["health"])


def health_check():
    """Health check endpoint to verify that the application is running.
    Returns a simple JSON response indicating the status of the application.
    """
    return {"status": "ok"}

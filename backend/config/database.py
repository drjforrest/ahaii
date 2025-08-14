"""
Database configuration and session management for AHAII
African Health AI Infrastructure Index
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from supabase import Client, create_client

from config.settings import settings

# Supabase client for auth and real-time features
supabase: Client = create_client(
    supabase_url=settings.NEXT_PUBLIC_SUPABASE_URL,
    supabase_key=settings.SUPABASE_SECRET_KEY,
)

# SQLAlchemy engine for direct database access (only if DATABASE_URL available)
engine = None
async_engine = None

try:
    db_url = settings.db_url
    engine = create_engine(
        db_url, pool_pre_ping=True, pool_recycle=300, echo=settings.DEBUG
    )

    # Async engine for async operations
    async_engine = create_async_engine(
        db_url.replace("postgresql://", "postgresql+asyncpg://"),
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG,
    )
except Exception as e:
    print(f"Warning: Could not create SQLAlchemy engines: {e}")
    print("Falling back to Supabase-only mode")

# Session factories (only if engines are available)
SessionLocal = None
AsyncSessionLocal = None

if engine is not None:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if async_engine is not None:
    AsyncSessionLocal = sessionmaker(
        class_=AsyncSession, autocommit=False, autoflush=False, bind=async_engine
    )


def get_db():
    """Dependency to get database session"""
    if SessionLocal is None:
        raise RuntimeError(
            "Database session not available - use Supabase client instead"
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Dependency to get async database session"""
    if AsyncSessionLocal is None:
        raise RuntimeError(
            "Async database session not available - use Supabase client instead"
        )
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_supabase() -> Client:
    """Get Supabase client"""
    return supabase

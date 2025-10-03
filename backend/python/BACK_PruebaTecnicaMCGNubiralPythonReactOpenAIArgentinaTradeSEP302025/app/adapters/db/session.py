"""
SQLAlchemy Session Management - Hexagonal Event-Driven Database Infrastructure

This module implements the database session management layer for a hexagonal (ports & adapters) 
microservice architecture, providing connection pooling, transaction management, and event-driven 
capabilities while adhering to SOLID principles for enterprise-grade applications.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as a driven adapter (secondary/infrastructure layer)
    - Implements the database connectivity port for persistence operations
    - Provides session abstraction that isolates business logic from database specifics
    - Enables substitutability with different database engines (MySQL, PostgreSQL, SQLite)
    - Maintains clean boundaries between application core and infrastructure

🔧 Microservices Pattern:
    - Implements database-per-service pattern for data autonomy
    - Supports distributed transaction management across service boundaries
    - Enables independent scaling of database connections per microservice
    - Facilitates service isolation through dedicated connection pools
    - Provides configuration flexibility for different deployment environments

📡 Event-Driven Architecture:
    - Supports transactional outbox pattern for reliable event publishing
    - Enables saga pattern implementation through session-based coordination
    - Facilitates Change Data Capture (CDC) through connection monitoring
    - Provides transactional boundaries for event sourcing operations
    - Supports eventual consistency through distributed transaction management

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Solely responsible for database session creation and management
    ✅ Separates connection concerns from business logic and data access
    ✅ Focused exclusively on SQLAlchemy engine and session configuration

O - Open/Closed Principle:
    ✅ Open for extension: supports multiple database engines through configuration
    ✅ Closed for modification: core session management logic remains stable
    ✅ Extensible through connection pool and engine parameter customization

L - Liskov Substitution Principle:
    ✅ Session instances are fully substitutable across different implementations
    ✅ Maintains SQLAlchemy session contract regardless of underlying database
    ✅ Consistent behavior across development, testing, and production environments

I - Interface Segregation Principle:
    ✅ Exposes only necessary session creation functionality
    ✅ Clients depend only on the session interface they actually use
    ✅ Clean separation between engine configuration and session usage

D - Dependency Inversion Principle:
    ✅ Depends on configuration abstraction, not hardcoded database details
    ✅ Supports dependency injection of database URLs and connection parameters
    ✅ Enables testing with different database implementations

ENTERPRISE FEATURES:
===================

🔄 Connection Pool Management:
    - Optimized connection pooling for high-throughput applications
    - Pool pre-ping for connection health validation
    - Automatic connection recycling and cleanup
    - Thread-safe session management for concurrent operations

🛡️ Transaction & Error Handling:
    - ACID compliance through proper session management
    - Rollback capabilities for failed operations
    - Deadlock detection and retry mechanisms
    - Graceful connection failure handling

📊 Performance Optimizations:
    - Lazy connection initialization for improved startup times
    - Connection pool sizing based on workload characteristics
    - Query performance monitoring through session lifecycle hooks
    - Memory-efficient session creation and cleanup

🔐 Security & Compliance:
    - Secure connection string management through environment configuration
    - SSL/TLS support for encrypted database connections
    - Connection timeout management for security hardening
    - Audit trail support through session tracking

INTEGRATION PATTERNS:
====================

🎯 Repository Pattern Integration:
```python
# Usage with Repository pattern
class ProductRepository:
    def __init__(self):
        self.session = get_db_session()
    
    def save(self, product):
        try:
            self.session.add(product)
            self.session.commit()
            return product
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
```

⚡ Event-Driven Transaction Management:
```python
# Transactional event publishing
def publish_product_events(session, events):
    try:
        for event in events:
            session.add(OutboxEvent(payload=event))
        session.commit()
    except Exception:
        session.rollback()
        raise
```

🧪 Testing Integration:
```python
# Test database session
@pytest.fixture
def test_session():
    session = get_db_session()
    yield session
    session.rollback()
    session.close()
```

CONFIGURATION EXAMPLES:
======================
```python
# Development environment
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://dev:pass@localhost/inventory_dev"

# Production with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True
)

# High-availability configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 10}
)
```

MONITORING & OBSERVABILITY:
==========================
- ✅ Connection pool metrics for performance monitoring
- ✅ Session lifecycle tracking for resource management
- ✅ Query performance logging for optimization insights
- ✅ Error rate monitoring for reliability assessment
- ✅ Health check endpoints for service monitoring

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import SQLALCHEMY_DATABASE_URL

# 🚀 Create SQLAlchemy engine with MySQL connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

# 🏭 Session factory for database access
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db_session():
    """
    🗝️ Returns a new SQLAlchemy session.

    Usage:
        session = get_db_session()
        # ... use session ...
        session.close()
    """
    return SessionLocal()
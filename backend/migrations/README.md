# Database migrations

This folder will contain Alembic migrations for Neon Postgres schema.

To initialize Alembic (do this once):
```bash
alembic init migrations
```

To create a new migration:
```bash
alembic revision --autogenerate -m "Add users table"
```

To apply migrations:
```bash
alembic upgrade head
```

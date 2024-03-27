## Migration

### Latest migration
After `alembic` package has been installed, run the following commands to start the initial migrations

```bash
alembic upgrade head
```

### Initial migration
If you want to make the initial migration from scratch (create database from scratch)

1st you would need to remove the `./server/alembic` from the `./server/`.

Then run the following commands in order.

```bash
alembic init alembic
```

```bash
alembic revision --autogenerate -m "Initial revision"
```

```bash
alembic upgrade head
```


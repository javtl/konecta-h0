"""Alembic environment configuration."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from pathlib import Path

# 1. Agrega la raíz del backend al path para que Python encuentre el módulo 'app'
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 2. Importa la Base de datos y las configuraciones de tu FastAPI
from app.db.database import Base
from app.config import get_settings
from app.models.db_models import User, Sparring, Vote, Ranking

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Reemplaza el 'None' original por la metadata de tus modelos para soportar --autogenerate
target_metadata = Base.metadata

# Instancia la configuración para leer las variables del archivo .env
settings = get_settings()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    
    # Extrae dinámicamente el DATABASE_URL asíncrono/síncrono configurado
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # Inyecta dinámicamente la URL del .env en la configuración de la conexión
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
from __future__ import with_statement

import os
import sys

import dotenv

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig


config = context.config
fileConfig(config.config_file_name)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from app.db.base import Base

target_metadata = Base.metadata
dotenv.load_dotenv(verbose=True)

def get_url():
    user = os.getenv("POSTGRES_USER", "admin_f5")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "13.38.159.23")
    db = os.getenv("POSTGRES_DB", "docker_university")
    return f"postgresql://{user}:{password}@{server}/{db}"


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from __future__ import with_statement
from logging.config import fileConfig  # Add this import

from alembic import context
from sqlalchemy import engine_from_config, pool
import logging.config
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from migrations.models import Base
from config import DATABASE_URI

config = context.config

# Override sqlalchemy.url with the value from config.py
config.set_main_option("sqlalchemy.url", DATABASE_URI)

fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Set target_metadata to the metadata from your models
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"),
                      target_metadata=target_metadata,
                      literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), 
        prefix='sqlalchemy.', 
        poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

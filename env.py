from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.models import Base

config = context.config # Получаем конфигурацию Alembic
fileConfig(config.config_file_name) # Загружаем конфигурацию логирования из файла, указанного в конфигурации Alembic

target_metadata = Base.metadata

def run_migrations_offline(): # Конфигурируем Alembic для работы в оффлайн-режиме, используя URL базы данных
    context.configure(url=config.get_main_option("sqlalchemy.url"))
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():  # Создаем движок SQLAlchemy для подключения к базе данных
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection: # Подключаемся к базе данных и выполняем миграции
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode(): # Определяем, работает ли Alembic в оффлайн-режиме или в режиме онлайн
    run_migrations_offline()
else:
    run_migrations_online()

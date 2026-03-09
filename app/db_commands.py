import click
from psycopg import sql
from .db import get_admin_connection

def register_db_commands(app):
    @app.cli.command("db-create")
    @click.argument("db_name")
    def db_create(db_name):
        try:
            conn = get_admin_connection()
            conn.autocommit = True

            with conn.cursor() as cur:
                query = sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db_name)
                )
                cur.execute(query)

            conn.close()
            click.echo(f"Base de datos '{db_name}' creada correctamente.")
        except Exception as e:
            click.echo(f"Error al crear la base de datos '{db_name}': {e}")

    @app.cli.command("db-drop")
    @click.argument("db_name")
    def db_drop(db_name):
        try:
            conn = get_admin_connection()
            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute("""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = %s
                      AND pid <> pg_backend_pid()
                """, (db_name,))

                drop_query = sql.SQL("DROP DATABASE IF EXISTS {}").format(
                    sql.Identifier(db_name)
                )
                cur.execute(drop_query)

            conn.close()
            click.echo(f"Base de datos '{db_name}' eliminada correctamente.")
        except Exception as e:
            click.echo(f"Error al eliminar la base de datos '{db_name}': {e}")
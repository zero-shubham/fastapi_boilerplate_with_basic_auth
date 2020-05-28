import sqlalchemy
from application import metadata, database
from permissions_system.constants import InternalTables

_customer_table_name = "customers"

Customer = sqlalchemy.Table(
    "customers",
    metadata,
    sqlalchemy.Column("customer_id", sqlalchemy.ForeignKey(
        f"{InternalTables.User}.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(
        length=500), unique=True, nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String(
        length=100
    ), unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=300)),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean(), default=False)
)

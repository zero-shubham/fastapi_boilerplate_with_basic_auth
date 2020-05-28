import sqlalchemy
from application import database, metadata
from permissions_system.constants import InternalTables


Token = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(
        f"{InternalTables.User}.id", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("token", sqlalchemy.String(length=1000),
                      nullable=False)
)

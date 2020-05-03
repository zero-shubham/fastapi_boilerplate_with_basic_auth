import sqlalchemy
from application import database, metadata


Token = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("token", sqlalchemy.String(length=1000),
                      nullable=False)
)

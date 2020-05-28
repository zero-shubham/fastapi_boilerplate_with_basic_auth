from fastapi import FastAPI
from dotenv import load_dotenv
import databases
import sqlalchemy
import os
from permissions_system.PermissionsSystemDatabases import PermissionsS

load_dotenv(verbose=True)
app = FastAPI(title="FastAPI Admin Setup")

DB_URI = os.environ["DB_URI"]

database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()
ps = PermissionsS(
    metadata,
    database,
    DB_URI
)

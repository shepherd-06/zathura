from peewee import SqliteDatabase, Model, UUIDField, CharField, TextField, CharField, BooleanField, IntegerField
from playhouse.migrate import SqliteMigrator, migrate
from datetime import datetime
from uuid import uuid4
from ZathuraProject.utility import Utility

db = SqliteDatabase('logger.db')
migrator = SqliteMigrator(db)


def database_start(database_name='logger.db'):
    db = SqliteDatabase(database_name)
    # migrator = SqliteMigrator(db)


class ErrorLog(Model):
    _id = UUIDField(unique=True, primary_key=False, default=str(uuid4()))
    user = CharField(null=False, max_length=40)
    error_name = CharField(null=False, max_length=20)
    error_description = TextField(null=False)
    point_of_origin = CharField(null=True, default=None, max_length=20)
    logged_at = IntegerField(default=Utility.current_time_in_milli())
    is_resolved = BooleanField(default=False)
    resolved_at = IntegerField(null=True)
    warning_level = IntegerField(default=0)

    class Meta:
        database = db


class DebugLog(Model):
    _id = UUIDField(unique=True, primary_key=False, default=str(uuid4()))
    user = CharField(max_length=40, null=False)
    message_data = TextField(null=False)
    point_of_origin = CharField(max_length=20, null=True)
    logged_at = IntegerField(default=Utility.current_time_in_milli())

    class Meta:
        database = db


def database_connection():
    # Connect to our database.
    if db is not None:
        db.connect(reuse_if_open=True)
    else:
        database_start()
        db.connect(reuse_if_open=True)

    # TODO: handle all migrations commands from here
    # Reference: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#migrate
    # with db.atomic():
    #     migrate(
    #         migrator.rename_column('DebugLog', 'id', '_id')
    #     )

    # Create the tables.
    db.create_tables([ErrorLog, DebugLog])


def close_db():
    if db is not None:
        db.close()

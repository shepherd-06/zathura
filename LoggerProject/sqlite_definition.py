from peewee import SqliteDatabase, Model, UUIDField, CharField, TextField, CharField, DateTimeField, BooleanField
from playhouse.migrate import SqliteMigrator, migrate
from datetime import datetime
from uuid import uuid1

db = SqliteDatabase('logger.db')
migrator = SqliteMigrator(db)

class ErrorLog(Model):
    _id = UUIDField(unique=True, primary_key = False, default=str(uuid1()))
    user = CharField(null=False, max_length=40)
    error_name = CharField(null=False, max_length=20)
    error_description = TextField(null=False)
    point_of_origin = CharField(null=True, default = None, max_length=20)
    logged_at = DateTimeField(default=datetime.now())
    is_resolved = BooleanField(default=False)
    resolved_at = DateTimeField(null=True)

    class Meta:
        database = db

class DebugLog(Model):
    _id = UUIDField(unique=True, primary_key = False, default=str(uuid1()))
    user = CharField(max_length=40, null=False)
    message_data = TextField(null=False)
    point_of_origin = CharField(max_length=20, null=True)
    logged_at = DateTimeField(default=datetime.now())

    class Meta: 
        database = db

def database_connection():
    # Connect to our database.
    db.connect()

    # TODO: handle all migrations commands from here
    # Reference: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#migrate
    # with db.atomic():
    #     migrate( 
    #         migrator.rename_column('DebugLog', 'id', '_id')
    #     )
    
    # Create the tables.
    db.create_tables([ErrorLog, DebugLog])
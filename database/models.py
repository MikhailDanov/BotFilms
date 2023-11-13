from peewee import Model, IntegerField, CharField, ForeignKeyField, SqliteDatabase, TextField
from config_data.config import DB_PATH


db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """Base model for creating the tables in database"""
    class Meta:
        database = db


class Film(BaseModel):
    """A table model for movie information"""
    class Meta:
        db_table = "films"

    kp_id = IntegerField()
    title = CharField()
    year = IntegerField()
    genres = CharField()
    poster = CharField()
    description = TextField()


class User(BaseModel):
    """A table model for user information"""
    class Meta:
        db_table = "users"

    user_id = IntegerField()
    first_name = CharField()
    last_name = CharField(null=True)


class PersonalRating(BaseModel):
    """A table model for personal rating information"""
    class Meta:
        db_table = "personal_rating"

    user_id = ForeignKeyField(User)
    film_id = ForeignKeyField(Film)
    rating = IntegerField(null=True)

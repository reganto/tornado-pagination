import peewee


DB = peewee.SqliteDatabase("db.sqlite3")


class Post(peewee.Model):
    title = peewee.CharField(max_length=255)
    body = peewee.TextField()

    class Meta:
        database = DB


DB.create_tables((Post, ), safe=True)

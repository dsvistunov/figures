import sqlite3


class DataBase:

    def __init__(self, db_file='db.sqlite3'):
        self.db_file = db_file
        self._sql_create_table = None

    def add(self, table):
        sql_str = 'CREATE TABLE IF NOT EXISTS %s (' % table.__name__
        sql_str += '\n\t\t\t\t\tid int PRIMARY KEY'
        for item in table.__dict__.items():
            field, value = item
            if field[:2] != '__' and field[-2:] != '__' \
                    and not callable(getattr(table, field)):
                sql_str += ',\n\t\t\t\t\t%s %s' % \
                           (field, value.get_modifiers())
        sql_str += '\n\t\t\t\t);'
        self._sql_create_table = sql_str

    @staticmethod
    def create_table(conn, sql_crate_table):
        c = conn.cursor()
        c.execute(sql_crate_table)

    def connect(self):
        return sqlite3.connect(self.db_file)

    def migrate(self):
        connection = self.connect()
        self.create_table(connection, self._sql_create_table)


class Model:

    @classmethod
    def select(cls, *args, **kwargs):
        conn = sqlite3.connect('mydb.sqlite3')
        c = conn.cursor()
        sql_str = 'SELECT * FROM {}'.format(cls.__name__)
        if kwargs:
            for key, val in kwargs.items():
                field, opt = key.split('__')
            if opt == 'startswith':
                sql_str += ' WHERE {} LIKE "{}%"'.format(field, val)
        sql_str += ';'
        c.execute(sql_str)
        return c.fetchall()


class CharField:
    field_type = 'VARCHAR'

    def __init__(self, max_length=255, null=False):
        self.max_lenght = max_length
        self.null = null

    def get_modifiers(self):
        if self.null:
            is_null = 'NULL'
        else:
            is_null = 'NOT NULL'
        return '%s %s' % (self.field_type.lower(), is_null)


class IntegerField:
    field_type = 'INT'

    def __init__(self, default, null=False):
        self.default = default
        self.null = null

    def get_modifiers(self):
        if self.null:
            is_null = 'NULL'
        else:
            is_null = 'NOT NULL'
        return '%s %s' % (self.field_type.lower(), is_null)


class Table1(Model):
    name = CharField(null=True)
    age = IntegerField(default=1)


if __name__ == '__main__':
    register = DataBase('mydb.sqlite3')
    register.add(Table1)
    register.migrate()

    slct1 = Table1.select()
    slct2 = Table1.select(name__startswith='B')
    print(slct1)
    print(slct2)

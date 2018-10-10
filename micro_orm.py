import sqlite3


class DataBase:

    def __init__(self, db_file='db.sqlite3'):
        self.db_file = db_file
        self._sql_query = None

    def add(self, table):
        sql_query = 'CREATE TABLE IF NOT EXISTS %s (' % table.__name__
        sql_query += '\n\t\t\t\t\tid int PRIMARY KEY'
        for item in table.__dict__.items():
            field, value = item
            if field[:2] != '__' and field[-2:] != '__' \
                    and not callable(getattr(table, field)):
                sql_query += ',\n\t\t\t\t\t%s %s' % \
                           (field, value.get_modifiers())
        sql_query += '\n\t\t\t\t);'
        table.db_file = self.db_file
        self._sql_query = sql_query

    @staticmethod
    def create_table(connection, sql_query):
        cursor = connection.cursor()
        cursor.execute(sql_query)

    @staticmethod
    def connect(db_file):
        return sqlite3.connect(db_file)

    def migrate(self):
        connection = self.connect(self.db_file)
        self.create_table(connection, self._sql_query)


class Model(DataBase):

    @classmethod
    def select(cls, *args, **kwargs):
        connection = cls.connect(cls.db_file)
        cursor = connection.cursor()
        table = cls.__name__
        clause = ''
        column = ''
        operator = ''
        pattern = ''

        if kwargs:
            for key, val in kwargs.items():
                for lookup in key.split('__'):
                    if lookup in cls.__dict__:
                        column = lookup
                    elif lookup == 'startswith':
                        clause = 'WHERE'
                        operator = 'LIKE'
                        pattern = '"{}%"'.format(val)
                    elif lookup == 'endswith':
                        clause = 'WHERE'
                        operator = 'LIKE'
                        pattern = '"%{}"'.format(val)
                    elif lookup == 'exact':
                        clause = 'WHERE'
                        column = '{}="{}"'.format(column, val)

        sql_query = 'SELECT * FROM {0} {1} {2} {3} {4};'.format(table, clause, column, operator, pattern)
        cursor.execute(sql_query)
        return cursor.fetchall()


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

    print(Table1.select())
    print(Table1.select(name__startswith='B'))
    print(Table1.select(name__endswith='k'))
    print(Table1.select(name__exact='Bob'))

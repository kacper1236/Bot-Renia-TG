import psycopg2

class Database:

    conn = None
    curr = None

    def __init__(self):
        self.conn = psycopg2.connect("postgresql://my_user:my_password@postgres/my_database")
        self.curr = self.conn.cursor()

    def checkPrimaryKey(self, table:str):
        """
        check table for primary key
        """
        self.curr.execute(f"""SELECT
                            kcu.column_name
                        FROM
                            information_schema.table_constraints AS tc
                        JOIN
                            information_schema.key_column_usage AS kcu
                        ON
                            tc.constraint_name = kcu.constraint_name
                        AND
                            tc.table_schema = kcu.table_schema
                        WHERE
                            tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = {table};""")
        return self.curr.fetchone()

    def insert(self, table:str, variables:str, values):
        command = f"""INSERT INTO {table} ({variables}) VALUES ({", ".join(f"%s" for _ in range(len(variables)))})
                          ON CONFLICT (ID) DO UPDATE
                          SET {", ".join(f"{i} = %s, " for i in variables)};"""
        self.curr.execute(command, values * 2)
        self.conn.commit()

    def select_one_piece(self, variables:str, table:str, where:str):
        """
        select one piece from table
        """
        self.curr.execute(f"SELECT {variables} FROM {table} WHERE {where};")
        return self.curr.fetchone()[0]

    
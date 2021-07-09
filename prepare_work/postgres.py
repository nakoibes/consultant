import psycopg2
# Подключение к существующей базе данных
connection = psycopg2.connect(user="kvakva",
                              # пароль, который указали при установке PostgreSQL
                              password="1111",
                              host="127.0.0.1",
                              port="5432")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# Курсор для выполнения операций с базой данных
cursor = connection.cursor()
sql_create_database = 'create database postgres_db'
cursor.execute(sql_create_database)

    cursor.close()
    connection.close()
    print("Соединение с PostgreSQL закрыто")
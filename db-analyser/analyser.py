import psycopg2

# Database connection parameters
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

# Connect to PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

def get_tables(cursor):
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    return [row[0] for row in cursor.fetchall()]

def get_columns(cursor, table):
    cursor.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{table}';
    """)
    return [row[0] for row in cursor.fetchall()]

# Get all tables
tables = get_tables(cursor)
print("Tables:", tables)

# Get all columns for each table
table_columns = {table: get_columns(cursor, table) for table in tables}
print("Schema:", table_columns)

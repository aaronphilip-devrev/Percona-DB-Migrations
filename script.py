import subprocess
import mysql.connector

def get_table_size(database, table):
    """Fetches the size of a table from the database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database=database
    )
    cursor = connection.cursor()
    query = f"SELECT table_name, (data_length + index_length) AS size FROM information_schema.tables WHERE table_schema = '{database}' AND table_name = '{table}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[1]  # Return the size in bytes

def apply_migration(database, table):
    """Applies the appropriate migration based on table size."""
    size = get_table_size(database, table)
    print(f"Table {table} size: {size} bytes")

    if size < 100000000:  # Example threshold: 100MB
        # Use regular ALTER TABLE if table is small
        flyway_command = [
            "flyway", "migrate", "-url=jdbc:mysql://localhost:3306/mydatabase",
            "-user=root", "-password=password", "-locations=filesystem:/sql"
        ]
        result = subprocess.run(flyway_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("Migration applied with ALTER TABLE")
        else:
            print("Flyway migration failed:", result.stderr.decode())
    else:
        # Use pt-online-schema-change for large tables
        pt_command = [
            "pt-online-schema-change",
            "--alter", "ADD INDEX idx_users_name (name)",
            f"D={database},t={table}",
            "--execute"
        ]
        result = subprocess.run(pt_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("Migration applied with pt-online-schema-change")
        else:
            print("Percona Toolkit migration failed:", result.stderr.decode())

# Example call to the migration function
apply_migration("mydatabase", "users")
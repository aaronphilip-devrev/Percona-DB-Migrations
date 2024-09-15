Here’s a **small README** explaining the code:

---

## README: Database Migration Automation with Python, Flyway, and Percona Toolkit

### Overview

This project automates database schema migrations by integrating **Flyway** for version control, **Python** for automation, and **Percona Toolkit** for optimizing performance. The Python script dynamically decides whether to use a regular `ALTER TABLE` operation or Percona's `pt-online-schema-change` based on the size of the table, reducing downtime for large databases.

### Prerequisites

Ensure the following are installed on your system:

1. **Python 3.x**
2. **Flyway**
3. **MySQL or Percona Server**
4. **Percona Toolkit** (for `pt-online-schema-change`)

### Installation

1. **Install Percona Toolkit**:
   ```bash
   sudo apt install percona-toolkit
   ```

2. **Install Flyway**:
   ```bash
   brew install flyway
   ```

3. **Install Python MySQL Connector**:
   ```bash
   pip install mysql-connector-python
   ```

### Usage

1. **Configure Database Connection**:
   Update the connection details in the `get_table_size` function in the Python script:
   ```python
   connection = mysql.connector.connect(
       host="localhost",
       user="root",
       password="password",
       database="mydatabase"
   )
   ```

2. **Run the Migration Script**:
   The Python script automatically decides whether to use Flyway’s `ALTER TABLE` or Percona’s `pt-online-schema-change` based on the table size.
   ```bash
   python migrate.py
   ```

### How it Works

- **Small Tables**: For tables smaller than 100MB, the script uses Flyway to run a regular `ALTER TABLE`.
- **Large Tables**: For tables larger than 100MB, it uses Percona Toolkit’s `pt-online-schema-change` to avoid downtime.

### Example Script

```python
def apply_migration(database, table):
    size = get_table_size(database, table)
    if size < 100000000:  # 100MB threshold
        flyway_command = ["flyway", "migrate", "-url=jdbc:mysql://localhost:3306/mydatabase", "-user=root", "-password=password", "-locations=filesystem:/sql"]
        subprocess.run(flyway_command)
    else:
        pt_command = ["pt-online-schema-change", "--alter", "ADD INDEX idx_users_name (name)", f"D={database},t={table}", "--execute"]
        subprocess.run(pt_command)
```

### Conclusion

This solution automates database migrations, reduces downtime, and optimizes performance for both small and large tables.

--- 


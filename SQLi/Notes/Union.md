# Union-Based SQL Injection Attacks

## Concept
A SQL injection **UNION attack** allows an attacker to retrieve data from other tables by appending results to the original query’s output.

### Requirements
For a UNION query to work:
- The original and injected queries must return the **same number of columns**.
- The data types of the columns must be **compatible**.

---

## Techniques

### 1. Determining the Number of Columns
Two common methods:

- **ORDER BY method**  
  Increment the column index in `ORDER BY n` until an error occurs.  
  The last valid index indicates the number of columns.  

- **SELECT NULL method**  
  Use `UNION SELECT NULL, NULL, ...` and keep adding `NULL` placeholders until the query succeeds.  
  `NULL` is used because it is compatible with most data types.  

**Note (Oracle):** Queries must select from the special `dual` table.  
Example:  
```sql
' UNION SELECT NULL,NULL FROM dual--
```

### 2. Finding a Column Accepting Text
Once the numer of columns is known, insert a string value into each position one at a time.
```sql
' UNION SELECT 'example',NULL,NULL--
```
If the application responds correctly then that column contains that data type.

### 3. Retrieving Multiple Values in a Single Column
**String concatenation** can be used to join the content of the columns.Every database has its own method for string concatenation.
String concatenation is useful when only one text-compatible column is available.
- For Oracle
    ```sql
    ' UNION SELECT NULL, username || '~' || password FROM users--
    ```
- For MySQL / PostgreSQL
    ```sql
    ' UNION SELECT NULL, CONCAT(username, ':', password) FROM users--
    ```
- For SQL Server
    ```sql
    ' UNION SELECT NULL, username + ':' + password FROM users--
    ```
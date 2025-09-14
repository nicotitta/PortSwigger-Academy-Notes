# Blind SQL Injection (SQLi)

## Concept
A **blind SQL injection** occurs when there is an SQLi vulnerability, but the results of the query are **not displayed in the HTTP response**.  
Since the attacker cannot directly see the query output, different inference techniques are required.

### Clues indicating blind SQLi:
- Differences in page content.
- HTTP response codes.
- Response time delays.
- External (out-of-band) interactions.

---

## Types of Blind SQLi

1. **Boolean-Based Blind**  
   - Use true/false conditions to alter the response.  
   - Example:  
     ```sql
     ' AND 1=1--
     ' AND 1=2--
     ```

2. **Time-Based Blind**  
   - Leverage query delays to confirm execution.  
   - Example (PostgreSQL):  
     ```sql
     ' || (SELECT pg_sleep(5))--
     ```

3. **Out-of-Band (OAST)**  
   - Trigger external interactions (e.g., DNS or HTTP requests).  
   - Example: Use [Burp Collaborator](https://portswigger.net/burp/documentation/desktop/tools/collaborator) to detect DNS lookups.

---

## Techniques

### 1. Conditional Responses
- Applications may behave differently depending on whether a query returns results.  
- Example:  
  ```sql
  ' AND SUBSTRING(password,1,1)='a'--
  ```
This can be used for infer certain data character by character.
In this case using tools, such as **Burp Intruder** or **custom scripts**, is necessary in order to brue-force conditions.

### 2. Error-Based Blind SQLi
- Applications may reveal errors that leak data.
- The goal could be to cause a database error only if our tested condition evaluates to true.
- We start from a vulnerable query, we add a boolean expression and finally we add an expression that returns an error only if the previous boolean expression evaluates to true. 
- If the application shows the error that means the condition is true.
- Example (Oracle, using CASE with division by zero):
    ```sql
    ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE NULL END FROM dual)--
    ```
The main problem in these situations is that **poor error handling** often exposes sensitive info.

### 3. Extracting sensitive data via verbose SQL error messages
- Sometimes the application returns verbose error messages.
- These error messages can also be *SQL errors*
- One technique could be to force **type casting errors**.
- Example (PostgreSQL):
    ```sql
    ' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
    ```
- Error message may reveal the actual value (e.g., *administrator*).

### 4. Time-Based Inference
- When errors and responses give no clues we can rely on **response times**.
- Example (PostgreSQL):
    ```sql
    ' || (SELECT CASE WHEN (LENGTH(password)=20) THEN pg_sleep(5) ELSE pg_sleep(0) END)--
    ```
- If we get a delayed response that means the condition is true.

### 5. Out-of-Band (OAST)
- If queries are executed **asynchronously** then time delays become useless.
- In this case the goal is to trigger *network interactions* (DNS/HTTP) to a domain we control.
- **Burp Collaborator** can be used to detect these lookups.
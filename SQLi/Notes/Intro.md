# Introduction to SQL Injection (SQLi)


## Concept
**SQL injection (SQLi)** is an attack that allows an attacker to interfere with queries made to the database.  
By exploiting SQLi, an attacker may:
- Retrieve sensitive data.
- Modify or delete information.
- Subvert application logic.
- Disrupt availability (denial of service).

**Main goal of SQLi:**  
Retrieve or manipulate sensitive data beyond the application’s intended access control.

---

## Detection Techniques
SQLi vulnerabilities can be identified by:
- Injecting **special characters** (`'`, `"`, `--`, `;`) and observing application behavior.
- Injecting **boolean conditions** (`OR 1=1`, `AND 1=2`) and checking response changes.
- Using **time delays** to detect blind SQLi.
- Relying on **application error messages** (if verbose).
- Leveraging **automated tools** (e.g., sqlmap).

---

## SQL Context
SQLi can occur in different queries and clauses (e.g., `WHERE`, `UNION`, `ORDER BY`).  

**Important syntax reminder:**  
```sql
--   # Single-line comment in SQL
```

## Simple example of SQLi
Given the following URL:
```
https://web-security-academy.net/filter?category=Accessories
```
The underlying query is:
```sql
SELECT * FROM products WHERE category='Accessories' AND released=0;
```
By injecting `Accessories'--` we obtain:
```sql
SELECT * FROM products WHERE category='Accessories'--' AND released=0;
```
and the rest of the query is commented, changing the application logic.

We can lavarage this by injecting this classic **authentication bypass payload**:
```sql
' OR 1=1--
```
this way we force the condition to evaluate always to true.

## Union-based SQLi
Union-based SQL injections are a special type of SQLi, they levarage the **UNION** clause to append results from another query to the original.
For more details see the dedicated notes on [Union-based SQLi](Union.md).

## Blind SQLi
Occurs when the application does not display query results or error messages.
Such types of SQLi can be performed using:
* Boolean conditions
* Time delays
* Out-of-band (**OAST**) interactions (e.g **DNS Lookup**)
For more deteails refer to the [Blind SQLi](Blind.md) note.

## Second order SQLi
In this type of SQLi the user input is not executed but it is stored in the the database for future user.
Later the application will emed this input inside a query without any **sanitization**.
The exploitation happens only after the second use and not immediately.

## Practical notes
- The first step is always to check for the precense of SQLi vulnerabilities
- Next gather information about the database
- Then extract meaningful data

## Cheat Sheets & References
- [https://portswigger.net/web-security/sql-injection/cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [https://portswigger.net/web-security/sql-injection](https://portswigger.net/web-security/sql-injection)
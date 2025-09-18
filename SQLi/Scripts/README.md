# SQL Injection Scripts

This folder contains automation scripts developed while solving the **SQL Injection labs** from the [PortSwigger Web Security Academy](https://portswigger.net/web-security).

Each script corresponds to one lab and demonstrates how to:
- Automate common injection tasks.
- Extract data (boolean-based, union-based, blind).
- Save time compared to manual exploitation in Burp Suite.

## ⚠️ Disclaimer
These scripts are for **educational purposes only**.  
They must **not** be used on real systems without explicit authorization.

---

## Script Naming Convention
Scripts are named according to the corresponding lab

---

## Usage
Most scripts are written in Python 3.  

Example usage:
```bash
python3 sqli-lab-01.py http://target.lab/login
```

## 🔍 BurpSuite Proxy (Optional)

Each script includes a `proxies` dictionary:

```python
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}
```
This is optional and only needed if you want to intercept and analyze the requestes or responses in **Burpsuite**.
If instead you don't want to use Burpsuite remove the `proxies` parameter in the `requests.get()` call.

---

## Notes
Not every lab has a dedicated script.  
- Some labs were straightforward enough to solve manually (e.g., Lab 13 and Lab 18).  
- Scripts are included only where automation adds value or demonstrates a useful technique.


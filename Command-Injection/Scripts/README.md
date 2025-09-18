# Command-Injection Scripts

This folder contains automation scripts developed while solving the **OS Command-Injection** from the [PortSwigger Web Security Academy](https://portswigger.net/web-security).

Each script corresponds to one lab and demonstrates how to:
- Automate common OS injection tasks.
- Extract data retreived by running the given command.
- Automate the exploitation with Burp Suite.

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
python3 command-injection-lab-01.py http://target.lab/login whoami
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


# Introduction to OS Command-Injection


## Concept
**Command-Injection** is an attack that allows an attacker to inject operating system commands through a web application, these commands will then be executed by the server running the application.  


---

## Injecting OS commands
We can inject operating system commands directly in the vulnerable components of the various requests performed by the application.

Main problem:
- **Sanitization** server-side on the user input


We can use the `echo` command followed by a string of our choice and see if the application is vulnerable to this attack.<br>
If the provided string will be printed then the application is vulnerable.

We usually put our malicious command between two `&`, that are **shell command separators**, so we will get for example something like this:
- `... & echo aString & ...`

The application at this point will execute three commands:
- what comes before the first `&`
- our injected command
- what comes after the second `&`

---

## Useful Commands
There are several useful commands that can be injected depending on the goal of the exploitation.
All of these commands are operting system commands so they refer to the Linux Operating System.  

---

## Blind OS command injection vulnerabilities
Most of the times the application doesn't return the output of the command inside the HTTP response, this makes most of the OS injections **blind vulnerabilities**.

**Stategy:**
- Detect blind operating system command injections using **time delays**.
- Observe how much time the application takes to generate the response to our request

A simple **shell command** that allows us to cause a time delay is the `ping` command in the following format:
- `ping -c 3 127.0.0.1`
where the `-c` flag tells the command how many **ICMP packets** have to be sent and the `127.0.0.1` is the **loopback address** where the pings are redirected.

---

## Exploiting blind OS command injection by redirecting output
We can also rely on the **redirection mechanism** to save the output of our injected command into an arbitrary file.<br>
In order to achieve this we can use the redirection character that is `>` followed by the path representing the location of the new file.

The reason for us to use such mechanism relies on the fact that the application sometimes doesn't show the result of the injected command, so what we can do is:
- inject the OS command and redirect its output inside another file
- access the file through the file system managed by the application


## References
- [https://portswigger.net/web-security/os-command-injection](https://portswigger.net/web-security/os-command-injection)
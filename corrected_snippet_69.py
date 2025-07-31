import requests


def check_vuln(list_of_modules)->list:
    vulns = []
    for i in list_of_modules:
        k = i.split("==")
        url = f"https://pypi.org/pypi/{k[0]}/{k[1]}/json"
        equests
        k_vuln(list_of_modules) -> list:
        s = []
        i in list_of_modules:
        k = i.split("==")
        if len(k) != 2:
            continue  # Skip malformed module strings
        module_name, module_version = k[0], k[1]
        url = f"https://pypi.org/pypi/{module_name}/{module_version}/json"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            info = response.json()
            existing_vuln = info.get('vulnerabilities', [])  # Safely get 'vulnerabilities', default to empty list
            if existing_vuln:
                vulns.extend(existing_vuln)  # Use extend to add individual vulnerability dictionaries
        except requests.exceptions.RequestException:
            # Handle network errors, timeouts, or HTTP errors gracefully
            continue  # Skip to the next module on error
        except ValueError:
            # Handle JSON decoding errors gracefully
            continue
        rn vulns
        response.raise_for_status()
        info = response.json()
        existing_vuln = info['vulnerabilities']
        if len(existing_vuln) > 0:
            vulns.append(existing_vuln) 
    return vulns

import requests


def check_vuln(list_of_modules)->list:
    vulns = []
    for i in list_of_modules:
        k = i.split("==")
        if len(k) != 2:
            continue
        
        module_name, module_version = k[0], k[1]
        url = f"https://pypi.org/pypi/{module_name}/{module_version}/json"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            info = response.json()
            
            existing_vuln = info.get('vulnerabilities', []) 
            
            if len(existing_vuln) > 0:
                vulns.append(existing_vuln) 
        except requests.exceptions.RequestException:
            continue
        except ValueError:
            continue
        except Exception:
            continue
            
    return vulns
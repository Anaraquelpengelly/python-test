```python
'''
import subprocess, json


cmd_str = "pwd; ls"
process = subprocess.Popen(
    ["sh", "-c", cmd_str],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
data = stdout.decode('utf-8')
stderr = stderr.decode('utf-8')
# res = json.loads(data)
# print("Stdout\n" + data)
print(data + stderr)
'''
import subprocess

import yaml

stream = open('/home/fox/test.yaml', 'r')
data = yaml.safe_load(stream)

'''
stdout, stderr = data.communicate()
stdout = stdout.decode('utf-8')
stderr = stderr.decode('utf-8')
'''
print(str(data) + "\n")
# print(stdout + "\n")
# print(stderr + "\n")
```
'''
import subprocess, json


cmd_str = "pwd; ls"
process = subprocess.Popen(
    cmd_str,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
data = stdout.decode('utf-8')
stderr = stderr.decode('utf-8')
# res = json.loads(data)
# print("Stdout\n" + data)
print(data + stderr)
'''
import yaml

stream = open('/home/fox/test.yaml', 'r')
data = yaml.safe_load(stream)
stream.close()
print(yaml.dump(data))
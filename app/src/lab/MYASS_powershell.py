import subprocess
# TYPE test.txt | findstr "Smith"

ps = subprocess.run(['type', 'test.txt'], check=True, capture_output=True, shell=True)
processNames = subprocess.run(['findstr', 'Smith'],
                              input=ps.stdout, capture_output=True, shell=True)
print(processNames.stdout.decode('utf-8').strip())
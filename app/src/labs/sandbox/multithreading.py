import subprocess
import platform



if platform.system() == "Windows":
    shell_option = True
else:
    shell_option = False

commands = [
  ["date"],
  ["sleep", "10"],
  ["echo", "hello world"],
  ["sleep", "5"]
]
# cmd = ["echo", "Hello World !"]

processes = [subprocess.Popen(
  cmd,
  shell=shell_option,
  # stdout=subprocess.PIPE
) for cmd in commands]


for p in processes: p.wait()
print("terminated")

# out, err = proc.communicate()

# print(" - OUT:", out.decode("utf-8").strip())

# if err is not None:
#     print(" - ERR:", err.decode("utf-8").strip())
# else:
#     print(" - ERR: None")
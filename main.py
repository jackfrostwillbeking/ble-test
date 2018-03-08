import subprocess

res = subprocess.call(["/bin/bash","-c","./test_script.sh"])
sys.stdout.write("########")
sys.stdout.write("res")
sys.stdout.write("########")

sys.exit(0)

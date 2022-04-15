import subprocess
import os

def change_mode():
    os.chmod('MDump', 0o755)
    os.chmod('MRestore', 0o755)

def run_sozin_to_hark_backup():
    rc = subprocess.call("./MDump")
    print(rc)

def run_hark_restore():
    rc = subprocess.call("./MRestore")
    print(rc)

def set_environment_variable(key: str, value: str):
    os.environ[key] = value

change_mode()
# run_sozin_to_hark_backup()
# set_environment_variable("TESTING", "DAMNSTRAIGHT")
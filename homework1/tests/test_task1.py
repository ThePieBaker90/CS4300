# i absolutely LOVE how this assumes we know how to do things between files in python!
# Cause i fuckin' dont!

#This entire thing is AI generated:
#I believe that this stuff is far too complicated to expect someone whose
#Never taken a python class ever. This is too much to expect someone to learn
#In addition to the stuff the class already has. PLEASE PLEASE PLEASE use
#A language that everyone took as a required class such as uhhhh idk, C!!!!!
# test_task1.py

import subprocess
import sys
from pathlib import Path


def test_task1_output():
    task_path = Path(__file__).parent / "../src/task1.py"
    result = subprocess.run(
        [sys.executable, str(task_path)],
        capture_output=True,
        text=True
    )

    assert result.stdout.strip() == "Hello, World!"
    assert result.returncode == 0


if __name__ == "__main__":
    test_task1_output()
    print("Test passed.")
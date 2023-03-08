import subprocess
import sys
from pathlib import Path

try:
  process = subprocess.Popen(['python', '-m', 'pytest', '--cov=src'])
  return_code = None
  while True:
    return_code = process.poll()
    if return_code != None:
      break

  Path("target").mkdir(parents=True, exist_ok=True)
  with open('target/test_results.txt', 'w+') as f:
    if return_code == 0:
      f.write("PASS")
    else:
      f.write("FAIL")
except:
  print("Unexpected error:", sys.exc_info()[0])
  with open('target/test_results.txt', 'w+') as f:
    f.write("FAIL")
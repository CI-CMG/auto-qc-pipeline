import subprocess
import sys

try:
  process = subprocess.Popen(['python', '-m', 'pytest'])
  return_code = None
  while True:
    return_code = process.poll()
    if return_code != None:
      break

  with open('target/test_results.txt', 'w+') as f:
    if return_code == 0:
      f.write("PASS")
    else:
      f.write("FAIL")
except:
  print("Unexpected error:", sys.exc_info()[0])
  with open('target/test_results.txt', 'w+') as f:
    f.write("FAIL")
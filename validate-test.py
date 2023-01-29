code = 0
with open('target/test_results.txt', 'r') as f:
  result = f.read()
  if result == 'FAIL':
    code = 1

exit(code)


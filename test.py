import re
match = re.fullmatch(r'\w1\w', '3133')
print(True if match else False)
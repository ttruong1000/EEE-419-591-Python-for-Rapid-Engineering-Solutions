import re
my_text = '<MOD<2357>X>'
match = re.search(r'<.*?>', my_text)
if match:
    print(match.group())
else:
    print('did not find')
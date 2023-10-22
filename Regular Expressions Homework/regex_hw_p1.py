import re
str = '### Subject: scuba diving at... From: steve.millman@asu.edu Body: Underwater, where it is at'
match = re.search(r'[\w ]*at$', str)
if match:
    print(match.group())
else:
    print('did not find')
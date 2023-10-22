import re

# NOTES
# (...) capture and place in a group
# (?:...) part of the match but NOT into a separate group
# (?<=...) do NOT capture, but must come before the following match
# (?=...) do NOT capture, but must come after the following match

# Find pattern that starts with 'the' and ends with a space but don't include
# the space and follows an _ but don't include the _. 
str1 = 'hello therefore hello_thereby so'
find_there = re.search(r'',str1)
print(find_there)

# Find pattern that starts with X or Y, has 2 digits, and ends with B
# but don't include the B in the match!
str2 = 'Model X25A versus Model Y25B'
find_by = re.findall(r'',str2)
print(find_by)
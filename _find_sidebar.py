import re

c = open('c:/Users/user/Desktop/test/user_admin.html', encoding='utf-8').read()
lines = c.split('\n')
for i, line in enumerate(lines, 1):
    if any(x in line.lower() for x in ['sidebar', 'side-nav', 'nav-item', '#ff6', '#f90', '#ffa', 'orange', 'yellow', 'aside', 'background', 'left-nav', 'sidenav']):
        print(f'{i}: {line.rstrip()}')

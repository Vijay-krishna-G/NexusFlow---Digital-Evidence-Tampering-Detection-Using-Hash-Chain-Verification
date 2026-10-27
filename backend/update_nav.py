import os
import glob

search_str = "{% elif request.user.role == 'user' %}\n                <li><a href=\"{% url 'home' %}\">Home</a></li>"
replace_str = "{% elif request.user.role == 'user' %}\n                <li><a href=\"{% url 'home' %}\">Home</a></li>\n                <li><a href=\"{% url 'user_case_history' %}\">History</a></li>"

d = r'd:\django projects\Digital Evidence Tampering\backend\templates'

for f in glob.glob(d + '/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if search_str in content:
        content = content.replace(search_str, replace_str)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated {f}')

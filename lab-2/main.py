import socket
import time
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("fucking-great-advice.ru", 80))


def get_page_content(id):
    request = 'GET /advice/' + str(id) + '/ HTTP/1.1\nHost: fucking-great-advice.ru\n\n'
    s.sendall(request)
    time.sleep(1.0)     # 1 second delay
    response = ''
    chunk = s.recv(14000)
    while chunk:
        response += chunk
        if len(response) >= 14000:
            break
        chunk = s.recv(14000)
    return response


def get_quote(html_page):
    match = re.search('''<p id="advice">(.*)</p>''', html_page)
    if match:
        return match.group(1).replace('&nbsp;', ' ')

f = open('russian_quotes.txt', 'w')
for i in range(100, 200):
    page = get_page_content(i)
    print str(i) + " " + str(get_quote(page))
    quote = str(get_quote(page))
    if quote == 'None':
        continue
    else:
        f.write('%\n' + quote + '\n')

f.close()
s.close()
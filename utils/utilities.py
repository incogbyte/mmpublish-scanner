


def parse_url(url):
    print(f"[INFO] parsing URL {url}")
    if url[-1] == '/':
        new_url = url[0:-1]
        return new_url
    return url


def banner():
    proxy = """ 
 
 author: rodnt
 twitter: @rodntt
 description: Small tool to exploit misconfigured mmpublish instances
 usage: python3 main.py --url https://mmpublish.com
 __   __  __   __  _______  _______  _______  _______  __    _ 
|  |_|  ||  |_|  ||       ||       ||       ||   _   ||  |  | |
|       ||       ||    _  ||  _____||       ||  |_|  ||   |_| |
|       ||       ||   |_| || |_____ |       ||       ||       |
|       ||       ||    ___||_____  ||      _||       ||  _    |
| ||_|| || ||_|| ||   |     _____| ||     |_ |   _   || | |   |
|_|   |_||_|   |_||___|    |_______||_______||__| |__||_|  |__|
 
 
 """

    print(proxy)

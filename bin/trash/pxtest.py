from main import pxcs
from requests import get

def test(proxy: str):
    try:
        response = get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        print(f"Proxy {proxy} works. Response: {response.json()}")
    except Exception as e:
        print(f"Proxy {proxy} failed. Error: {e}")


def test1():
    pxarr = pxcs()
    for proxy in pxarr:
        test(proxy)

def test2():
    print(pxcs())

a = int(input(">>>"))

if a == 1:
    test1()
elif a == 2:
    test2()

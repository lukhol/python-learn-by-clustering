# https://jupyter.org/try

import http.client
import requests

# ========== for/if for creating collections ==========
arr = [i for i in range(10) if i % 2 == 0]

# ========== lambda ==========
arr = filter(lambda x: x > 2, arr)
print(list(arr))

# ========== args and kwargs ==========
def argsFun(*args, **kwargs):
    a, b, c = args
    print(a, b, c) # 1 2 3
    print(args) # (1,2,3)
    print(*args) # 1 2 3
    
    print(kwargs) # {'first': '1', 'second': 2}
    print(*kwargs) # first second
    print(kwargs['first']) # 1
    print(kwargs['second']) # 2
    
    
argsFun(1, 2, 3, first = "1", second = 2)

print(" ========= ")
# ========== arr[start:stop:step] ==========
arr = [1,2,3,4,5,6]
print(arr[-1]) # last element
print(arr[::-1]) # reverse

myTuple = (1,2,3,4,5,6,7,8,9)
print(myTuple[::-3])

# ========== types ==========
def funWithType(value: str):
    print(value)
    
funWithType('From func with type')

# ========== with ==========

# ========== pass ==========
def funWithoutBody():
    pass # With pass it not require body of function/if statement etc.

funWithoutBody()

# ========== @property ==========

# ========== HTTP ==========
connection = http.client.HTTPSConnection("www.google.com")
connection.request("GET", "/")
response = connection.getresponse()
connection.close()

r = requests.get("http://www.google.com")
print(r.content)

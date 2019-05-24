import base64,gzip,json,zlib

token='eyJhbGciOiJSUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAD3OPw-CMBCH4e9yM0Ov5aAwahwcnBycaXtI_QOEQmJD-O6WmLi-l-eXW6E3LdRIqpAKC11mEGKY-X0cHKcuVAY-BKghLn30HfdPjpABf8afUqjVrnwz_2eqPSyBJ6hX8C7hMidBKCkXlc4RSaaJ0A3jeT8mImRREmwZPGafiiUy2lTYusbl3BrTlrYRiEzGWYuc9Gu4-_46LJNNb8LldjrA9gV3lAp2zQAAAA.BBuIl2Ae0cDTCXo8SLr8pk0NNJpfCf1AFntbPPYuQqLhHDkCo0NP7xFmr5YQEsfM8J27_t7JcV2g3N2v-YazQyTcLUBq9aDRpZb1ilBPq1vBM9T2Ojiu5k7p16hoaHZAx6UX0XzFktzm49b_UuEAmCteHj9z1fLIYVy5B9aO_6g'

sp=token.split('.')
a=sp[0].replace(r'-',r"+").replace(r'_',r"/")+'=='
b=sp[1].replace(r'-',r"+").replace(r'_', r"/")+'=='
a=a.encode('gbk')
headers=base64.b64decode(a)

b=b.encode('gbk')
print(b)
body=base64.b64decode(b)
body = gzip.decompress(body)
body=body.decode('gbk')
print(body)


token1='"nbf":1535619705,"systemCode":103,"iss":"yunyihenkey","exp":1535706405,"iat":1535620005,"user":{"id":"66666666666","shopId":"6666666"},"jti":"489e410e6e0f42bf9f35977f629e9751","loginSource":"MWEB"}'

aaaa=token1.encode('gbk')
aaa=gzip.compress(aaaa)
bbb=base64.b64encode(aaa)
print(bbb)
bbbb=bbb.decode('gbk')
print(bbbb)

b=sp[1].replace(r'-',r"+").replace(r'_', r"/")+'=='
bbbb=bbbb.replace('+','-').replace('/','_')
print(bbbb)
# 123456789




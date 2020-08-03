import re
st = "处女心经오!수정(2000)"
# result = ''.join(re.findall(r'[\u4e00-\u9fa5_()a-zA-Z0-9]', st))
result = ''.join(re.findall(r'[\u4e00-\u9fa5_()a-zA-Z0-9]', st))
print(result)
from types import MappingProxyType

number_dict = dict(one=1, two=2, three=3, four=4, five=5)

unmutable_dict = MappingProxyType(number_dict)

print(unmutable_dict)

try:
    unmutable_dict["six"] = 6
except TypeError as e:
    print(e)
number_dict["six"] = 6
print(number_dict)
print(unmutable_dict)

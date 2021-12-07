from ipwhois import IPWhois

obj = IPWhois('84.82.234.240')

print(obj)
response = obj.lookup_whois()
#res=obj.lookup()
print(response)

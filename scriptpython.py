import re
pattern = re.compile('[0-9]{8,8}[A-Za-z]')
#print(pattern)
count=0;
for i, line in enumerate(open('BOE-A-2015-5834.txt')):
     #print(i,line)
     #print(re.finditer(pattern,line))
     for match in re.finditer(pattern, line):
        #print(match)
        print('Encontrados en línea %s: %s' % (i+1, match.group()))
        count=count+1

print("Numero total de dnis encontrados: ",count)

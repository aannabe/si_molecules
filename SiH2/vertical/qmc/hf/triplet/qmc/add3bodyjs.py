import numpy as np

#f = open('qw.slater','w')
output = []
count = 0
with open('qw.jast3', 'r') as fhand:
    for line in fhand.readlines():
         if 'threebody' in line or 'THREEBODY' in line:
             count += 1
         if count > 0 and count < 5:
             count += 1
             output += [line]
fhand.close()

line_num = 0
with open('qw.opt.wfout','r') as f:
    for line in f.readlines():
        if line.split()[0] == 'twobody' or line.split()[0] == 'TWOBODY':
            break
        line_num += 1
f.close()


with open('qw.opt.wfout','r') as f:
     contents = f.readlines()
f.close

#print(contents)
#print(line_num)
#print(len(output))
contents.insert(line_num,''.join(output))

#print(''.join(contents))
with open('qw.opt.wfout','w') as f:
    contents = "".join(contents)
    f.write(contents)
f.close()


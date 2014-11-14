import sys
import requests

if len(sys.argv) != 3:
    print 'argv error, you need print python XXX.py URL1 newFileName'
    exit(0)

r = requests.get(sys.argv[1])
file('File/'+sys.argv[2],'w').write(r.content)
print 'save succeed'

#!/usr/bin/python
import sys
import zlib
import marshal
import py_compile
import os

def inject(filename, data):
    template = """#!/usr/bin/python
import sys
import zlib
import marshal
a = {}
eval(marshal.loads(zlib.decompress("".join([chr(ord(a[i%32])^ord(a[i])) for i in range(32,len(a))]))))
b = open({}).read().split(chr(10))[:-1]
c = open('/dev/urandom').read(32)
b[4] = "a = " + repr("".join([chr(ord(a[i])^ord(c[i%32])) for i in range(len(a))]))
with open({},'w') as e:
    for i in b:
        e.write(i + chr(10))
""".format(repr(data), repr(filename), repr(filename))
    with open(filename,'w') as f:
        f.write(template)

def main():
    if (len(sys.argv) > 1) and ('.py' in sys.argv[1]):
        code = open(sys.argv[1]).read()
        data = list(zlib.compress(marshal.dumps(compile(code, 'script.py', 'exec'))))
        rand = open('/dev/urandom').read(32)
        pack = "".join([chr(ord(data[i])^ord(rand[i%32])) for i in range(len(data))])
        inject(sys.argv[1], rand+pack)
    else:
        print "Usage: python loki.py filename"

if __name__ == "__main__":
    main()





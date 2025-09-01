from pyutils.class_test import Doctor
from datetime import datetime

if __name__=='__main__':
    # builtin abs
    print(abs(-1))
    print(abs(-1.1))
    print(abs(0))
    print(abs(3+4j))
    print(abs(Doctor(name='hachi',sex=False,birth=datetime(2023,8,10))))

    # builtin all
    itemgt0=[item>0 for item in [1,2,3]]
    print(all(itemgt0), any(itemgt0))

    # unicode to string 0~1114111, 0x0~0x10ffff
    print(chr(99), chr(8364), chr(0x1f625), '😥')
    print(hex(ord('😥')), ord('A'))

    # filter 
    print(list(filter(lambda x:x>0, [-1,1,10,20,-90,983,422,-2212])))
    print(list(filter(lambda d:'fs'in d and d['fs']>0, [{},{'fd':1},{'fs':-1},{'fs':222},{'fd':-5,'fs':-999},{'fd':40,'fs':8888}])))

    # map
    print(list(map(lambda x:str(x), [1,2,3,4,5])))

    # sum
    print(sum([1,2,3]))

    # pairfunc
    print(list(zip([x for x in range(1,10,2)], ['mos','cat','job'])))
    print(tuple(zip([x for x in range(1,10,2)], ['mos','cat','job'])))
    print(dict(zip([x for x in range(1,10,2)], ['mos','cat','job'])))
    print(list(enumerate(['mos','cat','job'])))
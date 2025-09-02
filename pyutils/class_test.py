from pyutils import (
    BaseType,
    datetimenow,
    write_obj2file,
    read_obj4file,
)
import datetime
from typing import Any
from typing_extensions import Self
from dateutil.relativedelta import relativedelta
from typing import TypeVar, Generic
from math import sqrt

_Tp_S = TypeVar('_Tp_S', str,bytes,bytearray)
_Tp_I = TypeVar('_Tp_I', int,float)

class Doctor(BaseType):
    name:str
    sex:bool
    birth:datetime.datetime
    desc:str
    family:list['Doctor']
    mates:list['Doctor']
    children:dict[str,'Doctor']

    def __init__(self, name:str,sex:bool,birth:datetime.datetime,
                 desc='',
                 family:list['Doctor']=[],
                 mates:list['Doctor']=[],
                 children:dict[str,'Doctor']={},
                ) -> None:
        self.name=name
        self.sex=sex
        self.birth=birth
        self.desc=desc
        self.family=family
        self.mates=mates
        self.children=children

    def __str__(self) -> str:
        return '{'f'name: {self.name}, sex: {"male" if self.sex else "female"}, age: {self.age()}''}'
    
    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other:'Doctor') -> Self:
        self.name+=other.name
        self.sex|=other.sex
        self.birth=min(self.birth,other.birth)
        return self

    def age(self) -> float:
        curtime=datetimenow()
        deltatime=relativedelta(curtime, self.birth)
        return round(deltatime.years + deltatime.months/12 + deltatime.days/365.2425, 1)

    def __getitem__(self, key:str) -> Any:
        match key:
            case 'name':
                return self.name
            case 'sex':
                return self.sex
            case 'age':
                return self.age()
            case 'birth':
                return self.birth.strftime('%m.%Y')
            case _:
                return None
    def __setitem__(self, key:str, value:Any) -> None:
        match key:
            case 'desc':
                if isinstance(value,str):
                    self.desc=value
            case 'family':
                if isinstance(value,list):
                    self.family.extend(value)
                elif isinstance(value,'Doctor'):
                    self.family.append(value)
            case 'mates':
                if isinstance(value,list):
                    self.mates.extend(value)
                elif isinstance(value,'Doctor'):
                    self.mates.append(value)
            case _:
                pass
    
    def __getattr__(self, name: str) -> Any:
        match name:
            case 'age_ch':
                return self.age()+1
            case 'age_ut':
                return self.age()
            case _:
                return None

    def __abs__(self) -> str:
        return str(self)
    
    @classmethod
    def some_new(cls, **kw) -> 'Doctor':
        return cls(**kw)
    
    @staticmethod
    def some_add(a,b:int) -> int:
        return a+b
    
    def __call__(self, s:str):
        self.desc=s

    def copy(self) -> 'Doctor':
        return Doctor(
            name=self.name,
            sex=self.sex,
            birth=self.birth,
            desc=self.desc,
            family=self.family.copy(),
            mates=self.mates.copy(),
            children=self.children.copy(),
        )

def test_Doctor():
    dct=Doctor(
        name='Hachimi',
        sex=False,
        desc='哈基米南北绿豆',
        family=[],
        mates=[],
        children={},
        birth=datetime.datetime(2000,1,1),
    )
    dct['age']=110
    dct['hachi']='value' # key(field) not in class
    dct['birth']=10      # key not in case
    dct['age']='kumi'    # value type not match
    # encode obj to json
    write_obj2file(dct, 'data/test/doctor')

    # decode json to obj
    dct2=Doctor(**{'name':'hachi', 'sex': False, 'birth': datetime.datetime(2000,12,2)})
    print(dct2['age'])
    dct3=dct2.copy()
    print(dct3.desc)
    dct3('hachimi')
    print(dct3.desc)

    print(dct3.age_ch)
    print(dct3.age_utc)

class PointT(Generic[_Tp_I]):
    x:_Tp_I
    y:_Tp_I
    z:_Tp_I

    def __init__(self,x:_Tp_I,y:_Tp_I,z:_Tp_I) -> None:
        self.x=x
        self.y=y
        self.z=z

    def __add__(self, other:'PointT') -> 'PointT':
        return PointT(
            self.x+other.x,
            self.y+other.y,
            self.z+other.z,
        )

    def __sub__(self, other:'PointT') -> 'PointT':
        return PointT(
            self.x-other.x,
            self.y-other.y,
            self.z-other.z,
        )
    
    def __mul__(self, other:'PointT') -> int:
        return self.x*other.x+self.y*other.y+self.z*other.z

    def __abs__(self) -> float:
        return sqrt(pow(self.x,2)+pow(self.y,2)+pow(self.z,2))

    def __index__(self) -> int:
        return int(abs(self))
    
    def __float__(self) -> float:
        return abs(self)
    
    def __str__(self) -> str:
        return f'PointT({self.x},{self.y},{self.z})'

    def __repr__(self) -> str:
        return str(self)

def test_Point():
    p1,p2=PointT(1,2,3),PointT(1.1,2.2,3.3)
    print(p1,p2,sep=',')
    print(p1+p2)
    print(p1-p2)
    print(p1*p2)
    print(int(p1)*int(p2))
    print(float(p1)*float(p2))

if __name__=='__main__':
    test_Point()
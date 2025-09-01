from pyutils import (
    BaseType,
    datetimenow,
    write_obj2file,
    read_obj4file,
)
import datetime
from typing import Any
from typing_extensions import Self

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

    def age(self) -> int:
        return datetimenow().year-self.birth.year

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
    
    def __abs__(self) -> str:
        return str(self)
    
    @classmethod
    def some_new(cls, **kw) -> 'Doctor':
        return cls(**kw)
    
    @staticmethod
    def some_add(a,b:int) -> int:
        return a+b

if __name__=='__main__':
    dct=Doctor(
        name='Hachimi',
        sex=False,
        desc='哈基米要怎样',
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
    dct2=Doctor(**{'name':'hachi', 'sex': False, 'birth': datetime.datetime(2001,11,22)})
    print(dct2['age'])
    dc1={}
    dct3=Doctor(**dc1)
    print(dct3)
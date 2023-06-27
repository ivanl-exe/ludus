from os import urandom
from base58 import b58encode
from collections import defaultdict 
from json import dumps, loads
from pickle import dump, load, HIGHEST_PROTOCOL

class Viewport:
    def __init__(self, width: int, height: int) -> None:
        self.x, self.y, self.z = 0, 0, 0
        self.width, self.height = width, height
    
    def position(self, x: int, y: int, z: int) -> None:
        self.x, self.y, self.z = x, y, z
    
    def resize(self, width: int, height: int) -> None:
        self.width, self.height = width, height

class Ludus(Viewport):
    def __init__(self) -> None:
        self.objects = defaultdict(dict)
        self.__grouping__()
    
    def __id__(prefix: str, n: int = 16) -> str:
        id = b58encode(urandom(n)).decode('UTF-8')
        return f'{prefix}-{id}'
    
    def new_object(self) -> str:
        return Ludus.__id__('u')

    def new_group(self) -> str:
        return Ludus.__id__('g')

    def get(self, id: str) -> dict:
        prefix = id[:id.rfind('-')]
        object = {}
        if prefix == 'u': object = self.objects[id]
        elif prefix == 'g': object = self.groups[id]
        return object
    
    def add_object(self, props: dict = {}, gid: list = None) -> None:
        uid = self.new_object()
        values = defaultdict(None)
        values.update({'gid': [], **props})
        self.objects.update({uid: values})
        if gid != None: self.attach_group(uid, gid)
        return uid

    def remove_object(self, uid: str) -> None:
        gid = self.objects[uid]['gid']
        for group in gid:
            self.groups[group].remove(uid)
            if len(self.groups[group]) == 0: del self.groups[group]
        del self.objects[uid]
    
    def attach_group(self, uid: str, gid: list) -> None:
        self.groups[gid].append(uid)
        if type(gid) == str: gid = [gid]
        self.objects[uid]['gid'].extend(gid)
    
    def detach_group(self, uid: str, gid: list) -> None:
        if type(gid) == str: gid = [gid]
        groups = self.objects[uid]['gid']
        groups = [group for group in groups if group not in gid]
        self.objects[uid]['gid'] = groups
        for group in gid:
            self.groups[group].remove(uid)
            if len(self.groups[group]) == 0: del self.groups[group]

    #def update(self, callback = None, *args) -> None:
    #    if callback != None: callback(*args)
    
    def render(self, viewport: Viewport) -> None:
        pass

    def __grouping__(self) -> None:
        self.groups = defaultdict(list)
        for uid, values in self.objects.items():
            groups = values['gid']
            for gid in groups:
                self.groups[gid].append(uid)

    def serialize(self, indent: int = 0) -> str:
        return dumps(self.objects, indent = indent)
    
    def deserialize(self, objects: str) -> None:
        self.objects = loads(objects)
        self.__grouping__()
    
    def dump(self, handle) -> None:
        dump(self.objects, handle, protocol = HIGHEST_PROTOCOL)
        handle.close()
    
    def load(self, handle) -> None:
        self.objects = load(handle)
        self.__grouping__()
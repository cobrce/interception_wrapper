import struct

class stroke():
    @property
    def data(self):
        raise NotImplementedError

class mouse_stroke(stroke):

    fmt = 'HHhiiI'    
    state = 0
    flags = 0
    rolling = 0
    x = 0
    y = 0    
    information = 0

    def __init__(self):
        super().__init__()
    
    @staticmethod
    def parse(data):
        return key_stroke(*struct.unpack(mouse_stroke.fmt,data))        

    @property
    def data(self):
        data =  struct.pack(self.fmt,self.state,self.flags,self.rolling,self.x,self.y,self.information)
        while len(data) < 20:
            data+=b'\0'
        return data

class key_stroke(stroke):

    fmt = 'HHI'
    code = 0
    state = 0
    information = 0
    
    def __init__(self,code,state,information):
        super().__init__()
        self.code = code
        self.state = state
        self.information = information
    
    
    @staticmethod
    def parse(data):
        return key_stroke(*struct.unpack(key_stroke.fmt,data))
    
    @property
    def data(self):
        data = struct.pack(self.fmt,self.code,self.state,self.information)
        while len(data) < 20:
            data+=b'\0'
        return data
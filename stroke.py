import struct

class stroke():
    @property
    def data(self):
        raise NotImplementedError

class mouse_stroke(stroke):

    fmt = 'HHhiiI'
    fmt_raw = 'HHHHIiiI'
    state = 0
    flags = 0
    rolling = 0
    x = 0
    y = 0    
    information = 0

    

    def __init__(self,state,flags,rolling,x,y,information):
        super().__init__()
        self.state =state
        self.flags = flags
        self.rolling = rolling
        self.x = x
        self.y = y
        self.information = information
    
    @staticmethod
    def parse(data):
        return mouse_stroke(*struct.unpack(mouse_stroke.fmt,data))        

    @staticmethod
    def parse_raw(data):
        unpacked= struct.unpack(mouse_stroke.fmt_raw,data)
        return  mouse_stroke(unpacked[1],unpacked[2],unpacked[3],unpacked[5],unpacked[6],unpacked[7])

    @property
    def data(self):
        data =  struct.pack(self.fmt,self.state,self.flags,self.rolling,self.x,self.y,self.information)
        while len(data) < 20:
            data+=b'\0'
        return data

class key_stroke(stroke):

    fmt = 'HHI'
    fmt_raw = 'HHHHI'
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
    
    @staticmethod
    def parse_raw(data):
        unpacked= struct.unpack(key_stroke.fmt_raw,data)
        return  key_stroke(unpacked[1],unpacked[2],unpacked[4])

    @property
    def data(self):
        data = struct.pack(self.fmt,self.code,self.state,self.information)
        while len(data) < 20:
            data+=b'\0'
        return data
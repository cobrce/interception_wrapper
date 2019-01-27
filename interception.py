import ctypes
from stroke import *
from consts import  *
from typing import overload

class interception():
    _buffer =  (ctypes.c_byte * 500)()
    def __init__(self):
        self._hinstance =ctypes.cdll.LoadLibrary("interception.dll")
        self._context  = self._hinstance.interception_create_context()

    def get_precedence(self,device:int):
        return self._hinstance.interception_get_precedence(device)

    @property
    def is_keyboard_predict(self):
        return self._hinstance.interception_is_keyboard
    
    @property
    def is_mouse_predict(self):
        return self._hinstance.interception_is_mouse

    def set_keyboard_filter(self,fltr):
        self.set_filter(self.is_keyboard_predict,fltr)
     
    def set_mouse_filter(self,fltr):
        self.set_filter(self.is_mouse_predict,fltr)

    def set_filter(self,predict,fltr):
        func = ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int)(predict)
        self._hinstance.interception_set_filter(self._context,func,ctypes.c_ushort(fltr))

    def get_filter(self,device : int):
        return self._hinstance.interception_get_filter(self._context,device)
    
    def wait(self, timeout_ms: int = -1 )->int:
        if timeout_ms == -1:
            return self._hinstance.interception_wait(self._context)
        else:
            return self._hinstance.interception_wait_with_timeout(self._context,ctypes.c_ulong(timeout_ms))
    
    def send(self,device:int,stroke:stroke)->int:
        data = stroke.data
        ctypes.memmove(self._buffer,data,len(data))
        return self._hinstance.interception_send(self._context,device,self._buffer,1)
    
    def receive(self,device : int)->stroke:
        self._hinstance.interception_receive(self._context,device,self._buffer,20)
        if self.is_keyboard_predict(device) > 0 :
            return key_stroke.parse(bytearray(self._buffer)[:8])
        elif self.is_mouse_predict(device) > 0:
            return mouse_stroke.parse(bytearray(self._buffer)[:18])

    def get_hardware_id(self,device:int)->bytes:
        size =  self._hinstance.interception_get_hardware_id(self._context,device,self._buffer,500)
        try:
            buffer = bytearray(self._buffer)
        except:
            pass
        if size > 0 and size:
            return buffer[:size]
        else:
            return b''
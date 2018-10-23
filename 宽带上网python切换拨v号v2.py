import os
import time
g_adsl_account = {"name": "�������",
                "username": "test9421",
                "password": "1578"}

class Adsl(object):
    #==============================================================================
    # __init__ : name: adsl����
    #==============================================================================
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

    #==============================================================================
    # set_adsl : �޸�adsl����
    #==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

    #==============================================================================
    # connect : �������
    #==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(5)

    #==============================================================================
    # disconnect : �Ͽ��������
    #==============================================================================
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)
        time.sleep(5)

    #==============================================================================
    # reconnect : ���½��в���
    #==============================================================================
    def reconnect(self):
        self.disconnect()
        self.connect()

if __name__ == "__main__":
    aa=Adsl()
    aa.reconnect()
    

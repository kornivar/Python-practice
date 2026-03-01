class ClientData:
    def __init__(self, conn, addr, id):
        self._conn = conn
        self._addr = addr
        self._id = id

    @property
    def conn(self):
        return self._conn

    @property
    def addr(self):
        return self._addr

    @property
    def id(self):
        return self._id
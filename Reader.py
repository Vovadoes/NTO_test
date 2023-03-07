class Reader:
    def __init__(self, a_serial, max_delay = 0.5, eol=b'\n'):
        self.a_serial= a_serial
        self.eol= eol
        self.max_delay= max_delay
        self.leneol = len(eol)
        self.line = bytearray()

    def readline(self):
        time_old = time()
        flag = True
        while True:
            c = self.a_serial.read(1)
            if c:
                self.line += c
                if self.line[-self.leneol:] == self.eol:
                    break
            else:
                break
            if time_old - time() > self.max_delay:
                flag = False
                break
        if flag:
            return bytes(self.line)
        return bytes('')
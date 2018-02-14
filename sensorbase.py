from bluepy import btle
from logging import getLogger
import threading
import time


logger = getLogger(__name__)

def get_sensor(addr):
    per = blts.Peripheral(addr)
    service = per.ServiceByUUID('19b10000-e8f2-537e-4f6c-d104768a1214')
    static = service.getCharacteristics()

    return ord(static.read()[0])


class DistanceSensor(threading.Thread):
    def __init__(self, addr, *args, **kwargs):
        super(DistanceSensor, self).__init__(*args, **kwargs)

        self.addr = addr
        self.logger = getLogger('.'.join([__name__, self.addr]))
        self.connection = None
        self._running = True
        self.state = None

    def _connect(self):
        if self.connection is None:
            self.logger.debug('[INFO] Create a new connection')
            self.connection = btle.Peripheral(self.addr)
            time.sleep(0.3)
            self.service = self.connection.getServiceByUUID('19b10000-e8f2-537e-4f6c-d104768a1214')
            self.static = self.service.getCharacteristics()[0]

    def run(self):
        while self._running:
            try:
                self._connect()
                self.state = ord(self.static.read())
                time.sleep(1)
            except btle.BTLEException as e:
                self.logger.debug('[ERROR] BTLE Exception')
                self.connection = None
                self.service = None
                self.state = None
                self.logger.exception(e)
                time.sleep(1)
            except BrokenPipeError:
                self.logger.debug('[ERROR] Catch a broken pipe error')
                break
            except Exception as e:
                self.logger.exception(e)
                break
            time.sleep(1)

        self.logger.debug('[INFO] Exit from threaded reader')

    def join(self, timeout=2):
        self.logger.debug('[INFO] Get a join signal')
        self._running = False
        super(DistanceSensor, self).join(timeout)


if __name__ == '__main__':
    sensor = DistanceSensor('98:4f:ee:0f:cc:60')
    sensor.start()

    for i in range(20):
        print(sensor.state)
        time.sleep(1)

    sensor.join()

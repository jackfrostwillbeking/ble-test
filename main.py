from sensorbase import DistanceSensor
import time
import sys
import os
import subprocess

BLE_DEVICE1 = os.getenv('BLE_DEVICE1', 'Cannot load the env')

sensors = [
    BLE_DEVICE1,
    '98:4f:ee:0f:cc:60'
]

sensorObjs = []
for i in sensors:
    sensorObjs.append(DistanceSensor(i))

[ i.start() for i in sensorObjs]

subprocess.call(["/bin/bash"],["-c"],["./test_script.sh"])

try:
    while True:
        sys.stdout.write('---\r\n')
        for i in sensorObjs:
            sys.stdout.write(" sensor {0} : {1}\r\n".format(i.addr, i.state))
            time.sleep(1)

except SystemExit:
    sys.stdout("detect")
    pass

except KeyboardInterrupt:
    [ i.join() for i in sensorObjs]
    sys.exit(0)

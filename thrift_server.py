#!/usr/bin/env python
 
import sys
sys.path.append('./gen-py')

from collectd_thrift import OpenTSDBUpload
from collectd_thrift.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket
import time
import sys
import os

class OpenTSDBUploadHandler:
    upload_interval = 5

    def __init__(self, tsdb_exe):
        self.ts = int(time.time())
        self._create_cache()
        self._tsdb_exe = tsdb_exe
        self._counter = 0

    def _create_cache(self):
        self._fname = "/tmp/collectd-"+str(self.ts)
        self._fh = open(self._fname, "w")
    
    def _flush_upload(self):
        ts = int(time.time())
        if ts > self.ts + self.upload_interval:
            self._fh.close()
            # os.system("%s import %s" % (self._tsdb_exe, self._fname))
            # os.system("rm %s" % (self._fname))
            self._create_cache()
            self.ts = ts

    def upload(self, d):
        # : CollectdData(timestamp=12345, value=32, instance='vm1', dev='eth0', env='ewr', type='in_bytes')

        self._fh.write("%s %d %d instance=%s dev=%s env=%s\n" % 
            (d.vtype, d.timestamp, d.value, d.instance, d.dev, d.env))
        self._counter += 1
        if (self._counter == 10):
            self._flush_upload()
            self._counter = 0

if len(sys.argv) != 2:
    print "usage: python %s <tsdb_path>" % (sys.argv[0])
    exit(1)

handler = OpenTSDBUploadHandler(sys.argv[1])
processor = OpenTSDBUpload.Processor(handler)
transport = TSocket.TServerSocket(port=30303)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print "Starting python server..."

server.serve()
print "done!"

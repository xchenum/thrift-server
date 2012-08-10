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

class OpenTSDBUploadHandler:
    def __init__(self):
        self.fh = open("/tmp/thrift-tmp", "w")
        pass
    
    def upload(self, d):
        print "received data: " + str(d)

handler = OpenTSDBUploadHandler()
processor = OpenTSDBUpload.Processor(handler)
transport = TSocket.TServerSocket(port=30303)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print "Starting python server..."

server.serve()
print "done!"

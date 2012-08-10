#!/usr/bin/env python
 
import sys
sys.path.append('./gen-py')

from collectd_thrift import OpenTSDBUpload
from collectd_thrift.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import sys

try:
    # Make socket
    transport = TSocket.TSocket('localhost', 30303)
             
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
                  
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
                       
    # Create a client to use the protocol encoder
    client = OpenTSDBUpload.Client(protocol)
                            
    # Connect!
    transport.open()

    m = CollectdData(timestamp=int(sys.argv[1]), value=32, instance="vm1", dev="eth0", env="ewr", vtype="in_bytes")

    client.upload(m)

    transport.close()


except Thrift.TException, tx:
    print "%s" % (tx.message)

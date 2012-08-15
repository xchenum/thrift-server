#!/usr/bin/env python
 
import sys
sys.path.append('./gen-py')

from collectd_thrift import OpenTSDBUploadV2
from collectd_thrift.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import sys

if len(sys.argv) != 6:
    print "usage: python %s <server_IP> <server port> <file_list> <mapping> <env_name>" % (sys.argv[0])
    exit(1)

inst_to_tenant = {}

for line in open(sys.argv[4]):
    p = line.strip().split(" ")
    inst_to_tenant[ p[0].partition("-")[2] ] = p[1]

client = None

try:
    transport = TSocket.TSocket(sys.argv[1], int(sys.argv[2]))
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = OpenTSDBUpload.Client(protocol)
                            
    transport.open()

except Thrift.TException, tx:
    print "%s" % (tx.message)
    exit(1)

for line in open(sys.argv[3]):
    instance = line.strip().split("/")[-3].partition("-")[2]
    if not inst_to_tenant.has_key(instance):
        continue
    p = line.strip().split("/")[-1].split("-")

    dev = ""
    if (not p[0].startswith('virt_cpu_total')):
        dev = p[1]

    fh = open(line.strip())
    header = fh.readline()
    header = header.split(",")

    for l in fh.readlines():
        ar = l.strip().split(",")

        for i in range(1, len(ar)):
            d = CollectdDataV2()
            d.timestamp = int(ar[0])
            d.dev = dev
            d.env = sys.argv[5]
            d.vtype = p[0] + "_" + header[i]
            d.instance = instance
            d.tenant = inst_to_tenant[instance]
            d.value = int(ar[i])

            print d
            exit(0)

#!/usr/bin/env python
 
import sys
import os
sys.path.append('./gen-py')

from collectd_thrift import OpenTSDBUploadV2
from collectd_thrift.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


if len(sys.argv) != 5:
    print "usage: python %s <file_list> <mapping> <env_name> <tsdb_exe>" % (sys.argv[0])
    exit(1)

inst_to_tenant = {}

for line in open(sys.argv[2]):
    p = line.strip().split(" ")
    inst_to_tenant[ p[0].partition("-")[2] ] = p[1]

filecount = 0
for line in open(sys.argv[3]):
    filecount += 1
    print "file #" + str(filecount)

    instance = line.strip().split("/")[-3].partition("-")[2]
    if not inst_to_tenant.has_key(instance):
        continue
    p = line.strip().split("/")[-1].split("-")

    dev = ""
    if (not p[0].startswith('virt_cpu_total')):
        dev = p[1]

    fh = open(line.strip())
    header = fh.readline()
    header = header.strip().split(",")

    tmp = open("/tmp/uploader-v2", "w")

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

            # if_octets_rx 1344976838 1208917 instance=instance-00000016 dev=vnet9 env=fp
            w = "%s %d %d" % (d.vtype, d.timestamp, d.value)
            for tag in ['instance', 'dev', 'env', 'tenant']:
                if getattr(d, tag) is not None and getattr(d, tag) != "":
                    w += " %s=%s" % (tag, getattr(d, tag))

            tmp.write(w + "\n")
    tmp.close()

    os.system("%s import --zkquorum zk-1,zk-2,zk-3,zk-4,zk-5 /tmp/uploader-v2" % (sys.argv[4))
    os.system("rm %s" % (self._fname))



#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#

import sys
import os
import signal
import glob
import shutil
import threading
import csv
import random
import time
import collections
import argparse

from datetime import datetime, timedelta, tzinfo
from subprocess import Popen, PIPE
from optparse import OptionParser

#Importation des modules HPSA
sys.path.append("/opt/opsware/pylibs2")
from pytwist import twistserver
from pytwist.com.opsware.common import *
from pytwist.com.opsware.folder import *
from pytwist.com.opsware.server import ServerRef
from pytwist.com.opsware.search import Filter

def exportToCSV(csvFilePath, serversStruct):
              """
              export struct to CSV
              :param csvFilePath:
              :return:
              """
              allFieldNames = ['name', 'customer', 'OS', 'Managed', 'Reachable','facility', 'id'] # facility et MANAGED
              with open(csvFilePath, "wb") as f:
                   writerObj = csv.DictWriter(f, fieldnames=allFieldNames, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n", extrasaction='ignore')
                   writerObj.writer.writerow(allFieldNames)
                   writerObj.writerows(serversStruct)
              print "Successfully write CSV file %s" % csvFilePath

def getServerList():
        dgpath = '/opsw/Group/Public/Reference/Reference_statut/SADG_Reference_Reachable'
        currentPath = dgpath.strip('/').split('/')
        if currentPath[2] == 'Private':
                del(currentPath[3])
        InvRef = DevGrpSvc.getDeviceGroupByPath(currentPath[2:])
        DevGrpSvc.refreshMembership(InvRef, True)
        serverRefs = DevGrpSvc.getDevices(InvRef)
        return serverRefs

def getSvrVOs(svrRefs):
        dictVO={}
        serverVO = ServerSvc.getServerVOs(svrRefs)
        for server in serverVO:
                serverId = server.ref.getId()
                dictVO[serverId]={}
                for k, v  in sorted(server.__dict__.iteritems()):
                            dictVO[serverId].update({k:v})
                del(dictVO[serverId]['__OPSW_CHANGED_ATTRS__'])
        return dictVO

processTime = datetime.now()
TwistSvr = twistserver.TwistServer()
DevGrpSvc = TwistSvr.device.DeviceGroupService
ServerSvc = TwistSvr.server.ServerService

startTime=datetime.now()
Current_File = "/opsw/Server/@/th3intaadm001/files/root/opt/adm_automation/state/hpsaServerListExportCsv.csv"

print 'Get DB Server Info'
svrRef = getServerList()
print 'found '+str(len(svrRef))+' servers to treat'
serverDetail = getSvrVOs(svrRef)
print 'Elapsed Time '+str(datetime.now() - startTime)

startTime=datetime.now()
print 'Build CSV Table'
CSVTable = []
for id, record in serverDetail.iteritems():
              svrDict = {}
              svrDict['id'] = id
              svrDict['name'] = record.get('name')
              svrDict['OS'] = record.get('osVersion')
              svrDict['Reachable'] = record.get('state')
              svrDict['customer'] = record.get('customer').getName()
              svrDict['Managed'] = record.get('opswLifecycle')
              svrDict['facility'] = record.get('facility').getName()
              CSVTable.append(svrDict)
print 'Elapsed Time '+str(datetime.now() - startTime)
#print CSVTable
startTime=datetime.now()
print 'Write CSV File'
exportToCSV(Current_File, CSVTable)
print 'Elapsed Time '+str(datetime.now() - startTime)
print 'Full Time Processing '+str(datetime.now() - processTime)

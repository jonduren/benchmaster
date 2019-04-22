#!/usr/bin/python
import json
import sys
import os
import sys
testname = sys.argv[1]
protocols = ['rbd', 'cephfs']
iopattern = ['seqwrite','seqread','randwrite','randread','mixed','backup','recovery','kvm','oltp-log','oltp-data']
clivar1 = sys.argv[1]

def search_files(directory, extension='benchmark'):
        mylist= []
        extension = extension.lower()
        for dirpath, dirnames, files in os.walk(directory):
                for name in files:
                        if extension and name.lower().endswith(extension):
                            mylist.append(os.path.join(dirpath, name))
        return mylist

filelist=search_files(clivar1)
for thisproto in protocols:
    for this iopat in iopattern:
        for thisfile in filelist:
            if thisproto in thisfile and iopat in thisfile:
                print thisfile




                # print '*******TEST NAME: %s *******' %(testname)
                with open('temp.json', 'r') as f:
                    fiodata = json.load(f)
                testnodecount=len(fiodata['client_stats'])-1
                rwsetting = fiodata['client_stats'][0]['job options']['rw']
                readpercentage = fiodata['client_stats'][0]['job options']['rwmixread']
                maxiodepth = fiodata['client_stats'][0]['job options']['iodepth']
                jobspernode = fiodata['client_stats'][0]['job options']['numjobs']
                bs = fiodata['client_stats'][0]['job options']['bs']
                if bs == '64M':
                    bso = '65536'
                elif bs == '4M':
                    bso = '4096'
                elif bs == '1M':
                    bso = '1024'
                elif bs == '64k':
                    bso = '64'
                elif bs == '8k':
                    bso = '8'
                elif bs == '4k':
                    bso = '4'
                else:
                    bso = 'broken'

                if testname[0:2] == 'ec':
                    protection='EC 3+1'
                elif testname[0:3] =='rep':
                    protection="3x Rep"

                if 'latency_target' in fiodata['client_stats'][0]['job options']:
                    lattarget = fiodata['client_stats'][0]['job options']['latency_target']
                    latwindow = fiodata['client_stats'][0]['job options']['latency_window']
                    latpercentage = fiodata['client_stats'][0]['job options']['latency_percentile']
                else:
                    lattarget = 0
                    latwindow = 0
                    latpercentage = 0

                for x in range(0, len(fiodata['client_stats'])):
                    # Since fio v2.99 time resolution changed to nanosecond, json output key name changed from 'lat' to 'lat_ns' accordingly
                    lat_key = 'lat_ns' if 'lat_ns' in fiodata['client_stats'][x]['write'] else 'lat'

                    if lat_key == 'lat_ns':
                        latdiv = 1000000
                    else:
                        latdiv = 1000
                    if x == len(fiodata['client_stats'])-1:
                        writebw = fiodata['client_stats'][x]['write']['bw']/1024
                        writeiops = fiodata['client_stats'][x]['write']['iops']
                        writeavglat = fiodata['client_stats'][x]['write'][lat_key]['mean']/latdiv
                        writemaxlat = fiodata['client_stats'][x]['write'][lat_key]['max']/latdiv
                        readbw = fiodata['client_stats'][x]['read']['bw']/1024
                        readiops = fiodata['client_stats'][x]['read']['iops']
                        readavglat = fiodata['client_stats'][x]['read'][lat_key]['mean']/latdiv
                        readmaxlat = fiodata['client_stats'][x]['read'][lat_key]['max']/latdiv
                        print '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"' % (testname, bso, protection,rwsetting, readpercentage, maxiodepth, jobspernode, lattarget, latwindow, latpercentage, writebw, writeiops, writeavglat, writemaxlat, readbw, readiops, readavglat, readmaxlat)
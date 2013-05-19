 # -*- coding: utf-8 -*- #
import sys
import re

# data = sys.stdin.readlines()
data = '''[root@nj01-hpc-master00.nj01.baidu.com server_priv]# diff job_policy.conf job_policy.conf.20130410
174,177d173
<                 "platform_new_fe_merge_batch_per-sf_train_mpi:320:very_high:FOREVER:yf-fcr-pub01.yf01.baidu.com^szwg-fcr-training01.szwg01.baidu.com^db-fcr-csmodel00.db01.baidu.com^db-fcr-training00.db01.baidu.com^db-fcr-training01.db01.baidu.com^yf-fcr-adfea00.yf01.baidu.com^yf-fcr-adfea01.yf01.baidu.com^yf-fcr-training00.yf01.baidu.com^yf-fcr-training01.yf01.baidu.com^szwg-fcr-adfea00.szwg01.baidu.com^szwg-fcr-training00.szwg01.baidu.com^yf-fcr-rank00.yf01.baidu.com^tc-fcr-rank00.tc.baidu.com^nj01-fcr-stat00.nj01.baidu.com^dbl-fcr-pub00.dbl01.baidu.com^nj01-fcr-stat01.vm.baidu.com:/home/work:XXX"
<                 "platform_new_fe_merge_batch_nop-sf_train_mpi:280:very_high:FOREVER:yf-fcr-pub01.yf01.baidu.com^szwg-fcr-training01.szwg01.baidu.com^db-fcr-csmodel00.db01.baidu.com^db-fcr-training00.db01.baidu.com^db-fcr-training01.db01.baidu.com^yf-fcr-adfea00.yf01.baidu.com^yf-fcr-adfea01.yf01.baidu.com^yf-fcr-training00.yf01.baidu.com^yf-fcr-training01.yf01.baidu.com^szwg-fcr-adfea00.szwg01.baidu.com^szwg-fcr-training00.szwg01.baidu.com^yf-fcr-rank00.yf01.baidu.com^tc-fcr-rank00.tc.baidu.com^nj01-fcr-stat00.nj01.baidu.com^dbl-fcr-pub00.dbl01.baidu.com^nj01-fcr-stat01.vm.baidu.com:/home/work:XXX"
<                 "platform_new_fe_merge_delta_per-sf_train_mpi:40:very_high:FOREVER:yf-fcr-pub01.yf01.baidu.com^szwg-fcr-training01.szwg01.baidu.com^db-fcr-csmodel00.db01.baidu.com^db-fcr-training00.db01.baidu.com^db-fcr-training01.db01.baidu.com^yf-fcr-adfea00.yf01.baidu.com^yf-fcr-adfea01.yf01.baidu.com^yf-fcr-training00.yf01.baidu.com^yf-fcr-training01.yf01.baidu.com^szwg-fcr-adfea00.szwg01.baidu.com^szwg-fcr-training00.szwg01.baidu.com^yf-fcr-rank00.yf01.baidu.com^tc-fcr-rank00.tc.baidu.com^nj01-fcr-stat00.nj01.baidu.com^dbl-fcr-pub00.dbl01.baidu.com^nj01-fcr-stat01.vm.baidu.com:/home/work:XXX"
<                 "platform_new_fe_merge_delta_nop-sf_train_mpi:40:very_high:FOREVER:yf-fcr-pub01.yf01.baidu.com^szwg-fcr-training01.szwg01.baidu.com^db-fcr-csmodel00.db01.baidu.com^db-fcr-training00.db01.baidu.com^db-fcr-training01.db01.baidu.com^yf-fcr-adfea00.yf01.baidu.com^yf-fcr-adfea01.yf01.baidu.com^yf-fcr-training00.yf01.baidu.com^yf-fcr-training01.yf01.baidu.com^szwg-fcr-adfea00.szwg01.baidu.com^szwg-fcr-training00.szwg01.baidu.com^yf-fcr-rank00.yf01.baidu.com^tc-fcr-rank00.tc.baidu.com^nj01-fcr-stat00.nj01.baidu.com^dbl-fcr-pub00.dbl01.baidu.com^nj01-fcr-stat01.vm.baidu.com:/home/work:XXX"'''
data = data.split('\n')
tag = '{color:red}%s{color}'

JOB_NAME = 0
NODE_COUNT = 1
PRIORITY = 2
PIERIOD = 3
PATH = 5

for i in xrange(len(data)):
    if i == 0:
        data[i] = re.sub(r'@(.*.com)', '@%s'%(tag%r'\1'), data[i])
    elif i == 1:
        continue
    else:
        print data[i].split('"')
        tmp = data[i].split('"')[1]
        tmp = tmp.split(':')
        for j in [JOB_NAME, NODE_COUNT, PRIORITY, PATH]:
            tmp[j] = tag%tmp[j]
        tmp = ':'.join(tmp)
        data[i] = re.sub(r'".*"', r'"%s"'%tmp, data[i])

print '已按照要求添加（更新）白名单如下，请确认无误：'
print '\n'.join(data)

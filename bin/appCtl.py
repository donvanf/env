#!/usr/bin/python
# -*- coding: UTF-8 -*-
#_DEBUG=True
import getopt
import sys
import subprocess
import time

class appCtl():
    def __init__(self):
        try:
            self.opts, self.argv = getopt.getopt(sys.argv[1:], 'ho:')
        except getopt.GetoptError, e:
            print str(e)
            self.usage()
            sys.exit(2)
#        print self.argv
        if len(self.argv) == 0:
            self.usage()
            sys.exit()
        self.cmd = self.argv[0]
        if len(self.argv) == 2:
            self.args = self.argv[1]
        else:
            self.args = ''
        self.cur_procs = list()
    def usage(self):
        print 'Usage: %s -o <start|stop|status|restart> cmd [args]'%sys.argv[0]
    def start(self):
        if self.status() == 'running':
            return 'already run'
        else:
            command = '%s %s'%(self.cmd, self.args)
#            print 'start:',command
            subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(0.5)
            if self.status() == 'running':
                return 'ok'
            else:
                return 'failed'
    def stop(self):
        if self.status() == 'stopped':
            return 'already stopped'
        else:
            command = 'ps axu|grep -v grep|grep -v %s|grep \'%s\''%(__file__, self.cmd)
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result.wait()
            pids = result.communicate()[0]
            pids = [i.split()[1] for i in pids.strip().split('\n')]
            for pid in pids:
                command = 'kill -9 %s'%pid
                subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(0.5)
            if self.status() == 'running':
                return 'failed'
            else:
                return 'ok'
    def status(self):
        command = 'ps axu|grep -v grep|grep -v %s|grep \'%s\''%(__file__, self.cmd)
#        print 'status:',command
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.wait() == 0:
            self.cur_procs = result.communicate()[0].strip().split('\n')
            return 'running'
        else:
            self.cur_procs = list()
            return 'stopped'
    def display(self, func):
        txtgrn = '\033[32m %s \033[0m'
        txtylw = '\033[33m %s \033[0m'
        txtred = '\033[31m %s \033[0m'
        print '[old processes:]'
        for proc in self.cur_procs:
            print ' -', proc
        result = func()
        if result in ['ok']:
            result = txtgrn%result
        elif result in ['already run', 'already stopped', 'running', 'stopped']:
            result = txtylw%result
        elif result in ['failed']:
            result = txtred%result
        print '[ACTION - %s]:\t%s'%(func.func_name, result)
        print '[new processes:]'
        for proc in self.cur_procs:
            print ' +', proc
    def run(self):
        for o, a in self.opts:
            if o == '-o':
                self.status()
                if a == 'start':
                    self.display(self.start)
                elif a == 'stop':
                    self.display(self.stop)
                elif a == 'status':
                    self.display(self.status)
                elif a == 'restart':
                    self.display(self.stop)
                    self.display(self.start)
                else:
                    self.usage()
                    sys.exit()
                    assert False, "unhandled option"

if __name__ == '__main__':
    ac = appCtl()
    ac.run()

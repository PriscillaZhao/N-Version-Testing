import sys
import os
import time
import argparse
import logging
import subprocess
from subprocess import call

def getCurrentPath():
    dir = os.path.dirname(os.path.abspath(__file__))
    return dir

def getLocalTime():
    localtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return localtime

def generateFile(filename,text):
    time.sleep(1)
    f = open(filename, 'w')
    f.write(text)
    f.close()

def wcRunner(command,casenum):
    command.strip('\n').strip('\t')
    call(command,shell=True)
    text = os.popen(command).read()
    getLog(text)
    localtime = getLocalTime()
    reportpath, filenames = getFileNames('/report')
    filepath = os.path.join(reportpath,casenum + '_' + localtime + '.txt')
    generateFile(filepath,text)
    reportname = casenum + '_' + localtime + '.txt'
    return reportpath,reportname

def getLog(text):
    localtime = getLocalTime()
    file = getCurrentPath() + '/log/' + 'log_'+ localtime + '.txt'
    logging.basicConfig(filename= file, level=logging.DEBUG)
    logging.info(text)

def compareOutputs(reportpath,reportname,casenum):
    expath = getCurrentPath() + '/testsuite/expected/' + casenum + '_expected.txt'
    expected = open(expath, 'r').read().strip('\n').strip('\t')

    #Show expected results
    text=('\n' + 'Expected:' + '\n'+ expected + '\n')
    print(text)
    getLog(text)

    #Show comparision results
    nm = getShortName(reportname)
    if casenum in nm:
        filename = reportpath + '/'+ reportname
        content = open(filename, 'r').read().strip('\n').strip('\t')
        if content == expected:
            print('Comparision report is shown as follows')
            print('------------------------------------------------------------------------------')
            print('Congratulations!')
            print(reportname + ' is same as ' + casenum+'_expected.txt'+',you passed the testing.')
            print('------------------------------------------------------------------------------' + '\n')
            getLog('Comparision report is shown as follows')
            getLog('------------------------------------------------------------------------------')
            getLog('Congratulations!')
            getLog(reportname + ' is same as ' + casenum + '_expected.txt' + ',you passed the testing.')
            getLog('------------------------------------------------------------------------------' + '\n')
        else:
            print('Comparision report is shown as follows')
            print('---------------------------------------------------------------------------------')
            print(reportname + ' does not meet ' + casenum+'_expected.txt'+',you failed the testing.')
            print('For differences, please compare these two files for further analysis')
            print('---------------------------------------------------------------------------------' + '\n')
            getLog('Comparision report is shown as follows')
            getLog('---------------------------------------------------------------------------------')
            getLog(reportname + ' does not meet ' + casenum + '_expected.txt' + ',you failed the testing.')
            getLog('For differences, please compare these two files for further analysis')
            getLog('---------------------------------------------------------------------------------' + '\n')


def caseRunner(cases,filenames):
    for case in filenames:
        casenum = getShortName(case)
        casepath = cases + '/' +case
        commands = open(casepath, 'r').read().strip('\n').strip('\t')
        ver = commands.split(' & ')
        for v in ver:
            reportpath, reportname = wcRunner(v,casenum)
            compareOutputs(reportpath,reportname, casenum)


def getFileNames(subpath):
    casepath = getCurrentPath() + subpath
    filenames = os.listdir(casepath)
    return casepath,filenames

def getShortName(filenames):
    casenum, extnum = os.path.splitext(filenames)
    return casenum


if __name__ == '__main__':
    cases,filenames = getFileNames('/testsuite/cases')
    caseRunner(cases,filenames)











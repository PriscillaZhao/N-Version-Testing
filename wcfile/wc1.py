# -*- coding: utf-8 -*-
import sys
import argparse

arr = []

def sortArgs(argv):
    for arg in range(len(argv) - 1, 0, -1):
        for i in range(1, arg):
            if str(argv[i + 1]).startswith('-') == True and str(argv[i + 1]) != '-' and str(
                    argv[i + 1]) != '--':
                temp = argv[i + 1]
                argv[i + 1] = argv[i]
                argv[i] = temp


def print_help(errmsg):
    err = errmsg.split()
    print(error('invalid', err[len(err) - 1]))


def parserArgs():
    parser = argparse.ArgumentParser(prog="wc",
                                     usage='''wc [OPTION]... [FILE]...
  or:  wc [OPTION]... --files0-from=F''',
                                     description='''Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.  With no FILE, or when FILE is -,
read standard input.  A word is a non-zero-length sequence of characters
delimited by white space.
The options below may be used to select which counts are printed, always in
the following order: newline, word, character, byte, maximum line length.''',
                                     epilog='''GNU coreutils online help: <http://www.gnu.org/software/coreutils/>
For complete documentation, run: info coreutils 'wc invocation' ''',
                                     add_help=False)

    parser.add_argument('-c', "--bytes", help='print the byte counts', action='store_true')
    parser.add_argument('-m', "--chars", help='print the character counts', action='store_true')
    parser.add_argument('-l', "--lines", help='print the newline counts', action='store_true')
    parser.add_argument("--files0-from=F",
                        help='''read input from the files specified by
                        NUL-terminated names in file F;
                        If F is - then read names from standard input''',
                        )
    parser.add_argument('-L', "--max-line-length", help='print the length of the longest line', action='store_true')
    parser.add_argument('-w', "--words", help='print the word counts', action='store_true')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS,
                        help='display this help and exit')
    parser.add_argument('--version', action='version', version="wc (GNU coreutils) 8.22"
                                                               "Copyright (C) 2013 Free Software Foundation, Inc."
                                                               "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
                                                               "This is free software: you are free to change and redistribute it."
                                                               "There is NO WARRANTY, to the extent permitted by law.\n"
                                                               "\nWritten by Paul Rubin and David MacKenzie.")
    parser.add_argument('filenames', help='filenames', nargs='*')
    parser.error = print_help
    return parser.parse_known_args()


def readFiles(args, filenames):
    linecountT = 0
    wordcountT = 0
    bytecountT = 0
    charcountT = 0
    maxLineLen = 0

    maxNum = 0
    for filename in filenames:
        content = b''
        if len(filename) > 256:
            arr.append(error("longFilename", filename))
        else:
            try:
                with open(filename, 'rb') as file:
                    content = file.read()
            except IsADirectoryError:
                arr.append(error('directory', filename))
            except FileNotFoundError:
                arr.append(error('noFile', filename))
                continue
            linecount = getLinecount(content)
            wordcount = getWordcount(content)
            bytecount = getBytecount(content)
            charcount = getCharcount(content)
            maxline = getMaxLcount(content)
            linecountT += linecount
            wordcountT += wordcount
            bytecountT += bytecount
            charcountT += charcount
            if maxline > maxLineLen:
                maxLineLen = maxline
            arr1 = output(args, linecount, wordcount, bytecount, charcount, maxline, filename)[0]
            arr2 = output(args, linecount, wordcount, bytecount, charcount, maxline, filename)[1]
            num = max(arr1)
            if num > maxNum:
                maxNum = num
            arr.append(arr1 + arr2)

    if len(filenames) > 1:
        arr1 = output(args, linecountT, wordcountT, bytecountT, charcountT, maxLineLen, "total")[0]
        arr2 = output(args, linecountT, wordcountT, bytecountT, charcountT, maxLineLen, "total")[1]
        num = max(arr1)
        if num > maxNum:
            maxNum = num
        arr.append(arr1 + arr2)
    resultFormat(str(maxNum), arr)


def stdinFiles(args, filenames):
    linecountT = 0
    wordcountT = 0
    bytecountT = 0
    charcountT = 0
    maxLineLen = 0

    for filename in filenames:
        content = b''
        if len(filename) > 256:
            print(error("longFilename", filename))
            continue
        elif filename == '-':
            stdin = sys.stdin.read()
            content = str.encode(stdin)
        else:
            try:
                with open(filename, 'rb') as file:
                    content = file.read()
            except IsADirectoryError:
                print(error('directory', filename))
            except FileNotFoundError:
                print(error('noFile', filename))
                continue
        linecount = getLinecount(content)
        wordcount = getWordcount(content)
        bytecount = getBytecount(content)
        charcount = getCharcount(content)
        if filename == '-':
            maxline = getMaxLcount(content, True)
        else:
            maxline = getMaxLcount(content)
        linecountT += linecount
        wordcountT += wordcount
        bytecountT += bytecount
        charcountT += charcount
        if maxline > maxLineLen:
            maxLineLen = maxline
        StdOutput(args, linecount, wordcount, bytecount, charcount, maxline, filename)

    if len(filenames) > 1:
        StdOutput(args, linecountT, wordcountT, bytecountT, charcountT, maxLineLen, 'total')


def resultFormat(maxNum, arr):
    for r in arr:  # for error
        if isinstance(r, str):
            print(r)
        else:
            for i in range(len(r)):
                if i == len(r) - 1:
                    print(str(r[i]))
                else:
                    print(str(r[i]).rjust(len(maxNum)), end=' ')


def getLinecount(content):
    line = content.count(b'\n')
    return line


def getWordcount(content):
    word = len(content.split())
    return word


def getBytecount(content):
    byte = len(content)
    return byte


def getCharcount(content):
    characters = len(content.decode("utf-8", "ignore"))
    return characters


def getMaxLcount(content, stdin=False):
    maxL = 0
    if stdin:
        lines = content.splitlines()
        for l in lines:
            arr = l.split(b'\t')
            lens = (len(arr) - 1) * 8 + len(arr[len(arr) - 1])
            if lens > maxL:
                maxL = lens
    else:
        lines = content.replace(b'\t', b'        ').splitlines()  # tab = 8 spaces
        for l in lines:
            if len(l) > maxL:
                maxL = len(l)
    return maxL


def output(args, linecount, wordcount, bytecount, charcount, maxline, filename):
    arr = []
    result = []
    maxNum = []
    if args.lines == False and args.words == False and args.bytes == False and args.chars == False and args.max_line_length == False:
        maxNum.append(linecount)
        maxNum.append(wordcount)
        maxNum.append(bytecount)
    else:
        if args.lines == True:
            maxNum.append(linecount)
        if args.words == True:
            maxNum.append(wordcount)
        if args.chars == True:
            maxNum.append(charcount)
        if args.bytes == True:
            maxNum.append(bytecount)
        if args.max_line_length == True:
            maxNum.append(maxline)

    result.append(filename)
    arr.append(maxNum)
    arr.append(result)
    return arr


def StdOutput(args, linecount, wordcount, bytecount, charcount, maxline, filename):
    if args.lines == False and args.words == False and args.bytes == False and args.chars == False and args.max_line_length == False:
        print(str(linecount).rjust(7) + ' ' + str(wordcount).rjust(7) + ' ' + str(bytecount).rjust(7) + ' ' + filename)
    else:
        val = []
        if args.lines == True:
            val.append(linecount)
        if args.words == True:
            val.append(wordcount)
        if args.chars == True:
            val.append(charcount)
        if args.bytes == True:
            val.append(bytecount)
        if args.max_line_length == True:
            val.append(maxline)
        val.append(filename)

        for i in range(len(val)):
            if i == len(val) - 1:
                print(str(val[i]))
            else:
                print(str(val[i]).rjust(7), end=' ')


def error(type, message):
    result = ''
    if type == 'invalid':
        result = "wc: invalid option -- " + message + "\nTry 'wc --help' for more information."
    elif type == 'extra':
        result = "wc: extra operand ‘" + message + "'\nfile operands cannot be combined with --files0-from\nTry 'wc --help' for more information."
    elif type == 'directory':
        result = 'wc: ' + message + ': Is a directory'
    elif type == 'directoryF':
        result = 'wc: ' + message + ': read error: Is a directory'
    elif type == 'longFilename':
        result = 'wc: ' + message + ': File name too long'
    elif type == 'noFile':
        if message == '':
            result = 'wc: No such file or directory'
        else:
            result = 'wc: ' + message + ': No such file or directory'
    elif type == 'noFileF':
        result = "wc: cannot open ‘" + message + "’ for reading: No such file or directory"
    return result


def FileFrom(filef):
    sortArgs(sys.argv)
    if len(parserArgs()[1]) > 0:
        print(error('invalid', "'" + str(parserArgs()[1][0]).replace('-', '', 1) + "'"))
    elif len(parserArgs()[0].__getattribute__('filenames')) > 0:
        print(error('extra', parserArgs()[0].__getattribute__('filenames')[0]))
    else:
        if filef == "-":
            FileFrom_Std()
        else:
            FileFrom_File(filef)


def FileFrom_Std():
    stdF = []
    while True:
        stdfile = sys.stdin.readline()
        if stdfile:
            if len(stdF) > 0:
                stdF[len(stdF) - 1] += stdfile
            else:
                stdF.append(stdfile)
            if '\x00' in stdfile:
                stdinFiles(parserArgs()[0], stdF[0].split('\x00'))
                stdF = []
        else:
            if len(stdF) == 0:
                stdinFiles(parserArgs()[0], ['\n'])
                sys.exit(0)
            else:
                stdinFiles(parserArgs()[0], stdF[0].split('\x00'))
                stdF = []


def FileFrom_File(filef):
    try:
        with open(filef, 'r') as file:
            content = file.read()
        readFiles(parserArgs()[0], content.split('\x00'))
    except IsADirectoryError:
        print(error('directoryF', filef))
    except FileNotFoundError:
        print(error('noFileF', filef))


def ExecuteArgument():
    sortArgs(sys.argv)
    if len(parserArgs()[1]) > 0:
        print(error('invalid', "'" + str(parserArgs()[1][0]).replace('-', '', 1) + "'"))
    else:
        args = parserArgs()[0]
        if len(args.filenames) == 0:
            print(error('noFile', ''))
        else:
            rs = [x for x in args.filenames if x == '-']
            if len(rs) > 0:
                stdinFiles(args, args.filenames)
            else:
                readFiles(args, args.filenames)


if __name__ == "__main__":
    if parserArgs() != None:
        if parserArgs()[0].__getattribute__('files0_from=F') != None:
            FileFrom(parserArgs()[0].__getattribute__('files0_from=F'))
        else:
            ExecuteArgument()

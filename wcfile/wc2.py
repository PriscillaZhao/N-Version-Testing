#
# FUNCTIONS
#
def openfile(filename):
    try:
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text
    except IOError:
        print('wc:' + filename + ': No such file or directory')


def wordcount(text):
    return len(str(text).split())


def linecount(text):
    return str(text).count('\n')


# ***** PROCESS SPECIAL LANGUAGES 多语言字符识别 *****

def bytecount(text):
    return len(str(text).encode('utf-8'))
    # return len(str(text))

def charcount(text):
    return len(str(text))


def maxlinelength(text):
    if text == None:
        return None
    maxll = 0
    for i in text.split('\n'):
        if len(i) > maxll:
            maxll = len(i)
    return maxll


def StdIn():
    text = ''
    while 1:
        try:
            currentline = sys.stdin.readline()
            if currentline == '':
                return text
            text = text + str(currentline)
        except KeyboardInterrupt:
            break


def buildprint(wordnum, linenum, bytenum, maxlinelength, charnum, filename, formatc):
    if flags.lines:
        if flags.words == False and flags.bytes == False and flags.max_line_length == False and flags.chars == False:
            print(linenum, end=' ')
        else:
            print(linenum.rjust(formatc), end=' ')

    if flags.words:
        if flags.lines == False and flags.bytes == False and flags.max_line_length == False and flags.chars == False:
            print(wordnum, end=' ')
        else:
            print(wordnum.rjust(formatc), end=' ')

    if flags.bytes:
        if flags.lines == False and flags.words == False and flags.max_line_length == False and flags.chars == False:
            print(bytenum, end=' ')

        else:
            print(bytenum.rjust(formatc), end=' ')

    if flags.chars:
        if flags.lines == False and flags.words == False and flags.max_line_length == False and flags.words == False:
            print(charnum, end=' ')
        else:
            print(charnum.rjust(formatc), end=' ')

    if flags.max_line_length:
        if flags.lines == False and flags.words == False and flags.words == False and flags.chars == False:
            print(maxlinelength, end=' ')

        else:
            print(maxlinelength.rjust(formatc), end=' ')

    if flags.lines == False and flags.words == False and flags.bytes == False and flags.max_line_length == False and flags.chars == False:
        print(linenum.rjust(formatc) + ' ' + wordnum.rjust(formatc) + ' ' + bytenum.rjust(formatc), end=' ')

    print(filename)


#
# MAIN FUNCTION
#


if __name__ == '__main__':
    import argparse
    import sys

    wordtotal = 0
    linetotal = 0
    bytetotal = 0
    maxlltotal = 0
    chartotal = 0

    # parser part: process flags filename
    #
    # **** 完善提示信息 版本信息

    parser_flags = argparse.ArgumentParser(description='Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified.  A word is a non-zero-length sequence of characters delimited by white space.')
    parser_files = argparse.ArgumentParser()
    parser_flags.add_argument('-w', '--words', help='print the word counts', action='store_true')
    parser_flags.add_argument('-l', '--lines', help='print the newline counts', action='store_true')
    parser_flags.add_argument('-c', '--bytes', help='print the byte counts', action='store_true')
    parser_flags.add_argument('-m', '--chars', help='print the character counts', action='store_true')
    parser_flags.add_argument('-L', '--max-line-length', help='print the maximum display width', action='store_true')
    parser_flags.add_argument('--files0-from', help='read filename from file')
    parser_flags.add_argument('--version', action='version', version='mimic GNU WC- need to be completed')
    parser_files.add_argument('filename', nargs='*', help='filename')
    flags, files = parser_flags.parse_known_args()
    flags = parser_files.parse_args(files,flags)

    # print(flags)
    # process --file0-from=
    # **** stdin 是否是应该输入 存储命令的文件的名字 wc分析的是文件？？？
    #

    if flags.files0_from != None:
        if flags.files0_from == '-':
            stdintext = StdIn()
            if stdintext != None:
                filetext = stdintext
        else:
            filetext = openfile(flags.files0_from)

        files = filetext.split('\0')


    # stdin
    # sys.stdin.readline()
    # **** ctrl+d 在连续输入的情况下会出现识别不出来的情况 wc也这样 不知道为啥****

    if len(files) < 1:
        text = ''
        text = StdIn()
        print()
        buildprint(str(wordcount(text)), str(linecount(text)), str(bytecount(text)), str(maxlinelength(text)), str(charcount(text)), '',7)

    #
    # COUNT part: COUNT EXACT NUMBER
    #

    printsentence = '\t'
    word = []
    line = []
    byte = []
    maxll = []
    char = []
    list = []

    for i in range(0, len(files)):
        if files[i] == '-':
            text = StdIn()
            count = 7
        elif files[i] == '--':
            text = None
        else:
            text = openfile(files[i])
        if text != None:
            wordtotal = wordtotal + wordcount(text)
            linetotal = linetotal + linecount(text)
            bytetotal = bytetotal + bytecount(text)
            maxlltotal = maxlltotal + maxlinelength(text)
            chartotal = chartotal + charcount(text)
            if '-' in files:
                buildprint(str(wordcount(text)), str(linecount(text)), str(bytecount(text)), str(maxlinelength(text)),
                           str(charcount(text)),files[i], 7)
            else:
                word.append(str(wordcount(text)))
                line.append(str(linecount(text)))
                byte.append(str(bytecount(text)))
                char.append(str(charcount(text)))
                maxll.append(str(maxlinelength(text)))

                list.append(files[i])
    if '-' not in files:
        count = max(len(str(wordtotal)), len(str(linetotal)), len(str(bytetotal)), len(str(maxlltotal)),len(str(chartotal)))

    for i in range(0, len(list)):
        buildprint(word[i], line[i], byte[i], maxll[i], char[i], list[i], count)

    if len(files) > 1:
        buildprint(str(wordtotal), str(linetotal), str(bytetotal), str(maxlinelength(text)), str(chartotal), 'total', count)

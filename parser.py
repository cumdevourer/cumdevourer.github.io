import sys
import os

def process_title(f):
    line = f.readline().replace('Є', '').replace('\n', '')
    f.readline()
    if 'Deleted' in line:
        return True
    return False

def process_options(f):
        q_type = None
        right = None
        while q_type is None or right is None:
            line = f.readline().replace('Є', '').replace('\n', '')
            if 'type' in line:
                q_type = int(line.split('=')[1])
            elif 'right' in line:
                right = int(line.split('=')[1])
        return (q_type, right)
    
def process_answers(f, q_type, right):
    buf = "\n<answers>\n<br>"
    if q_type == 7 or q_type == 1:
        while True:
            line = f.readline().replace('Є', '').replace('\n', '')
            if '<a_1>' in line:
                buf += '<b>'
                l = f.readline().replace('Є', '').replace('\n', '')
                while l == '':
                    l = f.readline().replace('Є', '').replace('\n', '')
                buf += l
                buf += '</b>\n</answers>\n<br><br>\n'
                return buf
    elif q_type == 2 or q_type == 6:
        for i in range(1, right+1):
            while True:
                line = f.readline().replace('Є', '').replace('\n', '')
                if f'<a_{i}>' in line:
                    buf += '<b>'
                    l = f.readline().replace('Є', '').replace('\n', '')
                    while l == '':
                        l = f.readline().replace('Є', '').replace('\n', '')
                    buf += l
                    buf += f'</b><br>\n'
                    break
        buf += '</answers>\n<br><br>\n'
        return buf
    else:
        return ''
            

def process_question(f, q_type, right):
    while True:
        line = f.readline().replace('Є', '').replace('\n', '')
        if '<question>' in line:
            q = '<question>\n'
            while True:
                line = f.readline().replace('Є', '').replace('\n', '')
                if '</question>' in line:
                    q += '\n</question>'
                    break
                q += line
            
            q += process_answers(f, q_type, right)
            return q
    

def parse(testname):
    f = open(f'{testname}', 'rt')
    lines_count = len(f.readlines())
    f.seek(0)
    
    contents = '<!DOCTYPE html>\n<head>\n</head>\n<body>\n'
    
    for i in range(0, lines_count):
        line = f.readline().replace('Є', '').replace('\n', '')
        
        if '<Q_TITLE>' in line:
            skip = process_title(f)
            (q_Type, Right) = process_options(f)
            contentsToAdd = process_question(f, q_Type, Right)
            if not skip:
                contents += contentsToAdd
    contents += '\n</body>\n'
    f.close()
    with open(f'{testname}.html', 'w+') as f:
        f.write(contents)

def parseDir(dirname):
    for filename in os.listdir(dirname):
        parse(dirname + '/' + filename)


if len(sys.argv) > 2:
    if sys.argv[2] == '-d':
        parseDir(sys.argv[1])
else:
    parse(sys.argv[1])

outf = open('ЧисловМодел.txt', 'w+')
for i in range(1,19):
    f = open(f'tests/ЧислМодел{i}.txt', 'rt')
    outf.write(''.join(f.readlines()))
    f.close()

f = open('tests/ЧислМодел18_2.txt', 'rt')
outf.write(''.join(f.readlines()))
f.close()
outf.close()

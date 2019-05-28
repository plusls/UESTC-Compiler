from .symbol import type_table


def analysis(file_name, err_file):
    source_file = open(file_name + '.pas', 'rb')
    out_file = open(file_name + '.dyd', 'w')
    line = 1
    out_line = 0
    idx = 0
    while True:
        ch = source_file.read(1)
        idx += 1
        buf = b''
        if ch == b'':
            out_file.write('{} {}\n'.format('EOF'.rjust(16, ' '), 25))
            return
        if ch.isspace():
            if ch == b'\n':
                line += 1
                idx = 0
                out_file.write('{} {}\n'.format('EOLN'.rjust(16, ' '), 24))
            continue
        if ch.isalpha():
            buf += ch
            while True:
                ch = source_file.read(1)
                idx += 1
                if not ch.isalnum():
                    if ch != b'':
                        source_file.seek(-1, 1)
                        idx -= 1
                    break
                buf += ch
        elif ch.isdigit():
            buf += ch
            while True:
                ch = source_file.read(1)
                idx += 1
                if not ch.isdigit():
                    if ch != b'':
                        source_file.seek(-1, 1)
                        idx -= 1
                    break
                buf += ch
        elif ch == b'=':
            buf = b'='
        elif ch == b'<':
            buf = b'<'
            ch = source_file.read(1)
            idx += 1
            if ch == b'>':
                buf += b'>'
            elif ch == b'=':
                buf += b'='
            else:
                if ch != b'':
                    source_file.seek(-1, 1)
                    idx -= 1
        elif ch == b'>':
            buf = b'>'
            ch = source_file.read(1)
            idx += 1
            if ch == b'=':
                buf += b'='
            else:
                if ch != b'':
                    source_file.seek(-1, 1)
                    idx -= 1
        elif ch == b'-':
            buf = b'-'
        elif ch == b'*':
            buf = b'*'
        elif ch == b':':
            buf = b':'
            ch = source_file.read(1)
            idx += 1
            if ch == b'=':
                buf += b'='
            else:
                err_file.write(
                    '***LINE:{} at:{} error:{}'.format(line, idx, 'error character ":"'))
                if ch != b'':
                    source_file.seek(-1, 1)
                    idx -= 1
        elif ch == b'(':
            buf = b'('
        elif ch == b')':
            buf = b')'
        elif ch == b';':
            buf = b';'
        else:
            err_file.write('***LINE:{} at:{} error:{}'.format(line,
                                                              idx, 'error character "{}"'.format(ch.decode())))
        buf = buf.decode()
        out_line += 1
        out_file.write('{} {}\n'.format(buf.rjust(16, ' '), 10))
        if buf.isdigit():
            out_file.write('{} {}\n'.format(buf.rjust(16, ' '), 11))
            continue
        t = type_table.get_type(buf)
        if t == None:
            out_file.write('{} {}\n'.format(buf.rjust(16, ' '), 10))
        else:
            #out_file.write('{} {}\n'.format(''.rjust(16, ' '), t))
            out_file.write('{} {}\n'.format(buf.rjust(16, ' '), t))
    source_file.close()
    out_file.close()
    err_file.flush()


if __name__ == '__main__':
    import sys
    err_file = open(sys.argv[1] + '.err', 'w')
    analysis(sys.argv[1], err_file)
    err_file.close()

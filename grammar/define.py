def define_analysis(filename):
    ret = []
    define_file = open(filename, 'r')
    while True:
        grammar = define_file.readline()
        if grammar == '':
            return ret
    define_file.close()

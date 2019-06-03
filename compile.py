import sys
import lexer
import grammar
if __name__ == '__main__':
    # sys.argv[2] = 'test/test1'
    # sys.argv[1] = 'all'

    err_file = open(sys.argv[2] + '.err', 'w')
    if sys.argv[1] == 'lex':
        lexer.analysis(sys.argv[2], err_file)
    elif sys.argv[1] == 'all':
        lexer.analysis(sys.argv[2], err_file)
        grammar.analysis(sys.argv[2], err_file)
    err_file.close()

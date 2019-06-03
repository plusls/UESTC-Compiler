import re
from .sym_table import Var, Proc, proc_dict
symbol_list = ['begin', 'end', 'integer', 'if', 'then', 'else', 'function',
               'read', 'write', 10, 11, '=', '<>', '<=', '<', '>=',
               '>', '-', '*', ':=', '(', ')', ';', 'ε']


class Grammar(object):
    __re = re.compile('<([^<>]*)>')
    grammar_dict = {}
    grammar_list = []

    now_proc_stack = []
    vkind = 0
    lev = 0
    now_line = 1
    errfile = None
    def __init__(self, define):
        self.__src = []
        self.__dst = []
        self.__parse_define(define)
        self.__head = ''
        if self.src() not in Grammar.grammar_dict:
            Grammar.grammar_dict[self.src()] = []
        Grammar.grammar_dict[self.src()].append(self)
        if not Grammar.is_grammar(self.__dst[0]):
            self.__head = self.__dst[0]
        print(self)

    def src(self):
        return self.__src[0]

    @staticmethod
    def is_grammar(s):
        if Grammar.__re.match(s) == None:
            return False
        else:
            return True

    def __parse_define_str(self, s):

        if self.__src[0] in ['<字母>', '<数字>']:
            self.__dst.append(s)
            return
        idx = 0
        l = len(s)
        while True:
            if idx == l:
                break
            if s[idx] == ' ':
                idx += 1
                continue
            for sym in symbol_list:
                if type(sym) == int:
                    continue
                if s.find(sym, idx) == idx:
                    self.__dst.append(sym)
                    idx += len(sym)
                    break
            else:
                raise Exception('??')

    def __parse_define(self, define):
        (src, dst) = define.split('→')  # (.*)→(.*)
        src_re = re.match('^<([^<>]*)>$', src)
        # print(define)
        if src_re != None:
            # self.__src.append(src_re.group(1))
            self.__src.append(src)
        else:
            raise Exception('????')
        while True:
            dst_re = re.search('<([^<>]*)>', dst)
            if len(dst) == 0:
                break
            elif dst_re == None:
                self.__parse_define_str(dst)
                dst = ''
            else:
                res = dst_re.span()
                l = dst[:res[0]]
                r = dst[res[0]:res[1]]
                dst = dst[res[1]:]
                if l != '':
                    self.__parse_define_str(l)
                self.__dst.append(r)
        if self.__dst[0].startswith(self.__src[0]):
            print('fuck {}'.format(define))

    def check_head(self, lex_result, idx):
        if lex_result[idx][0] != self.__head and self.__head != '':
            return False
        else:
            return True

    def is_empty(self):
        return self.__dst[0] == 'ε'

    @staticmethod
    def error(s):
        Grammar.err_file.write(s + '\n')

    def parse(self, lex_result, idx):
        print('233', repr(self), idx, lex_result[idx])
        i = 0
        l = len(self.__dst)
        while True:
            if i == len(self.__dst):
                break
            print('now {} idx={} grammar={} self={}'.format(
                lex_result[idx], idx, self.__dst[i], self))
            if lex_result[idx][1] == 24:
                # EOLN
                Grammar.now_line += 1
                idx += 1
                continue
            if self.src() == '<函数说明>':
                if i == 0:
                    p_name = lex_result[idx+2][0]
                    p = Proc(p_name, lex_result[idx][0], Grammar.lev)
                    # 函数重定义 出错处理
                    if p_name in proc_dict:
                        err_str = '***LINE:{} error:proc {} has been defined'.format(Grammar.now_line, p_name)
                        Grammar.error(err_str)
                    proc_dict[p_name] = p
                    Grammar.now_proc_stack.append(p_name)
            if self.__dst[i] == '<变量>':
                if self.src() != '<变量说明>' and self.src() != '<参数>':
                    v_name = lex_result[idx][0]
                    if lex_result[idx][1] != 10:
                        err_str = '***LINE:{} error:{}不是标识符'.format(Grammar.now_line, v_name)
                        Grammar.error(err_str)
                        exit()
                    for p_name in Grammar.now_proc_stack:
                        if v_name in proc_dict[p_name].v_dict:
                            break
                    else:
                        err_str = '***LINE:{} error:var {} undefined'.format(Grammar.now_line, v_name)
                        Grammar.error(err_str)
            if self.src() == '<参数>':
                Grammar.vkind = 1
            if self.src() == '<变量说明>':
                print(1231232134, self, lex_result[idx])
                # 如果是integer
                if i == 0:
                    now_fun = Grammar.now_proc_stack[-1]
                    v_name = lex_result[idx + 1][0]
                    # 定义变量
                    v = Var(v_name, now_fun,
                            Grammar.vkind, lex_result[idx][0], Grammar.lev)
                    # 变量重定义 出错
                    if v_name in proc_dict[now_fun].v_dict:
                        err_str = '***LINE:{} error:var {} has been defined'.format(Grammar.now_line, v_name)
                        Grammar.error(err_str)
                    elif lex_result[idx + 1][1] != 10:
                        err_str = '***LINE:{} error:{} 不是标识符'.format(Grammar.now_line, v_name)
                        Grammar.error(err_str)
                        exit()
                    proc_dict[now_fun].add_var(v)

            if self.__dst[i] == '<标识符>':
                print(123123213, self)
                if lex_result[idx][1] == 10:
                    idx += 1
                    i += 1
                    continue
            if self.__dst[i] == '<常数>':
                print(123123213, self)
                if lex_result[idx][1] == 11:
                    idx += 1
                    i += 1
                    continue
            if Grammar.is_grammar(self.__dst[i]):
                next_parse_list = Grammar.grammar_dict[self.__dst[i]]
                print('try ', next_parse_list)
                for g in next_parse_list:
                    print(g)
                    # 为空则返回
                    if g.is_empty():
                        i += 1
                        break

                    # 判函数声明还是变量声明
                    if self.__dst[i] == '<说明语句>':
                        if lex_result[idx][1] == 3 and lex_result[idx+1][1] == 7:
                            if g.__dst[0] != '<函数说明>':
                                continue
                    # 分号有歧义 判断是变量声明的结束还是 执行语句
                    #print(123213213, self, self.__dst[i])
                    if self.__dst[i] == '<说明语句表1>':
                        if lex_result[idx][1] == 23 and g.__dst[0] == ';':
                            j = idx+1
                            # 跳过换行
                            while True:
                                if lex_result[j][1] == 24:
                                    j += 1
                                else:
                                    break
                            # 如果不是int 则选择 ε
                            if lex_result[j][1] != 3:
                                continue

                    # 判断是否为函数 常数
                    if self.__dst[i] == '<因子>':
                        if lex_result[idx][1] == 10:
                            if lex_result[idx+1][1] == 21:
                                if g.__dst[0] != '<函数调用>':
                                    continue
                        elif lex_result[idx][1] == 11:
                            if g.__dst[0] != '<常数>':
                                continue

                    # 匹配头部失败
                    if g.check_head(lex_result, idx) is False:
                        # 出错处理 如果缺了分号后面会补
                        print(g.__head, lex_result[idx])
                        if g.__head == ';' and lex_result[idx][1] in (3, 4, 8, 9):
                            # 塞一个假分号
                            #lex_result[idx:idx+1] = [(';', 23)] + lex_result[idx:idx+1]
                            pass
                            #continue
                        else:
                            continue
                    res = g.parse(lex_result, idx)
                    if res == idx:
                        print(g)
                        raise Exception('')
                        continue
                    else:
                        if self.src() == '<参数>':
                            self.vkind = 0
                        idx = res
                        i += 1
                        break
                else:
                    # 没有一个文法可以匹配上
                    print('{}->{} error'.format(lex_result[idx], self))
                    raise Exception('')
                    break
            else:
                print(
                    '尝试匹配 {}->{} idx={}'.format(repr(lex_result[idx][0]), repr(self.__dst[i]), idx))
                if lex_result[idx][0] == self.__dst[i]:
                    print(
                        'ok {}->{}'.format(lex_result[idx][0], self.__dst[i]))
                    if lex_result[idx][0] == 'begin':
                        Grammar.lev += 1
                    elif lex_result[idx][0] == 'end':
                        Grammar.now_proc_stack.pop()
                        Grammar.lev -= 1
                    idx += 1
                    i += 1
                else:
                    # 缺少分号情况比较特殊
                    if self.__dst[i] == ';':
                        err_str = '***LINE:{} error:Missing ;'.format(Grammar.now_line)
                        #lex_result[idx:idx+1] = [(' ', 23)] + lex_result[idx:idx+1]
                        i += 1
                    else:
                        err_str = '***LINE:{} error:It should be {} not {}'.format(Grammar.now_line, self.__dst[i], lex_result[idx][0])
                        idx += 1
                        i += 1
                    Grammar.error(err_str)
                    
                    # 只有 以下语句允许回溯
                    # if self.src() not in ['<读语句>', '<写语句>', '<赋值语句>']:
                    #raise Exception('')
                    #break
        return idx

    def __repr__(self):
        return repr('{}→{}'.format(self.__src[0], self.__dst))


def generate_grammar(grammar_str):
    ret = []
    (src, dst) = grammar_str.split('→')
    dst_list = dst.split('|')
    for dst in dst_list:
        ret.append(Grammar('{}→{}'.format(src, dst)))
    return ret


def get_grammar():
    grammar_file = 'test/grammar.define'
    f = open(grammar_file, 'r')
    grammar_str_list = f.readlines()
    grammar_list = []
    for grammar_str in grammar_str_list:
        grammar_str = grammar_str.strip()
        if grammar_str == '':
            continue
        g = generate_grammar(grammar_str)
        grammar_list += g
    return grammar_list


def get_lex_result(file_name):
    fp = open('{}.dyd'.format(file_name), 'r')
    lex_result_str_list = fp.readlines()
    fp.close()
    for i in range(len(lex_result_str_list)):
        s = lex_result_str_list[i]
        s = s.strip()
        s = s.split(' ')
        lex_result_str_list[i] = (s[0], int(s[1]))
        # print(lex_result_str_list[i])
    return lex_result_str_list


def analysis(file_name, err_file):
    grammar_list = get_grammar()
    grammar_dict = Grammar.grammar_dict
    lex_result = get_lex_result(file_name)
    proc_dict['main'] = Proc('main', 'void', 0)
    Grammar.now_proc_stack.append('main')
    Grammar.err_file = err_file
    grammar_dict['<程序>'][0].parse(lex_result, 0)
    fproc = open('{}.proc'.format(file_name), 'w')
    fvar = open('{}.var'.format(file_name), 'w')
    fproc.write('{}{}{}{}{}\n'.format('pname'.ljust(16, ' '),
                                      'ptype'.ljust(16, ' '),
                                      'plev'.ljust(16, ' '),
                                      'fadr'.ljust(16, ' '),
                                      'ladr'.ljust(16, ' ')))
    fvar.write('{}{}{}{}{}{}\n'.format('vname'.ljust(16, ' '),
                                       'vproc'.ljust(16, ' '),
                                       'vkind'.ljust(16, ' '),
                                       'vtype'.ljust(16, ' '),
                                       'vlev'.ljust(16, ' '),
                                       'vadr'.ljust(16, ' ')))
    v_idx = 0
    for f_name in proc_dict:
        f = proc_dict[f_name]
        fadr = v_idx
        for v_name in f.v_dict:
            v = f.v_dict[v_name]
            fvar.write('{}{}{}{}{}{}\n'.format(v.name.ljust(16, ' '),
                                               v.proc.ljust(16, ' '),
                                               str(v.kind).ljust(16, ' '),
                                               v.vtype.ljust(16, ' '),
                                               str(v.lev).ljust(16, ' '),
                                               str(v_idx).ljust(16, ' ')))
            v_idx += 1
        if len(f.v_dict):
            ldar = v_idx - 1
        else:
            ldar = v_idx
        fproc.write('{}{}{}{}{}\n'.format(f.name.ljust(16, ' '),
                                          str(f.ptype).ljust(16, ' '),
                                          str(f.lev).ljust(16, ' '),
                                          str(fadr).ljust(16, ' '),
                                          str(ldar).ljust(16, ' ')))

    fproc.close()
    fvar.close()

    return


if __name__ == '__main__':
    import sys
    err_file = open(sys.argv[1] + '.err', 'w')
    analysis(sys.argv[1], err_file)
    err_file.close()

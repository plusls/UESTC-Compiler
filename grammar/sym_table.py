proc_dict = {}


class Var(object):
    def __init__(self, name, proc, kind, vtype, vlev):
        # 变量名
        self.name = name
        # 变量所属过程 类型：Proc
        self.proc = proc
        # 变量类型 （0-变参 1-形参）
        self.kind = kind
        # 变量类型 int or else
        self.vtype = vtype
        # 变量层次
        self.lev = vlev

    def __repr__(self):
        return '\nname={}\nproc={}\nkind={}\nvtype={}\nvlev={}\n'.format(self.name, self.proc, self.kind, self.vtype, self.lev)


class Proc(object):
    def __init__(self, name, ptype, lev):
        # 过程名
        self.name = name
        # 过程类型 （函数返回值类型）
        self.ptype = ptype
        # 过程层次 (在多少个begin内)
        self.lev = lev
        # var list
        self.v_dict = {}

    def add_var(self, v):
        self.v_dict[v.name] = v

    def __repr__(self):
        return 'pname={}\nptype={}\nplev={}\n\nvlist={}\n\n'.format(self.name, self.ptype, self.lev, self.v_dict)

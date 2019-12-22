import inspect, re
from pprint import pprint


class WrapperFunc:
    # separate func param define and use
    def __init__(self, func, **kwargs):
        self.func = func
        # default func params, inverse order, as len(args) >= len(defaults)
        argspec = inspect.getfullargspec(func)
        args, default_vals = argspec.args, argspec.defaults
        vals = ['nerver_use'] * (len(args) - len(default_vals)) + list(default_vals)  # left add None for postition args
        params = {}
        for k, v in zip(args, vals):
            if k not in args:  # false pass in args
                continue
            params[k] = v if k not in kwargs else kwargs[k]  # update if pass in
        self.func_params = {
            k: v for k, v in params.items() if v != 'nerver_use'  # filter no_set args
        }
        pprint(self.func_params)

    def __call__(self, *args):
        return self.func(*args, **self.func_params)


def namestrs(objs, namespace):
    return [name for name in namespace if namespace[name] in objs]  # 可返回多个，当 global() dict 中 val 一样时


def namestr(obj, namespace):  # 这个方法只要每次都指定 locals() 就好
    return [name for name in namespace if namespace[name] is obj]


def varname(p):  # 可以获取任意 namespace 下定义的变量
    # debug
    # for e in inspect.getframeinfo(inspect.currentframe().f_back):
    #     print(e)
    # return 5 things, and [3] = ['    print(varname(a))\n']

    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)  # 搜索括号中的变量
        if m:
            return m.group(1)


def test_namestr():
    a = 'hello'
    b = 'hello'
    print(namestr(a, namespace=locals()))  # 局部变量
    print(namestr(namestr, namespace=globals()))  # 全局变量


def test_varname():
    a = 'hello'
    b = 'hello'

    print(varname(a))
    print(varname(varname))


if __name__ == '__main__':
    # test_namestr()
    test_varname()

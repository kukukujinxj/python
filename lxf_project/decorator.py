import functools


# def log(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#
#     return wrapper

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('{0} {1}()'.format(text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log('execute')
def numbers(x):
    if not isinstance(x, int):
        raise TypeError('参数类型错误')
    a = list(range(x))
    print(a[10:20])


if __name__ == '__main__':
    numbers(100)

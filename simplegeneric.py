__all__ = ["generic"]

from types import ClassType, InstanceType
classtypes = type, ClassType

def generic(func):
    """Create a simple generic function"""

    _sentinel = object()

    def _by_class(*args, **kw):
        cls = args[0].__class__
        for t in type(cls.__name__, (cls,object), {}).__mro__:
            f = _gbt(t, _sentinel)
            if f is not _sentinel:
                return f(*args, **kw)
        else:
            return func(*args, **kw)

    _by_type = {object: func, InstanceType: _by_class}
    _gbt = _by_type.get

    def when_type(t):
        if not isinstance(t, classtypes):
            raise TypeError(
                "%r is not a type or class" % (t,)
            )
        def decorate(f):
            if t in _by_type:
                raise TypeError(
                    "%r already has method for type %r" % (func, t)
                )
            _by_type[t] = f
            return f
        return decorate






    _by_object = {}
    _gbo = _by_object.get

    def when_object(o):
        def decorate(f):
            if id(o) in _by_object:
                raise TypeError(
                    "%r already has method for object %r" % (func, o)
                )
            _by_object[id(o)] = o, f
            return f
        return decorate


    def dispatch(*args, **kw):
        f = _gbo(id(args[0]), _sentinel)
        if f is _sentinel:
            for t in type(args[0]).__mro__:
                f = _gbt(t, _sentinel)
                if f is not _sentinel:
                    return f(*args, **kw)
            else:
                return func(*args, **kw)
        else:
            return f[1](*args, **kw)

    dispatch.__name__       = func.__name__
    dispatch.__dict__       = func.__dict__
    dispatch.__doc__        = func.__doc__
    dispatch.__module__     = func.__module__

    dispatch.when_type = when_type
    dispatch.when_object = when_object
    dispatch.default = func

    return dispatch





def test_suite():
    import doctest
    return doctest.DocFileSuite(
        'README.txt',
        optionflags=doctest.ELLIPSIS|doctest.REPORT_ONLY_FIRST_FAILURE,
    )




































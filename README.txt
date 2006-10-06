=========================
Trivial Generic Functions
=========================

The ``simplegeneric`` module lets you define simple single-dispatch
generic functions, akin to Python's built-in generic functions like
``len()``, ``iter()`` and so on.  However, instead of using
specially-named methods, these generic functions use simple lookup
tables, akin to those used by e.g. ``pickle.dump()`` and other
generic functions found in the Python standard library.

As you can see from the above examples, generic functions are actually
quite common in Python already, but there is no standard way to create
simple ones.  This library attempts to fill that gap, as generic
functions are an `excellent alternative to the Visitor pattern`_, as
well as being a great substitute for most common uses of adaptation.

This library tries to be the as simple an implementation of generic
functions as possible, and therefore eschews the use of multiple
dispatch, and avoids using speedup techniques such as C dispatching or
code generation.  But it has absolutely no dependencies, other than
Python 2.4, and the implementation is just a single Python module of
less than 100 lines.

Usage is straightforward::

    >>> from simplegeneric import generic
    >>> @generic
    ... def move(item, target):
    ...     """Default implementation goes here"""
    ...     print "what you say?!"

    >>> @move.when_type(int)
    ... def move_int(item, target):
    ...     print "In AD %d, %s was beginning." % (item, target)

    >>> @move.when_type(str)
    ... def move_str(item, target):
    ...     print "How are you %s!!" % item
    ...     print "All your %s are belong to us." % (target,)

    >>> zig = object()
    >>> @move.when_object(zig)
    ... def move_zig(item, target):
    ...     print "You know what you %s." % (target,)
    ...     print "For great justice!"

    >>> move(2101, "war")
    In AD 2101, war was beginning.

    >>> move("gentlemen", "base")
    How are you gentlemen!!
    All your base are belong to us.

    >>> move(zig, "doing")
    You know what you doing.
    For great justice!

    >>> move(27.0, 56.2)
    what you say?!

Defining multiple methods for the same type or object is an error::

    >>> @move.when_type(str)
    ... def this_is_wrong(item, target):
    ...     pass
    Traceback (most recent call last):
    ...
    TypeError: <function move...> already has method for type <type 'str'>

    >>> @move.when_object(zig)
    ... def this_is_wrong(item, target): pass
    Traceback (most recent call last):
      ...
    TypeError: <function move...> already has method for object <object ...>

Methods defined for supertypes are inherited following MRO order::

    >>> class MyString(str):
    ...     """String subclass"""

    >>> move(MyString("ladies"), "drinks")
    How are you ladies!!
    All your drinks are belong to us.

Classic class instances are also supported (although the lookup process
is slower than for new-style instances)::

    >>> class X: pass
    >>> class Y(X): pass

    >>> @move.when_type(X)
    ... def move_x(item, target):
    ...     print "Someone set us up the %s!!!" % (target,)

    >>> move(X(), "bomb")
    Someone set us up the bomb!!!

    >>> move(Y(), "dance")
    Someone set us up the dance!!!

And the ``when_type()`` decorator only accepts classes or types::

    >>> @move.when_type(23)
    ... def move_23(item, target):
    ...     print "You have no chance to survive!"
    Traceback (most recent call last):
      ...
    TypeError: 23 is not a type or class

You can obtain a function's default implementation using its ``default``
attribute::

    >>> @move.when_type(Y)
    ... def move_y(item, target):
    ...     print "Someone set us up the %s!!!" % (target,)
    ...     move.default(item, target)

    >>> move(Y(), "dance")
    Someone set us up the dance!!!
    what you say?!


``help()`` and other documentation tools see generic functions as normal
function objects, with the same name, attributes, docstring, and module as
the prototype/default function::

    >>> help(move)
    Help on function move:
    ...
    move(*args, **kw)
        Default implementation goes here
    ...


Limitations
-----------

* The first argument is always used for dispatching, and it must always be
  passed *positionally* when the function is called.

* Documentation tools don't see the function's original argument signature, so
  you have to describe it in the docstring.

* If you have optional arguments, you must duplicate them on every method in
  order for them to work correctly.  (On the plus side, it means you can have
  different defaults or required arguments for each method, although relying on
  that quirk probably isn't a good idea.)

These restrictions may be lifted in later releases, if I feel the need.  They
would require runtime code generation the way I do it in ``RuleDispatch``,
however, which is somewhat of a pain.  (Alternately I could use the
``BytecodeAssembler`` package to do the code generation, as that's a lot easier
to use than string-based code generation, but that would introduce more
dependencies, and I'm trying to keep this simple so I can just
toss it into Chandler without a big footprint increase.)


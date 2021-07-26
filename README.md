# Python Utilities I wrote

This repository contains a few python utilities I think may be useful to some people (mainly me).
They do things like make a callable `strict` (that is, only allow it to accept and return the types given in its annotations, if those exist) (see `utils.decorators.strict`)

## modules

Currently I have some decorators, some things to do with types, and a cache module

### decorators
- `overload` allows you to specify different implementations of a function based on the types given to it
- `strict` allows you to make a function strict, as described above
- `template` allows you to make a "class template", as seen in C++ (except of course, everything in python happens at runtime, including type creation)

### types
- `NaturalNumber` and `StrictNaturalNumber`
- my own `isinstance` function that lets you check `Union` types as well

### cache
- a cache decorator that lets you specify a cache policy at function call time

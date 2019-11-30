# pysh

pysh brings the power of a general-purpose language to the command line by providing an auxiliary syntax for Python.

## components

pysh contains several components designed to improve developer quality of life when controlling a computer using the command line:

### pysh syntax

- alternative syntax to make Python ergonomic enough to use in a shell
- thin syntax layer is fully reversable into idiomatic standard Python

### frontends

- (in development) tty frontend (like `sh`)
- (planned) matrix frontend (like `mc`)
- (planned) full GUI frontend (maybe Wayland/Qt)
- (planned) webapp frontend (vanilla es6, service workers)
- (planned) templated web frontend (no client-side js necessary)

### prelude

- (planned) accomplish typical shell tasks without imports or module namespaces

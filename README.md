# Python Utilities
V2 of my python utilities (includes a GDT library)

## Usage

The pv_py_utils folder must be next to your main python file (in your current working directory).

E.g.:
```md
my_python_project/
├── pv_py_utils/
│   └── ...
├── __init__.py
├── gui.py
├── main.py
└── requirements.txt
```

## Outline of the modules

### `console`

Contains functions such as `log()`, `warning()`, `underline()`, `bold()`, `progress_bar()`, `timef()`, `bytesf()` etc.

You can print in colors by using the `bcolors` class. Pass it into the `color` parameter of a print-like function or append it to the start of the string.

You can do things like easily print the time something takes:

```py
from pv_py_utils import stdlib, console

start_time = stdlib.get_time() # Gets the current CPU time

for _ in range( 10 ):
	stdlib.wait( 2 ) # Equivalent to time.sleep( 2 )

end_time = stdlib.get_time()

console.log( "Executed logic in", console.timef( end_time - start_time ) )

# Output:
# | >> Executed logic in 20 seconds
```

`console.timef()` will dynamically make the unit singular if it's 1. `console.timef()` will also get remaining time from the calculation and format it with the correct unit.

E.g.:
- 180 (w/ a granularity of 2) would return "3 mins"
- 192.152 (w/ a granularity of 2) would return "3 mins, 12 secs"
- 192.152 (w/ a granularity of 3) would return "3 mins, 12 secs, 151 ms"
- 4825 (w/ a granularity of 2) would return "1 hour, 20 mins"
- 4825 (w/ a granularity of 3) would return "1 hour, 20 mins, 25 secs"

The same concept applies with `console.bytesf()`. You pass in an integer of the number of bytes, and it will format it based on your granularity.

For more function-specific information, hover over the function in VS Code or check the summary yourself in the function definition.

### `image`

Currently only has 2 functions: `image.get_dimensions()` and `image.has_alpha()`. They're pretty self-explanatory.

### `log`

Log level defaults to highest (error). `console.log()`, `console.warning()` and `console.error()` all use `log.info()`, `log.warning()` and `log.error()` respectively.

### `pathlib`

Higher-level access to `os.path` functions. E.g. `pathlib.get_base_name()` gives you the option of returning the extension or not through a boolean parameter.

### `stdlib`

Contains miscellaneous functions that don't belong to any specific module, or are "standard". E.g.

This module's `__all__` is also imported when you do `from pv_py_utils import *` for convenience, as constants like `true`, `false` and `undefined` are defined and exported through `__all__` so you no longer have to capitalise boolean statements. `undefined` is equal to `None` because I'm used to using undefined thanks to GSC.

I also define useful functions:
- `clamp()`, which is not otherwise seen in Python
- A simple implementation of a binary search algorithm through `binary_search()`
- `get_py_version()`, returning current py version as a string, e.g. `"3.11"`
- `pip_install()`, allowing you to install a python module at runtime.
- `exit()` (which runs `input()` w/ a message before running `sys.exit()`), `concatenate()` (and its short form version called `concat()`)

### `sysframe`

Higher-level access to the `inspect` module, allowing you to get parent function names, for example, or get the line number of the current line that is being executed, get the name of the current python file that is being executed, getting the current function name, etc. etc.

# ECVI – documentation
for version 0.0.3
## commands
**„spaces”** and „enters” are very important, look for the examples
### jump
easy if, without specific else (witch is the next line)
`jump to_what_line_(int) jump_if_>_0_(int)`
### !jump
easy if, without specific else (witch is the next line)
`!jump to_what_line_(int) jump_if_<=_0_(int)`
### mov
like jumps, but you do not name a specific line, but the shift from the `mov` line
`mov -2 (ax)`
### !mov
like !jump, but mov
`!mov -2 (ax)`
### print
add str to output str, witch will be returned at the end (when program exited)
`print arg1_(int or str, all will be converted to str) *arg2_optional *arg3_optional …`
### set
set a number (int) to variable "name_of_variable", add is default, you can use `-(name_of_variable)` to subtract
`set name_of_variable arg1_(int or str, all will be converted to int) *arg2_optional *arg3_optional …`
### str
the same like `set`, but for str (without subtracting)
`str name_of_variable arg1_(int or str, all will be converted to str) *arg2_optional *arg3_optional …`
### multi
set a number (int) to variable "name_of_variable", but this time it multiplies
`multi name_of_variable arg1_(int or str, all will be converted to int) *arg2_optional *arg3_optional …`
### def
it is used to definite new variable (int or str)
`def name_of_variable value_(int or str)`
### time
sets time in variable time; like `time.time()` in python3
`time`
## is use
in a practical way…
### using data in ECVI
if you want to use a variable (must be definite):
`(name_of_variable)`
if you want to use string → (str):
`"new_string"`
if you want to use a number → (int):
`new_number`
if you want to use a value from a variable to use the variable of this name, use:
`[(variable_A)]` → `(value_from_variable_A)`

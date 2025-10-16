solution0="""The result isn't exactly 0.3 because of precision limitations in binary floating-point representation.\n Internally, 0.1 and 0.2 can't be represented exactly as binary fractions, so their sum ends up being a number very close to 0.3, but not exactly 0.3.\n As a result, the condition a == 0.3 evaluates to False, triggering the else statement. => In general applies: avoid comparisons with floats!"""

solution_zen="""print(''.join([this.d.get(char, char) for char in this.s]))
With this line, we can can decrypt the Cesar Cypher.
For every character in this.s, the code checks if it exists in this.d. If the character exists in this.d, it replaces it with the corresponding value from the dictionary. If not, it leaves the character unchanged (returns char itself). 
''.join(...) takes the list of characters returned by the list comprehension and joins them into a single string, with no separator between the characters."""

solution_builtin="""There are many many error types! Errors are a big thing in Python, as it seems...""" 

solution1="""len(dir(int)): 73"""
#solution2

# --- Part III ---
solution_int = """Even for a simple int, all handling is managed with member functions! This reflects the overall abstraction of Python (e.g. compared to C). We only deal with abstracted objects, while the the technical backend is fully handled by the interpreter."""


solution3 = """No. Because assigning a value to b creates a new object which b then references -> it is decoupled from a! Try it out with id()."""

solution_ref1 = """Despite 'a' keeps its type, but 'int' is not mutable. Therefore, the asignment is a re-assignment with a nem memory allocation. The reference 'b' to the old a, however, keeps the old value of 'a' alive at the old address! This needs to be considered when writing memory efficient code!"""
solution_ref2="""Integers (and a few other built-ins, mostly the immutables: str, float, tuple) are also handled via Py_INCREF/Py_DECREF c_call, but through slightly different internal code paths, mainly for optimization reasons. They are often passed through additional C-level reference handling macros (sometimes incrementing a borrowed reference while fetching the value, adding an extra temporary INCREF).
The tracked count can therefore differ by 1 depending on how the object type is handled internally.

What happens step by step:
When you create test_var = 1234567, a new int object is allocated -> It gets a reference count of 1.
Now, when calling sys.getrefcount(test_var), the function call itself temporarily creates another reference (to pass the object into the underlying C function macros for optimization) -> Now, the refcount is 2.
Then, sys.getrefcount adds one more reference temporarily while retrieving the count internally in C -> 3.
After the call returns, the temporary references are derefenced and the count goes back to 1."""

def print_ref_count() -> None:
    import sys
    [print(f'{i}: {sys.getrefcount(i)}') for i in range(-10, 300)]

solution_ref3="""In modern CPython (>3.12), many “forever” objects like small integers are 'immortal' -> Small integers are a globally shared int (defacto singletons).
CPython marks such objects with a very large refcount (a sentinel) so they’re never deallocated.
The number is expected and not the “real” number of actually active references. By marking them immortal, Python can skip refcount updates entirely, gaining performance."""


# --- (Im)mutable ---
solution_im1="""Yes! For mutable objects, we do not have a re-assignement and therefore, another reference ('b') still points to the original object!
Code:
a = [1, 2, 3]  # list
b = a
print(id(a))
print(id(b))
a[0] = 10
print(id(a))
print(id(b))
print(b)
"""
solution_im2="""No. The references do not work like references and 'real' pointers in C! When we change 'b', this is a re-assignment!
Code:
b = [0,0,0]
print(id(a))
print(id(b))
print(a)
"""
solution_im3="""ALL (!) immutable. Therefore, also tuples and ints - as long as the elements are immutable!
Code:
print(dict({'apple': 1, 'banana': 2, ('apple','banana'): 3}))
print(dict({'apple': 1, 'banana': 2, ('apple',['banana']): 3}))  # Will fail!
"""

# --- Callable ---
solution_call1="""int() is simply the int constructor, which can be used for casting! In the example above, this does not work, as the instance of int 'x' does not implement the int constructor."""
solution_call2="""The logging should not spoil the runtime measurement!"""

# --- Speed ---
solution_speed0=""""""
solution_speed1="""Printing (or logging) in tight loops destroys performance in any language,
but in Python, it is even worse because print() involves type conversion, function call overhead, reference management, and GIL synchronization!"""
solution_speed2="""C implements low-level arithmetics and high-performant, compiled loops. On top, Python has a comparably large interpreter overhead."""





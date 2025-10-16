tip0="""Use dir(int) to get the members. BUT: do not count them! You will get a list from dir(int). Check, if lists may have a handy member that gives you the length."""  
tip1="""
def print_ref_count() -> None:
    import sys
    [print(f'{i}: {sys.getrefcount(i)}') for i in range(-10, 300)]
"""
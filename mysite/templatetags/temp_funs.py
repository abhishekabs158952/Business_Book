from django import template

register = template.Library()

def add_val(value, arg):
    length=len(arg)
    arg=range(length+1)
    print(len(arg))
    return arg
    
def sub_val(value, arg):
    length=len(arg)
    if length>1:
        arg=range(length-1)
    print(len(arg))
    return arg
    
register.filter('add_val', add_val)
register.filter('sub_val', sub_val)
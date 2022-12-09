print("-------------------------------------------------------------------------------")
print("# ASSIGNING FUNCTIONS TO VARIABLES")
def my_function(number):
    return number + 1
my_new_function = my_function
print(my_new_function(1))

print("-------------------------------------------------------------------------------")
print("# DEFINING FUNCTIONS INSIDE OTHER FUNCTIONS")
def my_function(number):
    def my_inner_function(number):
        return number + 1
    result = my_inner_function(number)
    return result
print(my_function(2))

print("-------------------------------------------------------------------------------")
print("# PASSING FUNCTIONS AS ARGUMENTS TO OTHER FUNCTIONS")
def my_function(number):
    return number + 1
def call_my_function(passed_function):
    number_to_add = 3
    return passed_function(number_to_add)
print(call_my_function(my_function))

print("-------------------------------------------------------------------------------")
print("# FUNCTIONS RETURNING OTHER FUNCTIONS")
def hello_function():
    def say_hi():
        return "Hi"
    return say_hi
hello = hello_function()
print(hello())

print("-------------------------------------------------------------------------------")
print("# NESTED FUNCTIONS HAVE ACCESS TO THE ENCLOSING FUNCTION'S VARIABLE SCOPE")
def print_message(message):
    "Enclosing function"
    def message_send():
        "Nested function"
        print(message)
    message_send()
print_message("Some random message")

print("-------------------------------------------------------------------------------")
print("# CREATING DECORATORS")
def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

# Classic syntax
def say_hi():
    return "hi there"
decorate = uppercase_decorator(say_hi)
print("- Decorator classic syntax")
print(decorate())

# @ syntax
@uppercase_decorator
def say_hey():
    return "hey there"
print("- Decorator @ syntax")
print(say_hey())

print("-------------------------------------------------------------------------------")
print("# APPLYING MULTIPLE DECORATORS TO A SINGLE FUNCTION")
def split_string(function):
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string
    return wrapper

## Applies from the bottom's up
@split_string # Apply second
@uppercase_decorator # Apply first
def say_ho():
    return "ho there"
print(say_ho())

print("-------------------------------------------------------------------------------")
print("# ACCEPTING ARGUMENTS IN DECORATOR FUNCTIONS")
def decorator_with_arguments(function):
    def wrapper_accepting_arguments(arg1, arg2):
        print ("My arguments are: {0} {1}".format(arg1, arg2))
        function(arg1,arg2)
    return wrapper_accepting_arguments

@decorator_with_arguments
def cities(city_one, city_two):
    print("Cities I love ar {0} and {1}".format(city_one, city_two))

cities("London","New-York")

print("-------------------------------------------------------------------------------")
print("# DEFINING GENERAL PURPOSE DECORATORS")
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    def a_wrapper_accepting_arbitrary_arguments(*args,**kwargs):
        print('The positional arguments are', args)
        print('The keyword arguments are', kwargs)
        function_to_decorate(*args)
    return a_wrapper_accepting_arbitrary_arguments

@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print("No arguments here.")

print("- Function with no arguments")
function_with_no_argument()

@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print(a, b, c)

print("- Function with arguments")
function_with_arguments(1,2,3)

# Keyword arguments are passed using keywords
@a_decorator_passing_arbitrary_arguments
def function_with_keyword_arguments():
    print("This has shown keyword arguments")

print("- Function with keywords arguments")
function_with_keyword_arguments(first_name="Derrick", last_name="Mwiti")

print("-------------------------------------------------------------------------------")
print("# PASSING ARGUMENTS TO THE DECORATOR")
def decorator_maker_with_arguments(decorator_arg1, decorator_arg2, decorator_arg3):
    def decorator(func):
        def wrapper(function_arg1, function_arg2, function_arg3) :
            "This is the wrapper function"
            print("The wrapper can access all the variables\n"
                  "\t- from the decorator maker: {0} {1} {2}\n"
                  "\t- from the function call: {3} {4} {5}\n"
                  "and pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,decorator_arg3,
                          function_arg1, function_arg2,function_arg3))
            return func(function_arg1, function_arg2,function_arg3)

        return wrapper

    return decorator

pandas = "Pandas"
@decorator_maker_with_arguments(pandas, "Numpy","Scikit-learn")
def decorated_function_with_arguments(function_arg1, function_arg2,function_arg3):
    print("This is the decorated function and it only knows about its arguments: {0}"
           " {1}" " {2}".format(function_arg1, function_arg2,function_arg3))

decorated_function_with_arguments(pandas, "Science", "Tools")
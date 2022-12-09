# See https://www.geeksforgeeks.org/python-os-environ-object/

# -----------------------------------------------------------------------------
# Code #1: Use of os.environ to get access of environment variables
# Python program to explain os.environ object
  
# importing os module 
import os
import pprint
  
# Get the list of user's
# environment variables
env_var = os.environ
  
# Print the list of user's
# environment variables
print("User's Environment variable:")
pprint.pprint(dict(env_var), width = 1)

# -----------------------------------------------------------------------------
# Code #2: Accessing a particular environment variable
# Get the value of
# 'HOME' environment variable
home = os.environ['HOME']
  
# Print the value of
# 'HOME' environment variable
print("HOME:", home)
  
# Get the value of
# 'JAVA_HOME' environment variable
# using get operation of dictionary
java_home = os.environ.get('JAVA_HOME')
  
# Print the value of
# 'JAVA_HOME' environment variable
print("JAVA_HOME:", java_home)

# -----------------------------------------------------------------------------
# Code #3: Modifying a environment variable
# Print the value of
# 'JAVA_HOME'  environment variable 
print("JAVA_HOME:", os.environ['JAVA_HOME'])
  
# Modify the value of
# 'JAVA_HOME'  environment variable 
os.environ['JAVA_HOME'] = '/home / ihritik / jdk-10.0.1'
  
# Print the modified value of
# 'JAVA_HOME' environment variable
print("Modified JAVA_HOME:", os.environ['JAVA_HOME'])


# -----------------------------------------------------------------------------
# Code #4: Adding a new environment variable
# Python program to explain os.environ object

# importing os module
import os

# Add a new environment variable
os.environ['GeeksForGeeks'] = 'www.geeksforgeeks.org'

# Get the value of
# Added environment variable
print("GeeksForGeeks:", os.environ['GeeksForGeeks'])



# -----------------------------------------------------------------------------
# Code #5: Accessing a environment variable which does not exists
# Python program to explain os.environ object

# importing os module
import os

# Print the value of
# 'MY_HOME' environment variable
print("MY_HOME:", os.environ['MY_HOME'])


# If the key does not exists
# it will produce an error

# -----------------------------------------------------------------------------
# Code #6: Handling error while Accessing a environment variable which does not exists
# Python program to explain os.environ object

# importing os module
import os

# Method 1
# Print the value of
# 'MY_HOME' environment variable
print("MY_HOME:", os.environ.get('MY_HOME', "Environment variable does not exist"))


# Method 2
try:
	print("MY_HOME:", os.environ['MY_HOME'])
except KeyError:
	print("Environment variable does not exist")

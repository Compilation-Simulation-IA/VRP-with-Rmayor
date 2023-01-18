import networkx as nx
import matplotlib.pyplot as plt
import random
import datetime



from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

def fibonacci( n):
    if n==0 or n==1:
        return 1
    return fibonacci(n -1) + fibonacci(n - 2)

print(fibonacci(20))
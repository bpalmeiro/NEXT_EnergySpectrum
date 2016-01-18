from tools import *
from sys import argv

prefijo = argv[1] if len(argv) > 1 else 'Toy/'

for x,y,z,E,dE,chiR,chiN in ReadData(prefijo):
    a = Plot4D(x,y,z,E)
    raw_input()

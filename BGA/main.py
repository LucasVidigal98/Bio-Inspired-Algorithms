from AG import AG
from graphic import plot
import sys

npop = 30
ngen = 30
nelite = 1
pc = 1
pm = 0.05
precision = 0
dimension = 0

try:
    precision = int(sys.argv[1])
    dimension = int(sys.argv[2])
except:
    precision = 6
    dimension = 2

genetic_algorithm = AG(npop, ngen, nelite, precision, dimension, pc, pm)
history = genetic_algorithm.init()
plot(history, precision, dimension)

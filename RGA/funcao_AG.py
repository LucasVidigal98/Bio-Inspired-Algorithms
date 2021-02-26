# coding: utf-8
import math
import numpy as np


def func_obj(x):

	n = float(len(x))
	f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))

	t = 0
	for i in range(0, len(x)):
		t += np.cos(2 * math.pi * x[i])

	s_exp = 1.0/n * t
	f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
    
	return f



x = [-2,2]
print (func_obj(x))

x =[ -0.01,-0.01]

print (func_obj(x))


x = [0,0]
print (func_obj(x))

x =[ 0.01,0.01]

print(func_obj(x))


x =[ 2,2]

print(func_obj(x))

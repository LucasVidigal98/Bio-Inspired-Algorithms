from PSOA import PSO
from graphic import plot
import sys

try:
    w = float(sys.argv[1])
    c1 = float(sys.argv[2])
    c2 = float(sys.argv[3])
except:
    print('Erro nos praêmtros W,C1,C2 - python3 main.py w c1 c2')
    sys.exit(1)

p = PSO(w, c1, c2, 20, 100)
history, g_best = p.init()
plot(history, w, c1, c2)
print(f'Valor FO = {history[99][1]} g_best = {g_best}')

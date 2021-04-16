import numpy as np


def calculate_statics(statics_dict=dict()):
    median = list()
    dsvp = list()

    for key in statics_dict.keys():
        median.append(statics_dict[key]["Media"])
        dsvp.append(statics_dict[key]["DSVP"])

    #print('Média das gerações = ' + str(np.median(median)))
    #print('Desvio Padrão Médio = ' + str(np.std(dsvp)))

    return [np.median(median), np.std(dsvp)]


def save_statics(best_fo=float, best_median=float, best_dsvp=float, best_history=list(), npop=int(), ngen=int(), pc=float, pm=float):
    file_name = f'{npop}_{ngen}_{pc}_{pm}.tsv'
    file = open(f'Exec/{file_name}', 'w')

    best_fo = round(best_fo, 2)
    best_dsvp = round(best_dsvp, 2)
    best_median = round(best_median, 2)

    file.write(
        f'{npop}\t{ngen}\t{pc}\t{pm}\t{best_fo}\t{best_median}\t{best_dsvp}\n')
    file.write(str(best_history))
    file.close()

    table = open('Table.csv', 'a')
    table.write(
        f'{npop}\t{ngen}\t{pc}\t{pm}\t{best_fo}\t{best_median}\t{best_dsvp}\n')
    table.close()

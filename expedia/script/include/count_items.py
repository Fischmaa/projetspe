import pandas as pd
import numpy as np

import time

def count_values(file, col, nb_lignes):
        start_time = time.time()
        
        print("Lecture du fichier...")

        ch_size = 100000

        chunks = pd.read_csv(file, iterator=True, chunksize=ch_size, usecols=[col])
        values = pd.read_csv(file, nrows=1, usecols=[col])

        current_chunk = 0
        chunk_nb = np.ceil(nb_lignes/ch_size)

        print("Début du compte du nombre de valeurs différentes")
        for chunk in chunks:
                values = values.append(chunk).drop_duplicates(col)
                current_chunk += 1;
                print("{} %".format(np.round(current_chunk*100/chunk_nb, 2)))

        print("Temps d'exécution : {} seconds".format(np.round(time.time()-start_time,2)))
        print("Nombre de valeurs : {}".format(len(values)))
        return len(values),values


import pandas as pd
import numpy as np
from threading import Thread, RLock

import time

class Count (Thread):
	def __init__(self,chunk,values,col):
		Thread.__init__(self)
		self.chunk = chunk
		self.values = values
		self.col = col
		
		
	def run(self):
		self.values = self.values.append(self.chunk).drop_duplicates(self.col)
		

def count_values(file, col, nb_lignes, nb_threads):
        start_time = time.time()
        
        print("Lecture du fichier...")

        ch_size = 100000

        chunks = pd.read_csv(file, iterator=True, chunksize=ch_size, usecols=[col])
        values = pd.read_csv(file, nrows=1, usecols=[col])

        current_chunk = 0
        chunk_nb = np.ceil(nb_lignes/ch_size)

        print("Début du compte du nombre de valeurs différentes")
        
        threads = []
        current_thread = 0;
        
        for chunk in chunks:
        	threads.append(Count(chunk,values,col))
        	threads[current_thread].start()
        		
        	current_chunk += 1;
        	current_thread = (current_thread + 1);
        	print("thread {}  {} %".format(current_thread,np.round(current_chunk*100/chunk_nb, 2)))
        
        

        print("Temps d'exécution : {} seconds".format(np.round(time.time()-start_time,2)))
        print("Nombre de valeurs : {}".format(len(values)))
        return len(values),values


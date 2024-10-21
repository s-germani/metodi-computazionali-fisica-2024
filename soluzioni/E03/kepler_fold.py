#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 3 - Numpy, Pandas, Matplotlib:      #
#                                                   #
#   Lettura File CSV (nella sottocartella dati)     #
#   + prduzione grafici curva di luce con folding   #
#   + valori mediati curva di luce con folding      #
#                                                   #
#####################################################

import sys,os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


################################### Dati Input  ##########################################
# Lettura file

kplr1 = 'https://raw.githubusercontent.com/s-germani/metodi-computazionali-fisica-2024/refs/heads/main/dati/moduli_scientifici/kplr010666592-2011240104155_slc.csv'
#kplr1 = 'dati/kplr010666592-2011240104155_slc.csv'

kplrdf = pd.read_csv(kplr1)

print('Columns:', kplrdf.columns)
#print(lcdf)

# ------------- Colonne usate per i grafici ----------------------------------------------
#  TIME           : BJD - 2454833 --> barycenter corrected JD
#  PDCSAP_FLUX    : e-/s          --> Pre-search Data Conditioning (PDC)
#                                      aperture photometry flux, (electrons per second) 
#  PDCSAP_FLUX_ERR: e-/s          --> PDC aperture photometry flux error
#-----------------------------------------------------------------------------------------


## grafico Flusso vs. Tempo 
fig, ax = plt.subplots(figsize=(12,6))
plt.errorbar(kplrdf['TIME'], kplrdf['PDCSAP_FLUX'], yerr=kplrdf['PDCSAP_FLUX_ERR'], fmt='.', color='cornflowerblue' )
plt.xlabel('Time (BJD - 2454833)', fontsize=14)
plt.ylabel(r'Flux ($e^-/s$)',      fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()



t0_fold = 939.32
t1_fold = 941.52


T = t1_fold-t0_fold


# Scan Periodo 
#tt = np.linspace(2.2040, 2.2060, 5)
tt = np.linspace(2.2020, 2.2080, 5)

fig, ax = plt.subplots(5,1, figsize=(12,12))
for t, ai in zip(tt, ax):

    folded_time = (((kplrdf['TIME'].values - t0_fold+t/2)*1e6).astype(int)%int(t*1e6) )/1e6 -t/2

    ## grafico Flusso vs. Tempo con folding
    ai.errorbar(folded_time, kplrdf['PDCSAP_FLUX'], yerr=kplrdf['PDCSAP_FLUX_ERR'], fmt='.', color='cornflowerblue' )
    ai.set_xlabel('Time (BJD - 2454833)', fontsize=14)
    ai.set_ylabel(r'Flux ($e^-/s$)',      fontsize=14)
    ai.set_xlim(-0.5,0.5)

plt.show()



# Periodo orbitale identificato
T=2.2047

# Folding con periodo identificato
folded_time = (((kplrdf['TIME'].values - t0_fold+T/2)*1e6).astype(int)%int(T*1e6) )/1e6 -T/2

# Aggiungo colonna con il tempo riferito al periodo (Folded Time)
kplrdf['FOLDED_TIME'] = folded_time

# Riordino DataFrame sulla base del Folded Time (non necessario ma utule in funzioni di possibili ulteriori elaborazioni)
kplrdf.sort_values(by='FOLDED_TIME', inplace=True)
print(kplrdf)


## grafico Flusso vs. Tempo con folding
fig, ax = plt.subplots(figsize=(12,6))
plt.errorbar(kplrdf['FOLDED_TIME'], kplrdf['PDCSAP_FLUX'], yerr=kplrdf['PDCSAP_FLUX_ERR'], fmt='.', color='cornflowerblue' )
plt.xlabel('Time (BJD - 2454833)', fontsize=14)
plt.ylabel(r'Flux ($e^-/s$)',      fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.show()



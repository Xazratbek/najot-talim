from multiprocessing import Pool

def hisobla(son):
    return son * son

with Pool(processes=8) as pool:
    natijalar = pool.map(hisobla, range(8))
print(natijalar)
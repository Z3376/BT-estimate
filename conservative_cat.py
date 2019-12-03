from astropy.io import fits
import pandas as pd
import numpy as np
from tqdm import tqdm

def binary(n):
	binn = np.zeros(32,dtype=int)
	ctr = 0
	while(n>0):
		binn[ctr] = n%2
		n = n//2
		ctr+=1
	return binn

with fits.open('Meert_rBT_all.fits') as hdul:
	data = hdul[1].data
	columns = hdul[1].columns

flag = list(map(binary,data['ffl']))
flag_indices = []

for i in tqdm(range(len(flag))):
	if(flag[i][19]!=1 and flag[i][13]!=1 and flag[i][11]==1 and data['nBg'][i]<8):
			flag_indices.append(i)

c = [[] for i in range(len(columns))]

print(len(flag_indices))

i = 0
for col in columns:
	c[i] = fits.Column(name=col.name,format=col.format,array=data[col.name][flag_indices])
	i+=1

cols = fits.ColDefs([c[i] for i in range(len(c))])

hdu = fits.BinTableHDU.from_columns(cols)

hdu.writeto('Meert_rBT_two_component.fits')

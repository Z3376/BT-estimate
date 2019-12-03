from astropy.io import fits
import os
import numpy as np
from tqdm import tqdm
import argparse
import random
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('num',help='Number of images to download',type=int)
parser.add_argument('--cat',help='Catalogue fits file. [default = Meert_rBT_two_component.fits]',type=str)
parser.add_argument('--scale',help='arcsec/pixel [default = 0.396127 (natural scale of SDSS)]',type=float)
parser.add_argument('--size',help='Image size [default=128]',type=int)

def get_url(ra,dec,width,height):
	# return 'http://skyserver.sdss.org/dr7/SkyServerWS/ImgCutout/getjpeg?ra='+str(ra)+'&dec='+str(dec)+'&scale='+str(scale)+'&width='+str(width)+'&height='+str(height)
	return 'http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra='+str(ra)+'&dec='+str(dec)+'&scale='+str(scale)+'&width='+str(width)+'&height='+str(height)

def get_filename(objid,ra,dec,BT,ctr):
	return './img/'+str(ctr)+'_objID_'+str(objid)+'_RA_'+str(ra)+'_DEC_'+str(dec)+'_BT_'+str(BT)+'.jpg'


args = parser.parse_args()

num = args.num

if(args.scale):
	scale = args.scale
else:
	scale = 0.396127

if(args.size):
	size = args.size
else:
	size = 128

if(args.cat):
	cat_name = args.cat
else:
	cat_name = 'Meert_rBT_two_component.fits'

with fits.open(cat_name) as hdul:
	data = hdul[1].data

ln = len(data['_RAJ2000'])

if(num==0):
	num=ln

ind_arr = random.sample(range(ln),num)

flag = True
while(flag):
	skip_arr = []
	for i in tqdm(range(len(ind_arr))):
		ind = ind_arr[i]
		objid = data['objID'][ind]
		ra = data['_RAJ2000'][ind]
		dec = data['_DEJ2000'][ind]
		BT = data['BT'][ind]
		url = get_url(ra,dec,size,size)
		file = get_filename(objid,ra,dec,BT,ind)
		try:
			with open(os.devnull,'wb') as devnull:
				subprocess.check_call(['wget','-O',file,url],stdout=devnull,stderr=subprocess.STDOUT)
		except:
			print('Skipping')
			skip_arr.append(ind)
	if(len(skip_arr)==0):
		flag = False
	else:
		ind_arr = skip_arr[:]
		print('Skipped: '+str(len(skip_arr)))

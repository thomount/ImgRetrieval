import cv2
import pandas as pd
import os
import numpy

def getfiles(path):
	folders = os.listdir(path)
	#print(folders)
	ret = []
	for folder in folders:
		files = os.listdir(path+'/'+folder)
		#print(folder, ':', file)
		ret += [path+'/'+folder+'/'+x for x in files if x[-3:] == "jpg"]
	#print(ret)
	return ret


def pre(ipath, opath1, opath2):
	files = getfiles(ipath)
	img = cv2.imread(files[0])
	#print(numpy.reshape(img, (img.shape[0]*img.shape[1], 3)))
	#cv2.imshow("test", img)
	#cv2.waitKey(0)
	df16 = pd.DataFrame()
	df128 = pd.DataFrame()
	tot, t = len(files), 0
	
	for file in files:
		t += 1
		if t % 10 == 0:
			print(t, '/', tot)
		img = cv2.imread(file)
		n, m = img.shape[0], img.shape[1]
		img = pd.DataFrame(numpy.reshape(img, (n*m, 3)))
		img16 = img.copy()
		img16.loc[:, 0] //=128;
		img16.loc[:, 1] //=64;
		img16.loc[:, 2] //=128;
		img16.loc[:, 3] = img16.loc[:, 0]*8+img16.loc[:, 1]*2+img16.loc[:, 2];
		#print(img16)
		img128 = img.copy()
		img128.loc[:, 0] //=64;
		img128.loc[:, 1] //=32;
		img128.loc[:, 2] //=64;
		img128.loc[:, 3] = img128.loc[:, 0]*32+img128.loc[:, 1]*4+img128.loc[:, 2];
		
		pixelid16 = img16.loc[:, 3].values.reshape(n*m).tolist()
		pixelid128 = img128.loc[:, 3].values.reshape(n*m).tolist()
		#print(type(pixelid16), pixelid16.shape)
		d16 = [pixelid16.count(i) for i in range(16)]
		d128 = [pixelid128.count(i) for i in range(128)]
		#print(d16)
		#print(d128)
		df16 = df16.append([[file, d16]])
		df128 = df128.append([[file, d128]])
	df16.to_csv(opath1)
	df128.to_csv(opath2)


if __name__ == "__main__":
	pre('../data/DataSet', '../output/vec16.csv', '../output/vec128.csv')
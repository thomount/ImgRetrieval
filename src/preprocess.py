import cv2
import pandas as pd
import os
import numpy as np

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

BN = 4
BM = 4
def pre(ipath, opath1, size, flag=0):
	files = getfiles(ipath)
	df = pd.DataFrame()
	tot, t = len(files), 0

	size1 = size >> 1
	pw = 0
	while size1 > 1:
		pw += 1
		size1 >>= 3
	div1 = 256 >> pw
	tm = [1<<(2*pw+1), 1<<(pw)]
	print(div1)
	if flag == 1:
		size <<= (pw)
		print(size)
	for file in files:
		t += 1
		if t % 10 == 0:
			print(t, '/', tot)
		img = cv2.imread(file)
		n, m = img.shape[0], img.shape[1]
		if flag == 2:
			gimg = cv2.imread(file)
			gd = np.zeros((BN,BM,3), dtype = int)
			nd = [int(n*i/BN) for i in range(BN+1)]
			md = [int(m*i/BM) for i in range(BM+1)]
			for i in range(BN):
				for j in range(BM):
					gd[i, j, 0] = np.mean(gimg[nd[i]:nd[i+1], md[j]:md[j+1], 0])
					gd[i, j, 1] = np.mean(gimg[nd[i]:nd[i+1], md[j]:md[j+1], 1])
					gd[i, j, 2] = np.mean(gimg[nd[i]:nd[i+1], md[j]:md[j+1], 2])
			

		img = pd.DataFrame(np.reshape(img, (n*m, 3)))
		if flag == 1:
			img.loc[:, 3] = (img.loc[:, 0]+img.loc[:, 1]+img.loc[:, 2])//3
			#print(img.loc[:, 3])
			img.loc[:, 3] //= div1
			#print(size)
			#print(256//div1)
			#print(img.loc[:, 3])
			img.loc[:, 3] *= (1<<(3*pw+1))

			#print(size)
		else:
			img.loc[:, 3] = 0
		img.loc[:, 0] //=div1
		img.loc[:, 1] //=(div1>>1)
		img.loc[:, 2] //=div1;
		img.loc[:, 3] += img.loc[:, 0]*tm[0]+img.loc[:, 1]*tm[1]+img.loc[:, 2];
		pixelid = img.loc[:, 3].values.reshape(n*m).tolist()
		d = [pixelid.count(i) for i in range(size)]
		if flag == 2:
			d += gd.reshape(BN*BM*3).tolist()
		df = df.append([[file, d]])
	df.to_csv(opath1)

if __name__ == "__main__":
	#pre('../data/DataSet', '../output/vec16.csv', 16)
	#pre('../data/DataSet', '../output/vec128.csv', 128)
	#pre('../data/DataSet', '../output/vec512.csv', 128, 1)
	pre('../data/DataSet', '../output/vec1024.csv', 1024)
	
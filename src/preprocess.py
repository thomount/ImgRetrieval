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


def pre(ipath, opath1, size, flag=False):
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
	if flag:
		size <<= 1
	for file in files:
		t += 1
		if t % 10 == 0:
			print(t, '/', tot)
		img = cv2.imread(file)
		n, m = img.shape[0], img.shape[1]
		img = pd.DataFrame(numpy.reshape(img, (n*m, 3)))
		if flag:
			img.loc[:, 3] = (img.loc[:, 0]+img.loc[:, 1]+img.loc[:, 2])//3
			#print(img.loc[:, 3])
			img.loc[:, 3] //= div1
			#print(img.loc[:, 3])
			img.loc[:, 3] *= (1<<(3*pw+1))
		else:
			img.loc[:, 3] = 0
		img.loc[:, 0] //=div1
		img.loc[:, 1] //=(div1>>1)
		img.loc[:, 2] //=div1;
		img.loc[:, 3] += img.loc[:, 0]*tm[0]+img.loc[:, 1]*tm[1]+img.loc[:, 2];
		pixelid = img.loc[:, 3].values.reshape(n*m).tolist()
		d = [pixelid.count(i) for i in range(size)]
		df = df.append([[file, d]])
	df.to_csv(opath1)

if __name__ == "__main__":
	#pre('../data/DataSet', '../output/vec16.csv', 16)
	#pre('../data/DataSet', '../output/vec128.csv', 128)
	pre('../data/DataSet', '../output/vec256.csv', 128, True)
	#pre('../data/DataSet', '../output/vec1024.csv', 1024)
	
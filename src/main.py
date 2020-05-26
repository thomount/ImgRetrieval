import pandas as pd
import numpy as np
import sys

def getQuery(path, pp):
	f = open(path)
	ret = []
	for line in f.readlines():
		if len(line) > 1:
			ret.append(pp+line.split()[0])
	return ret

def dis(a, b, t):
	if t == 0:
		return sum((a-b) ** 2)
	if t == 1:
		return -sum(np.minimum(a,b))
	if t == 2:
		return -sum((a*b)**0.5)
if __name__ == "__main__":
	argv = sys.argv
	config = [16, 0, '../input/QueryImages.txt', 0]
	if '-v=16' in argv:
		config[0] = 16
	if '-v=128' in argv:
		config[0] = 128
	if '-q' in argv:
		config[2] = '../input/QueryImages.txt'
		config[3] = 0
	if '-a' in argv:
		config[2] = '../input/AllImages.txt'
		config[3] = 1
	if '-L2' in argv:
		config[1] = 0
	if '-HI' in argv:
		config[1] = 1
	if '-Bh' in argv:
		config[1] = 2

	df = pd.read_csv('../output/vec'+str(config[0])+'.csv')

	
	Queries = getQuery(config[2],'../data/DataSet/')

	n = df.shape[0]
	dic = {}
	lis= []
	for i in range(n):
		dic[df.loc[i, '0']] = np.array(eval(df.loc[i, '1']), dtype = np.int64)
		lis.append((df.loc[i, '0'], np.array(eval(df.loc[i, '1']), dtype = np.int64)))

	if config[3] == 1:
		Of = open('../output/res_overall.txt', 'w')
		avc = []
	for query in Queries:
		tar = dic[query]
		lis.sort(key=lambda x: dis(tar, x[1], config[1]))
		if config[3] == 0:
			parts = query.split('/')
			name = '../output/quereis/res_'+parts[-2]+'_'+parts[-1][:-4]+'.txt'
			#print(parts[-2]+'_'+parts[-1][:-4])
			outf = open(name, 'w')
			for i in range(1,31):
				print(lis[i][0][16:], '\t', dis(tar, lis[i][1], config[1]), file = outf)
			outf.close()
		else:
			parts = query.split('/')
			cate = parts[-2]
			cnt = 0
			for x in lis[1:31]:
				if cate in x[0].split('/'):
					cnt += 1
			print(query[16:], '\t', cnt/30, file=Of)
			avc.append(cnt/30)
	if config[3] == 1:
		print('average = ', np.mean(avc), file = Of)
		print('average = ', np.mean(avc))
		Of.close()



	

	#for i in range()
	#print(dic16)
	#for i in range(df16.shape[0]):
		
	
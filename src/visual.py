from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('../output/vec128.csv')
n = df.shape[0]
vec = []
typ = []
for i in range(n):
	vec.append(np.array(eval(df.loc[i, '1']), dtype = np.int64).tolist())
	typ.append(df.loc[i, '0'].split('/')[-2])

#print(vec)
#print(typ)
s = ['00', '80', 'FF']
cdic = {}
i = 0
for tp in set(typ):
	cdic[tp] = '#'+s[i//9]+s[(i//3)%3]+s[i%3]
	i += 1
print(cdic)
X_pca = PCA().fit_transform(vec)

#plt.figure(figsize=(20, 15))

for i in range(n):
    #plt.scatter(X_pca[i, 0], X_pca[i, 1], s = 800, c=cdic[typ[i]], marker='$'+typ[i]+'$')
	plt.scatter(X_pca[i, 0], X_pca[i, 1], c=cdic[typ[i]])

plt.savefig('../output/words.jpg')
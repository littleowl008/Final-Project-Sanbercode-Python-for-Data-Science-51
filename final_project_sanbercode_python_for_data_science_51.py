# -*- coding: utf-8 -*-
"""Final Project Sanbercode Python for Data Science #51.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15Dxb00V2b5a6_rlV2K8oA3i6vX2XcYBq

# Sanbercode Basic Python for Data Science
# Final Project Guide
---
---
---

## 1. Business/Project Understanding


> **Objective**:
Untuk mengkategorikan negara menggunakan faktor sosial ekonomi dan kesehatan yang menentukan pembangunan negara secara keseluruhan.


> **Tentang Organisasi**:
HELP International adalah LSM kemanusiaan internasional yang berkomitmen untuk memerangi kemiskinan dan menyediakan fasilitas dan bantuan dasar bagi masyarakat  di negara-negara terbelakang saat terjadi bencana dan bencana alam.


> **Permasalahan**:
HELP International telah berhasil mengumpulkan sekitar $ 10 juta. Saat ini, CEO LSM perlu  memutuskan bagaimana menggunakan uang ini secara strategis dan efektif. Jadi, CEO harus mengambil keputusan untuk memilih negara yang paling membutuhkan bantuan. Oleh karena itu, Tugas teman-teman  adalah mengkategorikan negara menggunakan beberapa faktor sosial ekonomi dan kesehatan yang menentukan perkembangan negara secara keseluruhan. Kemudian kalian perlu menyarankan negara mana saja  yang paling perlu menjadi fokus CEO.

---
---
---
"""

import numpy as np #linear algebra
import pandas as pd #data manipulation and analysis
import seaborn as sns #data visualization
import matplotlib.pyplot as plt #data visualization
import sklearn.preprocessing as skp #machine learning (preprocessing)
import sklearn.cluster as skc #machine learning (clustering)
import warnings # ignore warnings
warnings.filterwarnings('ignore')

"""Silakan download dataset di sini :

https://drive.google.com/file/d/1LMaH9o3W5BkOCL8ECBCWL8DlbvFaFvoO/view?usp=sharing

## 2. The Data

### 2.1 Dataset Understanding
1. Elaborate the source data you're working with.
    -  What are the dataset's features?
    -  How many rows it has?
"""

df=pd.read_csv('Data_Negara_HELP.csv')
df

"""Dataset's Features:

* **Negara** : Nama negara
* **Kematian_anak**: Kematian anak di bawah usia 5 tahun per 1000 kelahiran
* **Ekspor** : Ekspor barang dan jasa perkapita
* **Kesehatan**: Total pengeluaran kesehatan perkapita
* **Impor**: Impor barang dan jasa perkapita
* **Pendapatan**: Penghasilan bersih perorang
* **Inflasi**: Pengukuran tingkat pertumbuhan tahunan dari Total GDP
* **Harapan_hidup**: Jumlah tahun rata-rata seorang anak yang baru lahir akan hidup jika pola kematian saat ini tetap sama
* **Jumlah_fertiliti**: Jumlah anak yang akan lahir dari setiap wanita jika tingkat kesuburan usia saat ini tetap sama
* **GDPperkapita**: GDP per kapita. Dihitung sebagai Total GDP dibagi dengan total populasi.

Dataset terdiri dari 167 baris x 10 kolom

Selanjutnya kita perlu melihat info dataset dengan menggunakan .info()

"""

df.info()

"""Dari info diperoleh informasi bahwa data terdiri dari 167 baris dengan 10 kolom variabel.

Selanjutnya kita perlu mencari analisa deskripsi untuk melihat karakteristik data lebih lanjut.

"""

df.describe()

"""### 2.2 Data Cleaning
1. Missing values
    - Check if exist.
    - Handle if exist.
    - Recheck after handling (see the handling result).
    - Elaborate how exactly you handle them.
    - Elaborate why do you handle them in such way.

Kita dapat memeriksa jika ada missing value pada data dengan menggunakan .isnull()
"""

df.isnull().sum()

"""Dari hasil analisa diketahui bahwa data tidak memiliki missing value.

Selanjutnya perlu dilakukan analisa jika terdapat duplikasi dalam dataset.
"""

df[df.duplicated(keep=False)]

"""Dari hasil analisa diperoleh kesimpulan bahwa tidak ada duplikasi data dalam dataset.

2. Outliers
    - Check if exist (Even better if graphical representation is used).
    - Handle if exist.
    - Recheck after handling (see the handling result).
    - Elaborate how exactly you handle them.
    - Elaborate why do you handle them in such way.

> Untuk mengetahui apakah terdapat nilai outlier dalam data, maka kita dapat menganalisisnya dengan melihat jenis distribusi dari setiap variabel data.Hal ini dapat kita lakukan dengan menggunakan Histogram. Dari bentuk distribusi dapat dilihat jika ada kemungkinan penyimpangan dari data (outlier).
"""

# memvisualisasikan distribusi dari setiap variabel data

plt.figure(figsize=(8,10))
for i, j in enumerate(df.describe().columns):
    plt.subplot(5,2, i+1)
    sns.histplot(x=df[j])
    plt.xlabel(j)
    plt.ylabel('count')
    plt.title('{} Distribution'.format(j))
    plt.subplots_adjust(wspace=.2, hspace=.5)
    plt.tight_layout()
plt.show()

"""> Dari histogram dapat diambil kesimpulan sebagai berikut :
- Kematian_anak: right-skewed distribution.
- Ekspor: right-skewed distribution.
- Kesehatan: right-skewed distribution.
- Impor: right-skewed distribution.
- Pendapatan: right-skewed distribution.
- Inflasi: right-skewed distribution.
- Harapan_hidup: left-skewed distribution.
- Jumlah_fertiliti: right-skewed distribution.
- GDPperkapita: right-skewed distribution.

Selanjutnya kita juga dapat menggunakan diagram boxplot untuk melihat jika ada data outlier dari setiap variabel data.
"""

# membuat diagram boxplot

plt.figure(figsize=(10,8))
for i, j in enumerate(df.describe().columns):
    plt.subplot(3,3, i+1)
    sns.boxplot(x=df[j])
    plt.title('{} Boxplot'.format(j))
    plt.tight_layout()

plt.show()

"""> Karena diketahui bahwa setiap negara memiliki data yang bervariasi, maka kita tidak dapat menghilangkan outlier begitu saja. Diketahui bahwa ada yang nilainya sangat tinggi tapi ada juga yang nilainya sangat rendah. Kita dapat memeriksa kembali outlier setelah kita memutuskan variabel mana yang akan kita gunakan.


> Diagram boxplot menunjukkan bahwa variabel GDPperkapita dan Pendapatan memiliki outlier terbanyak. Oleh karenanya kita perlu mengevaluasi negara mana yang memiliki kesulitan ekonomi sesuai tujuan kasus proyek ini, dengan mempertimbangkan tingkat ekonomi dan kesehatan masing-masing negara.

### 2.3 EDA Part 1
1. Do multivariate analysis on the dataset to catch the glimpse of the relation between datasets' features.


> Multivariate analysis digunakan untuk menganalisa lebih dari 2 (dua) variabel secara bersamaan. Analisis ini akan membantu kita dalam menentukan korelasi antar semua variabel dalam dataset.
Kita dapat menggunakan .pairplot() untuk membuat grup scatterplot dari setiap pasangan variabel dalam dataset.
"""

pairplot = sns.pairplot(df, corner=True)
plt.show(pairplot)

"""

> Selain itu, kita juga dapat menggunakan kombinasi .heatmap()  dengan fungsi korelasi untuk menunjukkan hubungan antar setiap variabel dalam dataset berdasarkan koefisien korelasi.
"""

correlation_metrics=df.corr()
fig = plt.figure(figsize=(12,7))
sns.heatmap(correlation_metrics,square=True, annot=True, vmax=1, vmin=-1,
            cmap='RdBu')
plt.title('Correlation Between Variables', size=14)
plt.show()

"""> Korelasi adalah metode statistik untuk menentukan apakah variabel berhubungan secara numerik atau secara kategori. Nilai koefisien korelasi dapat diinterpretasikan sebagai berikut :
- -1 hingga -0.91 ATAU 0.91 hingga 1 : sangat kuat
- -0.90 hingga -0.71 ATAU 0.71 hingga 0.90 : kuat
- -0.70 hingga -0.51 ATAU 0.51 hingga 0.70 : sedang
- -0.50 hingga -0.31 ATAU 0.31 hingga 0.50 : lemah
- -0.30 hingga -0.01 ATAU 0.01 hingga 0.30 : sangat lemah
- 0 : tidak berhubungan


> Dari diagram heatmap dan nilai korelasi di atas, dapat kita peroleh kesimpulan sebagai berikut :
- Pendapatan & GDPperkapita : korelasi sangat kuat positif
- Harapan_hidup & Jumlah_fertiliti : korelasi kuat negatif
- Jumlah_fertiliti & Kematian_anak : korelasi kuat positif
- Harapan_hidup & Kematian_anak : korelasi kuat negatif
- Ekspor & Impor : korelasi kuat positif
- Harapan_hidup & GDPperkapita : korelasi sedang positif
- Harapan_hidup & Pendapatan : korelasi sedang positif
- Pendapatan & Kematian_anak : korelasi sedang negatif
- Pendapatan & Ekspor : korelasi sedang positif

### 2.4 Feature Selection
1. Choose 2 features of the dataset to be used as the base of analyses and clustering.<b>*</b>
2. Elaborate the reason you chose them.

> Untuk menentukan variabel yang tepat, kita perlu meninjau kembali tujuan dari proyek ini. Proyek ini bertujuan untuk mengkategorikan negara menggunakan faktor sosial ekonomi dan kesehatan yang menentukan pembangunan negara secara keseluruhan.


> Variabel Pendapatan dan GDPperkapita adalah variabel yang tepat untuk mewakili faktor sosial-ekonomi suatu negara. Tapi dengan mempertimbangkan korelasi antara kedua variabel tersebut yang merupakan korelasi kuat positif, maka kita dapat hanya menggunakan variabel Pendapatan saja. Hal ini untuk mencegah hasil analisa merujuk pada negara yang memiliki Pendapatan yang tinggi.


> Selanjutnya kita perlu menentukan pasangan variabel yang tepat, untuk mewakili faktor kesehatan suatu negara, dan memiliki hubungan dengan Pendapatan. Dari korelasi heatmap, variabel Pendapatan memiliki hubungan (sedang) dengan Kematian_anak, Ekspor, dan Harapan _hidup. Dari pilihan variabel ini kita dapat menentukan Kematian _anak sebagai wakil faktor kesehatan suatu negara.  


> Dengan demikian untuk selanjutnya kita akan menggunakan variabel Pendapatan dan Kematian_anak sebagai fitur pengelompokkan.

> Sebelum kita lanjutkan ke proses penglompokkan, kita perlu melakukan 'handling outlier' seperti yang sudah disebutkan sebelumnya.
Untuk memperkecil kelompok negara yang akan kita pilih, kita dapat memfilter negara dengan Pendapatan di bawah nilai median Pendapatan, untuk memastikan bahwa perusahaan memberikan bantuam keuangan pada negara yang sangat membutuhkannya.


> Nilai yang digunakan sebagai acuan adalah nilai median karena distribusi data variabel Pendapatan berbentuk skew ke kanan, sehingga akan lebih tepat jika kita menggunakan nilai median daripada nilai mean.
"""

# filter negara dengan pendapatan di bawah nilai median
df_filter_pendapatan = df[df.Pendapatan < df.Pendapatan.median()]
df_filter_pendapatan

"""

> Dari hasil filter tersebut diperoleh jumlah negara yang dapat dipilih sekitar 50% dari jumlah awal. Kita bisa periksa kembali histogram dan boxplot untuk melihat jika masih terdapat outlier pada data."""

# membuat histogram dan boxplot baru untuk Pendapatan dan Kematian_anak
df_baru=df_filter_pendapatan

fig = plt.figure(figsize=(8,6))
plt.subplot(2,2,1)
sns.boxplot(x=df_baru['Pendapatan'])
plt.title('Pendapatan Boxplot New')
plt.tight_layout()

plt.subplot(2,2,2)
sns.boxplot(x=df_baru['GDPperkapita'])
plt.title('GDPperkapita Boxplot New')
plt.tight_layout()

plt.subplot(2,2,3)
sns.histplot(x=df_baru['Pendapatan'])
plt.title('Pendapatan Histogram New')
plt.tight_layout()

plt.subplot(2,2,4)
sns.histplot(x=df_baru["GDPperkapita"])
plt.title('GDPperkapita Histogram New')
plt.tight_layout()

plt.show()

"""> Dari diagram di atas, kita dapat menyimpulkan bahwa data baru setelah filter Pendapatan lebih "clean" dari data awal, di mana tidak terdapat nilai outlier pada data baru. Dengan demikian data baru ini dapat kita proses selanjutnya untuk Clustering.

### 2.5 EDA Part 2
1. Do univariate analyses on selected features. Elaborate what information you can extract from this.
2. Do bivariate analyses between selected features. Elaborate what information you can extract from this.

1. Univariate analysis


> Untuk melakukan Univariate Analysis pada kedua variabel, kita akan membuat Histogram & Poligon. Histogram akan menunjukkan distribusi frekuensi suatu data, sedangkan poligon akan menghubungkan titik tengah atas setiap batang histogram.
"""

# membuat histogram & polygon untuk Pendapatan dan Kematian_anak
fig = plt.figure(figsize=(8,6))
plt.subplot(2,2,1)
sns.histplot(df_baru['Pendapatan'], bins=10, alpha=0.7, color='#7BC8F6',
             edgecolor='#069AF3', label='Histogram')
hist, edges = np.histogram(df_baru['Pendapatan'], bins=10)
midpoints = (edges[1:] + edges[:-1])/2
plt.plot(midpoints, hist, color='#00008B', label='Polygon')
plt.scatter(midpoints, hist, color='#00008B', marker='o', s=20, label='Points')
plt.xlabel('Pendapatan')
plt.ylabel('Freqency')
plt.title('Histogram vs Polygon Pendapatan')
plt.legend()
plt.tight_layout()

plt.subplot(2,2,2)
sns.histplot(df_baru['Kematian_anak'], bins=10, alpha=0.7, color='#7BC8F6',
             edgecolor='#069AF3', label='Histogram')
hist, edges = np.histogram(df_baru['Kematian_anak'], bins=10)
midpoints = (edges[1:] + edges[:-1])/2
plt.plot(midpoints, hist, color='#00008B', label='Polygon')
plt.scatter(midpoints, hist, color='#00008B', marker='o', s=20, label='Points')
plt.xlabel('Kematian_anak')
plt.ylabel('Freqency')
plt.title('Histogram vs Polygon Kematian_anak')
plt.legend()
plt.tight_layout()

plt.show()

"""2. Bivariate analysis :

> Sebelum kita lakukan clustering, kita perlu melihat korelasi antar variabel yang telah kita pilih dengan menggunakan scatterplot dan fungsi .hexbin() untuk melihat konsentrasi nilai variabel tersebut.
"""

# membuat scatterplot dan hexagonal bin
fig = plt.figure(figsize=(9,4))

plt.subplot(1,2,1)
sns.scatterplot(x=df_baru['Pendapatan'],
                y=df_baru['Kematian_anak'])
plt.title('Pendapatan vs Kematian_anak')
plt.tight_layout()

plt.subplot(1,2,2)
hexplot=plt.hexbin(x=df_baru['Pendapatan'],
                   y=df_baru['Kematian_anak'],
                   gridsize = 25, cmap='Blues')
plt.title('Pendapatan vs Kematian_anak Hexbin')
plt.xlabel('Pendapatan')
plt.ylabel('Kematian_anak')
plt.colorbar(hexplot, label='count')
plt.tight_layout()

plt.show()

"""> Dari kedua diagram di atas dapat dilihat bahwa variable Pendapatan dan Kematian_anak memiliki hubungan sedang negatif. dan dari diagram hexbin menunjukkan bahwa ada hubungan kuat antara kedua variabel tersebut pada beberapa negara.

---
---
---

## 3. Clustering
3.1 Scale the Data

3.2 Decide the number of clusters, you're free to choose the method:
- Elbow method
- Silhouette score method
- Directly decide the number (Elaborate the number and why)

3.3 Do clustering with the decided amount of cluster.

3.4 Create the clustering result graph.

3.1. Scale the Data

> Membuat dataframe baru untuk proses scaling
"""

# membuat dataframe baru untuk scaling process

df_cluster = df_baru[['Negara', 'Pendapatan', 'Kematian_anak']].reset_index()
df_cluster.drop('index', inplace=True, axis=1)
display(df_cluster)

#scaling process

sc = skp.StandardScaler()
data_scale = np.array(df_cluster[['Pendapatan', 'Kematian_anak']])
scaled = sc.fit_transform(data_scale.astype(float))
df_scaled = pd.DataFrame(scaled, columns=['Pendapatan', 'Kematian_anak'])
display(df_scaled)

"""Selanjutnya kita perlu memeriksa kembali korelasi kedua variabel untuk memastikan skala yang kita gunakan sudah tepat.

"""

# do bivariate analysis untuk melihat kondisi data setelah scaling
fig = plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
sns.scatterplot(x=df_scaled['Pendapatan'],
                y=df_scaled['Kematian_anak'])
plt.title('Pendapatan vs Kematian_anak After Scaling')
plt.tight_layout()
plt.subplot(1,2,2)
hb = plt.hexbin(x=df_scaled['Pendapatan'],
                y=df_scaled['Kematian_anak'],
                gridsize = 20, cmap ='Blues')
cb = plt.colorbar(hb)
plt.title('Pendapatan vs Kematian_anak After Scaling')
plt.xlabel('Pendapatan')
plt.ylabel('Kematian_anak')
plt.tight_layout()

plt.show()

"""Dari perbandingan korelasi setelah scaling menunjukkan tidak ada perbedaan dengan sebelumnya, artinya skala kita sudah tepat.

3.2. Decide the number of cluster

> Menggunakan Elbow Method untuk menentukan K-Means
"""

# elbox method untuk menentukan k
wcss=[]
k_range = range(1,11)
for i in k_range:
    kmeans = skc.KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)
fig, ax = plt.subplots(figsize=(8, 6), dpi=80)
plt.plot(k_range, wcss, marker='o')

plt.xticks(k_range)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')

plt.show()

"""> Dari grafik di atas dapat dilihat bahwa nilai K yang tepat adalah 3"""

# validasi nilai k apakah sudah tepat

!pip install kneed

from kneed import KneeLocator
kl = KneeLocator(range(1, 11), wcss, curve="convex", direction="decreasing")
kl.elbow

"""> Dari hasil perhitungan diperoleh jumlah kelas clustering adalah K = 3

3.3. Do Clustering
"""

# Clustering K Means, K=3
kmeans_3 = skc.KMeans(n_clusters=3,random_state=42)
kmeans_3.fit(df_scaled)
kmeans_3.labels_

# menggabungkan hasil clustering ke dalam setiap negara dalam dataframe

df_cluster['cluster_id'] = kmeans_3.labels_
display(df_cluster)

# menghitung jumlah negara dalam setiap cluster

df_cluster.cluster_id.value_counts(ascending=True)

"""3.4. Create the clustering Result Graph"""

# Centroid Inverse Scaling
centroids_ori_scale = sc.inverse_transform(kmeans_3.cluster_centers_)

# Plot hasil clustering
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
plt.scatter(df_cluster.Pendapatan[df_cluster.cluster_id == 0], df_cluster['Kematian_anak'][df_cluster.cluster_id == 0], color = 'green', s=100, label= '0')
plt.scatter(df_cluster.Pendapatan[df_cluster.cluster_id == 1], df_cluster['Kematian_anak'][df_cluster.cluster_id == 1], color = 'red', s=100, label = '1')
plt.scatter(df_cluster.Pendapatan[df_cluster.cluster_id == 2], df_cluster['Kematian_anak'][df_cluster.cluster_id == 2], color = 'blue', s=100, label = '2')
ax.scatter(centroids_ori_scale[:, 0], centroids_ori_scale[:,1], c='black', s=200, marker='o', alpha=0.6, label = 'centroid')
plt.legend(title= "Cluster ID", labelspacing=1.5, borderpad=1)
plt.xlabel('Pendapatan')
plt.ylabel('Kematian_anak')
plt.title("Clustering Pendapatan & Kematian Anak")

plt.show()

"""---
---
---

## 4. Recommendation

1. Choose which country cluster to focus.
<br><br>
2. Show which countries included in that cluster.
<br><br>
3. Among those countries, choose the best coutries to receive help
    - Remember, USD 10 Mil. is a small amount for this kind of cause, choose the countries wisely.
    - Elaborate the reason you chose them.

1. Untuk memilih cluster negara yang akan difokuskan maka kita perlu membuat tabel untuk melihat karakter data tiap cluster
"""

# melihat karakter tiap cluster

grouped_df=df_cluster.groupby('cluster_id').agg({'Pendapatan':['max','min','mean'],
                                                 'Kematian_anak':['max','min','mean']})
grouped_df

"""> Country to focus : cluster 2 (berwarna biru) merupakan kelompok negara yang memiliki rata-rata pendapatan terendah dan nilai rata-rata kematian anak tertinggi.

2. Negara yang termasuk dalam cluster 2
"""

# menunjukkan isi negara di cluster 2

df_cluster2 = df_cluster[df_cluster.cluster_id == 2]
display(df_cluster2)

"""3. Choose which country to received the help of USD 10Mill

> Untuk memilih negara yang tepat untuk menerima bantuan, maka diperlukan analisis lebih lanjut mengenai negara di cluster 2. Kita dapat mengurutkan negara di cluster 2 berdasarkan pendapatan terendah dan tingkat kematian anak tertinggi.
"""

# mengurutkan data berdasarkan pendapatan terendah (asc)
df_cluster2_sort_pendapatan = df_cluster2.sort_values('Pendapatan').head(10).reset_index().drop('index', axis=1, inplace=False)
display(df_cluster2_sort_pendapatan)

# Visualisasi data setelah diurutkan
x = df_cluster2_sort_pendapatan.Negara.tolist()
y = df_cluster2_sort_pendapatan.Pendapatan.tolist()
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
sns.barplot(x=df_cluster2_sort_pendapatan.Negara,
            y=df_cluster2_sort_pendapatan.Pendapatan)
ax.set_xticklabels(df_cluster2_sort_pendapatan.Negara,
                   rotation = 90)

plt.title('10 Negara dengan Pendapatan Terendah di CLuster 2')

plt.show()

# mengurutkan data berdasarkan tingkat kematian anak (desc)
df_cluster2_sort_kematian = df_cluster2.sort_values('Kematian_anak', ascending=False).head(10).reset_index().drop('index', axis=1, inplace=False)
display(df_cluster2_sort_kematian)

# Visualisasi data setelah diurutkan
fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
df_cluster2_sort_kematian = df_cluster2.sort_values('Kematian_anak',
                                                    ascending=False).head(9)
sns.barplot(x=df_cluster2_sort_kematian.Negara,
            y=df_cluster2_sort_kematian.Kematian_anak)
ax.set_xticklabels(df_cluster2_sort_kematian.Negara,
                   rotation = 90)
plt.title('10 Negara dengan Tingkat Kematian Anak Tertinggi di CLuster 2')

plt.show()



"""> Setelah pengurutan data, dapat kita peroleh informasi sebagai berikut :

- Negara pendapatan terendah : Congo
- Negara dengan tingkat kematian anak tertinggi : Haiti
- Niger merupakan negara dengan pendapatan k-4 terendah dan memiliki tingkat kematian anak ke-7 tertinggi
- Central African Republik merupakan negara dengan pendapatan k-5 terendah dan memiliki tingkat kematian k-4 tertinggi
- Sierra Leone merupakan negara dengan pendapatan ke-10 terendah dan memiliki tingkat kematian anak k-2 tertinggi
- Negara lainnya merupakan negara yang termasuk di salah satu urutan peringkat pendapatan terendah atau tingkat kematian tertinggi (tidak termasuk di 2 kategori)

> **Kesimpulan akhir untuk rekomendasi** :

> Sesuai dengan tujuan proyek untuk memberikan bantuan finansial kepada negara yang membutuhkan berdasarkan faktor sosial ekonomi dan kesehatan, maka kita memprioritaskan pada faktor pendapatan terendah dan tingkat kematian anak tertinggi. Adapun setelah diurutkan sesuai faktor pendapatan terendah, negara Congo ada di peringkat terendah. Sedangkan dari faktor tingkat kematian tertinggi, maka Haiti menduduki peringkat pertama.  

> Selanjutnya kita juga dapat mengambil negara yang termasuk dalam kategori 10 negara pendapatan terendah dan 10 negara dengan tingkat kematian anak tertinggi. Maka dapat merekomendasikan negara sbb:
- Niger
- Central African Republik
- Sierra Leone

---
---
---
"""
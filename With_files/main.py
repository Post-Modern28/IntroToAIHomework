import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import tarfile
import datetime

from pandas import Series
from six.moves import urllib
from zlib import crc32
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from pandas.plotting import scatter_matrix
from datetime import datetime, date

pd.set_option("display.notebook_repr_html", False)
pd.set_option("display.max_columns", 8)
pd.set_option("display.max_rows", 10)
pd.set_option("display.width", 80)

s = pd.Series([1, 2, 3, 4])
#print(s.index)
dates = pd.date_range('2022-12-01', '2022-12-04')
temperature = pd.Series([0, -2, -6, -4], index=dates)
#print(temperature)
temperature2: Series = pd.Series([10, 8, 11, 12], index=dates)
diff = temperature2 - temperature
#print(diff.mean())
temps_dataframe = pd.DataFrame({'Kazan': temperature, 'Krasnodar': temperature2}, dtype="float64")
#print(temps_dataframe)
#print(temps_dataframe[temps_dataframe > -3])
#print(np.arange(1, 10))

df = pd.DataFrame(np.array([[1, 2.4, 6], [3, 4, 8]]), index=['first', 'second'], columns=['arr1', 'arr2', 'arr3'], ).astype('int64')
#arr = np.array([[1, 2, 3], ['a', 'b', 'c']])
#df = pd.DataFrame(*arr)
#print(df.at['first', 'arr2'])
#print(df)
#ctn = pd.concat([df, df], axis=0)
#print(ctn)
#ctn = pd.concat([df, df, df], axis=1)
#print(ctn)
#del ctn['arr1']
#print(ctn.drop('first'))
#print(ctn)
df_int = pd.DataFrame({"First_Row": np.arange(20, 111, 10), "Second_Row": np.arange(10, 101, 10), "Third_Row": np.arange(15, 106, 10)},\
                      index=pd.IntervalIndex.from_breaks(np.arange(0, 101, 10)))
fi = df_int['First_Row']
#print(df_int.sub(fi, axis=0))
#print(df_int.value_counts())
#print(df_int)
#print(df_int.iloc[1])
#print(df_int.iloc[0].nlargest(2))
#print(df_int.describe().astype('float16')-df_int.describe().astype('float32'))
#print(df_int.describe().astype('float32')-df_int.describe().astype('float16'))
#print(df_int.describe().astype('float64'))
#df_int['First_Row'].plot()
r = df_int.rolling(window=2, axis=1)
#print(r.mean())
dt_rng = pd.date_range('1/1/2022', periods=62, freq="MIN")
ts = pd.Series(np.random.randn(len(dt_rng)), index=dt_rng)
#print(ts)
arr = [5] * 9
grades = np.array([np.array([5 for i in range(9)]), np.array([(4.66+5)/2 for j in range(40)]), np.array([(4.33+4.66)/2 for k in range(30)]),
                   np.array([(4+4.33)/2 for z in range(44)]), np.array([(3.66+4)/2 for x in range(19)]), np.array([(3.33 + 3.66)/2 for c in range(8)]),
                   np.array([(3+3.33)/2 for v in range(2)]), np.array([2.75]), np.array([2.25 for b in range(3)])], dtype='object')

a = []
for i in grades:
    for j in i:
        a.append(j)
gd = np.array(a)
print(gd.mean())
print(gd.std())
a = pd.Series(gd)
print(a.describe())

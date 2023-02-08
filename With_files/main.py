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

























"""
def test_set_check(identifier, test_ratio):
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32


def split_train_test_by_id(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]


HOUSING_PATH = os.path.join("datasets", "housing")


def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


housing = load_housing_data()


def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

#print(housing.info())
housing_with_id = housing.reset_index() # adds an `index` column
housing_with_id["id"] = housing["longitude"] * 1000 + housing["latitude"]
train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "id")
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
housing["income_cat"] = pd.cut(housing["median_income"],
    bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
    labels=[1, 2, 3, 4, 5])
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]


for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

housing = strat_train_set.copy()

housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"]/housing["total_rooms"]
housing["population_per_household"]=housing["population"]/housing["households"]
corr_matrix = housing.corr()
attributes = ["median_house_value", "median_income", "total_rooms",
 "housing_median_age"]
corr_matrix["median_house_value"].sort_values(ascending=False)
scatter_matrix(housing[attributes], figsize=(12, 8))
housing.plot(kind="scatter", x="median_income", y="median_house_value",
 alpha=0.1)
plt.show()
#print(corr_matrix["median_house_value"].sort_values(ascending=False))
"""
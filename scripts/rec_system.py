import numpy as np
import pandas as pd
import os
import scipy.sparse as sp
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error

# Load the pre-split datasets
filename = 'Home_and_Kitchen.csv'
file_directory = os.path.join(os.getcwd(), 'data')

data = pd.read_csv(os.path.join(file_directory, filename))
data = data.iloc[:2500000, 0:]

print(data.head())
print(data.shape)
print(data.dtypes)
print(data.describe()['rating'].T)




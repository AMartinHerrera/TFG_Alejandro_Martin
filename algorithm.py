import numpy as np
import pandas as pd

from statistics import mean, stdev
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import zero_one_loss
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.pipeline import make_pipeline

input_file = "data/players_data_November_03_OK.csv"

# comma delimited is the default
all_data = pd.read_csv(input_file, header = 0)

# remove the non-numeric columns
all_data = all_data._get_numeric_data()

# put the numeric column names in a python list
# numeric_headers = list(all_data.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
numpy_array = all_data.as_matrix()

print(numpy_array[0])

coodenate_x = pd.DataFrame(all_data, dtype=np.int64)
coodenate_x = coodenate_x.astype('object')
c = pd.get_dummies(coodenate_x)

coodenate_y = all_data.iloc[:, -1]

error = []

for _ in range(100):
    dataTrainX, dataTestX, dataTrainY, dataTestY = train_test_split(coodenate_x, coodenate_y, test_size=0.20)
    data = KNeighborsClassifier(n_neighbors=50, metric="euclidean").fit(dataTrainX, dataTrainY)
    error.append(zero_one_loss(dataTestY, data.predict(dataTestX)))

print("-----------------KNeighborsClassifier--------------------")

print(f"ERROR--> {mean(error):.4f}")
print(f"DESV ESTANDAR--> {stdev(error):.4f}")

print("-----------------SGDClassifier--------------------")

for _ in range(100):
    dataTrainX, dataTestX, dataTrainY, dataTestY = train_test_split(coodenate_x, coodenate_y, test_size=0.25)
    clasificador = make_pipeline(StandardScaler(), SGDClassifier(max_iter=10, alpha=100)).fit(dataTrainX, dataTrainY)
    error.append(zero_one_loss(dataTestY, clasificador.predict(dataTestX)))

print(f"ERROR--> {mean(error):.4f}")
print(f"DESV ESTANDAR--> {stdev(error):.4f}")

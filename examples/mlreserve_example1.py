import mlreserve as mr 
import pandas as pd
from sklearn.linear_model import TweedieRegressor
from mlreserve import Triangle

#auto = mr.load_sample('auto')
df = pd.read_csv('./mlreserve/utils/data/auto.csv')
columns = ["incurred", "paid"]
index = ["lob"]
origin = "origin"
development = "development"
cumulative = True
auto = Triangle(
        df,
        origin=origin,
        development=development,
        index=index,
        columns=columns,
        cumulative=cumulative,
    )

dev = mr.MLReserve(regr=TweedieRegressor,
    design_matrix='C(development) + C(origin)').fit(auto)

print("dev", dev)

# Grab LDFs vs traditional approach
mlr = dev.ldf_.iloc[..., 0, :].T.iloc[:, 0].rename('MLR')

print("mlr", mlr)
#traditional = mr.Development().fit(auto).ldf_.T.iloc[:, 0].rename('Traditional')

# # Plot data
#results = pd.concat((mlr, traditional), axis=1)

#print(result#)
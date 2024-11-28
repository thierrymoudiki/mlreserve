import mlreserve as mr 
import pandas as pd
from sklearn.linear_model import TweedieRegressor

genins = mr.load_sample('genins')

dev = mr.MLReserve(regr=TweedieRegressor,
    design_matrix='C(development) + C(origin)').fit(genins)

print(dev)

# # Grab LDFs vs traditional approach
# mlr = dev.ldf_.iloc[..., 0, :].T.iloc[:, 0].rename('MLR')
# traditional = mr.Development().fit(genins).ldf_.T.iloc[:, 0].rename('Traditional')

# # Plot data
# results = pd.concat((mlr, traditional), axis=1)

# print(results)
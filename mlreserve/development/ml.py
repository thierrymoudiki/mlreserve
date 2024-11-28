# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pandas as pd
import numpy as np
from mlreserve.development.base import DevelopmentBase
from mlreserve.development.learning import DevelopmentML
from sklearn.pipeline import Pipeline
from mlreserve.utils.utility_functions import PatsyFormula


class MLReserve(DevelopmentBase):
    """ This estimator creates development patterns with a machine learning. 

    The Tweedie family includes several of the more popular distributions including
    the normal, ODP poisson, and gamma distributions.  This class is a special case
    of `DevleopmentML`.  It restricts to just GLM using a TweedieRegressor and
    provides an R-like formulation of the design matrix.

    .. versionadded:: 0.8.1

    Parameters
    ----------
    regr: object
        An object with fit and predict methods.         
    design_matrix: formula-like
        A patsy formula describing the independent variables, X of the GLM
    response:  str
        Column name for the reponse variable of the GLM.  If ommitted, then the
        first column of the Triangle will be used.
    weight: str
        Column name of any weight to use in the GLM. If none specified, then an
        unweighted regression will be performed.
    verbose: int, default=0
        For the lbfgs solver set verbose to any positive number for verbosity.

    Attributes
    ----------
    model_: sklearn.Pipeline
        A scikit-learn Pipeline of the GLM
    """

    def __init__(self, regr, design_matrix='C(development) + C(origin)',
                 response=None, weight=None, verbose=0, **kwargs):
        self.regr=regr
        self.response=response
        self.weight=weight
        self.design_matrix = design_matrix        
        self.verbose=verbose
        self.args = kwargs             

    def fit(self, X, y=None, sample_weight=None):
        response = X.columns[0] if not self.response else self.response
        self.model_ = DevelopmentML(Pipeline(steps=[
            ('design_matrix', PatsyFormula(self.design_matrix)),
            ('model', self.regr(**self.args))]), 
            y_ml=response, weight_ml=self.weight).fit(X)
        return self

    @property
    def ldf_(self):
        return self.model_.ldf_

    @property
    def triangle_ml_(self):
        return self.model_.triangle_ml_

    def transform(self, X):
        return self.model_.transform(X)

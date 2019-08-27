# D. Across group analysis (nonhedgers/semi-hedgers/hedgers) Codes

from sklearn.linear_model import Lasso, LinearRegression
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

import matplotlib.pyplot as plt
from yellowbrick.features.importances import FeatureImportances

import warnings
warnings.filterwarnings("ignore")

#----------------------------------------------------------------------------------------------------------------------------
# Non-hedge-monthly-integrated -----------------------------------------------------------------------

hedger_list = list(dict_hedgers.keys())

non_hedge_monthly = monthly_dataset_model_1[~monthly_dataset_model_1.ticker.isin(hedger_list)]
non_hedge_monthly_integrated = non_hedge_monthly[non_hedge_monthly.ticker.isin(integrated)]
non_hedge_monthly_independent = non_hedge_monthly[non_hedge_monthly.ticker.isin(independent)]

print('non_hedge_monthly_independent: ', non_hedge_monthly_independent['ticker'].unique())
print('non_hedge_monthly_integrated: ', non_hedge_monthly_integrated['ticker'].unique())

NT_X = non_hedge_monthly_integrated.loc[:, ~non_hedge_monthly_integrated.columns.isin(['logsize_y' , 'ticker']) ]
NT_y = non_hedge_monthly_integrated['logsize_y']

# Linear Regression ( Non-hedge-monthly-integrated ) ----------------------------------------------------------------------

model = LinearRegression()
regfit = model.fit(NT_X, NT_y)

print('Rsq: ', regfit.score(NT_X, NT_y))
print('intercept: ', regfit.intercept_)
list(zip(NT_X.columns, regfit.coef_))

# Lasso ( Non-hedge-monthly-integrated ) ----------------------------------------------------------------------

lasso = Lasso(normalize=False)
tss = TimeSeriesSplit(5)

alpha_space = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])
param_grid = {'alpha': alpha_space}

model = GridSearchCV(lasso, param_grid=param_grid, cv=tss).fit(NT_X,NT_y)
lasso_ = Lasso(normalize = False, alpha = model.best_params['alpha']).fit(NT_X, NT_y)

print('Rsq: ', lasso_.score(NT_X, NT_y))
print('intercept: ', lasso_.intercept_)
list(zip(NT_X.columns, lasso_.coef_))

#----------------------------------------------------------------------------------------------------------------------------

# Non-hedge-monthly-independent----------------------------------------------------------------------------------------------

ND_X = non_hedge_monthly_independent.loc[:, ~non_hedge_monthly_independent.columns.isin(['logsize_y' , 'ticker']) ]
ND_y = non_hedge_monthly_independent['logsize_y']

# Linear Regression ( Non-hedge-monthly-integrated ) ----------------------------------------------------------------------

model = LinearRegression()
regfit = model.fit(ND_X, ND_y)

print('Rsq: ', regfit.score(ND_X, ND_y))
print('intercept: ', regfit.intercept_)
list(zip(ND_X.columns, regfit.coef_))

# Lasso ( Non-hedge-monthly-integrated ) ----------------------------------------------------------------------

lasso = Lasso(normalize=False)
tss = TimeSeriesSplit(5)

alpha_space = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])
param_grid = {'alpha': alpha_space}

model = GridSearchCV(lasso, param_grid=param_grid, cv=tss).fit(ND_X,ND_y)
lasso_ = Lasso(normalize = False, alpha = model.best_params['alpha']).fit(ND_X, ND_y)

print('Rsq: ', lasso_.score(ND_X, ND_y))
print('intercept: ', lasso_.intercept_)
list(zip(ND_X.columns, lasso_.coef_))

#----------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
# Semi-hedge-monthly-independent -----------------------------------------------------------------------

semi_hedge_monthly = monthly_dataset_model_1[monthly_dataset_model_1.ticker.isin(semihedger)]
semi_hedge_monthly_integrated = semi_hedge_monthly[semi_hedge_monthly.ticker.isin(integrated)]
semi_hedge_monthly_independent = semi_hedge_monthly[semi_hedge_monthly.ticker.isin(independent)]

print('semi_hedge_monthly_independent: ', semi_hedge_monthly_independent['ticker'].unique())
print('semi_hedge_monthly_integrated: ', semi_hedge_monthly_integrated['ticker'].unique())

SD_X = semi_hedge_monthly_independent.loc[:, ~semi_hedge_monthly_independent.columns.isin(['logsize_y' , 'ticker']) ]
SD_y = semi_hedge_monthly_independent['logsize_y']

# Linear Regression ( Semi-hedge-monthly-independent ) ----------------------------------------------------------------------

model = LinearRegression()
regfit = model.fit(SD_X, SD_y)

print('Rsq: ', regfit.score(SD_X, SD_y))
print('intercept: ', regfit.intercept_)
list(zip(SD_X.columns, regfit.coef_))

# Lasso ( Semi-hedge-monthly-independent ) ----------------------------------------------------------------------

lasso = Lasso(normalize=False)
tss = TimeSeriesSplit(5)

alpha_space = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])
param_grid = {'alpha': alpha_space}

model = GridSearchCV(lasso, param_grid=param_grid, cv=tss).fit(SD_X,SD_y)
lasso_ = Lasso(normalize = False, alpha = model.best_params['alpha']).fit(SD_X, SD_y)

print('Rsq: ', lasso_.score(SD_X, SD_y))
print('intercept: ', lasso_.intercept_)
list(zip(SD_X.columns, lasso_.coef_))
#----------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
# Hedger-monthly-independent -----------------------------------------------------------------------

hedge_monthly = monthly_dataset_model_1[monthly_dataset_model_1.ticker.isin(hedger)]
hedge_monthly_integrated = hedge_monthly[hedge_monthly.ticker.isin(integrated)]
hedge_monthly_independent = hedge_monthly[hedge_monthly.ticker.isin(independent)]

print('hedge_monthly_independent: ', hedge_monthly_independent['ticker'].unique())
print('hedge_monthly_integrated: ', hedge_monthly_integrated['ticker'].unique())

HD_X = hedge_monthly_independent.loc[:, ~hedge_monthly_independent.columns.isin(['logsize_y' , 'ticker']) ]
HD_y = hedge_monthly_independent['logsize_y']

# Linear Regression ( Semi-hedge-monthly-independent ) ----------------------------------------------------------------------

model = LinearRegression()
regfit = model.fit(HD_X, HD_y)

print('Rsq: ', regfit.score(HD_X, HD_y))
print('intercept: ', regfit.intercept_)
list(zip(HD_X.columns, regfit.coef_))

# Lasso ( Semi-hedge-monthly-independent ) ----------------------------------------------------------------------

lasso = Lasso(normalize=False)
tss = TimeSeriesSplit(5)

alpha_space = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])
param_grid = {'alpha': alpha_space}

model = GridSearchCV(lasso, param_grid=param_grid, cv=tss).fit(HD_X,HD_y)
lasso_ = Lasso(normalize = False, alpha = model.best_params['alpha']).fit(HD_X, HD_y)

print('Rsq: ', lasso_.score(HD_X, HD_y))
print('intercept: ', lasso_.intercept_)
list(zip(HD_X.columns, lasso_.coef_))
#----------------------------------------------------------------------------------------------------------------------------

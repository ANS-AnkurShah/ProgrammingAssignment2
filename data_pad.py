# -*- coding: utf-8 -*-
"""data-PAD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12j-getQCMUB_fBaP9d4BCrADXcNIXeP0
"""

# !pip install shap
pip install sklearn
# !pip install --upgrade openpyxl=='3.0.0'

# !pip install pyxll

# !pip install --upgrade plotly

import numpy as np
np.busday_count('2021-02-15', '2021-02-21')

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
import operator
from dateutil.relativedelta import relativedelta
import calendar

import random

random.seed(10)

df3=pd.read_excel('ml_test4.xlsx')

df3.columns

df3=df3[['PAD registration number','Request date','Final disclosure / closure date ','Profile of requester', 'Subject',
       'CASES', 'Typology of documents ','Glyphosate ', 'Unit ','number of pages ', 'number of documents ','Assignment to a legal officer ','Number of pages in emails ','Total of outputs ','Number of consultations by email ','Number of emails ']]

df3.head()



# df[df['Request date'].isnull() & df['PAD registration number'].notnull()]

# df[df['Final disclosure / closure date '].isnull()& df['PAD registration number'].notnull()]['PAD registration number']

# non_av=set(df[df['Final disclosure / closure date '].isnull()]['PAD registration number'])

# av=set(list(df[df['Final disclosure / closure date '].notnull()]['PAD registration number']))

# a=set(non_av.intersection(av))

# no_clos_date=list(non_av.symmetric_difference(a))

# df[df['PAD registration number'].i(no_clos_date) & df['PAD registration number'].notnull() ].to_excel('missing_final_date.xlsx')

# df=df[df['Duration'].notnull()]



# df3['Final disclosure / closure date ']=pd.to_datetime(df3['Final disclosure / closure date '],errors='coerce',dayfirst=True)
# df3['Request date']=pd.to_datetime(df3['Request date'],errors='coerce',dayfirst=True)

# np.busday_count(str(df3['Request date'][0].date()), str(df3['Final disclosure / closure date '][0].date()))

# duration=[]
# for i in range(0,len(df3['Final disclosure / closure date '])):
#   try:
#     duration.append(np.busday_count(str(df3['Request date'][i].date()), str(df3['Final disclosure / closure date '][i].date())))
#   except:
#     duration.append(-1)

# df3['Duration']=duration

df3['Duration']=pd.to_datetime(df3['Final disclosure / closure date '],errors='coerce',dayfirst=True)-pd.to_datetime(df3['Request date'],errors='coerce',dayfirst=True)

df3['Year']=pd.to_datetime(df3['Request date'],errors='coerce',dayfirst=True).apply(lambda x:x.year)

df3['Month']=pd.to_datetime(df3['Request date'],errors='coerce',dayfirst=True).apply(lambda x:x.month)

df3['Day']=pd.to_datetime(df3['Request date'],errors='coerce',dayfirst=True).apply(lambda x:x.day)

df3['Duration']=[i.days for i in df3['Duration'] ]

df3['Subject']=df3['Subject'].fillna('')

df3['isCA']=df3['PAD registration number'].isin(list(df3[df3['PAD registration number'].str.contains(r'CA|Confirm')]['PAD registration number'])).astype(int)
df3['isAarhus']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'Aarhus')]['PAD registration number'])).astype(int)
df3['Old_Document_Requested']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'199[0-9]|200[0-9]|201[0-4]')]['PAD registration number'])).astype(int)
df3['Article4(2)']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'4(2)')]['PAD registration number'])).astype(int)
df3['Data_Protection']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'4(1)|45/2001|GDPR|2018/1725')]['PAD registration number'])).astype(int)
df3['Notification_to_MS']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'MS|member state|notification|food consumption data|chemical occurrence data|pesticides data|residues data|food composition')]['PAD registration number'])).astype(int)
df3['Confidential_Information']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'application dossiers|full application')]['PAD registration number'])).astype(int)
df3['Third_Parties']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'third part')]['PAD registration number'])).astype(int)

sum(df3['Data_Protection'])

df3['Glyphosate ']=df3['PAD registration number'].isin(list(df3[df3['Subject'].str.contains(r'Glyphosate|glyphosate')]['PAD registration number'])).astype(int)

df3['resources']=np.select([df3['Year']==2015,df3['Year']==2016,df3['Year']==2017,df3['Year']==2018,df3['Year']==2019,df3['Year']==2020,df3['Year']==2021],[7,11,8,13,15,9,11],default=0)

"""# **Current live** **Documents** """

from tqdm import tqdm

df3['Final disclosure / closure date ']=pd.to_datetime(df3['Final disclosure / closure date '],errors='coerce',dayfirst=True)
df3['Request date']=pd.to_datetime(df3['Request date'],errors='coerce',dayfirst=True)

all_current_workload=[]
for i in tqdm(range(0,len(df3['PAD registration number']))):
  current_workload=df3[(df3['Request date'] < df3['Request date'][i]) & (df3['Final disclosure / closure date ']>df3['Request date'][i])].shape[0]
  all_current_workload.append(current_workload)

df3['Current_Workload']=all_current_workload

"""# Vacations"""

for i in tqdm(range(0,len(df3['PAD registration number']))):
  if (df3['Month'][i]==12 and df3['Day'][i]>20) or (df3['Month'][i]==1 and df3['Day'][i]<10):
      df3['Duration'][i]=df3['Duration'][i]-7

# df3[df3['Duration']<0].to_excel('negative_duration_check_pad.xlsx')

# df3[(df3['Duration']<0) | (df3['Duration'].isnull() )][['PAD registration number','Request date','Final disclosure / closure date ']].to_excel('wrong_dates_PAD.xlsx')

df3=df3.drop(['Request date',	'Final disclosure / closure date ','Subject','Day'],axis=1)

df3['Assignment to a legal officer '] = df3['Assignment to a legal officer '].fillna('')
# df3['Assignment to a legal officer ']= np.where(df3['Assignment to a legal officer '] ==0,0,1)

duration=list(df3['Duration'])
df3=df3.drop('Duration',axis=1)
df3['Duration']=duration



df=df3.copy()

df.to_excel('PAD_enriched.xlsx')

df['Glyphosate '] = df['Glyphosate '].fillna(0)

df['Glyphosate ']= np.where(df['Glyphosate '] ==0,0,1)



df.corr()

df

sns.set(rc={'figure.figsize':(50,10)})
sns.set(font_scale = 1.5)
plt.ylim(0, 400)
ax = sns.boxplot(x="Profile of requester", y="Duration", data=df)

df

sns.set(rc={'figure.figsize':(35,10)})
sns.set(font_scale = 1.2)
import matplotlib.pyplot as plt
plt.ylim(0, 500)
ax = sns.boxplot(x="Unit ", y="Duration", data=df)

sns.set(rc={'figure.figsize':(35,10)})
sns.set(font_scale = 1.2)
import matplotlib.pyplot as plt
plt.ylim(0, 500)
ax = sns.boxplot(x="Assignment to a legal officer ", y="Duration", data=df)

dt=df.groupby(['Unit ','Typology of documents '])['Glyphosate '].count().reset_index()
dt=dt[dt['Glyphosate ']>2]
fig = px.sunburst(dt, path=['Unit ','Typology of documents '], values='Glyphosate ')
fig.show()

df[['Profile of requester',	'Typology of documents '	,	'Unit '	,'CASES']]

le = preprocessing.LabelEncoder()

df['Profile of requester']=df['Profile of requester'].apply(str)
df['Typology of documents ']=df['Typology of documents '].apply(str)
df['Unit ']=df['Unit '].apply(str)

le.fit(df['Profile of requester'])
df['Profile of requester']=le.transform(df['Profile of requester'])
le.fit(df['Typology of documents '])
df['Typology of documents ']=le.transform(df['Typology of documents '])
le.fit(df['Unit '])
df['Unit ']=le.transform(df['Unit '])
le.fit(df['Assignment to a legal officer '])
df['Assignment to a legal officer ']=le.transform(df['Assignment to a legal officer '])



list(df.columns)

df[list(df.columns)[5]]

df['number of pages ']=df['number of pages '].apply(float)

df['number of documents ']=df['number of documents '].apply(float)

df[list(df.columns)[6]]

# from scipy import stats
# import numpy as np
# z = np.abs(stats.zscore(df[list(df.columns)[5:7]],nan_policy='omit'))

df.shape

# df_o =df[(z < 3).all(axis=1)]

df.head()

# df_o=df.fillna(-1)
# df_o=df[['Profile of requester',	'CASES',	'Typology of documents ',	'Glyphosate ',	'Unit ',	'number of pages ',	'number of documents ',	'Assignment to a legal officer ','Duration']].dropna()
# df[list(df.columns)[5]]=df[list(df.columns)[5]].fillna(-1)

df.shape

df[df['number of pages ']>5000]['number of pages '].reset_index()

df_o=df.sample(frac=1)

for col in list(df_o.columns):
  try:
    df_o[col]=df_o[col].fillna(df_o[col].mean())
  except Exception as e:
    pass
df_o=df_o[df_o['Duration']>5]

#df_o=df_o[df_o['Year']>2015]

# df_o=df_o[df_o['number of pages ']<10000]
# df_o=df_o[df_o['number of pages ']>0]
df_o=df_o[df_o['Duration']<100]
# df_o=df_o[df_o['number of documents ']<5000]



# df_o=df_o[df_o['number of documents ']>0]
#df_o=df[df_o[list(df_o.columns)[5]]>0]

df_o.shape

# from sklearn import preprocessing

# x = df_o.loc[:, df_o.columns != 'Duration'].values #returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# df_o1 = pd.DataFrame(x_scaled)
# df_o1['12']=df['Duration'] 
# df_o=df_o1.rename(columns=dict(zip(df_o1.columns,df.columns)))





df_o.shape

# df[df['Duration']<0].to_excel('PADS')



df_o=df_o[df_o['Duration'].notnull()]

sum(df_o['Duration'].isnull())



df_o

df['Glyphosate '].unique()

df_o=df_o.dropna()

df_app_numbers=list(df_o['PAD registration number'])
df_o=df_o.drop(['PAD registration number'],axis=1)

X=df_o.loc[:, df_o.columns != 'Duration']
#X=X.loc[:, X.columns != 'CASES']

y=df_o['Duration']

train_size=int(X.shape[0]*0.7)
test_size=int(X.shape[0]*0.3)

X_train=X.head(train_size)
y_train=y.head(train_size)

y_train

X_test=X.tail(test_size)
y_test=y.tail(test_size)

# rf=RandomForestRegressor(max_depth=20)
##min_samples_leaf=3, min_samples_split=3, max_depth=10,criterion='poisson'criterion='absolute_error',

max(df_o['Duration'])

all_scores=[]
for i in range(1,20):
  rf=RandomForestRegressor(max_depth=i,warm_start=True)
  rf.fit(X_test,y_test)
  all_scores.append(rf.score(X_train,y_train))

all_scores_depth=dict(zip(list(range(1,20)),all_scores))
best_depth=max(all_scores_depth.items(), key=operator.itemgetter(1))[0]
all_scores_depth[best_depth]

rf=RandomForestRegressor()
#max_depth=best_depth)
rf.fit(X_train,y_train)

# rf=RandomForestRegressor()
# rf.fit(X_train,y_train)

rf.score(X_train,y_train)

rf.score(X_test,y_test)

scores = cross_val_score(
rf, X, y, cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0))

scores

np.median(scores)

from sklearn.linear_model import LinearRegression

#  reg = make_pipeline(StandardScaler(with_mean=True), LinearRegression())
reg=LinearRegression()

reg.fit(X_train, y_train,)

reg.score(X_train,y_train)

reg.score(X_test,y_test)

from sklearn.linear_model import Ridge
lmr = Ridge()
lmr.fit(X_train, y_train)

lmr.score(X_test,y_test)

from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
n_samples, n_features = 10, 5
rng = np.random.RandomState(0)

regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2,kernel='linear'))
regr.fit(X_train, y_train)

#!pip install catboost

X_train.columns

# from catboost import CatBoostRegressor

# model = CatBoostRegressor(iterations=50,
#                           learning_rate=1)
# # Fit model
# model.fit(X_train, y_train)
# # Get predictions
# model.score(X_test,y_test)

# model.score(X_train,y_train)

regr.score(X_train,y_train)

regr.score(X_test,y_test)

from sklearn import linear_model
clf = linear_model.Lasso(alpha=0.5)

clf.fit(X_train, y_train)

clf.score(X_test,y_test)

clf.score(X_train, y_train)

df_o.corr()['Duration'].reset_index()

X_train

X_train.head()

import xgboost as xgb
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error

def report_best_scores(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

xgb_model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42,tree_method='exact',verbose=4)

xgb_model.fit(X_train, y_train,verbose=4)

y_pred = xgb_model.predict(X_test)

mse=mean_squared_error(y_test, y_pred)

print(np.sqrt(mse)/np.mean(y_test))

# help(xgb_model.score(X_test,y_test))

xgb_model.score(X_test,y_test)

clf.coef_

lmr.coef_

df_pred=X_test.copy().reset_index()

df_pred['actual']=list(y_test)

df_pred['RF_pred']=[round(x) for x in rf.predict(X_test)]

df_pred['XGB_pred']=[round(x) for x in xgb_model.predict(X_test)]

df_pred['CLF_pred']=[round(x) for x in clf.predict(X_test)]

df_pred['LMR_pred']=[ round(x) for x in lmr.predict(X_test)]

# df_pred=df_pred.drop('PAD registration number',axis=1)

df_pred.insert(0,'PAD registration number',list(df_app_numbers[-len(y_test):]))

df_pred.to_excel('result_pad.xlsx')

pd.set_option("display.max_rows", None, "display.max_columns", None)

# df_pred.to_excel('PAD_pred0203.xlsx')

# df_pred['diff']=np.where(abs(df_pred['pred']-df_pred['actual'])<5,1,0)

df_pred

# sum(df_pred['diff'])/len(df_pred['diff'])

np.mean(y_test)

sum(np.abs(clf.predict(X_test)-y_test)/X_test.shape[0])

#!pip install shap

import shap

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_train)

shap.summary_plot(shap_values, features=X_train, feature_names=X_train.columns)

shap.summary_plot(shap_values, X_train, plot_type="bar")

shap.summary_plot(shap_values, X_train, plot_type="bar")

import datetime



df.head()

# df=df.fillna(-1)

def convert_date(year, month):
    try:
        return datetime.datetime(int(year), int(month),1)
    except:
      pass
    return datetime.datetime.strptime('01/01/1900', '%d/%m/%Y')

# df['CreatedDate']= df.apply(lambda x: convert_date(x['Year'], x['Month']), axis=1)

# df['CreatedDate']

# start_date = datetime.datetime(2017, 6, 1)
# end_date = datetime.datetime(2021, 12, 1)

# # window size in month
# train_window_size = 3
# test_window_size = 1

# data = df
# target = 'Duration'

# def window_training_performance(train_window_size=8, test_window_size=1):
#     # on how many months I will be doing some tests? 
#     # It means there will be 12 training/testing phase

#     cur_start_date_train = start_date
#     cur_end_date_train = start_date + relativedelta(months=train_window_size)
#     cur_end_date_test = cur_end_date_train + relativedelta(months=test_window_size)

#     month_acc = dict()
#     month_r2=dict()
#     month_test_size = dict()
#     month_train_size = dict()
#     month_positive_prop = dict()
#     while cur_end_date_test <= end_date:

#         cur_year = cur_end_date_train.year
#         cur_month = calendar.month_name[cur_end_date_train.month]
#         month_date = str(cur_month)[0:3] + '.' + '\n' + str(cur_year)[2:]

#         data_train = data[(data['CreatedDate'] >= cur_start_date_train) & (data['CreatedDate'] < cur_end_date_train)]
#         data_test = data[(data['CreatedDate'] >= cur_end_date_train) & (data['CreatedDate'] < cur_end_date_test)]

#         X_train = data_train.drop(columns=[target, 'CreatedDate'])
#         X_test = data_test.drop(columns=[target, 'CreatedDate'])
#         y_train = data_train[target]
#         y_test = data_test[target]
#         if y_test.shape[0] !=0:

#           xgb_model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42,max_depth=20,tree_method='exact',verbose=4)

#           xgb_model.fit(X_train, y_train,verbose=4)

#           y_pred = xgb_model.predict(X_test)

#           mse=mean_squared_error(y_test, y_pred)
#           r2=xgb_model.score(X_test,y_test)

#           month_acc[month_date] = mse
#           month_r2[month_date] = r2
#           month_test_size[month_date] = y_test.shape[0]
#           month_train_size[month_date] = y_train.shape[0]
#           month_positive_prop[month_date] = np.sum(y_test)/y_test.shape[0]
          


#         # decision_tree = decision_tree_classification(verbose=False)
#         # decision_tree.train_on_best_hyperparameters_cv(X_train, X_test, y_train, y_test,  
#         #                                                min_max_depth=5,
#         #                                                max_max_depth=20,
#         #                                                class_weight='balanced',
#         #                                                cross_val_params={'cv':3})
        

#         cur_start_date_train += relativedelta(months=test_window_size)
#         cur_end_date_train += relativedelta(months=test_window_size)
#         cur_end_date_test += relativedelta(months=test_window_size)


#     res = [[x, month_acc[x], month_r2[x], month_test_size[x], month_train_size[x]] for x in month_acc]
#     res = pd.DataFrame(res, columns=['month', 'mse','r2', 'test_size', 'train_size']) 

#     # # barplot creation
#     # fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(18,9), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
#     # ax1.set_title('Prediction Balanced Accuracy Through Time (model trained on {} months prior testing)'.format(train_window_size), fontsize=16)
#     # sns.barplot(x='month', y='train_size', data=res, color= '#86BC25', label="Training set size", ax=ax1)
#     # ax1 = sns.barplot(x='month', y='test_size', data=res, color= '#43B02A', label="Testing set size", ax=ax1)
#     # ax1.set_xlabel('Testing Month', fontsize=12)
#     # ax1.set_ylabel('Nbr. Observations', fontsize=12)
#     # ax1.axhline(1.25)
#     # ax1.legend()
#     # ax2 = ax1.twinx()
#     # color = '#046A38'
#     # ax2.set_ylabel('Acc.', fontsize=12)
#     # ax2 = sns.lineplot(x='month', y='acc', data=res, sort=False, color=color, marker="o")
#     # ax2.axhline(0.7, color='red')
#     # ax2.set_ylim([0.5, 1])

#     # ax3 = sns.barplot(x='month', y='postive_prop', data=pos_df, color= '#86BC25', label="Training set size", ax=ax3)
#     # ax3.set_xlabel('Testing Month', fontsize=12)
#     # ax3.set_ylabel('Proportion of positive', fontsize=12)
#     # #ax3.set_yscale('log')

#     return res

# window_training_performance(train_window_size=24)

to_excel()

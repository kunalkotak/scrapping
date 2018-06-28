import pandas as pd
import numpy as np
import os
os.getcwd()
os.chdir(r'C:\python wd\regression')


##import edited train data
train_data=pd.read_csv('Train_Data_Kunal_csv.csv')
train_data.isnull().sum()
##copy data
copy_data=train_data

##Droping NA
copy_data=copy_data.dropna()


##converting Location to numeric type
#######copy_data['Q5a']=number.fit_transform(copy_data['Q5a'].astype('str'))
location_dummies = pd.get_dummies(copy_data.Q5a, prefix='Location').iloc[:, 1:]
copy_data = pd.concat([copy_data, location_dummies], axis=1)



#converting Q4c(working hours) to numeric type
copy_data['Hrs'] = copy_data.Q4c.map({'< 6 hours':0, '6-12 hours':1,'12-23 hours':2,'24 hours':3})

copy_data.isnull().sum()

##test data for Provision type Stores
Provision_data=copy_data[copy_data['Final Shoptype']=='Provision']



###test data for Semi-retailer type Stores
SemiRetailer_data=copy_data[copy_data['Final Shoptype']=='Semi Retailer FMCG']




#####################     Provision Store Type
###########

X_provision=Provision_data.drop(['Hrs','Count_Total','ResponseID','Q4c','Q5a','Storecode','Final Shoptype','NSPC'], axis=1)
y_provision=Provision_data['NSPC']


####################test train Split
from sklearn.model_selection import train_test_split

X_train_provision, X_test_provision, y_train_provision, y_test_provision = train_test_split(X_provision,y_provision,test_size=0.2)


####model application sklearn
from sklearn.linear_model import LinearRegression
lm=LinearRegression()
lm.fit(X_train_provision,y_train_provision)
#print(result.summary())
predicted_sklearn=lm.predict(X_train_provision)

#####Cross_Validation

from sklearn.model_selection import cross_val_score
cv_results=cross_val_score(lm,X_train_provision,y_train_provision,cv=10)
print(cv_results)
print(np.mean(cv_results))

##############################Stats Model 
import statsmodels.formula.api as sm
result = sm.OLS(y_train_provision,X_train_provision).fit()
print(result.params)
prediction_OLS=result.predict()
print(result.rsquared)
print(result.summary())


#####################
###########################3           Semi-Retailer
#############
##########
X_semiRetail=SemiRetailer_data.drop(['Count_Total','ResponseID','Q4c','Q5a','Storecode','Final Shoptype','NSPC'], axis=1)
y_semiRetail=SemiRetailer_data['NSPC']


X_train_semiRetail, X_test_semiRetail, y_train_semiRetail, y_test_semiRetail = train_test_split(X_semiRetail,y_semiRetail,test_size=0.2)

result_semiRetail = sm.OLS(y_train_semiRetail,X_train_semiRetail).fit()
print(result_semiRetail.params)
prediction_OLS_semiRetail=result_semiRetail.predict()
print(result_semiRetail.rsquared)

print(result_semiRetail.summary())

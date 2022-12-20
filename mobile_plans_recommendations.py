#!/usr/bin/env python
# coding: utf-8

# # Mobile Plans Recommendations

# The data shows the behavior of customers who have already switched to a specific mobile plan. The task is to build a model that will choose the appropiate plan. The preprocessng data phase is already done. The objective is to buid a model with the maximum accuracy value. The desire value is at least 0.75. 

# # Data Overview

# First, we import the libraries that we are going to use.

# In[1]:


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.dummy import DummyClassifier


# In[2]:


df=pd.read_csv(r'C:\Users\pinos\Desktop\statistics\users_behavior.csv')


# Overview of the data types we have.

# In[3]:


df.info()


# We see that the calls and messages variables should be of type int, not float, so we're going to change them to the correct type. The is_ultra column, despite being essentially a category, is encoded with zeros and ones, so we're leaving it that way.

# In[4]:


df['calls'] = df['calls'].astype('int')


# In[5]:


df['messages'] = df['messages'].astype('int')


# # Data Samples

# We divide the data into 3 samples: training, validation and test.

# In[6]:


df_train, df_valid_test = train_test_split(
    
    df, test_size=0.25, 
    
    random_state=12345)

df_valid, df_test = train_test_split(
    
    df_valid_test, 
    
    test_size=0.5, 
    
    random_state=12345)


# In[7]:


features_train = df_train.drop(['is_ultra','calls'], axis=1)

target_train = df_train['is_ultra']

features_valid = df_valid.drop(['is_ultra','calls'], axis=1)

target_valid = df_valid['is_ultra']

features_test = df_test.drop(['is_ultra','calls'], axis=1)

target_test = df_test['is_ultra']


# # Exploring Models

# Two models to consider here: decision tree and random forest.

# In[9]:


# loop to explore the reccommended depth 

# and his respective accuracy score for decision tree model

for depth in range(1, 15):
    
    model_tree = DecisionTreeClassifier(
        
        random_state=12345, 
        
        splitter='best', 
        
        max_depth = depth) 
    
    model_tree.fit(features_train, target_train)
    
    predictions_valid = model_tree.predict(features_valid)  
    
    print('max_depth =', depth, ': ', end ='')
    
    print(accuracy_score(target_valid, predictions_valid))


# Based on the results, the best depth will be 4th, in any case it would be advisable in our model not to use a depth of more than 10.

# In[12]:


best_model = None

best_result = 0

best_est = 0

best_depth = 0

for est in range(10, 51, 10):
    
    for depth in range(1, 11):
        
        model_forest = RandomForestClassifier(
            
            random_state=12345, n_estimators=est, max_depth=depth)
        
        model_forest.fit(features_train, target_train)
        
        predictions_valid = model_forest.predict(features_valid)
        
        result = accuracy_score(target_valid, predictions_valid)
    
        if result > best_result:
            
            best_model = model_forest
            
            best_result = result
            
            best_est = est
            
            best_depth = depth
            
print("Number of trees:", best_est)

print("The best tree depth:", best_depth)

print("Accuracy:", best_result)


# The random forest model recommends us a depth of 7, the number of trees is 30 and offers us an accuracy of 0.82. Given the results, our best choice would be a random forest model.

# # Checking the Model on a Test Sample

# In[13]:


predictions_test_forest = model_forest.predict(features_test)

accuracy_forest = accuracy_score(target_test, predictions_test_forest)

print('Accuracy Random Forest:', accuracy_forest)


# When testing random forest models, it behaves similarly to the accuracy obtained at the training stage, so we can say that it is possible to implement this model.

# # Checking the Models for Adequacy

# Let's check the adequacy of the models using Dummy Classifier.

# In[15]:


dummy_class = DummyClassifier(strategy = 'most_frequent', random_state = 12345)

dummy_class.fit(features_train, target_train)

result = dummy_class.score(features_test, target_test)

print('Accuracy Dummy Classifier:', result)

print('Accuracy Random Forest:', accuracy_forest)


# Comparing the two models, we see that the forest model is still the best option that we can use to predict plans.

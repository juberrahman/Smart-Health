#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sb
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


import os
import shutil
import posixpath
import wfdb


# In[3]:



# Download all the WFDB records and annotations from a small PhysioNet Database

# Make a temporary download directory in your current working directory
#cwd = os.getcwd()
#dl_dir = os.path.join(cwd, 'tmp_dl_dir')

# Download all the WFDB content
#wfdb.dl_database('apnea-ecg', dl_dir=dl_dir)

# Display the downloaded content in the folder
#display(os.listdir(dl_dir))


# In[4]:


#Download the file
df = pd.read_csv('apnee.csv')


# In[5]:


df.head()


# In[6]:


# set conditions for the values of a new column
#AHI is the sum of AI and AHI
conditions = [
    (df['AHI'] >5), 
    (df['AHI'] <= 5)]
values = [1,0]  # 1 mean the patient have apnea
#add the new column
df['positive'] = np.select(conditions, values)


# In[7]:


#subset my data
patients = df['sex'].value_counts()


# In[8]:


patients # total of patients


# In[9]:


# subset data into 2 categories according to AHI score 
healthy = df[df["AHI"] <= 5]
sick = df[df["AHI"] > 5]


# In[10]:


# set new conditions for a coumn in the subdata sick
#AHI is the sum of AI and AHI
conditions = [
    (sick['AHI'] <= 15), 
    (sick['AHI'] >= 15.01) & (sick['AHI'] <= 30 ),
    (sick['AHI'] > 30)]

values = ['mild', 'moderate', 'severe']
#add the new column
sick['status'] = np.select(conditions, values) # 


# In[11]:


sick.tail(10)


# In[12]:


#visualisation relation weight with AHI
sb.lineplot(data=df, x='weight', y='AHI') 


# In[13]:


#visualisation relation age with AHI
sb.lineplot(data=df, x='age', y='AHI' , color='green')


# In[14]:


#visualisation relation height with AHI
sb.lineplot(data=df, x='height', y='AHI')


# In[15]:


#using the subdata sick to see realtion of time sleep and AHI
sb.lineplot(data=sick, x='Length minutes', y='AHI')


# In[16]:


#visualisation relation hours with AHI
sb.lineplot(data=sick, x='hours(w/apenea)', y='AHI')


# In[17]:


#time sleep and AHI score for sick patients
sb.lineplot(data=sick, x='Length minutes', y='AHI')


# In[18]:


#times sleep and AHI score for healthy patient
sb.lineplot(data=healthy, x='Length minutes', y='AHI')


# In[19]:


# patients sicks
ps =pd.concat([sick], axis=1).groupby('status').positive.count()


# In[20]:


ps


# In[21]:


#visualisation variation AHI according weight
sb.lineplot(data=sick, x='weight', y='AHI')


# In[22]:


#correlation times apnea and positive
df['apnea'].corr(df['positive'])


# In[23]:


#correlation hours of apnea with positive
df['hours(w/apenea)'].corr(df['positive'])


# In[24]:


# correlation age and positivity
df['age'].corr(df['positive'])


# In[25]:


# variation AHI according age
sb.lineplot(data=sick, x='age', y='AHI')


# In[26]:


# age positive
sb.barplot(data=df, x='positive', y='age')


# In[27]:


#see women in the data
women = df[(df["sex"] == 'F')]
women.head()


# In[28]:


#see men in the data
men = df[(df["sex"] == 'M')]
men.head()


# In[29]:


healthy.head()


# In[30]:


#df.AHI.hist(bins=20)


# In[31]:


sb.lineplot(data=sick, x='Length minutes', y='AHI');


# In[32]:


# Visualisation relation column with cloumn
sb.pairplot(df.head(25), hue='positive')


# In[33]:


sb.violinplot(data=sick, x="hours(w/apenea)", y='AHI')


# In[34]:


#for every patient time of non apnea 
g = sb.FacetGrid(df, col="Record", col_wrap=7, height=3, hue='positive', aspect=.5)
g.map(sb.barplot, "sex", "Non-apnminutes", order=['F', 'M'])
g.add_legend()


# In[35]:


#this graph complete the first as you see people with long periode of non apnea but also short time of apnea
g = sb.FacetGrid(sick, col="Record", col_wrap=7, height=3, hue='positive', aspect=.5)
g.map(sb.barplot, "sex", "apnea", order=['F', 'M'])
g.add_legend()


# In[36]:


sb.violinplot(data=sick, x='AHI', y='status')


# In[37]:


#Visualisation of level AHI according age . show also the severity
sb.scatterplot(data=sick, x='apnea', y='AHI', 
                hue = 'status', 
                size = 'sex');


# In[ ]:





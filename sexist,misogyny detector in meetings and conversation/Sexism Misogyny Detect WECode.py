#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[9]:


get_ipython().run_line_magic('pip', 'install cohere')


# ## Loading dataset created manually
# 

# In[13]:


data = pd.read_csv('sexism Data final.csv')


# ## Classifying the comment as sexist or not 

# In[16]:


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


# In[57]:


train_data, test_data, train_labels, test_labels = train_test_split(data['text'], data['sexist'], test_size=0.4)


# In[58]:


# Convert text data into numerical feature vectors using TfidfVectorizer
vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(train_data)
test_vectors = vectorizer.transform(test_data)


# In[59]:


# Train an SVM model on the training data
model = LinearSVC()
model.fit(train_vectors, train_labels)


# In[60]:


# Evaluate the model on the testing data
accuracy = model.score(test_vectors, test_labels)
print("Accuracy: ", accuracy)


# In[61]:


#predicting the comment as sexist or not -- 1 INCIDATES THAT THE COMMENT IS STRONGLY SEXIST
new_text = "Men are superior than women and women are shit"
new_vector = vectorizer.transform([new_text])
prediction = model.predict(new_vector)
print("Prediction: ", prediction)


# In[62]:


new_text = "not at all good" # 0 - indicates that the comment is not sexist
new_vector = vectorizer.transform([new_text])
prediction = model.predict(new_vector)
print("Prediction: ", prediction)


# ## Now predicting the Toxicity level of the sexist comment 
# 
# 

# In[41]:


from sklearn.svm import SVR


# In[42]:


vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(data['text'])


# In[38]:


model = SVR()
model.fit(vectors, data['toxicity'])


# In[39]:


# Predict the toxicity level of new text
new_text = "A woman will never be truly fulfilled in life"
new_vector = vectorizer.transform([new_text])
toxicity_level = model.predict(new_vector)[0]
print("Toxicity level: {:.2f}%".format(toxicity_level * 100))


# In[48]:


# Predict the toxicity level of new text
new_text = "Men are superior than women and women are shit, useless and meant to be insulted"
new_vector = vectorizer.transform([new_text])
toxicity_level = model.predict(new_vector)[0]
print("Toxicity level: {:.2f}%".format(toxicity_level * 100))


# In[52]:


from cohere.classify import Example


# In[ ]:


toxicInputs = ["this women sucks, men best",  "stop being a dumbass","Let's do this and make a judgement","This is coming along nicely"  ]
toxicExamples = [
  Example("you are hot trash Mrs.", "Toxic"),  
  Example("She should go to hell", "Toxic"),
  Example("get rekt moron", "Toxic"),  
  Example("get a brain and use it", "Toxic"), 
  Example("say what you mean, you jerk.", "Toxic"), 
  Example("Are you really this stupid", "Toxic"), 
  Example("I will honestly kill you", "Toxic"),  
  Example("yo how are you", "Benign"),  
  Example("I'm curious, how did that happen", "Benign"),  
  Example("Try that again", "Benign"),  
  Example("Hello everyone, excited to be here", "Benign"), 
  Example("I think I saw it first", "Benign"),  
  Example("That is an interesting point", "Benign"), 
  Example("I love this", "Benign"), 
  Example("We should try that sometime", "Benign"), 
  Example("You should go for it", "Benign")
]


# In[ ]:





# In[ ]:





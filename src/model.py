import gensim
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# importing dataset 
dataset = pd.read_csv('../datasets/merged.csv')
dataset = dataset.dropna().reset_index()
dataset.text = dataset.text.apply(lambda x: x.split())
dataset = dataset[['text', 'label']]

#spilltings into training and testing
Xtrain, Xtest, ytrain, ytest = train_test_split(dataset['text'], dataset['label'], test_size=0.2)

#creating word2vec model
w2v_model = gensim.models.Word2Vec(
    window = 10,
    min_count = 2,
)

#building vocabulary and testing
w2v_model.build_vocab(Xtrain)
w2v_model.train(Xtrain, total_examples = w2v_model.corpus_count, epochs = w2v_model.epochs)

#setting the all vectors to same lenght 
words = set(w2v_model.wv.index_to_key )
Xtrain_vect = np.array([np.array([w2v_model.wv[i] for i in ls if i in words], dtype=object)
                         for ls in Xtrain], dtype=object)
Xtest_vect = np.array([np.array([w2v_model.wv[i] for i in ls if i in words], dtype=object)
                         for ls in Xtest], dtype=object)


Xtrain_vect_avg = []
for v in Xtrain_vect:
    if v.size:
        Xtrain_vect_avg.append(v.mean(axis=0))
    else:
        Xtrain_vect_avg.append(np.zeros(100, dtype=float))
        
Xtest_vect_avg = []
for v in Xtest_vect:
    if v.size:
        Xtest_vect_avg.append(v.mean(axis=0))
    else:
        Xtest_vect_avg.append(np.zeros(100, dtype=float))




#creating a SVM model 
model = SVC()

model.fit(Xtrain_vect_avg, ytrain)

model.score(Xtest_vect_avg, ytest)


#Saving the model for future use
filename = 'finalized_model.sav'
joblib.dump(model, filename)


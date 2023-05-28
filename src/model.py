import gensim
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def vectorize(traindoc):
    '''
    takes a corpus and returns its word2vec model and vector form
    and also saves the model for future use
    '''

    w2v_model = gensim.models.Word2Vec(
        window = 10,
        min_count = 2,
    )

    w2v_model.build_vocab(traindoc)
    w2v_model.train(traindoc, total_examples = w2v_model.corpus_count, epochs = w2v_model.epochs)

    words = set(w2v_model.wv.index_to_key )
    traindoc_vect = np.array([np.array([w2v_model.wv[i] for i in ls if i in words], dtype=object)
                         for ls in traindoc], dtype=object)

    traindoc_vect_avg = []
    for v in traindoc_vect:
        if v.size:
            traindoc_vect_avg.append(v.mean(axis=0))
        else:
            traindoc_vect_avg.append(np.zeros(100, dtype=float))

    filename = 'w2v_model.sav'
    joblib.dump(w2v_model, filename)

    print("word2vec training completed!!")
    return w2v_model,traindoc_vect_avg 

def makevector(w2v_model, doc):
    '''
    takes a word2vec model and a corpus and returns its vector form 
    '''

    words = set(w2v_model.wv.index_to_key )
    doc_vect = np.array([np.array([w2v_model.wv[i] for i in ls if i in words], dtype=object)
                         for ls in doc], dtype=object)
        
    doc_vect_avg = []
    for v in doc_vect:
        if v.size:
            doc_vect_avg.append(v.mean(axis=0))
        else:
            doc_vect_avg.append(np.zeros(100, dtype=float))
    return doc_vect_avg



def SvmModel(doc_vect_avg, target):
    '''
    takes a corpus in vector form and returns a SVM trained model 
    '''

    model = SVC()
    print("training model...")
    model.fit(doc_vect_avg, target)
    print("model training completed!!")
    return model 


def savemodel(model):
    '''
    saves the model locally
    '''
    filename = 'finalized_model.sav'
    joblib.dump(model, filename)

def accuracy(model,test,target):
    return model.score(test,target)


def main():
    # importing dataset 
    dataset = pd.read_csv('../datasets/merged.csv')
    dataset = dataset.dropna().reset_index()
    dataset.text = dataset.text.apply(lambda x: x.split())
    dataset = dataset[['text', 'label']]


    Xtrain, Xtest, ytrain, ytest = train_test_split(dataset['text'], dataset['label'], test_size=0.2)

    w2v_model,Xtrain_vect_avg = vectorize(Xtrain)

    Xtest_vect_avg = makevector(w2v_model,Xtest)

    model = SvmModel(Xtrain_vect_avg, ytrain)

    print(accuracy(model,Xtest_vect_avg, ytest))
    savemodel(model)

if __name__ == "__main__":
    main()
    




import model 
import joblib

def main():
    loadmodel = joblib.load("finalized_model.sav")
    w2v_model = joblib.load("w2v_model.sav")

    sentence = input("enter a sentence\n")
    sen_vec = model.makevector(w2v_model,[sentence.split()])

    print(model.accuracy(loadmodel,sen_vec,[1]))


if __name__ == "__main__":
    main()


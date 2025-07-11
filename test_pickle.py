import pickle

with open("careerlast.pkl", "rb") as f:
    model = pickle.load(f)

print("Model loaded successfully!")

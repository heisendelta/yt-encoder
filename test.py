import numpy as np
import pickle

with open('encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
with open('decoder.pickle', 'rb') as f:
    decoder = pickle.load(f)

encoder = encoder[::2, ::2].flatten()
decoder = decoder[::2, ::2].flatten()
encoder = encoder[:np.where(encoder >= 128)[0][0]]
decoder = decoder[:np.where(decoder >= 128)[0][0]]
print(len(encoder), len(decoder))

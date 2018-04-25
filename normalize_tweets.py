import json
import pickle
from collections import defaultdict
from generate_mapping import *
from generate_pos_info import *
from generate_candidate import *
from generate_feature import *
from load_store_data import *
from predictor import *

with open('mapping_unconstrained', 'rb') as fp:
    maps = pickle.load(fp)

def mapATweet(tweet):
    mappedTweet = initWithPOS([tweet])
    candidateTweets = generateCandidates(mappedTweet, maps, True, False)
    notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
    dataset = generateFeatureVectors(notDroppedTweets, featureTweets)
    tweet_idx, indices, categories, tokens, features, labels = dataset
    print('\n'.join([str(i) + ' ' + str(j) + ' ' + c + ' ' + t + ' ' + str(f) for (i, j, c, t, f) 
                        in zip(tweet_idx, indices, categories, tokens, features)]))
    # TODO using 'features' to classify, categories may help. Substitute the highest probability one with token
    #      and ' '.join them to form a new tweet.
    group_ix, tokens, features, labels = load_dataset(tweet_idx,indices, tokens, features, labels)
    model = load_model()
    predicted = model.predict(group_ix, features)
    return list(tokens[predicted]) # the result

if __name__ == '__main__':
    tweet = input()
    mapATweet(tweet)
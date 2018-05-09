# CS410 Final Project - Tweet Normalizer

## Introduction

The Tweet Normalizer is the implementation of the unconstrained mode of [this paper](http://www.aclweb.org/anthology/W15-4313): NCSU-SAS-Ning: Candidate Generation and Feature Engineering for Supervised Lexical Normalization. Tweets are retrieved by the Twitter API /statuses/filter on the account @TestNormalizer specifically registered for this application. With the training on dataset provided by [this competition](https://noisy-text.github.io/2015/norm-shared-task.html), and static mapping expanded by Lexical normalisation dictionary (found in Resource section in the competition). The application supplies the revision feature, which expand the dataset to enable better normalization.

## Setup

*The application only runs on MacOS or Linux.

### Set up Python 3 environment
Make sure Python 3 is installed by `which python3`, and install the required libraries
```
pip install -r requirements.txt
```

### Set up Electron

Install [Node.js and NPM](https://nodejs.org/en/), and install the packages:
```
cd twimalizer
npm install -g electron-forge
npm install --save
```

### Start the application

Stay in twimalizer folder, and run
```
electron-forge start
```

## Architecture

Two-step procedure including candidate generation and candidate evaluation is proposed in the paper.

### Feature Set

Feature set are generated for a token by calculating its n-gram and k-skip-n gram (In this application the configuration is 2-gram and 1-skip-2 gram). '$' is prepended and appended before and after the first and last n-gram, and '|' is added between skips. For example:

```
love -> { $lo, ov, ve$, l|v, o|e }
```

### Similarity Index

The paper propose to use Jaccard index as the similarity measure, which is the cardinality ratio of the intersection of two feature sets and their union.

### Candidate Generation

### Candidate Evaluation

For a token t<sub>i</sub> in the tweet T composed of "t<sub>1</sub> t<sub>2</sub> t<sub>3</sub> ... t<sub>i-1</sub> t<sub>i</sub> ... t<sub>n</sub>", candidates for it are associated with the following feature vectors for the classifier to determine if the candidate is the correct form to normalize to.

| Feature                  | Association | Definition                                                                               | Assumption                                                                                            |
| ------------------------ | ----------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Support                  | Token       | The number of times that the token appears during training                               | 0 if the token never appears during training                                                          |
| Confidence               | Candidate   | The probability that the token is normalized to this candidate form during training      | 1 if the corresponding token never appears during training                                            |
| Similarity               | Candidate   | Jaccard index calculated between the token and the candidate                             |                                                                                                       |
| Token Length             | Token       | The length of the token string                                                           |                                                                                                       |
| Candidate Length         | Candidate   | The length of the candidate string                                                       |                                                                                                       |
| Length Difference        | Candidate   | Difference of length between the token and the candidate                                 |                                                                                                       |
| Mean POS Confidence Diff | Candidate   | The change in the mean POS confidence for the whole tweet before and after normalization |                                                                                                       |
| POS Confidence Diff      | Candidate   | The change in POS confidence for the current token before and after normalization        | If the candidate is of multiple words, average POS confidence is used to calculate against the change |
| POS of t<sub>i-1</sub>   | Candidate   | The part-of-speech tagging of the previous token                                         | Empty for the first token                                                                             |
| POS of t<sub>i</sub>     | Candidate   | The part-of-speech tagging of the previous candidate                                     | If the candidate is of multiple words, the POS tagging for the first word is used                     |

# ~~TODO CLASSIFIER DETAIL, WHAT TYPE, TWO MODES~~


## Implementation

Training data is provided in JSON file, and the basic for of a tweet is the following:
```
{
    'input':  ['token1', 'token2', ...],
    'output': ['token1', 'token2', ...]
}
```
'input' is the original tweet tokenized, 'output' is the tokens normalized with correspondence to 'input'.

### Normalizer Implementation

Dataset generation:
- `generate_mapping.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|generateMap|tweets:List|(static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict)||
|augmentMapUsingEMNLP|(static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict)|(static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict)||
|augmentMapUsingFeiLiu|(static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict)|(static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict)||
|consolidateMap|(static_map(defaultdict),<br> support_map(defaultdict),<br> confidence_map(defaultdict),<br> index_map(defaultdict))|(static_map,<br> support_map,<br> confidence_map,<br> index_map):(dict, dict, dict, dict)||
- `generate_pos_info.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|initWithPOS|tweets:List|mappedTweets:List||
|generatePOSConfidence|tweets:List|(originalTweets, mappedTweets):(List, List)||
- `similarity_index.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|ngram|word:string<br>ninteger|k0gram:set||
|skipgram|word:string<br>n:integer<br>k:integer|kngram:set||
|sim_feature|word:string<br>n:integer<br>k:integer(default=1)|features:set||
|JaccardIndex|s1:string<br>s2:string<br>n:integer(default=2)<br>k:integer(default=1)<br>tailWeight:integer(default=3)|score:float||
- `generate_candidate.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||
- `generate_feature.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||
- `create_dataset.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||

Training & testing:
- `predictor.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||
- `training.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||
- `load_store_data.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||

Frontend:
- `normalize_tweets.py`

|Function|Parameters|Return|Description|
|--------|----------|------|-----------|
|||||

### GUI Implementation

The GUI is implemented using modern techniques with web development. The wrapper is Electron and the framework is Vue.js. Electron configuration is in `src/index.html` and `src/index.js`. Vue component `src/normalizer.vue` is using Semantic UI to create the feed list. A Twitter client is connected at the creation of the component, stream API is hooked to a function that continuously push new tweets to the array.

Normalizing process is achieved through using [Subprocess](https://www.npmjs.com/package/subprocess) to spawn a python instance to execute `normalize_tweets.py` with the input being the tweet and its output parsed to substitute the chosen tweet.

## Training & Testing

To train a new model, or, if new data are added and you would like to rebuild the dataset. Run
```
python3 create_dataset.py
```

~~TODO CONTINUE~~
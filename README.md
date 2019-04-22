# Event-Driven Stock Prediction using NLP
Objective: Design a news surveillance system targeting financial news from Reuters to predict market volatility from the position of a single investor without any access to real time trading infrastructure, using Natural Language Processing and Deep Learning techniques.


## Methodology

1. Data Collection and Dataset Construction

    1.1 crawl a ticker list to obtain the details of public companies from [NASDAQ](http://www.nasdaq.com/screening/companies-by-industry.aspx)

    1.2 crawl news from [Reuters](http://www.reuters.com/finance/stocks/overview?symbol=FB.O) using BeautifulSoup and proxy rotation
    
    1.3 crawl historical prices from [Yahoo Finance](https://finance.yahoo.com/) using selenium
    
    1.4 Build labels by calculating relative daily return w.r.t. S&P 500

2. Pre-Processing

    - Aggregate news by date
  
    - Remove stop words and keep only the top 20,000 most frequent financial words in news corpus
  
    - Merge news and labels by date
  
    - Make a single dataframe out of all the news
  
3. Feature Preparation, Model Building and Evaluation

    3.1 Neural Tensor Networks (1D-CNN-GMP and BI-DIR-GRU)
    
        - Vectorize news into a 2D integer tensor and pad sequences

        - Cluster labels and implement one-hot encoding

        - Train/Val Split

        - Prepare Embedding Matrix using GloVe

        - Declare Neural Architectues

        - Train, evaluate and test models
    
    3.2 Fine-tuning with BERT
    
        - Format data for BERT and do Train/Val Split

        - Download Pre-Trained Model (uncased_L-12_H-768_A-12.zip)

        - Configure fine-tuning parameters

        - Train and test model


## Requirement
* Python 3
* pandas
* numpy
* requests
* lxml
* bs4
* fake_useragent
* tor_request (script and folder included, used for only experimental purposes and for future work)
* selenium
* tqdm
* multiprocessing
* string
* [NLTK](https://www.nltk.org/install.html)
* pickle
* keras
* sklearn
* wget
* zipfile
* tensorflow


## Usage

Note: If you don't want to take time to crawl and pre-process data, you can skip steps 1 & 2, and start directly from 3. In addition you can take a look at the github directory https://github.com/antujn/Event-Driven-Stock-Prediction-using-NLP for full set of files and folders.

## Documentation 

Please find all the documentation including the final report in the documentation folder

## References:

1. Yoon Kim, [Convolutional Neural Networks for Sentence Classification](http://www.aclweb.org/anthology/D14-1181), EMNLP, 2014
2. J Pennington, R Socher, CD Manning, [GloVe: Global Vectors for Word Representation](http://www-nlp.stanford.edu/pubs/glove.pdf), EMNLP, 2014
3. Max Welling, Yee Whye Teh, [Bayesian Learning via Stochastic Gradient Langevin Dynamics](https://pdfs.semanticscholar.org/aeed/631d6a84100b5e9a021ec1914095c66de415.pdf), ICML, 2011
4. Tim Loughran and Bill McDonald, 2011, “When is a Liability not a Liability?  Textual Analysis, Dictionaries, and 10-Ks,” Journal of Finance, 66:1, 35-65.
5. H Lee, etc, [On the Importance of Text Analysis for Stock Price Prediction](http://nlp.stanford.edu/pubs/lrec2014-stock.pdf), LREC, 2014
6. Xiao Ding, [Deep Learning for Event-Driven Stock Prediction](http://ijcai.org/Proceedings/15/Papers/329.pdf), IJCAI2015
7. [IMPLEMENTING A CNN FOR TEXT CLASSIFICATION IN TENSORFLOW](http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/)
8. [Keras predict sentiment-movie-reviews using deep learning](http://machinelearningmastery.com/predict-sentiment-movie-reviews-using-deep-learning/)
9. [Keras sequence-classification-lstm-recurrent-neural-networks](http://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/)
10. [tf-idf + t-sne](https://github.com/lazyprogrammer/machine_learning_examples/blob/master/nlp_class2/tfidf_tsne.py)
11. [Implementation of CNN in sequence classification](https://github.com/dennybritz/cnn-text-classification-tf)
12. [Getting Started with Word2Vec and GloVe in Python](http://textminingonline.com/getting-started-with-word2vec-and-glove-in-python)
13. [BERT code adapted from the official google colab notebook](https://colab.research.google.com/github/tensorflow/tpu/blob/master/tools/colab/bert_finetuning_with_cloud_tpus.ipynb)
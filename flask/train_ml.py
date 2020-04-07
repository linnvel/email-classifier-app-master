## required packages

# system imports
import os
import sys
from termcolor import colored
from colorama import init
from nltk.corpus import stopwords
import pipeline
import pickle


# default data path
DATA_PATH = '../../data'

# default parameters
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
"it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
"should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
"hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
"mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
"wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]\
+ ['would','could','may','also', 'one', 'two', 'three','first', 'second' ,'third',
'someone', 'anyone', 'something', 'anything','subject', 'organization', 'lines',
'article', 'writes', 'wrote']

tokenize_regex1 = r"\w+|\$[\d\.]+"

def main_test(path):

    dir_path = path or DATA_PATH
    TRAIN_DIR = os.path.join(dir_path, "train")
    TEST_DIR = os.path.join(dir_path, "test")

    # load data
    print (colored('Loading files into memory', 'green', attrs=['bold']))

    train_path_list, ylabel_train = pipeline.parse_files(TRAIN_DIR)
    test_path_list, ylabel_test = pipeline.parse_files(TEST_DIR)

    train_documents = [pipeline.load_document(path = path, label = y) for \
                       path, y in zip(train_path_list, ylabel_train)]
    test_documents = [pipeline.load_document(path = path, label = y) for \
                      path, y in zip(test_path_list, ylabel_test)]

    # clean all documents
    print (colored('Cleaning all files', 'green', attrs=['bold']))
    pipeline.clean_all_documents(train_documents,
                                 word_split_regex = tokenize_regex1,
                                 stop_words = stop_words,
                                 contraction_dict = 'default')


    # encode labels
    print (colored('Encoding labels', 'green', attrs=['bold']))
    y_train, y_test, category = pipeline.label_encoder(ylabel_train, ylabel_test, 'ordinal')


    ## *************************** machine learning ***************************

    print (colored('Training SVM model', 'green', attrs=['bold']))
    model = pipeline.svm_clf
    model.fit(train_documents, y_train)

    print(colored('Finished train, save model', 'green', attrs=['bold']))
    path = 'app/static/models/svm_model.sav'
    pickle.dump(model, open(path, 'wb'))

    ##test predict

    # load the model from disk
    print(colored('Test prediction', 'green', attrs=['bold']))
    test_doc = test_documents[462]
    pipeline.clean_document(test_doc,
                            word_split_regex = tokenize_regex1,
                            stop_words = stop_words,
                            contraction_dict = 'default')
    loaded_model = pickle.load(open(path, 'rb'))
    result = loaded_model.predict([test_doc])
    print('Predicted label: ', category[int(result[0])])
    print('True label: ', test_doc._topic)



def main():
    init()

    # get the dataset
    print (colored("Where is the dataset?", 'cyan', attrs=['bold']))
    print (colored('Press return with default path', 'yellow'))
    ans = sys.stdin.readline()
    # remove any newlines or spaces at the end of the input
    path = ans.strip('\n')
    if path.endswith(' '):
        path = path.rstrip(' ')

    print ('\n\n')

    # do the main test
    main_test(path)

if __name__ == '__main__':
    main()

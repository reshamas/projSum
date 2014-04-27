__author__ = 'reshamashaikh'
# --------------------------------------------------------------------------
# Date:         4/25/14
# Version:      Python 2.7
#
# Path:         /Users/reshamashaikh/_0ba/_projects/_sumall/q3_classify
# Script:       q3_a.py
# Description:  SumAll.org Assessment Assignment
# --------------------------------------------------------------------------

from operator import itemgetter
import re


# set working directory
dataraw = "/Users/reshamashaikh/_0ba/_projects/_sumall/q3_classify/_data_raw/"
datapath = "/Users/reshamashaikh/_0ba/_projects/_sumall/q3_classify/_data/"
datader = "/Users/reshamashaikh/_0ba/_projects/_sumall/q3_classify/_data_out/"

#print("-" * 100)
print("-------------------------")
print("         begin")
print("-------------------------")

# ------------------------------
# Part 1 - read in files
# ------------------------------

# Files
# train_insult.csv --> 3,948 rows

# Insult	Date	Comment
# 1	20120514051050Z	"You want a smack on the back of your head punk?"
# 0	20120618235842Z	"Deb, some of it will fix itself when you start to trust yourself more and don't look to see where the ball went before you hit it."
# 0		"Only a moron would see things the way you do. You get alot more "bang for you buck" out of the military than food stamps."
# 0	20120530151552Z	"I live in Michigan, and there's a meth lab right down the road that got busted. What say you?"

# test_insult.csv --> 2,000 rows + 1 (header) = 2001 rows total
# Date	Comment
# 20120609203436Z	"Is that you, Yannick??????? Give it a rest."
# 20120618190345Z	"The BBC and left wing bias.\nHere's a rather clever analogy I heard a while ago..\nImagine this... You are an avid reader of say, The Telegraph-Mail or \nExpress. You go into your local newsagents and try to buy your copy to be told, "Sorry pal. If you want to buy that you MUST by the Guardian."
# 20120320204233Z	"\u201cF**k you man. Who do you think you are you poor c**t. F**k you, f**k your mother, f**k your father, f**k your wife, your children and your life. You are f**kall P***face.... Go f**k your hand.\u201d F""k your dogs"

# Unix - remove first line which is header
# to see how many lines in file:  wc -l *
# sed '1d' test_insult.csv > test_insult_2000.csv


# ------------------------------------------
# 1: separate into training/validate data
# ------------------------------------------
# Unix - remove first line which is header
# to see how many lines in file:  wc -l *
# sed '1d' train_insult.csv > train_insult_3947.csv

fileAllda = 'train_insult_3947.csv'          # use file with header row removed
fileTrain = 'insults_train_3000.txt'
fileValid = 'insults_valid_947.txt'
fileTest  = 'insults_test_2000_dclass.txt'

trainData = open(datapath + fileTrain, 'w')
validData = open(datapath + fileValid, 'w')

def createTrainTest():
  linect = 0
  rawData = open(dataraw + fileAllda)
  trainData = open(datapath + fileTrain,'w')
  validData = open(datapath + fileValid,'w')
  for line in rawData:
    linect += 1
    #line = line.strip('\n')
    if linect <= 3000:
      # print linect
      #line = line.strip('\n')
      trainData.write(line)
    else:
      validData.write(line)
trainData.close()
validData.close()

# Run module to split into train/validate data
createTrainTest()




# ------------------------------------------
# 2: reduce data; create feature vector
# ------------------------------------------
# 1 -- put all words in email in a list
# 2 -- make list into set (remove duplicate words)
#   -- turn set back into list so you can access indices
# 3 -- add set to a dictionary (this will give count of how often each word appears)
# 4 -- remove the words with < 30 occurrences
# 5 -- use dictionary to make a matrix, mxn, depending on how many words have >= 30 occurrences
# ------------------------------------------

debug = 1
print("-" * 100)

# for test file, it is missing classification
# insert dummy classification so file has similar structure to other files
# this will allow it to work with the current function
# dclass = dummy class

with open(datapath + 'test_insult_2000.csv', 'r') as f:
    lines = f.readlines()
lines = ['99,'+line for line in lines]
with open(datapath + 'insults_test_2000_dclass.txt', 'w') as f:
    f.writelines(lines)




# function reads in messy file
# writes out clean file


def readfile(filein, fileout, debug, label):
    f = open(datapath + filein,'r')
    g = open(datader + fileout,'w')

    linenum = -1
    for line in f:
        linenum += 1
        #print type(line)
        if debug == 1:
            print("\n")
            print("*"*50)
            print("linenum:  ")
            print(linenum)
            print("line:     ")
            print(line)
        line = line.strip('\n')
        #line = line.replace('.', '')
        #line = line.replace("'", '_')
        #if line.find('"') > -1:
        #    line = line.replace('"', '')

        record = line.split(',')
        #print(type(record))
        #print((record))
        classify = record[0]
        record = record[1:]
        #print((record))
        datet = record[0]
        date = datet[0:8]
        #print("date ", date)
        time = datet[8:10]
        #print("time ", time)
        if date:
            date = str(date)
        else:
            date = "x"
        if time:
            time = str(time)
        else:
            time = "x"

        temp3 = record[1:]
        temp4 = ''.join(temp3)  # join all the words in one line
        temp4 = ''.join(i for i in temp4 if not i.isdigit())  # remove digits
        email = temp4


        #if debug == 1:

        #print(temp1)
        #print(temp2)
        #print(temp3)
        #print(temp4)
        #print(type(temp1))
        #print(type(temp2))
        #print(type(temp3))
        #print(type(temp4))

        # clean up string keep only words, remove punctuation
        somestring = email
        rx = re.compile('\W+')
        email = rx.sub(' ', somestring).strip()
        email = email.lower()
        email = email.replace("_", '')
        if debug == 1:
            print("\n")
            print("cleaned string: ")
            print(email )

        g.write(classify + "," + date + "," + time + "," + email + "\n")
        if debug == 1:
            print('classify: ', classify)
            print("date:     ", date)
            print("time:     ", time)
            print("email:    ", email)
    print(" ")
    print('read file:    ', filein)
    print('lines read:   ', linenum+1)
    print('created file: ', fileout)
    print(" ")
    f.close()
    g.close()

readfile(fileTrain,'clean_train_3000.txt',0, 1)
readfile(fileValid,'clean_valid_947.txt',0, 1)
readfile(fileTest, 'clean_test_2000_dclass.txt',0, 1)



#exit()
# function reads in clean txt file
# sets dictionary with words in file

def crWordListBase(filein,debug):
    # initialize dictionary of word list
    wordDict = dict()

    f = open(datader + filein,'r')
    linect = -1
    for line in f:
        linect += 1
        line = line.strip('\n')
        line = line.split(',')
        email = line[3]
        if debug == 1:
            print(line)
            print(linect, email)

        email_words = email.split()
        #print(type(email))
        #print("\n")
        #print(len(email_words))

        # initialize wordlist for each line
        email_wordList = []

        for word in email_words:
            email_wordList.append(word)  # add to list

        if debug == 1:
            print('len(email_wordList)')
            print(len(email_wordList))
        # make into set (remove duplicate words)
        set_email_wordList = set(email_wordList)
        #print(len(set_email_wordList))

        # turn back into list
        wordList = list(set_email_wordList)
        if debug == 1:
            print('len(wordList)')
            print(len(wordList))

        # add wordList to dictionary
        for i in range(0, (len(wordList))):
            if wordList[i] in wordDict:
                wordDict[wordList[i]] += 1
                #print(i, wordList[i], wordDict[wordList[i]])
            else:
                wordDict[wordList[i]] = 1
    print("\n")
    print("len(wordDict): ", len(wordDict))
    f.close()
    return wordDict




wordDict = crWordListBase('clean_train_3000.txt',0)

#exit()

#-----------------------------------------
# remove words with low frequency counts
#-----------------------------------------
wordDict = {key: value for key, value in wordDict.items() if value > 20}

print('len(wordDict_reduced): ', len(wordDict))
#print("\nsum of all counts: ", sum_count)

print("\n")


#exit()
#------------------------------------------------------------------
# function - checks line of file to see if word is in dictionary
#            sets matrix of 0 and 1
#------------------------------------------------------------------
def setDataArray(dir, file, dim_row,debug):
    print(" ")
    # initialize arrays and matrix
    yarray = []
    #print dim_row

    # initialize matrix
    matrix = [[0] * dim_row for x in range(1)]
    linect = -1

    f = open(dir + file, 'r')
    for line in f:
        linect += 1
        if debug == 1: print('linect: ', linect)
        line = line.strip('\n')
        record = line.split(',')
        #print('record', record)
        #print('type(record)', type(record))
        record_0_2 = record[0:2]
        #record=record.split()
        record = record[3:]
        record = record[0].split()
        if debug == 1:
            print("record: ")
            print(record)
        xarray = []

        tempy = (int(record_0_2[0]))
        #tempy = (int(record[0]))
        if tempy == 0:
            yarray.append(-1)
        else:
            yarray.append(1)

        for dictword in sorted_key:
            dwordct=0
            for word in record:
                if word in dictword:
                    dwordct +=1
                    #print linect, dictword, word, dwordct
            if dwordct > 0:
                xarray.append(1)
            else:
                xarray.append(0)
        matrix.append(xarray)
        #print matrix
    f.close()

    #print matrix
    X = np.mat(matrix)
    # delete first row, which was initialization
    X = np.delete(X, (0), axis=0)
    #print "X type: ", type(X)

    #print "x matrix: "
    #print X
    y = (np.mat(yarray)).T


    data_xy = np.hstack([X, y])
    print('Created matrices:  ')
    print('---------------------------')
    print('using file:        ', file)
    print("dim of X: ", X.shape)
    print("dim of y: ", y.shape)
    print(" ")
    print("data_xy.shape: ", data_xy.shape)
    print("data_xy: ", type(data_xy))
    print(" ")
    #print data_xy
    dataxy = np.squeeze(np.asarray(data_xy))
    return (dataxy, X, y, yarray)


sorted_key = sorted(wordDict.items(), key=itemgetter(0))
#wordsinDict = len(sorted_key)
DictLength = len(sorted_key)


# function returns matrix of 0 and 1 if word is in dictionary
# Input:  cleaned email file
data_train, X, y, y1d = setDataArray(datader,'clean_train_3000.txt', DictLength,0)

data_valid, Xv, yv, y1dv = setDataArray(datader,'clean_valid_947.txt', DictLength,0)

data_test, Xt, yt, y1dt = setDataArray(datader,'clean_test_2000_dclass.txt', DictLength,0)


print("-------------------------------")
print("start analysis")
print("-------------------------------")

import numpy as np
import pylab as pl


from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()


def runLogis(label, Xdata, ydata, XNoLabel, testcase, debug):
    print("-------------- ")
    print(label)
    print("---------------")
    print("X(shape):  ", Xdata.shape)
    print("y(shape):  ", ydata.shape)
    if debug == 1:
        print("type(X):   ", type(Xdata))
        print("type(y):   ", type(ydata))
    print("-------------------------")
    if debug == 1:
        print("X:")
        print(Xdata)
        print("-------------------------")
        print("y:")
        print(ydata)
        print("-------------------------")
    print("-------------------------")
    lr = LogisticRegression(C = 1.0)
    lr.fit(Xdata, ydata)
    print("\n")
    print(lr.fit(Xdata, ydata))
    print("-------------------------")
    print("prediction probabilities of X:")
    print("The returned estimates for all classes are ordered by the label of classes")
    print("number of samples x number of classes (2 if 0-1)")
    lr.predict_proba(Xdata)
    print(lr.predict_proba(Xdata))
    print("-------------------------")
    print("Predict confidence scores for samples.")
    print("The confidence score for a sample is the signed distance of that sample to the hyperplane")
    print("Confidence scores per (sample, class) combination. In the binary case, ")
    print("confidence score for self.classes_[1] where >0 means this class would be predicted.")
    print(" ")
    print(lr.decision_function(Xdata))
    print("-------------------------")
    print("regression coefficients shape[n_classes-1, n_features]")
    #print(lr.coef_)
    print("-------------------------")
    print("params: ")
    print(lr.get_params(deep=True))
    print("-------------------------")
    print("fit_transform: ")
    print("Fits transformer to X and y with optional parameters fit_params and returns a transformed version of X")
    print(lr.fit_transform(Xdata, ydata))
    print("-------------------------")
    print("scores, Returns the mean accuracy on the given data and labels: ")
    print(lr.score(Xdata, ydata))
    print("-------------------------")
    if testcase == 1:
        print("XNoLabel:")
        #print("shape(XNoLabel)", shape.XNoLabel )
        print(XNoLabel)
        predY = lr.predict(XNoLabel)

        print("-------------------------")
        print("Predict class labels for samples in X ")
        print("len(lr.predict(XNoLabel))", len(predY) )
        print("type(lr.predict(XNoLabel))", type(predY) )
        print(" ")
        print("predY:")
        print(predY[0:20])
        return predY

Xexamp = np.random.randn(5, 4)
yexamp = np.array([1, 0, 0, 1, 1])
xexampPP = np.array([1.,0.,0.,1.])   # test case, no labels, only X variables

Xexamp = [[ 0.19320016, -0.05708582,  0.28401233,  1.56950937],
 [-0.2556172,  -0.11653671,  0.72221708,  1.75652408],
 [-1.49007995, -0.03109934, -1.71674537,  2.27005546],
 [ 0.1494321,  -0.24853998,  2.12769413, -0.68453802],
 [ 1.31304209, -0.33632986, -1.63709794, -0.67353963]]

Xexamp=np.array(Xexamp)
yexamp = [1, 0, 0, 1, 1]
yexamp=np.array(yexamp)

runLogis('example', Xexamp, yexamp,xexampPP, 1, 1)

Xtrain = np.array(X)
ytrain = np.array(y1d)

Xvalid = np.array(Xv)
yvalid = np.array(y1dv)

predYvalid = runLogis('training', Xtrain, ytrain, Xvalid, 1, 1)

# run logistic model on test data (has 2000 rows)
Xtest = np.array(Xt)
ytest = np.array(y1dt)

predYtest = runLogis('test', Xtrain, ytrain, Xtest, 1, 1)


f = open(datader + 'insults_test_prediction_2000.csv','w')
for i in range(len(predYtest)):
    resp = predYtest[i]
    if resp == -1:
        f.write("0" + "\n")
    else:
        f.write("1" + "\n")
    #print(predYtest[i])

f.close()
exit()


def getError(yobs, ypred, debug):
    print(" ")
    print("-------------------------")
    print(" get error ")
    print("-------------------------")
    if debug == 1:
        print(type(yobs))
        print(type(ypred))
        print(len(yobs))
        print(len(ypred))
        print((yobs.shape))
        print((ypred.shape))
        print(yobs[0:20])
        print(ypred[0:20])
    errors = 0
    correct = 0
    n = len(yobs)
    for i in range(len(yobs)):
        y_obs = yobs[i]
        y_pred = ypred[i]
        diff = y_obs - y_pred
        if yobs[i] == ypred[i]:
            correct += 1
        else:
            errors += 1

        if debug == 1 and i< 20:
            print(i, y_obs, y_pred, diff, errors, correct)

    error_rate = float(errors) / float(n)
    accuracy = 1 - error_rate
    print("-----------------------------")
    print("error_rate %.3f, accuracy %.3f): "  %(error_rate, accuracy))
    print("-----------------------------")
    return (error_rate, accuracy)

getError(yvalid, predYvalid,0)


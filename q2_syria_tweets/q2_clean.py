__author__ = 'reshamashaikh'
# --------------------------------------------------------------------------
# Date:         4/24/14
# Version:      Python 3.3
#
# Path:         /Users/reshamashaikh/_0ba/_projects/_sumall/q2_syria_tweets
# Script:       01_q2_a.py
# Description:  SumAll.org Assessment Assignment
# --------------------------------------------------------------------------

# set working directory
path_data = "/Users/reshamashaikh/_0ba/_projects/_sumall/q2_syria_tweets/_data/"

print("-" * 100)

from collections import Counter
from operator import itemgetter


# ------------------------------
# Part 1 - read in files
# ------------------------------
# Files
# tweets.json --> 4,132,406 rows
# { "_id" : "371045756826050561", "text" : "RT @arabic_Leos: لو #الأسد في حالة إعجاب، تجده يتحدث عن الشخص طول الوقت، يفكر به ويكتب عنه يبحث عن صفحاته في النت ويدمن عليه، لذا احتمالية …", "created_at" : "Fri Aug 23 23:06:16 +0000 2013" }
# { "_id" : "371045780997808128", "text" : "RT @arabic_Leos: #الأسد يشبه القطة لو كان في مكان لأول مرة أو بين أشخاص جدد، خجول وهادئ مترقب يحاول استيعاب ما حوله قبل القيام بأي خطوة.", "created_at" : "Fri Aug 23 23:06:22 +0000 2013" }
# { "_id" : "371045827567173632", "text" : "RT @arabic_Leos: كونك أكبر مني لا يعطيك الأحقية لتخبرني ماذا علي أن أفعل ومن أصادق وكيف أصرف نقودي -هكذا يفكر #الأسد-", "created_at" : "Fri Aug 23 23:06:33 +0000 2013" }
# _id, text, created_at


import json
from datetime import datetime


filename = "tweets.json"


tweet_info = []
linect = -1
maxlines = 4132406 + 1
#maxlines = 10000

# read json file

#with open('tw3.json', encoding='utf-8') as f:
with open(path_data+filename, encoding='utf-8') as f:
    for line in f:
        linect += 1
        if linect < maxlines:
            #print('\n')
            #print(linect, repr(line))
            d = json.loads(line)
            #print(type(d))
            #print(d)
            tw_date = d['created_at']    # d is of type dictionary
            #print(tw_date)
            tw_date= datetime.strptime(tw_date,'%a %b %d %H:%M:%S +0000 %Y')
            #tw_date= datetime.strptime(tw_date,'%a %b %d 00:00:00 +0000 %Y')
            tw_date = datetime.date(tw_date)
            tw_date_str = tw_date.strftime('%Y-%m-%d')
            #print(test)
            #print(type(tw_date))
            #tweet_info.append(tw_date)
            tweet_info.append(tw_date_str)



print("-" * 100)

print("file 1: ")
print("linect: ", linect)
print("len(tweet_info): ", len(tweet_info))
#print("tweet_info: ", tweet_info[0])


counts = Counter(tweet_info)


print("-" * 100)
print(type(counts))
#print(counts)

x_date =[]
x_date_str = []
y_count = []
sum_count = 0
keynum = 0
maxkeys = 500
maxkeys = 1000000
for k, v in sorted(counts.items(), key=itemgetter(0)):
    keynum += 1
    if keynum < maxkeys:
        print(keynum, "\t", k,"\t\t\t", v)
        k_str = str(k)
        print(k_str)
        x_date.append(k)
        x_date_str.append(k_str)
        y_count.append(v)
        sum_count += v

print("-" * 100)
print("sum of all counts: ", sum_count)

sorted_counts = sorted(counts.items(), key=itemgetter(0))
#print(counts)
print("x_date, y_count")
print(x_date, y_count)

print("-" * 100)
print(x_date[0])
f = open('date_tweets.tsv','w')
g = open('date_tweets_freq.tsv', 'w')


for i in range(len(x_date)):
    if i == 0:
        g.write('letter' + '\t' + 'frequency' + '\n')
    total_tweets = 4132406
    pct = y_count[i]/total_tweets
    pctf = format(pct, '.5f')
    day = str(i+1).zfill(2)
    f.write(x_date[i] + '\t' + str(y_count[i]) + '\n') #, '\n') # python will convert \n to os.linesep
    g.write(day + '\t' + pctf + '\n')
    #temp = x_date[i] + '\t' , y_count[i], '\n'
    #f.write(x_date[i] ,  '\t' , y_count[i], '\n')
f.close()


# do simple line chart
# import matplotlib.pyplot as pyplot

#pyplot.plot(x_date,y_count)
#pyplot.show()








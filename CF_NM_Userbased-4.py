__author__ = 'rohit'
import numpy
import csv
import random
import math
from math import sqrt
import etl_utils
from scipy import stats, optimize, interpolate
import scipy.stats
import Queue
import threading
import time
import sys

from operator import mul
ITEM_INDEX = 'item_id'
USER_INDEX = 'user_id'
RATING_INDEX = 'overall_rating'
TOTAL_USERS = '943'
TOTAL_ITEMS = '1682'
TOTAL_RATINGS = '20000'
N=str(sys.argv[1])
print N
SimilarityFile = str(sys.argv[2])
print SimilarityFile
EstimatedRatingFile = str(sys.argv[3])
print EstimatedRatingFile
Type = str(sys.argv[4])
M='1'
trainingSet = etl_utils.ETLUtils.load_csv_file('./MovieLensData/u'+N+'.csv', '\t')

#SijData = etl_utils.ETLUtils.load_csv_file('./SValuesUserBased/Pearson_Sij_UserBased-test'+N+'.csv', '\t')
SijData = etl_utils.ETLUtils.load_csv_file('./SValuesUserBased/'+SimilarityFile, '\t')
TestSet = etl_utils.ETLUtils.load_csv_file('./MovieLensData/u'+N+'-test.csv', '\t')


#Calculate the estimated rating
def EstimatedRating(S, Aui):
    S2 = 0.0
    S1 = 0.0
    R = 0.0
    for records in S:
        S1 = S1 + float(records[0]) * ( float(records[1]) - float(records[2]) )
        S2 = S2 + float(records[0])
        R = float(Aui) + (abs(float(S1))/abs(float(S2)))
    return R

def adjustedCosineSim(trainingSet, USER1, USER2):
    num = []
    deno1 = []
    deno2 = []
    item_ratings =[]
    #Get all the records for items I and J
    my_user_records_user1 = etl_utils.ETLUtils.filter_records(trainingSet, USER_INDEX,[USER1])
    my_user_records_user2 = etl_utils.ETLUtils.filter_records(trainingSet, USER_INDEX,[USER2])

    #Loop through records from items I and J and calculate numerator and denominator values for adjusted cosine formula
    for records_user1 in my_user_records_user1:
        for records_user2 in my_user_records_user2:
            if records_user1[ITEM_INDEX] == records_user2[ITEM_INDEX]:
                my_user_records_ITEM = etl_utils.ETLUtils.filter_records(trainingSet,ITEM_INDEX,[records_user1[ITEM_INDEX]])
                for records in my_user_records_ITEM:
                    item_ratings.append(float(records[RATING_INDEX]))

                avgRating_ITEM = sum(item_ratings)/len(item_ratings)

                #Calculate denominator and numerator values for adjusted cosine simliarity
                num.append((float(records_user1[RATING_INDEX]) - float(avgRating_ITEM)) * (float(records_user2[RATING_INDEX]) - float(avgRating_ITEM)))
                deno1.append(math.pow((float(records_user1[RATING_INDEX]) - float(avgRating_ITEM)),2))
                deno2.append(math.pow((float(records_user1[RATING_INDEX]) - float(avgRating_ITEM)),2))

    #If denominator values are 0. Return 0
    if sum(deno1) == 0:
        return 0
    if sum(deno2) == 0:
        return  0

    return (sum(num) / math.sqrt(sum(deno1)) * math.sqrt(sum(deno2)))

def cosineSim(trainingSet, USER1, USER2):
    num = []
    deno1 = []
    deno2 = []

    #Get all the records for items I and J
    my_user_records_user1 = etl_utils.ETLUtils.filter_records(trainingSet, USER_INDEX,[USER1])
    my_user_records_user2 = etl_utils.ETLUtils.filter_records(trainingSet, USER_INDEX,[USER2])

    #Loop through records from items I and J and calculate numerator and denominator values for adjusted cosine formula
    for records_user1 in my_user_records_user1:
        for records_user2 in my_user_records_user2:
            if records_user1[ITEM_INDEX] == records_user2[ITEM_INDEX]:
                num.append(float(records_user1[RATING_INDEX]) * float(records_user2[RATING_INDEX]))
                deno1.append(math.pow((float(records_user1[RATING_INDEX])),2))
                deno2.append(math.pow((float(records_user2[RATING_INDEX])),2))

    #If denominator values are 0. Return 0
    if sum(deno1) == 0:
        return 0
    if sum(deno2) == 0:
        return  0

    return (sum(num) / math.sqrt(sum(deno1)) * math.sqrt(sum(deno2)))


#Calculate Pearson and Sij values. Return Sij value.
def PearsonSij(trainingSet,U1,U2):
    x=[]
    y=[]
    xy = []
    xsquare = []
    ysquare = []
    xsum =0
    ysum = 0
    xysum = 0
    xsqr_sum = 0
    ysqr_sum = 0
    coeff = 0
    num = 0
    deno = 0

    my_user_records1 = etl_utils.ETLUtils.filter_records(trainingSet, USER_INDEX, [U1])
    my_user_records2 = etl_utils.ETLUtils.filter_records(trainingSet, USER_INDEX, [U2])

    for user_record1 in my_user_records1:
       for user_record2 in my_user_records2:
            if user_record1[ITEM_INDEX] == user_record2[ITEM_INDEX]:
                x.append(float(user_record1[RATING_INDEX]))
                y.append(float(user_record2[RATING_INDEX]))
                xy.append(float(user_record1[RATING_INDEX])*(float(user_record2[RATING_INDEX])))
                xsquare.append(float(user_record1[RATING_INDEX])*float(user_record1[RATING_INDEX]))
                ysquare.append(float(user_record2[RATING_INDEX])*float(user_record2[RATING_INDEX]))

    xsum = sum(x)
    ysum = sum(y)
    xysum = sum(xy)
    xsqr_sum = sum(xsquare)
    ysqr_sum = sum(ysquare)
    n=len(x)
    if n == 0:
        return 0

    num = (float(n) * float(xysum)) - (float(xsum) * float(ysum))
    deno = (float(n) * float(xsqr_sum) - (float(xsum) * float(xsum)) * (float(n) * float(ysqr_sum)) - (float(ysum) * float(ysum)))
    if float(deno) == float(0):
        return 0
    coeff = float(num) / float(deno)
    Sij = (float(len(x)) / (float(len(x)) + 100)) * float(coeff)
    return Sij

def AverageAu(trainingSet, U1):
    x = []
    Au = 0.0
    my_user_records1 = etl_utils.ETLUtils.filter_records(trainingSet, 'user_id', [U1])
    for records in my_user_records1:
        x.append(float(records[RATING_INDEX]))

    Au = sum(x) / len(x)
    return float(Au)
    '''
    for record in trainingSet:
        if int(record[USER_INDEX]) == int(U1):
			x.append(float(record[RATING_INDEX]))
    Au = numpy.mean(x)
    return float(Au)'''


def RealRatings(trainingSet, I1, U1):
    x = 0
    my_user_records1 = etl_utils.ETLUtils.filter_records(trainingSet, 'user_id', [U1])
    for records in my_user_records1:
        if records['item_id']== I1:
            x=records['overall_rating']

    if x is None:
        return 0.0

    return float(x)


def AverageAi(trainingSet, I1):
    x = []
    Ai = 0
    for record in trainingSet:
        if record[ITEM_INDEX] == I1:
            x.append(float(record[RATING_INDEX]))

    if len(x) == 0:
        return 0.0

    Ai=numpy.mean(x)
    return float(Ai)



def main():
    Rating_difference = []
    Rating_difference2 = []
    i= 1
    from timeit import default_timer as timer
    start = timer()
    #fo = open('Estimated-Ratings-Pearson-u'+N+'-test.csv','rw+')
    fo = open(EstimatedRatingFile,'rw+')
    for records in TestSet:
        Sij= []
        user2 = []
        num = []
        deno = []
        num2 = []
        deno2 = []

        user1 = records['user_id']
        user1_item = records['item_id']
        user1_rating = records['overall_rating']
        AvgUser1 = AverageAu(trainingSet, user1)
        my_sij_records = etl_utils.ETLUtils.filter_records(SijData, 'user1', [user1])

        for all_sij_records in my_sij_records:
            Sij.append(float(all_sij_records['sij_values']))
            user2.append(all_sij_records['user2'])


        SijValues = zip(Sij,user2)

        SijValues.sort(reverse=True)
        TopHundredValues = SijValues[0:100]
        TopFiftyValues = SijValues[0:50]

        #Calculate estimated rating for 50 nearest neighbors
        for records in TopFiftyValues:
            #records[0] = Sij Values, records[1] = user2. User2 is required to calculate Average user rating.
            num.append(records[0] * (float(RealRatings(trainingSet, user1_item, records[1])) - float(AverageAu(trainingSet,records[1]))))
            #print records[0], float(RealRatings(trainingSet, user1_item, records[1])), float(AverageAu(trainingSet,records[1]))
            deno.append(records[0])

        Estimated_rating = float(AvgUser1) + (abs((sum(num)) / abs(sum(deno))))
        #print float(AvgUser1) ,"+",sum(num), "/",sum(deno)
        diff = float(Estimated_rating) - float(user1_rating)
        #fo.seek(0,2)
        #str1= str(user1)+"  "+str(user1_item)+"    "+str(user1_rating)+"   "+str(Estimated_rating)+"   "+str(diff)+"\n"
        #fo.write(str1)
        Rating_difference.append(pow(diff,2))

        #Calculate estimated ratings for 100 nearest neighbors
        for records in TopHundredValues:
            #records[0] = Sij Values, records[1] = user2. User2 is required to calculate Average user rating.
            num2.append(records[0] * (float(RealRatings(trainingSet, user1_item, records[1])) - float(AverageAu(trainingSet,records[1]))))
            #print records[0], float(RealRatings(trainingSet, user1_item, records[1])), float(AverageAu(trainingSet,records[1]))
            deno2.append(records[0])

        Estimated_rating2 = float(AvgUser1) + (abs((sum(num2)) / abs(sum(deno2))))
        #print float(AvgUser1) ,"+",sum(num), "/",sum(deno)
        diff2 = float(Estimated_rating2) - float(user1_rating)
        #fo.seek(0,2)
        #str1= str(user1)+"  "+str(user1_item)+"    "+str(user1_rating)+"   "+str(Estimated_rating)+"   "+str(diff)+"\n"
        #fo.write(str1)
        Rating_difference2.append(pow(diff2,2))

        print '(Test-'+N+') Records for Test-'+N+'completed ->', i,'/'+'2000'
        i = int(i)+1
        del num[:]
        del deno[:]
        del num2[:]
        del deno2[:]
        del SijValues[:]
        del Sij[:]
        del TopFiftyValues[:]
        del TopHundredValues[:]
        del user2[:]


    RMSE = sqrt(sum(Rating_difference) / len(Rating_difference))
    RMSE100 = sqrt(sum(Rating_difference2) / len(Rating_difference2))
    print 'Pearson-Test-'+N+'RMSE (50)-'+N+' = ', RMSE
    print 'Pearson-Test-'+N+'RMSE (100)-'+N+' = ', RMSE100
    end = timer()
    print 'Time = ',(end - start)/60,' mins'
    fo.seek(0,2)
    str2 = 'u'+N+'-test-'+Type+': RMSE (50) = '+RMSE+', and RMSE (100) = '+RMSE100+' Time Required = '+(end - start)/60+' mins'
    fo.write(str2)
    fo.close()
    del Rating_difference[:]
    del Rating_difference2[:]


'''
    Similarity = {}
    Similarity_mat = Similarity

    for user1 in xrange(1, int(TOTAL_USERS)):
        Similarity[user1] = {}

    fo = open('PearsonSij-U2.csv','rw+')
    for user1 in xrange(1, int(TOTAL_USERS)):
        for  user2 in xrange (user1+1, int(TOTAL_USERS)):
                Svalue = PearsonSij(trainingSet, str(user1), str(user2))
                Similarity_mat[user1][user2] = Svalue
                Similarity_mat[user2][user1] = Svalue
                fo.seek(0,2)
                str1 = str(user1)+"    "+str(user2)+"     "+str(Svalue)+"\n"
                str2 = str(user2)+"    "+str(user1)+"     "+str(Svalue)+"\n"
                fo.write(str1)
                fo.write(str2)

    fo.close()


    Similarity_Cosine = {}
    Similarity_Cosine_mat = Similarity_Cosine

    for user in xrange(1, int(TOTAL_USERS)):
        Similarity_Cosine[user] = {}

    fo = open('CosineSij-U1.csv','rw+')
    for user1 in xrange(1, int(TOTAL_USERS)):
        for  user2 in xrange (user1+1, int(TOTAL_USERS)):
                Svalue = cosineSim(trainingSet, str(user1), str(user2))
                Similarity_Cosine_mat[user1][user2] = Svalue
                Similarity_Cosine_mat[user2][user1] = Svalue
                fo.seek(0,2)
                str1 = str(user1)+"    "+str(user2)+"     "+str(Svalue)+"\n"
                str2 = str(user2)+"    "+str(user1)+"     "+str(Svalue)+"\n"
                fo.write(str1)
                fo.write(str2)
    fo.close()


    Similarity_AdjCosine = {}
    Similarity_AdjCosine_mat = Similarity_AdjCosine
    for user in xrange(1, int(TOTAL_USERS)):
        Similarity_AdjCosine[user] = {}

    fo = open('AdjCosineSij-U1.csv','rw+')
    for user1 in xrange(1, int(TOTAL_USERS)):
        for  user2 in xrange (user1+1, int(TOTAL_USERS)):
                Svalue = adjustedCosineSim(trainingSet, str(user1), str(user2))
                Similarity_AdjCosine_mat[user1][user2] = Svalue
                Similarity_AdjCosine_mat[user2][user1] = Svalue
                fo.seek(0,2)
                str1 = str(user1)+"    "+str(user2)+"     "+str(Svalue)+"\n"
                str2 = str(user2)+"    "+str(user1)+"     "+str(Svalue)+"\n"
                fo.write(str1)
                fo.write(str2)
    fo.close()
'''


'''
    u = recommenderUtils.AverageAu(trainingSet,USER)
    for i in xrange(1, int(TOTAL_USERS)):
        if int(i) != int(ITEM):
            S1 = recommenderUtils.PearsonSij(trainingSet, str(USER), str(i))
            S.append(S1)
            temp = recommenderUtils.RealRatings(trainingSet, str(i), str(USER))
            Rj.append(temp)
            Aj.append(recommenderUtils.AverageAi(trainingSet,str(i)))
            Jposition.append(i)

    AllValues = zip(S, Rj, Aj, Jposition)
    AllValues.sort(reverse=True)
    TopNVal = AllValues[:50]
    Rating = EstimatedRating(TopNVal,u)
    print Rating
'''

'''
    my_records = random.shuffle(trainingSet)

    for records in my_records:
        DataSet = my_records


    TrainingSet = DataSet[0:799]
    TestSet = DataSet[800:1000]

    fo = open('TrainingSet-U1.csv','rw+')
    for records in TrainingSet:
        str1 = str(records[USER_INDEX])+"    "+str(records[ITEM_INDEX])+"    "+str(records[RATING_INDEX])+"\n"
        fo.seek(0,2)
        fo.write(str1)
    fo.close()

    fo = open('TestSet-U1.csv','rw+')
    for records in TestSet:
        str1 = str(records[USER_INDEX])+"    "+str(records[ITEM_INDEX])+"    "+str(records[RATING_INDEX])+"\n"
        fo.seek(0,2)
        fo.write(str1)
        fo.write("\n")
    fo.close()
'''



main()





__author__ = 'rohit'
import os
#Run CF_NM_UserBased-4.py with arguments
# argv[0] = CF_NM_UserBased-4.py
#argv[1] = Value of N - used for changing file name for trainingSet (e.g. u'+N+'.csv = u1.csv where N=1) and TestSet (e.g. ./MovieLensData/u'+N+'-test.csv' = ./MovieLensData/u1-test.csv' where N=1)
#argv[2] = Similarity file (./SValuesUserBased/'+SimilarityFile where SimilarityFile=Pearson_Sij_UserBased-test4.csv)
#argv[3] = Estimated Reating File to record RMSE values for each test.
#argv[4] = "Type" of similarity measure (e.g. pearson, Cosine, Adj. Cosine etc). Used at the very end while storing final RMSE values in Estimated Ratings File. It should be changed in the future.
 
os.system('python CF_NM_UserBased-4.py "4" "Pearson_Sij_UserBased-test4.csv" "Estimated-Ratings-Pearson-u4-test.csv" "Pearson"')

os.system('python CF_NM_UserBased-4.py "5" "Pearson_Sij_UserBased-test5.csv" "Estimated-Ratings-Pearson-u5-test.csv" "Pearson"')

os.system('python CF_NM_UserBased-4.py "1" "Cosine_Sij_UserBased-test1.csv" "Estimated-Ratings-Cosine-u1-test.csv" "Cosine"')

os.system('python CF_NM_UserBased-4.py "2" "Cosine_Sij_UserBased-test2.csv" "Estimated-Ratings-Cosine-u2-test.csv" "Cosine"')

os.system('python CF_NM_UserBased-4.py "3" "Cosine_Sij_UserBased-test3.csv" "Estimated-Ratings-Cosine-u3-test.csv" "Cosine"')

os.system('python CF_NM_UserBased-4.py "4" "Cosine_Sij_UserBased-test4.csv" "Estimated-Ratings-Cosine-u4-test.csv" "Cosine"')

os.system('python CF_NM_UserBased-4.py "5" "Cosine_Sij_UserBased-test5.csv" "Estimated-Ratings-Cosine-u5-test.csv" "Cosine"')

os.system('python CF_NM_UserBased-4.py "1" "AdjCosine_Sij_UserBased-test1.csv" "Estimated-Ratings-AdjCosine-u1-test.csv" "AdjCosine"')

os.system('python CF_NM_UserBased-4.py "2" "AdjCosine_Sij_UserBased-test2.csv" "Estimated-Ratings-AdjCosine-u2-test.csv" "AdjCosine"')

os.system('python CF_NM_UserBased-4.py "3" "AdjCosine_Sij_UserBased-test3.csv" "Estimated-Ratings-AdjCosine-u3-test.csv" "AdjCosine"')

os.system('python CF_NM_UserBased-4.py "4" "AdjCosine_Sij_UserBased-test4.csv" "Estimated-Ratings-AdjCosine-u4-test.csv" "AdjCosine"')

os.system('python CF_NM_UserBased-4.py "5" "AdjCosine_Sij_UserBased-test5.csv" "Estimated-Ratings-AdjCosine-u5-test.csv" "AdjCosine"')


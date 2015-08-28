
import csv
import json
import numpy as np

__author__ = 'franpena'


class ETLUtils:
    def __init__(self):
        pass

    @staticmethod
    def load_json_file(file_path):
        """
        Builds a list of dictionaries from a JSON file
        :type file_path: string
        :param file_path: the path for the file that contains the businesses
        data
        :return: a list of dictionaries with the data from the files
        """
        records = [json.loads(line) for line in open(file_path)]

        return records

    @staticmethod
    def save_json_file(file_path, records):
        with open(file_path, 'w') as outfile:
            for record in records:
                json.dump(record, outfile)
                outfile.write('\n')

    @staticmethod
    def drop_fields(fields, dictionary_list):
        """
        Removes the specified fields from every dictionary in the dictionary
        list
        :rtype : void
        :param fields: a list of     strings, which contains the fields that are
        going to be removed from every dictionary in the dictionary list
        :param dictionary_list: a list of dictionaries
        """
        for dictionary in dictionary_list:
            for field in fields:
                del (dictionary[field])

    @staticmethod
    def select_fields(fields, dictionary_list):
        """
        Returns a list of dictionaries with each dictionary containing only the
        keys given in the fields list
        :param fields: a list of the keys that each dictionary will have.
        This list must be a subset of all the keys available in each dictionary
        :param dictionary_list: a list of dictionaries
        :return: a list of dictionaries with each dictionary containing only the
        keys given in the fields list
        """
        filtered_records = [{field: dictionary[field] for field in fields} for
                            dictionary in dictionary_list]
        return filtered_records

    @staticmethod
    def filter_records(dictionary_list, field, values):
        """
        Returns a list with the dictionaries in dictionary_list that contain any
        of the values inside the field key. This method is the equivalent of
        SELECT * FROM my_table WHERE field IN (values) in SQL
        :param dictionary_list: a list of dictionaries
        :param field: the key of the dictionaries that is going to be used for
        filtering
        :param values: a list of values
        :return: a list with the dictionaries in dictionary_list that contain
        any of the values inside the field key
        """
        filtered_records = [dictionary for dictionary in dictionary_list if
                            dictionary[field] in values]
        return filtered_records

    @staticmethod
    def filter_out_records(dictionary_list, field, values):
        """
        Returns a list with the dictionaries in dictionary_list that do not
        contain any of the values inside the field key. This method is the
        equivalent of SELECT * FROM my_table WHERE field NOT IN (values) in SQL
        :param dictionary_list: a list of dictionaries
        :param field: the key of the dictionaries that is going to be used for
        filtering
        :param values: a list of values
        :return: a list with the dictionaries in dictionary_list that do not
        contain any of the values inside the field key
        """
        filtered_records = [dictionary for dictionary in dictionary_list if
                            dictionary[field] not in values]
        return filtered_records

    @staticmethod
    def add_transpose_list_column(field, dictionary_list):
        """
        Takes a list of dictionaries and adds to every dictionary a new field
        for each value contained in the specified field among all the
        dictionaries in the field, leaving 1 for the values that are present in
        the dictionary and 0 for the values that are not. It can be seen as
        transposing the dictionary matrix.
        :param field: the field which is going to be transposed
        :param dictionary_list: a list of dictionaries
        :return: the modified list of dictionaries
        """
        values_set = set()
        for dictionary in dictionary_list:
            values_set |= set(dictionary[field])

        for dictionary in dictionary_list:
            for value in values_set:
                if value in dictionary[field]:
                    dictionary[value] = 1
                else:
                    dictionary[value] = 0

        return dictionary_list

    @staticmethod
    def add_transpose_single_column(field, dictionary_list):
        """
        Takes a list of dictionaries and adds to every dictionary a new field
        for each value contained in the specified field among all the
        dictionaries in the field, leaving 1 for the values that are present in
        the dictionary and 0 for the values that are not. It can be seen as
        transposing the dictionary matrix.
        :param field: the field which is going to be transposed
        :param dictionary_list: a list of dictionaries
        :return: the modified list of dictionaries
        """

        values_set = set()
        for dictionary in dictionary_list:
            values_set.add(dictionary[field])

        for dictionary in dictionary_list:
            for value in values_set:
                if value in dictionary[field]:
                    dictionary[value] = 1
                else:
                    dictionary[value] = 0

        return dictionary_list


    @staticmethod
    def split_train_test(records, split=0.8, shuffle_data=True, start=0.):
        """
        Splits the data in two disjunct datasets: train and test
        :param split: % of training set to be used (test set size = 100-percent)
        :type split: float
        :param shuffle_data: shuffle dataset?
        :type shuffle_data: bool
        :returns: a tuple <Data, Data>
        """
        if shuffle_data:
            np.random.shuffle(records)
        length = len(records)
        split_start = split + start

        if start == 0:
            train = records[:int(round(split*length))]
            test = records[int(round(split*length)):]
        elif split_start > 1:
            train = records[int(round(start*length)):] + records[:int(round((split_start-1)*length))]
            test = records[int(round((split_start-1)*length)):int(round(start*length))]
        else:
            train = records[int(round(start*length)):int(round(split_start*length))]
            test = records[int(round(split_start*length)):] + records[:int(round(start*length))]

        return train, test

    @staticmethod
    def load_csv_file(file_path, delimiter=','):

        records = []

        with open(file_path) as read_file:
            reader = csv.DictReader(read_file, delimiter=delimiter)  # read rows into a dictionary format
            for row in reader:
                dictionary = {}
                for (key, value) in row.items(): # go over each column name and value
                    dictionary[key] = value
                records.append(dictionary)

        return records

    @staticmethod
    def save_csv_file(file_path, records, headers, delimiter=','):

        with open(file_path, 'wb') as write_file:
            writer = csv.DictWriter(write_file, headers, delimiter=delimiter)
            writer.writeheader()

            for record in records:
                writer.writerow(record)

#my_records = ETLUtils.load_csv_file('/Users/rohitdhamane/Work/Pycharm/Movielens100k.csv', '\t')

#item_id1 = '242'
#item_id2 = '302'
#my_user_records1 = ETLUtils.filter_records(my_records, 'item_id', [item_id1])
#my_user_records2 = ETLUtils.filter_records(my_records, 'item_id', [item_id2])

#print(my_records[0])
#print(my_records[1])



#for user_record in my_user_records1:
#    print(user_record['item_id'])

#user_items1 = [record['user_id'] for record in my_user_records1]
#user_items2 = [record['user_id'] for record in my_user_records2]

#my_set = set(user_items1)
#print(my_set.intersection(user_items2))

#print(ETLUtils.filter_records(my_user_records1, 'user_id', ['740']))
#print(ETLUtils.filter_records(my_user_records2, 'user_id', ['740']))



# headers = ['Algorithm',
#            # 'Multi-cluster',
#            # 'Similarity',
#            # 'Distance metric',
#            # 'Dataset',
#            # 'MAE	RMSE',
#            # 'Execution time',
#            # 'Cross validation',
#            'Machine']
# records = [
#     {'Algorithm': 'Clu_Overall', 'Machine': 'Mac'},
#     {'Algorithm': 'Clu_CF_Euc', 'Machine': 'Mac'},
#     {'Algorithm': 'Single_CF', 'Machine': 'PC'}
# ]
# ETLUtils.save_csv_file('/Users/fpena/tmp/test.csv', records, headers, delimiter='|')



from __future__ import division
import pandas as pd

def split_text_train(text_in_label):
    data = []
    data_dict ={'0': [], '1': []}
    vocabulary = 0
    PR = 0
    PnR = 0
    sumdata = 0

    for row in text_in_label:
        sumdata += 1

        if row[1] == 1:
            split = row[0].split()
            PR += 1

            for i in split:
                data.append(i)
                if i not in data_dict['1']:
                    vocabulary += 1
                data_dict['1'].append(i)

        if row[1] == 0:
            split = row[0].split()
            PnR += 1

            for i in split:
                data.append(i)
                if i not in data_dict['0']:
                    vocabulary += 1
                data_dict['0'].append(i)

    return data, data_dict, vocabulary, PR, PnR, sumdata


def count_class_freq(dictionary):
    data_dict_racism = {}
    data_dict_not_racism = {}

    for word in dictionary['1']:
        if word not in data_dict_racism:
            data_dict_racism[word] = 0

    for word in dictionary['0']:
        if word not in data_dict_not_racism:
            data_dict_not_racism[word] = 0

    return data_dict_racism, data_dict_not_racism


def training(dataset, test_data, data_dictionary, dict_racism_words, dict_not_racism_words, vocabulary, alpha = 1):
    prob_racism_words = {}
    prob_not_racism_words = {}
    racism_words = {}
    not_racism_words = {}
    num_of_word_in_racism = len(data_dictionary['1'])
    num_of_word_in_not_racism = len(data_dictionary['0'])

    for word in dataset:
        if word not in dict_racism_words:
            racism_words[word] = 0 #this line is used for adding the word to the set

        if word in dict_racism_words:
            if word in racism_words:
                racism_words[word] += 1 #increment the frequency
            if word not in racism_words:
                racism_words[word] = 0 #add new words to spam words

        if word not in dict_not_racism_words:
            not_racism_words[word] = 0 #this line is used for adding the words to the set

        if word in dict_not_racism_words:
            if word in not_racism_words:
                not_racism_words[word] += 1 #increment the frequency
            if word not in not_racism_words:
                not_racism_words[word] = 0 #this line is used for adding the words

    for word in test_data:

        if word not in dict_racism_words:
            racism_words[word] = 0

        if word not in dict_not_racism_words:
            not_racism_words[word] = 0

    for word in racism_words:
        prob_racism_words[word] = (racism_words[word] + alpha)/(num_of_word_in_racism + vocabulary)

    for word in not_racism_words:
        prob_not_racism_words[word] = (not_racism_words[word] + alpha)/(num_of_word_in_not_racism + vocabulary)

    return prob_racism_words, prob_not_racism_words


def predict(test_data, dict_prob_racism, dict_prob_not_racism, Pracism, Pnotracism, sumdata):
    probability_racism = []
    probability_not_racism = []
    prediction = []
    racism_meter = 1
    not_racism_meter = 1

    for word in test_data:
        if word in dict_prob_racism:
            probability_racism.append(dict_prob_racism[word])
        if word in dict_prob_not_racism:
            probability_not_racism.append(dict_prob_not_racism[word])
        else:
            probability_racism.append(dict_prob_racism[word])
            probability_not_racism.append(dict_prob_not_racism[word])

    for value in probability_racism:
        racism_meter *= value
    racism_meter = racism_meter * (Pracism/sumdata)

    # print('Spam meter:  %s' %(spam_meter))

    for value in probability_not_racism:
        not_racism_meter *= value
    not_racism_meter = not_racism_meter * (Pnotracism/sumdata)

    # print('Not Spam meter: %s' %(not_spam_meter))

    if racism_meter > not_racism_meter:
        prediction.append(1)
    if not_racism_meter > racism_meter:
        prediction.append(0)
    if racism_meter == not_racism_meter:
        prediction.append(None)

    prediction_val = max(racism_meter, not_racism_meter)

    return prediction, prediction_val, not_racism_meter, racism_meter


df = pd.read_csv('twitter_racism_parsed_dataset.csv', encoding='latin-1')
x = df.iloc[:, 0]
y = df.iloc[:, 1]

data = []
for i in range(len(df)):
    data.append([x[i], y[i]])

dataset, data_dictionary, vocab, Pracism, Pnotracism, sumdata = split_text_train(data)
dict_racism, dict_not_racism = count_class_freq(data_dictionary)


def execute_single_test():
    comment = input()
    # print(type(comment))
    test_data = comment.split()

    print(test_data)

    prob_racism, prob_not_racism = training(dataset, test_data, data_dictionary, dict_racism, dict_not_racism, vocab)
    pred, val, no_racism_meter, racism_meter = predict(test_data, prob_racism, prob_not_racism, Pracism, Pnotracism, sumdata)

    print(('\nPREDICTION:  %s \nprobability measure:  %s') %(pred, val))
    print(('\nRacism meter:  %s\nNot racism meter:  %s') %(racism_meter, no_racism_meter))
    if pred[0]==0:
      print("Your input is acceptable!")
    else:
      print("Your input is related to racism!")

    print(len(data_dictionary['1']), ':1   =    0:', len(data_dictionary['0']))
    # print(Pracism, Pnotracism, sumdata)
    # print(vocab)
    # print(len(dataset))
    # print(prob_not_racism)

execute_single_test()

from Code.info import *
import os
import numpy as np
import pandas as pd
import time


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("new folder")
    else:
        print("There is this folder")


def diff(listA, listB):
    retA = [i for i in listA if i in listB]
    return retA


def CHA(listA, listB):
    retD = list(set(listB).difference(set(listA)))
    return retD


def BING(listA, listB):
    retC = list(set(listA).union(set(listB)))
    return retC


def csvtodata(casename):
    csv_path = './inputData/AML/' + casename + "/all-normal-tx.csv"
    raw_data = pd.read_csv(csv_path)
    dict_from = {}
    dict_to = {}
    relation = []
    count_from = 0
    count_to = 0
    print('Read transactions complete\n')
    datasetoverview(casename)
    print('Building index-address mapping')
    for idx, data in raw_data.iterrows():
        if data['value'] == 0.0:
            continue
        getFrom = data['from']
        getTo = data['to']
        if not getFrom in dict_from:
            dict_from[getFrom] = count_from
            count_from += 1
        if not getTo in dict_to:
            dict_to[getTo] = count_to
            count_to += 1
        relation.append([dict_from[getFrom], dict_to[getTo]])
    print('Index-address mapping complete')
    relation.sort()
    relation_new = []
    relation_new.append(relation[0])
    new_count = 1
    for i in relation:
        if i != relation_new[new_count - 1]:
            relation_new.append(i)
            new_count += 1

    relation_count = pd.value_counts(relation)
    print('Storing address mapping files...\n')
    new_dict_from = dict(zip(dict_from.values(), dict_from.keys()))
    from_keys = new_dict_from.keys()
    sorted(from_keys)
    new_dict_from_sort = [(key, new_dict_from[key]) for key in from_keys]
    mkdir('data/' + casename + "/")
    dict_from_path = './inputData/AML/data/' + casename + '/all-normal-tx_from.txt'
    with open(dict_from_path, 'w') as f:
        f.write(str(new_dict_from_sort))

    new_dict_to = dict(zip(dict_to.values(), dict_to.keys()))
    to_keys = new_dict_to.keys()
    sorted(to_keys)
    new_dict_to_sort = [(key, new_dict_to[key]) for key in to_keys]
    dict_to_path = './inputData/AML/data/' + casename + '/all-normal-tx_to.txt'
    with open(dict_to_path, 'w') as f:
        f.write(str(new_dict_to_sort))

    edgef = []
    edget = []
    edgenum = []
    for d, v in relation_count.items():
        edgef.append(d[0])
        edget.append(d[1])
        edgenum.append(v)

    txtname = './inputData/AML/data/' + casename + '/all-normal-tx' + 'count.txt'
    with open(txtname, 'w') as f:
        for i in relation:
            f.write(str(i[0]) + ' ' + str(i[1]) + '\n')


def myReadData(path):
    f = open(path, 'r')
    a = f.read()
    data = eval(a)
    f.close()
    return data


def num_to_addr(casename):
    path = './inputData/AML/data/' + casename + '/all-normal-tx_from.txt'
    dict_from = myReadData(path)
    path = './inputData/AML/data/' + casename + '/all-normal-tx_to.txt'
    dict_to = myReadData(path)
    return dict_from, dict_to


def addr_to_num(csvname):
    dict_from, dict_to = num_to_addr(csvname)
    dict_from = np.array(dict_from)
    dict_to = np.array(dict_to)
    new_dict_from = dict(zip(dict_from[:, 1], dict_from[:, 0]))
    new_dict_to = dict(zip(dict_to[:, 1], dict_to[:, 0]))
    return new_dict_from, new_dict_to


def saveaddr(csvname, ifrows, data):
    dict_from, dict_to = num_to_addr(csvname)
    path = 'out/' + csvname + '_result'
    if ifrows:
        path = path + '_rows.txt'
        f = open(path, 'w')
        for i in data:
            f.write(str(dict_from[i]) + '\n')
        f.close()
    else:
        path = path + '_cols.txt'
        f = open(path, 'w')
        for i in data:
            f.write(str(dict_to[i]) + '\n')
        f.close()


def datasetoverview(casename):
    csv_path = './inputData/AML/' + casename + '/all-normal-tx.csv'
    raw_data = pd.read_csv(csv_path)
    raw_data[['value']] = raw_data[['value']].astype(float)
    raw_data[['timeStamp']] = raw_data[['timeStamp']].astype(int)
    heist = pd.read_csv('./inputData/AML/' + casename + '/accounts-hacker.csv')
    heist = heist[heist['label'] == 'heist']['address'].tolist()
    account_from = raw_data['from'].tolist()
    account_to = raw_data['to'].tolist()
    account_total = BING(account_from, account_to)
    tol_value = float(raw_data['value'].sum()) * 1e-18
    tmx = max(raw_data['timeStamp'])
    tmn = min(raw_data['timeStamp'])
    tres = (tmx - tmn) / (60 * 60 * 24)
    timeArray = time.localtime(tmx)
    tmx = time.strftime("%Y.%m.%d", timeArray)
    timeArray = time.localtime(tmn)
    tmn = time.strftime("%Y.%m.%d", timeArray)
    print(casename, 'Dataset overview:\n  Total accounts:', len(account_total),
          '\n  Total transactions:', len(raw_data),
          '\n  Total heist addresses:', len(heist),
          '\n  Total value (ETH):', tol_value,
          '\n  Time span:', tmn, '-', tmx, ', duration', tres, '(days)')

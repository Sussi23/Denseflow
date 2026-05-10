import os
import pandas as pd
from Code.info import *


def check_metrics_my(casename, level=1, k=10):
    """
    Evaluate DenseFlow (HoloScope + MaxFlow) results.

    Returns a dict with key 'HOLO+MAXFLOW' mapping to [precision, mcr, |M|]
    where:
      precision  = fraction of detected addresses that are true heist accounts
      mcr        = money coverage rate (fraction of illicit transaction value covered)
      |M|        = size of the suspicious account set M detected by the model
    """
    METRICS = {}

    label_file = f'./inputData/AML/{casename}/accounts-hacker.csv'
    if not os.path.exists(label_file):
        print(casename, "! Error: missing label file")
        return METRICS

    address = pd.read_csv(label_file)
    heist = address.loc[address['label'] == 'heist']
    heist_address = heist['address'].tolist()

    out_path = './Result/' + casename + "_out/"
    myfile = casename + '_k_' + str(k) + '_level_' + str(level) + '.xlsx'
    file_path = out_path + myfile

    if not os.path.exists(file_path):
        print(f"Missing result file: {file_path}")
        return METRICS

    result = pd.read_excel(file_path, sheet_name='Sheet3')
    result = result['all_heist'].tolist()

    correct = [fh for fh in result if fh in heist_address]
    pre = len(correct) / len(result) if len(result) != 0 else -1
    rec = len(correct) / len(heist_address)

    method = 'HOLO+MAXFLOW'
    print(f"\n{method}  (level={level}, k={k})")
    print(f"  |M| (detected):     {len(result)}")
    print(f"  Correct heist:      {len(correct)}")
    print(f"  Precision:          {pre:.4f}")
    print(f"  Recall:             {rec:.4f}")

    csv_path = './inputData/AML/' + casename + '/all-normal-tx.csv'
    raw_data = pd.read_csv(csv_path)
    raw_data[['value']] = raw_data[['value']].astype(float)
    raw_data[['timeStamp']] = raw_data[['timeStamp']].astype(int)

    account = list(set(raw_data['from'].tolist() + raw_data['to'].tolist()))
    fromisheist = raw_data[raw_data['from'].isin(result)]
    fromisheisttrue = raw_data[raw_data['from'].isin(heist_address)]

    m1 = fromisheist['value'].sum() * 1e-18
    m2 = fromisheisttrue['value'].sum() * 1e-18
    mcr = min(m1 / m2, 1.0) if m2 != 0 else 0.0

    print(f"  Traced value (ETH): {m1:.4f}")
    print(f"  True illicit (ETH): {m2:.4f}")
    print(f"  MCR:                {mcr:.4f}")
    print(f"  Total accounts:     {len(account)}")

    METRICS[method] = [pre, mcr, len(result)]
    return METRICS

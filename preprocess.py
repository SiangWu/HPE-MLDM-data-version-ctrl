import argparse
import pickle
import os
import pandas as pd
from talib import abstract

def preprocess():
    '''
    使用 TA-Lib 套件來計算技術指標 KD、MACD、RSI、布林通道、ATR，作為特徵
    TA-Lib GitHub: https://ta-lib.org
    '''
    for dirpath, _, files in os.walk('/pfs/raw/'):
        n_total = len(files)
        current = 0
        print(f"Current path: {os.path.abspath('.')}, {n_total} files found.")
        
        for file in files:
            file_path = os.path.join(
                dirpath, 
                file
            )
            current += 1

            if not file_path.lower().endswith(('.csv')):  # Not a CSV file, skip
                print(f'Skipping {file_path}: Not a CSV file.')
            
            else:  # CSV file
                print(f'Processing {file_path} ({current}/{n_total})...')
                df = pd.read_csv(
                    file_path,
                    header=0
                )
                df.columns = [col.lower() for col in df.columns]  # Make all column headers lower case
                
                # KD
                df.loc[:, ['slowk', 'slowd']] = abstract.STOCH(
                    df
                )
                # MACD
                df.loc[:, ['macd']] = abstract.MACD(
                    df, 
                    fastperiod=12, 
                    slowperiod=26, 
                    signalperiod=9
                )
                # RSI
                df.loc[:, ['rsi']] = abstract.RSI(
                    df, 
                    14
                )
                # Bollinger band
                df.loc[:, ['bollinger_band']] = abstract.BBANDS(
                    df, 
                    timeperiod=20, 
                    nbdevup=2.0, 
                    nbdevdn=2.0, 
                    matype=0
                )
                # ATR
                df.loc[:, ['atr']] = abstract.ATR(
                    df
                )
                
                df.to_csv(
                    f'/pfs/out/{file}_processed.csv',
                    index=False
                )
                print(f'/pfs/out/{file}_processed.csv saved.')


def main():
    preprocess()


if __name__ == '__main__':
    main()

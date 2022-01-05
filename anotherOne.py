import pandas as pd
# используется для файлов
import os
'''
[[] [] [] [] ]
df = pd.DataFrame([[1,'Bob', 8000],
                  [2,'Sally', 9000],
                  [3,'Scott', 20]], columns=['id','name', 'power level'])

df.to_csv('datasets/test_ds.csv')
'''
directory = 'datasets/Train_3500/Train_3500/3 класса/прочие звери/'
files = os.listdir(directory)
firs_box = [0]*len(files)
second_box = ['another'] *len(files)

df = pd.DataFrame(files, columns=['filename'])
df["width"] = firs_box
df["height"] = firs_box
df["types"] = second_box
df["Xmin"] = firs_box
df["Ymin"] = firs_box
df["Xmax"] = firs_box
df["Ymax"] = firs_box

df.to_csv('datasets/test_ds.csv', index=False)
df = pd.read_csv('datasets/test_ds.csv')
print(df)
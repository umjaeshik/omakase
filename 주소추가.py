import pandas as pd
import glob



data_paths = glob.glob('./*sum.csv')
df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df = pd.concat([df, df_temp])
    print(path)
if not df.empty:
    # Check if 'keyword' column is present in the DataFrame
    if 'keyword' in df.columns:
        print(df['keyword'].value_counts())
    else:
        print("Column 'keyword' not found in the DataFrame.")

    df.info()

    df.drop_duplicates(subset='names',inplace=True)

    df.info()
    df.to_csv('./음식점_sum.csv',index=False)
    print('con저장하고난후')
else:
    print("DataFrame is empty. No CSV file generated.")
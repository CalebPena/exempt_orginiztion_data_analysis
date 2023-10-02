import pandas as pd
import glob
from all_codes import all_codes

all_files = glob.glob("data/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)


def get_by_code(df, code):
    return df[df['NTEE_CD'] == code]


def print_code(df, code):
    amount = len(get_by_code(df, code))
    print(f'{code}: {amount}')


# prepped_data = []
# for code in all_codes:
#     row = [code]
#     row.append(len(get_by_code(df, code)))
#     row.append(len(get_by_code(df[df['STATE'] == 'CO'], code)))
#     prepped_data.append(row)
# by_code_df = pd.DataFrame(prepped_data, columns=('Code', 'National', 'Colorado'))
# by_code_df.to_csv('out_data/amount_with_code.csv')

# print(df['ACTIVITY'])
# print(df['NTEE_CD'])
# print('total', len(df))

# ntee_null = pd.isnull(df['NTEE_CD'])
# activity_null = df['ACTIVITY'] == 0
# print('missing both', len(df[ntee_null & activity_null]))
# print('missing ntee', len(df[ntee_null]))
# print('missing activity', len(df[activity_null]))

# print('both', len(df[pd.notnull(df['NTEE_CD']) & df['ACTIVITY'] > 0]))
# print('ntee', len(df[pd.notnull(df['NTEE_CD'])]))
# print('activity', len(df[df['ACTIVITY'] > 0]))
# print_code(df, 'J20')
# print_code(df, 'J21')
# print_code(df, 'J22')
# print_code(df, 'J30')
# print_code(df, 'J32')
# print_code(df, 'J33')
# print_code(df, 'J99')

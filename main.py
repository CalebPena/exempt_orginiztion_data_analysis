import pandas as pd
import glob
from all_codes import all_codes

# Get all files in the data directory
# Data is CSV files from:
# https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf

# Data documentation is available here:
# https://www.irs.gov/pub/irs-soi/eo_info.pdf

all_files = glob.glob("data/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, converters={'ACTIVITY': lambda a: str(a)})
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)


def get_by_code(df, code):
    return df[df['NTEE_CD'] == code]


all_budget_codes = tuple(range(0, 10))


# Split activity codes into 3 columns
activity_name = ['ACTIVITY_1', 'ACTIVITY_2', 'ACTIVITY_3']
df[activity_name] = df['ACTIVITY'].str.extract('(...)(...)(...)', expand=True)

# Get the number of each activity code and write it to a CSV file
codes = ('150', '154', '566', '568', '569')
activity_sum = []
for code in codes:
    row = [code]
    n_df = df[
        (df['ACTIVITY_1'] == code) |
        (df['ACTIVITY_2'] == code) |
        (df['ACTIVITY_3'] == code)
    ]
    state_series = n_df['STATE'] == 'CO'
    s_df = n_df[state_series]
    row.append(len(n_df))
    row.append(len(s_df))

    for b_code in all_budget_codes:
        row.append(len(n_df[n_df['INCOME_CD'] == b_code]))

    for b_code in all_budget_codes:
        row.append(len(s_df[s_df['INCOME_CD'] == b_code]))

    activity_sum.append(row)

columns = ['Code', 'National', 'Colorado']
columns += ['National Budget ' + str(code) for code in all_budget_codes]
columns += ['State Budget ' + str(code) for code in all_budget_codes]
pd.DataFrame(activity_sum, columns=columns).to_csv('out_data/amount_with_activity_code.csv')

# Write the number of each NTEE code to a CSV file
prepped_data = []
for code in all_codes:
    row = [code]
    n_code_df = get_by_code(df, code)
    s_code_df = get_by_code(df[df['STATE'] == 'CO'], code)
    row.append(len(n_code_df))
    row.append(len(s_code_df))
    for b_code in all_budget_codes:
        row.append(len(n_code_df[n_code_df['INCOME_CD'] == b_code]))

    for b_code in all_budget_codes:
        row.append(len(s_code_df[s_code_df['INCOME_CD'] == b_code]))
    prepped_data.append(row)

columns = ['Code', 'National', 'Colorado']
columns += ['National Budget ' + str(code) for code in all_budget_codes]
columns += ['State Budget ' + str(code) for code in all_budget_codes]
by_code_df = pd.DataFrame(prepped_data, columns=columns)
by_code_df.to_csv('out_data/amount_with_ntee_code.csv')

# Data frame for Colorado
s_df = df[df['STATE'] == 'CO']

# Write the exempt businesses with NTEE code to a CSV file
c_df = s_df[s_df['NTEE_CD'].isin(all_codes)]
c_df.to_csv('out_data/all_ntee_code_co.csv')

# Write the exempt businesses with activity code to a CSV file
a_df = s_df[
    s_df['ACTIVITY_1'].isin(codes) |
    s_df['ACTIVITY_2'].isin(codes) |
    s_df['ACTIVITY_3'].isin(codes)
]
a_df.to_csv('out_data/all_activity_code_co.csv')

# Write businesses with specific NTEE codes nationally to a file
specific_codes = (
    'B30',
    'J20',
    'J21',
    'J22',
    'J30',
    'J32',
    'J33',
    'J99',
    'P20',
    'P51',
)
df[df['NTEE_CD'].isin(specific_codes)].to_csv('out_data/specific_ntee_national.csv')

import pandas as pd
df = pd.DataFrame(columns=['标识符', '机型', '始发地', '出发', '到达'])
print(df.shape)
df.loc[df.shape[0] + 1] = [1,2,3,4,5]
print(df)
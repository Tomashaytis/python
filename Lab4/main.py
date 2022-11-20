import pandas as pd

if __name__ == "__main__":
    instance_df = pd.read_csv('annotation.csv')
    instance_df.drop(['relative path'], axis=1, inplace=True)
    instance_df = instance_df.rename(columns={'absolute path': 'absolute_path', 'class': 'class_mark'})
    mask = (instance_df.class_mark == 'leopard')
    instance_df['numerical_class_mark'] = mask.astype(int)
    print(instance_df)

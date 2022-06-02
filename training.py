import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class TrainMethods:
    def __init__(self, data: pd.DataFrame,
                 method: str,
                 column: str):
        self.data = data
        self.method = method
        self.column = column

    def regression(self):
        from sklearn import linear_model
        df = self.data.dropna()
        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]
        regr = linear_model.LinearRegression()
        x = np.asanyarray(train[self.training_columns()])
        y = np.asanyarray(train[[self.column]])
        regr.fit(x, y)
        print('Coefficients: ', regr.coef_)
        x = np.asanyarray(test[self.training_columns()])
        y = np.asanyarray(test[[self.column]])
        print('Variance score: %.2f' % regr.score(x, y))
        return regr.score(x, y)

    def call_method(self):
        methods = {'regression': self.regression()}
        return methods[self.method]

    def training_columns(self):
        trainers = self.data.columns.tolist()
        trainers.remove(self.column)
        return trainers


if __name__ == '__main__':
    kline = pd.read_csv('./data/2h_31 Jan, 2021_7 Feb, 2022.csv', index_col='Date')

    print(kline.columns.tolist())
    trainer = TrainMethods(kline, 'regression', 'Close')
    print(trainer.call_method())
    print(trainer.training_columns())

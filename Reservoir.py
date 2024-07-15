import csv
import time
import requests
import json


class ReservoirAPI():
    def __init__(self, url, token):
        self.URL = url
        self.Token = token
        self.header = {"accept": "*/*", "x-api-key": token}
        self.collection_specification = None

    def get_info_ntfs(self):
        self.collection_specification = []
        url = self.URL + "collections/v7"
        response = requests.get(url, headers=self.header)
        result = json.loads(response.text)['collections']
        print(f"Collection Count :  {len(result)}")

        for item in result:
            record = dict(
                ChainID=item['chainId'],
                ID=item['id'],
                Name=item['name'],
                Symbol=item['symbol'],
                TokenCount=item['tokenCount']
            )
            self.collection_specification.append(record)

    def data_gathering_nfts(self):
        self.get_info_ntfs()
        for item in self.collection_specification:
            url = self.URL + f"collections/daily-volumes/v1?id={item['ID']}&limit=2000"
            response = requests.get(url, headers=self.header)
            result = json.loads(response.text)['collections']
            name = item['Name']
            self.save_data_csv(name, result)

        print('End Gathering')

    def save_data_csv(self, filename, data):
        print(f"Create Filename (CSV) : {filename} \n \t Row Count By Price and Volume : {len(data)} \n -------------")
        with open(f'Data/{filename}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["date", "price", "volume"]
            writer.writerow(field)
            for volume in data:
                struct_time = time.localtime(int(volume['timestamp']))
                date = time.strftime("%Y-%m-%d", struct_time)
                writer.writerow([date, volume['floor_sell_value'], volume['volume']])
        self.Analyses_data(f'Data/{filename}.csv')

    def Analyses_data(self, filename):
        import pandas as pd
        import numpy as np
        from sklearn.preprocessing import MinMaxScaler
        from keras.api.models import Sequential
        from keras.api.layers import LSTM, Dense
        import matplotlib.pyplot as plt

        # Load historical NFT price data
        data = pd.read_csv(filename)
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)

        # Prepare data for LSTM
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['price'].values.reshape(-1, 1))

        # Split data into training and testing sets
        train_size = int(len(scaled_data) * 0.8)
        train_data = scaled_data[:train_size]
        test_data = scaled_data[train_size:]

        def create_dataset(data, time_step=1):
            X, y = [], []
            for i in range(len(data) - time_step - 1):
                X.append(data[i:(i + time_step), 0])
                y.append(data[i + time_step, 0])
            return np.array(X), np.array(y)

        time_step = 5
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, y_test = create_dataset(test_data, time_step)

        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        # Build LSTM model
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(X_train, y_train, batch_size=1, epochs=10)

        # Make predictions
        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)

        # Inverse transform predictions
        train_predict = scaler.inverse_transform(train_predict)
        test_predict = scaler.inverse_transform(test_predict)
        y_train = scaler.inverse_transform([y_train])
        y_test = scaler.inverse_transform([y_test])

        # Plot the results
        plt.figure(figsize=(14, 8))
        plt.plot(data.index, data['price'], label='Original Data')
        train_plot = np.empty_like(data['price'])
        train_plot[:] = np.nan
        train_plot[time_step:len(train_predict) + time_step] = train_predict.flatten()
        plt.plot(data.index, train_plot, label='Training Predictions')

        test_plot = np.empty_like(data['price'])
        test_plot[:] = np.nan
        test_plot[len(train_predict) + (time_step * 2) + 1:len(data) - 1] = test_predict.flatten()
        plt.plot(data.index, test_plot, label='Test Predictions')

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    api = ReservoirAPI("https://api.reservoir.tools/", "eadfb758-7639-51a3-8c9e-58a3af40cfbe")
    api.data_gathering_nfts()

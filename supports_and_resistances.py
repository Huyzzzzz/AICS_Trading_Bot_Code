import pandas as pd
import plotly.graph_objs as go 
import numpy as np


def supports_and_resistances(dataframe, rollsize, field_for_support='low', field_for_resistance='high'): 
    # B1.Tính toán mức biến động của 2 hàng liên tiếp bắt đầu từ hàng 1. Lấy trị tuyệt đối của hiêu(hàng 1- hàng 0;hàng 2 - hàng 1; ...)
    diffs1 = abs(dataframe['high'].diff().abs().iloc[1:]) 
    diffs2 = abs(dataframe['low'].diff().abs().iloc[1:]) 

    # B2.Tính trung bình của các mức biến động trên. Cộng tất cả lại chia trung bình (riêng support và resistance)
    mean_deviation_resistance = diffs1.mean() 
    mean_deviation_support = diffs2.mean() 

    #B3.Tìm giá trị support và resistance
    supports = dataframe[dataframe.low == dataframe[field_for_support].rolling(rollsize, center=True).min()].low 
    resistances = dataframe[dataframe.high == dataframe[field_for_resistance].rolling(rollsize, center=True).max()].high 

    #B4.Lọc (Chỉ giữ lại các giá trị support khi trị tuyệt đối của (hiệu giá trị đang xét trừ  giá trị liền trước) lớn hơn trung bình biến động)
    supports = supports[abs(supports.diff()) > mean_deviation_support] 
    resistances = resistances[abs(resistances.diff()) > mean_deviation_resistance] 
    return supports,resistances 


if __name__ == "__main__":
    # READ DATA
    df = pd.read_csv(r"C:\Users\ThinkPadT450s\Documents\data\ADA_4h.csv") 
    supports, resistances = supports_and_resistances(df, 11, field_for_support='low', field_for_resistance='high')
    df['Support'] = None
    df.loc[supports.index, "Support"] = supports.values
    df['Resistance'] = None
    df.loc[resistances.index, "Resistance"] = resistances.values

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                        open=df['open'],
                                        high=df['high'],
                                        close=df['close'],
                                        low=df['low'])])

    number_candles_to_draw = 15

    for i in range(len(df)):
        if (df['Support'][i] != None):
            fig.add_trace(go.Scatter(
                x=np.arange(i + 1 - number_candles_to_draw, i + number_candles_to_draw, 1),
                y=np.full([1, number_candles_to_draw * 2], df['Support'][i])[0],
                marker=dict(color='green', size=7),
                mode='lines',
                name='Support',
            ))

    for i in range(len(df)):
        if (df['Resistance'][i] != None):
            fig.add_trace(go.Scatter(
                x=np.arange(i + 1 - number_candles_to_draw, i + number_candles_to_draw, 1),
                y=np.full([1, number_candles_to_draw * 2], df['Resistance'][i])[0],
                marker=dict(color='red', size=7),
                mode='lines',
                name='Resistance',
            ))

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()

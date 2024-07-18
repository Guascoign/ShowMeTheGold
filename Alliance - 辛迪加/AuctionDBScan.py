import plotly.graph_objs as go
import plotly.offline as py

# 假设这是你准备好的数据，格式为时间序列
time_series_data = {
    'timestamps': ['2024-07-17 18:55', '2024-07-17 18:56', '2024-07-17 18:57'],
    'item_id': [14484, 14971, 8113],
    'lowest_price': [200, 300, 500]
    # 添加更多的价格数据和时间戳
}

# 创建每个物品的价格曲线
traces = []
for item_id in time_series_data['item_id']:
    item_data = time_series_data['lowest_price']
    item_timestamps = time_series_data['timestamps']
    item_trace = go.Scatter(
        x=item_timestamps,
        y=item_data,
        mode='lines+markers',
        name=f'Item {item_id}'
    )
    traces.append(item_trace)

# 设置图表布局
layout = go.Layout(
    title='物品价格曲线',
    xaxis=dict(title='时间'),
    yaxis=dict(title='价格')
)

# 创建并显示图表
fig = go.Figure(data=traces, layout=layout)
py.plot(fig, filename='item_price_curve.html')

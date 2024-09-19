import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# File paths
csv_files = [
    '/home/codeplay/PycharmProjects/tradebook_analysis/data/2022-tradebook-CLH027-EQ.csv',
    '/home/codeplay/PycharmProjects/tradebook_analysis/data/2023-tradebook-CLH027-EQ.csv',
    '/home/codeplay/PycharmProjects/tradebook_analysis/data/2024-tradebook-CLH027-EQ.csv'
]

# Read and concatenate CSV files
df_list = [pd.read_csv(file) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Convert trade_date to datetime
df['trade_date'] = pd.to_datetime(df['trade_date'])

# Filter buy and sell trades
buy_trades = df[df['trade_type'] == 'buy']
sell_trades = df[df['trade_type'] == 'sell']

# Create scatter plots for buy and sell trades
fig = go.Figure()

# Add buy trades
fig.add_trace(go.Scatter(
    x=buy_trades['trade_date'],
    y=buy_trades['price'],
    mode='markers',
    marker=dict(color='green'),
    name='Buy Trades'
))

# Add sell trades
fig.add_trace(go.Scatter(
    x=sell_trades['trade_date'],
    y=sell_trades['price'],
    mode='markers',
    marker=dict(color='red'),
    name='Sell Trades'
))

# Add dropdown menu for symbol selection
symbols = df['symbol'].unique()
dropdown_buttons = [
    {'label': 'All', 'method': 'update', 'args': [{'visible': [True, True]}, {'title': 'Trade Prices Over Time'}]}
]

for symbol in symbols:
    visible = [False, False]
    visible[0] = buy_trades['symbol'] == symbol
    visible[1] = sell_trades['symbol'] == symbol
    dropdown_buttons.append(
        {'label': symbol, 'method': 'update', 'args': [
            {'visible': visible},
            {'title': f'Trade Prices Over Time - {symbol}'}
        ]}
    )

fig.update_layout(
    title='Trade Prices Over Time',
    xaxis_title='Trade Date',
    yaxis_title='Price',
    legend_title='Trade Type',
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'down',
        'showactive': True,
    }]
)

# Show the plot
fig.show()
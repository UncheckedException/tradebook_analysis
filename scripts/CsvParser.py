import pandas as pd
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

# Create figure
fig = go.Figure()

# Add scatter plots for each stock symbol
symbols = df['symbol'].unique()
for symbol in symbols:
    # Filter buy and sell trades for each symbol
    buy_trades = df[(df['trade_type'] == 'buy') & (df['symbol'] == symbol)]
    sell_trades = df[(df['trade_type'] == 'sell') & (df['symbol'] == symbol)]

    # Add buy trades
    fig.add_trace(go.Scatter(
        x=buy_trades['trade_date'],
        y=buy_trades['price'],
        mode='markers',
        marker=dict(color='green', size=10, symbol='circle'),
        name=f'{symbol} - Buy',
        visible=True if symbol == symbols[0] else False,  # Initially show the first symbol's data
        hovertemplate=(
                '<b>Symbol:</b> %{text}<br>' +
                '<b>Trade Type:</b> Buy<br>' +
                '<b>Price:</b> %{y}<br>' +
                '<b>Quantity:</b> %{customdata[0]}<br>' +
                '<b>Date:</b> %{x}<br>' +
                '<extra></extra>'
        ),
        text=[symbol] * len(buy_trades),
        customdata=buy_trades[['quantity']]
    ))

    # Add sell trades
    fig.add_trace(go.Scatter(
        x=sell_trades['trade_date'],
        y=sell_trades['price'],
        mode='markers',
        marker=dict(color='red', size=10, symbol='x'),
        name=f'{symbol} - Sell',
        visible=True if symbol == symbols[0] else False,  # Initially show the first symbol's data
        hovertemplate=(
                '<b>Symbol:</b> %{text}<br>' +
                '<b>Trade Type:</b> Sell<br>' +
                '<b>Price:</b> %{y}<br>' +
                '<b>Quantity:</b> %{customdata[0]}<br>' +
                '<b>Date:</b> %{x}<br>' +
                '<extra></extra>'
        ),
        text=[symbol] * len(sell_trades),
        customdata=sell_trades[['quantity']]
    ))

# Add dropdown menu for symbol selection including "All" option
dropdown_buttons = [
    {'label': 'All', 'method': 'update', 'args': [
        {'visible': [True if trace['name'].endswith('Buy') or trace['name'].endswith('Sell') else False for trace in
                     fig.data]},
        {'title': 'Trade Prices Over Time - All Symbols'}
    ]}
]

for i, symbol in enumerate(symbols):
    visibility = [False] * len(fig.data)
    visibility[2 * i] = True  # Buy trades for this symbol
    visibility[2 * i + 1] = True  # Sell trades for this symbol

    dropdown_buttons.append(
        {'label': symbol, 'method': 'update', 'args': [
            {'visible': visibility},
            {'title': f'Trade Prices Over Time - {symbol}'}
        ]}
    )

# Add an empty trace for profit/loss line
fig.add_trace(go.Scatter(
    x=[],
    y=[],
    mode='lines+markers+text',
    line=dict(color='blue', dash='dash'),
    marker=dict(size=8, color='blue'),
    name='Profit/Loss %',
    text=[],  # Text labels for profit/loss percentage
    visible=False  # Start with this trace hidden
))

# Add callbacks for interaction to draw the line
# This is an example; in a real app, callbacks need to be handled in a web framework like Dash

fig.update_layout(
    title='Trade Prices Over Time',
    xaxis_title='Trade Date',
    yaxis_title='Price',
    legend_title='Trade Type',
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'down',
        'showactive': True,
    }],
    hovermode='x unified'
)


# Function to calculate profit/loss between selected points
def calculate_profit_loss_percentage(buy_price, sell_price):
    return ((sell_price - buy_price) / buy_price) * 100


# Add custom interactivity
# In actual implementation, you'd use a more interactive tool like Dash to handle click events and dynamically update this line
selected_buy_price = None
selected_sell_price = None
selected_dates = []

# Placeholder logic for clicking events (requires web framework for actual usage)
# Update `selected_buy_price` and `selected_sell_price` based on user clicks, and calculate profit/loss

# Show the plot
fig.show()

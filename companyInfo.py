import yfinance as yf

stock = yf.Ticker("AAL")

# get stock info
stock.info

print(stock)
print(stock.info.floatShares)
print(stock.info.shortPercentOfFloat)

# get historical market data
hist = stock.history(period="max")

# show actions (dividends, splits)
stock.actions

# show dividends
stock.dividends

# show splits
stock.splits

# show financials
stock.financials
stock.quarterly_financials

# show major holders
stock.major_holders

# show institutional holders
stock.institutional_holders

# show balance sheet
stock.balance_sheet
stock.quarterly_balance_sheet

# show cashflow
stock.cashflow
stock.quarterly_cashflow

# show earnings
stock.earnings
stock.quarterly_earnings

# show sustainability
stock.sustainability

# show analysts recommendations
stock.recommendations

# show next event (earnings, etc)
stock.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
stock.isin

# show options expirations
stock.options

# show news
stock.news

# get option chain for specific expiration
opt = stock.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts

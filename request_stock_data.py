import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time

def fetch_stock_data(ticker, sma=False, ema=False):
	api_key = 'FP2YNP4PVWVSKZ4J'
	ts = TimeSeries(key=api_key, output_format='pandas')
	ts_data, ti_meta_data = ts.get_daily(symbol=ticker, outputsize='full')

	output_df = ts_data

	if sma or rsi or ema:
		
		ti = TechIndicators(key=api_key, output_format='pandas')
		
		if sma:
			sma_data, sma_meta_data = ti.get_sma(symbol=ticker,
												 interval='daily',
												 time_period=180,
												 series_type='open')
			output_df = pd.merge(output_df,
								 sma_data,
								 left_index=True,
								 right_index=True)
		
		if ema:
			ema_data, ema_meta_data = ti.get_ema(symbol=ticker,
												 interval='daily',
												 time_period=20,
												 series_type='open')
			output_df = pd.merge(output_df,
								 ema_data,
								 left_index=True,
								 right_index=True)

	print(output_df.head())
	return output_df

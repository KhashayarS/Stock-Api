from django.shortcuts import render, redirect
import requests
import json
from django.contrib import messages

from .models import Stock
from .forms import StockForm

# API Data
token_lim = 'pk_c310bac998dd43cb8d05ce8ffdcb682c'
token_gen = 'Tsk_56d4843ca59440b8b992730b11fe175e'

# Link for multiple quotes with connecting to api just once (example):
#https://sandbox.iexapis.com/stable/stock/market/batch?symbols=aapl,fb&types=quote&token=Tsk_56d4843ca59440b8b992730b11fe175e


# Create your views here.
def home(request):
	if request.method == 'POST':
		ticker = request.POST['ticker']
		page_title = 'Home | {}'.format(ticker)
		api_url = 'https://cloud.iexapis.com/stable/stock/{}/quote?token={}'.format(ticker, token_lim)
		# print('URL:', api_url)
		api_response = requests.get(api_url)

		try:
			ticker = api_response.json()

		except Exception as e:
			print(e)
			ticker = "Error..."


		return render(request, 'home.html', {
				'page_title': page_title,
				'ticker': ticker

			})
			


	else:
		page_title = 'Home'
		return render(request, 'home.html', {
				'page_title': page_title,
			})


def about(request):
	page_title = 'About Me'
	return render(request, 'about.html', {
			'page_title': page_title,
		})


def add_stock(request):
	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			stock_name = request.POST['ticker']

			messages.success(request, '"{}" Has Been Added To Portfolio Successfully'.format(stock_name))
			return redirect('add_stock')

		else:
			messages.error(request, 'An Error Happened, Please Try Again!')
			return redirect('add_stock')

	else:
		page_title = 'Add Stocks'
		all_stocks = Stock.objects.all()
		all_stocks_list = [item.ticker for item in all_stocks]
		# print(all_stocks_list)
		all_tickers_url ='https://sandbox.iexapis.com/stable/stock/market/batch?symbols={}&types=quote&token={}'.format(all_stocks_list, token_gen)
		api_respone = requests.get(all_tickers_url)
		try:
			ticker = json.loads(api_respone.content)
		except Exception as e:
			print(e)
			ticker = 'Error...'

		# print('THIS IS THE URL ============>', all_tickers_url)
		return render(request, 'add_stock.html', {
				'page_title': page_title,
				'all_stocks': all_stocks,
				'ticker': ticker,
			})


def delete(request, stock_id):
	stock = Stock.objects.get(pk=stock_id)
	stock_name = stock.ticker
	# print('stock name =============>', stock_name)
	stock.delete()
	messages.success(request , '"{}" Has Been Deleted Successfully'.format(stock_name))
	return redirect('delete_stock')


def ticker_view(request, symbol):
	ticker = symbol
	page_title = 'Home | {}'.format(ticker)
	api_url = 'https://cloud.iexapis.com/stable/stock/{}/quote?token={}'.format(ticker, token_lim)
	print('URL:', api_url)
	api_response = requests.get(api_url)

	try:
		ticker = api_response.json()

	except Exception as e:
		print(e)
		ticker = "Error..."

	return render(request, 'home.html', {
				'page_title': page_title,
				'ticker': ticker

			})


def delete_stock(request):
	page_title = 'Delete Stock'
	all_stocks = Stock.objects.all()

	return render(request, 'delete_stock.html', {
			'page_title': page_title,
			'all_stocks': all_stocks,
		})
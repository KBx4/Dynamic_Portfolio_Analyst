# Dynamic_Portfolio_Analyst
Dynamic portfolio analyst uses historical stock price data to predict future trends and analyzes sentiments behind news articles related to stocks in order to help users make informed trading decisions.

The model uses long short-term memory (LSTM) recurrent neural networks to predict prices for the next seven days.

News headlines and descriptions are scraped from [TickerTape](www.tickertape.in) using BeautifulSoup and Selenium. The data is passed on to FinBert model which predicts the sentiment for every description. 

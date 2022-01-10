from ggbet import GGBet
bet = GGBet()

#for index, url in enumerate(bet.get_matchs_urls()):
#    print(index, bet.get_ratio(url), url)

print(bet.get_ratio('https://ggbet.ru/esports/match/big-academy-vs-fnatic-rising-11-01'))
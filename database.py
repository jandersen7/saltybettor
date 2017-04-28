#! /usr/bin/env python3

import sqlite3
from datetime import datetime as dt


# TODO existence checks on table creations
class betdb(object):

    def __init__(self):
        self.conn = sqlite3.connect("bet.db")

    def create_fight_table(self):
        self.conn.execute('CREATE TABLE fights (date text, time '
                          'timestamp, team1 text, team2 text, odds1'
                          ' float, odds2 float, money1 integer, '
                          'money2 integer)')

    def create_bettor_table(self, team1, team2, date):
        self.conn.execute('create table fight_{}_{}_{} '
                          '(team text, bettor text, bet integer)'
                          ''.format(team1, team2,
                                    dt.strftime(date, '%m-%d-%Y-%M:%S')))

    def insert_bettors(self, team1, team2, date, bets):
        for team, bet_table in bets.items():
            insert_bets = []
            for bet in bet_table:
                insert_bets.append(tuple(team, bet['bettor'], bet['bet']))
            self.conn.executemany('insert into fight_{}_{}_{}(team, bettor, bet)'
                                  ' values(?, ?, ?)'.format(
                                      team1, team2,
                                      dt.strftime(date, '%m-%d-%Y-%M:%S')), insert_bets)

    def new_fight(self, team1, team2, odds1=0, odds2=0, money1=0, money2=0):
        date = dt.today()
        self.conn.execute('insert into fights(date, time, team1, '
                          'team2) values (?, ?, ?, ?, ?, ?, ?, ?)',
                          date, date, team1, team2, odds1, odds2,
                          money1, money2)
        self.create_bettor_table(team1, team2, date)

    def update_odds(self, team1, team2, odds1, odds2):
        self.conn.execute('update fights set (odds1=:odds1, '
                          'odds2=:odds2) where team1=:team1, '
                          'team2=:team2',
                          {"team1": team1, "team2": team2,
                           "odds1": odds1, "odds2": odds2})

    def update_money(self, team1, team2, money1, money2):
        self.conn.execute('update fights set (money1=:money1, '
                          'money2=:money2) where team1=:team1, '
                          'team2=:team2',
                          {"team1": team1, "team2": team2,
                           "money1": money1, "money2": money2})

    def update_bet(self, team1, team2, date, team, bettor, bet):
        self.conn.execute('update fight_{}_{}_{}(team, bettor, bet)'
                          ' set (bet=:bet) where team=:team, '
                          'bettor=:bettor'.format(
                              team1, team2,
                              dt.strftime(date, '%m-%d-%Y-%M:%S')),
                          {'team': team, 'bettor': bettor, 'bet': bet})

    def get_last_fight(self):
        day = dt.today()
        time = dt.now()
        self.conn.execute("select top 1 * from fights where date < "
                          ":date and time < :time order by date desc",
                          {"date": day, "time": time})
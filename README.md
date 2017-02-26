# BitBox Server

## A continuous hosting system for rapid prototyping and monitoring of Bitcoin trading algorithms.

# Getting Started
## Setting up BitBox on a new Ubuntu 16.04 LTS server

1. Make sure `python3` and `python3-pip` are installed:
    ```
    sudo apt install python3 python3-pip
    ```

2. Clone and install `cointk`
    ```
    cd && git clone https://github.com/cointk/cointk.git
    cd cointk
    sudo pip3 install .
    ```

3. Initialize `cointk`
    ```
    cd && python3 -c 'import cointk.init'
    ```

4. Clone and install `bitbox-server`
    ```
    cd && git clone https://github.com/cointk/bitbox-server.git
    cd bitbox-server
    sudo pip3 install .
    ```

5. Setup `mongodb`
    ```
    sudo apt install mongodb
    sudo service mongod start
    ```

6. Start writing strategies!  As an example, try backtesting the naive
strategy included in the `bitbox-server` package.
    ```
    cd && mkdir -p plots histories
    bitbox substrat bitbox/strategies/naive.py naive
    bitbox subtest naive --data data/coinbaseUSD.npz
    ```

# Usage

### Top level usage

```
usage: bitbox [-h] {substrat,runserver,subtest} ...

positional arguments:
  {substrat,runserver,subtest}
                        sub-command help
    substrat            submit strategy
    runserver           run server
    subtest             submit backtest

optional arguments:
  -h, --help            show this help message and exit
```

### Strategy submission usage

```
usage: bitbox substrat [-h] [--longname LONGNAME] cmd fnm name

positional arguments:
  cmd
  fnm                  Filename of file defining strategy
  name                 Unique name of strategy

optional arguments:
  -h, --help           show this help message and exit
  --longname LONGNAME  Human readable name of strategy
```

### Server running usage

```
 usage: bitbox runserver [-h] [--port PORT] cmd

positional arguments:
  cmd

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  Port for running server
```

### Backtest submission usage

```
 usage: bitbox subtest [-h] [--funds FUNDS] [--balance BALANCE]
                      [--fill-prob FILL_PROB] [--fee FEE] [--data DATA]
                      [--history HISTORY] [--data-name DATA_NAME]
                      [--datapart DATAPART] [--plot PLOT]
                      [--train-prop TRAIN_PROP] [--val-prop VAL_PROP]
                      [--verbosity VERBOSITY] [--print-freq PRINT_FREQ]
                      [--name NAME] [--longname LONGNAME]
                      cmd strategy

positional arguments:
  cmd
  strategy              Strategy name

optional arguments:
  -h, --help            show this help message and exit
  --funds FUNDS         Initial funds (in USD)
  --balance BALANCE     Inital bitcoin balance (in BTC)
  --fill-prob FILL_PROB
                        Probability of filling a valid order
  --fee FEE             Market fee (%) per transaction
  --data DATA           Filename of .npz backtesting data
  --history HISTORY     Filename of resulting .npz backtesting data
  --data-name DATA_NAME
                        Name used in .npz archive for data
  --datapart DATAPART   Use train, val, or test part of data
  --plot PLOT           Use train, val, or test part of data
  --train-prop TRAIN_PROP
                        Proportion of dataset that is for training
  --val-prop VAL_PROP   Proportion of data that is for validation
  --verbosity VERBOSITY
                        Verbosity level (0, 1, 2, or 3)
  --print-freq PRINT_FREQ
                        Frequency (in ticks) of logging (verbosity > 1)
  --name NAME           Unique name of backtest
  --longname LONGNAME   Human readable name of backtest
```

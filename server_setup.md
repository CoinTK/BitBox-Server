# Setting up BitBox on a new Ubuntu 16.04 LTS server

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

5. Start writing strategies!  As an example, try backtesting the naive
strategy included in the `bitbox-server` package.
    ```
    bitbox substrat strategies/naive.py naive
    bitbox subtest naive --data data/coinbaseUSD.npz
    ```
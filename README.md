# CS1440/2440 Lab 7: Simultaneous Auctions (Part 2)

## Introduction

Welcome to Lab 7: In this lab, you'll upgrade your auction agent by combining price prediction with the optimization method from last week. Your agent will learn to predict opponents' bids through self-play and use these insights to compute expected marginal values, allowing it to adjust bids dynamically over time.

## Setup and Installation

Follow these steps to set up your environment and install the necessary package for the lab.

**IMPORTANT: Please install/use a version of `Python >= 3.10`**
To check which version of Python you're using please run

```bash
python --version
```

If you installed Python 3.11 but your computer defaults to Python 3.9 you can initialize the virtual environment below to use
Python 3.11 instead by running:

If you own a Mac

```bash
python3.11 -m venv .venv
```

Instead of

```bash
python3 -m venv .venv
```

If you own a Windows

```bash
py -3.11 -m venv .venv
```

### Step 1: Git Clone the Repository

Open your terminal and navigate to where you want to clone the repository

```bash
git clone https://github.com/brown-agt/lab06-stencil.git
```

### Step 2: Create a Virtual Environment

Please then navigate to your project directory. Run the following commands to create a Python virtual environment named `.venv`.

If you own a Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you own a Windows

```bash
python3 -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install the agt server package

```bash
pip install --upgrade pip
pip install --upgrade agt-server
```

## Agent Methods

For the `Simultaneous Auction Agent`s here are a few methods that you may find helpful!

- **`self.get_goods()`**  - Returns the set of goods available in the auction.

- **`self.get_num_goods()`** - Returns the total number of goods available.

- **`self.get_goods_to_index()`** - Returns a dictionary mapping goods names to their index (useful for array operations).

- **`self.calculate_valuation(goods)`** - Calculates the total valuation for a given set of goods.  
  *Note:* If you pass in a list of good names, the method converts them to indices using the mapping returned by `self.get_goods_to_index()`.

- **`self.calculate_price(goods)`**  -  Calculates the total price for a given set of goods (using the agent’s current price data).

- **`self.calculate_total_util(goods)`**  - Computes the utility for a set of goods by subtracting the calculated price from the valuation.

- **`self.get_valuation_as_array()`**  - Returns the agent's valuations as a NumPy array.

- **`self.get_valuation(good)`**  - Retrieves the valuation for a specific good.

- **`self.get_valuations(bundle=None)`** - Returns a dictionary of valuations for a set of goods. If no bundle is provided, it returns valuations for all goods.

- **`self.get_game_report()`**  - Returns the game report, which includes all the recorded data from the auction rounds.

- **`self.get_valuation_history()`**  - Returns a list of valuation data from previous rounds.

- **`self.get_util_history()`** - Returns a list of your utilities from previous rounds.

- **`self.get_bid_history()`** - Returns the history of bids you have made in past rounds.

- **`self.get_payment_history()`** - Returns the history of payments made in past rounds.

- **`self.get_price_history()`** - Returns the history of price vectors from previous rounds.

- **`self.get_winner_history()`** - Returns the history of winning bids (or winners) from previous rounds.

NOTE: To run your agent locally you can just run it as normal but with the `--mode` arguement, to run it in the lab for the live competition please run it with arguments:

```
python3.10 scpp_agent.py --ip 'example_ip_on_board' --join_server
```

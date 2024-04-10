import click
from coinbase.rest import RESTClient
from json import dumps
import logging
import os
import sys
import time

# Create a logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)  # Set logger level to INFO

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set handler level to INFO

# Create a formatter and set it for the handler
formatter = logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)

# Add the handler to the logger
log.addHandler(console_handler)

def assert_env_vars_set():
    required_vars = ['COINBASE_API_KEY', 'COINBASE_API_SECRET']
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        log.error(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

def get_asset_price(client, asset, limit=0):
    product_id = f"{asset}-USD"
    trades = client.get_market_trades(product_id, limit)
    bid = float(trades['best_bid'])
    ask = float(trades['best_ask'])
    return sum([bid, ask]) / 2


@click.group()
def cli():
    pass

@cli.command(help='Get the balance(s) of your portfolio')
@click.option('--portfolio', help='The name of the portoflio', required=False, default='Default')
def balance(portfolio):
    client = RESTClient() # Uses environment variables for API key and secret
    portfolios = client.get_portfolios()['portfolios']
    p = next((p for p in portfolios if p['name'] == portfolio and p['deleted'] == False), None)
    if not p:
        log.error(f"Error: Portfolio '{portfolio}' not found.")
        sys.exit(1)
    breakdown = client.get_portfolio_breakdown(p['uuid'])['breakdown']
    accounts = breakdown['spot_positions']
    # Sort accounts by total_balance_fiat descending
    accounts.sort(key=lambda a: a['total_balance_fiat'], reverse=True)
    # Print accounts
    for account in accounts:
        staked = account['total_balance_fiat'] - account['available_to_trade_fiat']
        if staked > 0:
            log.info(f"{account['asset']}: {account['total_balance_crypto']} (${account['total_balance_fiat']:,.2f}; ${account['available_to_trade_fiat']:,.2f} available)")
        else:
            log.info(f"{account['asset']}: {account['total_balance_crypto']} (${account['total_balance_fiat']:,.2f})")


@cli.command(help='Buy a desired asset with USD at the current market price')
@click.option('--asset', help='The asset to buy', required=True)
@click.option('--usd', help='The amount of USD to spend buying desired asset', required=True, type=float)
@click.option('--threshold', help='The asset price above which no purchases will be made', required=False, type=float)
def buy(usd, asset, threshold=None):
    client = RESTClient()
    log.info(f"Buying {asset} with ${usd}")
    if threshold:
        asset_price = get_asset_price(client, asset)
        log.info(f"Asset price: {asset_price}")
        if asset_price > threshold:
            log.info(f"Asset price is above threshold. No purchase will be made.")
            sys.exit(0)
    order = client.create_order(
        client_order_id=f"{int(time.time())}-buy-{asset}",
        product_id=f"{asset}-USD",
        side='BUY',
        order_configuration={
            "market_market_ioc": {
                "quote_size": str(usd)
            }
        }
    )
    log.info(f"Order placed: {dumps(order, indent=2)}")


@cli.command(help='Sell a desired asset for USD at the current market price')
@click.option('--asset', help='The asset to sell', required=True)
@click.option('--qty', help='The amount of crypto to sell', required=True, type=float)
@click.option('--threshold', help='The minimum asset price required for sales to go through', required=False, type=float)
def sell(asset, qty, threshold=None):
    client = RESTClient()
    if threshold:
        asset_price = get_asset_price(client, asset)
        log.info(f"Asset price: {asset_price}")
        if asset_price < threshold:
            log.info(f"Asset price is below threshold. No sale will be made.")
            sys.exit(0)
    order = client.create_order(
        client_order_id=f"{int(time.time())}-sell-{asset}",
        product_id=f"{asset}-USD",
        side='SELL',
        order_configuration={
            "market_market_ioc": {
                "base_size": str(qty)
            }
        }
    )
    log.info(f"Order placed: {dumps(order, indent=2)}")


if __name__ == '__main__':
    assert_env_vars_set()
    cli()

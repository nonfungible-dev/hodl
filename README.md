# hodl
A CLI for DCAing into and out of crypto via the Coinbase Advanced API.

## Setup
0. Ensure you have python3 installed
1. Clone the repo
2. Use a virtual environment (optional but recommended)
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
`pip install -r requirements.txt`
```

4. Set Environment Variables:
```bash
export COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"
export COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"
```

5. Run the CLI with `python hodl/cli.py`

## Running on the Crontab
Consider creating a shell script to invoke the application and then adding that to the crontab.
For example, say you create the following shell script at `/path/to/hodl.sh`:

```bash
#!/bin/bash

# Activate the virtual environment
source /path/to/hodl/venv/bin/activate

# Set your API keys in the environment
export COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"
export COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"

# Invoke the hodl Python script, forwarding all arguments
python /path/to/hodl/cli.py "$@"

# Deactivate the virtual environment
deactivate
```

This bash script handles the activation of the virtual environment, which enables running of the script from the crontab.
It will pass our arguments through to the Python script, which will be invoked with the virtual environment activated.

Add the shell script to the crontab with `crontab -e`:

```cron
0 0 * * * /path/to/hodl.sh sell --asset BTC --qty 0.001 --threshold 69420
```

Et voila, you're now selling 0.001 BTC every day at midnight (as long as the price is at least $69,420)!

You can also run this script with other assets listed on Coinbase. For example:

```cron
0 12 * * * /path/to/hodl.sh sell --asset SOL --qty 2
```

This will sell 2 SOL every day at noon, regardless of the price.

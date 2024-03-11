# hodl
A CLI for DCAing into and out of crypto via the Coinbase Advanced API.

## Setup
0. Ensure you have python3 installed
1. Clone the repo
2. `pip install -r requirements.txt`
3. Set Environment Variables:

```bash
export COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"
export COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"
```

4. Run the CLI with `python hodl.py`

### Running on the Crontab
Consider creating a shell script to invoke the application and then adding that to the crontab. For example:

```bash
TODO
```

## Usage

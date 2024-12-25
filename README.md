# Zerodha to Ghostfolio Converter

## Overview
This Python script converts a Zerodha trade book CSV file into a Ghostfolio-compatible activities CSV format. It processes trade data, calculates fees, and ensures compatibility with Ghostfolio's import requirements.

## Features
- Converts Zerodha trade book CSV files to Ghostfolio activities format.
- Automatically calculates fees based on rounded amounts.
- Supports customizable rounding values.
- Maps trade types (`BUY` and `SELL`) to Ghostfolio-compatible actions.
- Outputs a summary of the conversion process.

## Requirements

### Python Dependencies
- Python 3.7 or later
- `pandas`

Install dependencies using pip:
```bash
pip install pandas
```

## Usage

### Command-Line Arguments
```bash
python zerodha_to_ghostfolio.py <input_file> <output_file> [--round-to ROUND_TO]
```
- `<input_file>`: Path to the Zerodha trade book CSV file.
- `<output_file>`: Path to the output Ghostfolio CSV file.
- `--round-to ROUND_TO`: Optional argument to specify the rounding value (default: 100).

### Example
```bash
python zerodha_to_ghostfolio.py zerodha_trades.csv ghostfolio_trades.csv --round-to 50
```

## Input File Format
The input CSV file from Zerodha should have the following columns:
- `trade_date` (e.g., `2024-12-25`)
- `symbol` (e.g., `TCS`)
- `trade_type` (e.g., `buy` or `sell`)
- `quantity` (e.g., `10`)
- `price` (e.g., `3500.50`)
- `trade_id` (e.g., `123456`)
- `order_id` (e.g., `78910`)

### Example Input
```csv
trade_date,symbol,trade_type,quantity,price,trade_id,order_id
2024-12-25,TCS,buy,10,3500.50,123456,78910
2024-12-26,INFY,sell,5,1500.00,123457,78911
```

## Output File Format
The output CSV file for Ghostfolio will have the following columns:
- `Date`: Date of the trade (formatted as `YYYY-MM-DD`).
- `Code`: Stock code (e.g., `TCS.NS`).
- `DataSource`: Defaulted to `YAHOO`.
- `Currency`: Defaulted to `INR`.
- `Price`: Trade price per unit.
- `Quantity`: Number of units traded.
- `Action`: Trade action (`BUY` or `SELL`).
- `Fee`: Calculated fee based on the rounding difference.
- `Note`: Additional trade details, including trade and order IDs.

### Example Output
```csv
Date,Code,DataSource,Currency,Price,Quantity,Action,Fee,Note
2024-12-25,TCS.NS,YAHOO,INR,3500.5,10,BUY,49.5,"Trade ID: 123456, Order ID: 78910, Total: ₹35005.00, Rounded: ₹35050.00"
2024-12-26,INFY.NS,YAHOO,INR,1500.0,5,SELL,25.0,"Trade ID: 123457, Order ID: 78911, Total: ₹7500.00, Rounded: ₹7550.00"
```

## Functionality Details

### Main Functions
1. **`round_up_to_nearest(number, nearest=100)`**
   Rounds up a given number to the nearest specified value (default: 100).

2. **`calculate_fee(quantity, price)`**
   Calculates the fee as the difference between the rounded total amount and the actual amount.

3. **`convert_zerodha_to_ghostfolio(input_file, output_file)`**
   Reads Zerodha CSV, processes trade data, and outputs a Ghostfolio-compatible CSV.

### Command-Line Interface
The script provides a CLI to specify input and output file paths and customize rounding values.

## Error Handling
The script handles errors gracefully and prints detailed error messages if the conversion fails.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
For questions or issues, feel free to open an issue in the repository!
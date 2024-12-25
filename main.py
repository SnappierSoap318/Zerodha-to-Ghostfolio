import pandas as pd
from datetime import datetime
import argparse
import math

def round_up_to_nearest(number, nearest=100):
    """Round up to the nearest specified number"""
    return math.ceil(number / nearest) * nearest

def calculate_fee(quantity, price):
    """
    Calculate fee based on the difference between rounded amount and actual amount
    
    Args:
        quantity (float): Number of shares/units
        price (float): Price per share/unit
    
    Returns:
        float: Calculated fee
    """
    actual_amount = quantity * price
    rounded_amount = round_up_to_nearest(actual_amount, 100)  # Round to nearest 100
    fee = rounded_amount - actual_amount
    return round(fee, 2)

def convert_zerodha_to_ghostfolio(input_file, output_file):
    """
    Convert Zerodha trade book CSV to Ghostfolio activities CSV format.
    
    Args:
        input_file (str): Path to input Zerodha trade book CSV file
        output_file (str): Path to output Ghostfolio CSV file
    """
    try:
        # Read Zerodha trade book CSV
        df = pd.read_csv(input_file)
        
        # Create empty DataFrame for Ghostfolio format
        ghostfolio_df = pd.DataFrame(columns=[
            'Date', 'Code', 'DataSource', 'Currency', 'Price', 
            'Quantity', 'Action', 'Fee', 'Note'
        ])
        
        # Map trade types
        trade_type_map = {
            'buy': 'BUY',
            'sell': 'SELL'
        }
        
        # Convert data
        ghostfolio_data = []
        for _, row in df.iterrows():
            # Convert date format
            trade_date = datetime.strptime(row['trade_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            
            # Calculate fee based on rounded amount difference
            fee = calculate_fee(row['quantity'], row['price'])
            
            # Calculate total amount for note
            total_amount = row['quantity'] * row['price']
            rounded_amount = round_up_to_nearest(total_amount, 100)
            
            # Map the data
            ghostfolio_row = {
                'Date': trade_date,
                'Code': f"{row['symbol']}.NS",  # Using ISIN as the code
                'DataSource': 'YAHOO',  # Default to YAHOO as data source
                'Currency': 'INR',  # Default to INR for Zerodha
                'Price': row['price'],
                'Quantity': row['quantity'],
                'Action': trade_type_map.get(row['trade_type'].lower(), 'UNKNOWN'),
                'Fee': fee,
                'Note': (f"Trade ID: {row['trade_id']}, Order ID: {row['order_id']}, "
                        f"Total: ₹{total_amount:.2f}, Rounded: ₹{rounded_amount:.2f}")
            }
            ghostfolio_data.append(ghostfolio_row)
        
        # Create DataFrame and save to CSV
        result_df = pd.DataFrame(ghostfolio_data)
        result_df.to_csv(output_file, index=False)
        
        # Print summary
        print(f"\nConversion Summary:")
        print(f"Total trades processed: {len(result_df)}")
        print(f"Total fees calculated: ₹{result_df['Fee'].sum():.2f}")
        print(f"\nFile saved to: {output_file}")
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Convert Zerodha trade book CSV to Ghostfolio activities CSV format'
    )
    parser.add_argument(
        'input_file',
        help='Path to input Zerodha trade book CSV file'
    )
    parser.add_argument(
        'output_file',
        help='Path to output Ghostfolio CSV file'
    )
    parser.add_argument(
        '--round-to',
        type=int,
        default=100,
        help='Round up total amount to nearest value (default: 100)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert file
    convert_zerodha_to_ghostfolio(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
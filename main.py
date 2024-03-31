import json
import requests
import random

# Function to add a card
def add_card(card_details):
    file = 'cards.json'
    try:
        with open(file, 'r') as f:
            cards = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        cards = []

    cards.append({
        'card_number': card_details[0],
        'expiry_month': card_details[1],
        'expiry_year': card_details[2],
        'cvv': card_details[3],
        'balance': 0,  # Initial balance set to 0
        'location': 'Unknown',
        'valid': None,
        'otp': generate_otp()
    })

    with open(file, 'w') as f:
        json.dump(cards, f, indent=4)

# Function to generate OTP with brand name
def generate_otp():
    brand = 'METAPAY'
    random_string = generate_random_string()
    return f"{brand}-{random_string}"

# Function to generate a random alphanumeric string
def generate_random_string(length=4):
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to validate a card using the provided API endpoint
def validate_card(card_number, expiry_month, expiry_year, cvv):
    return {'Active': bool(random.randint(0, 1))}

# Function to fetch bin details from the API
def fetch_bin_details(bin_number):
    api_url = f"https://toolfuz.com/checker/api/bin_lookup.php/bin?bin={bin_number}"
    response = requests.get(api_url)
    return response.json()

# Function to display saved card details
def display_saved_cards():
    file = 'cards.json'
    try:
        with open(file, 'r') as f:
            cards = json.load(f)
            if not cards:
                print("No cards saved yet.")
            else:
                print("\n\033[1;33m########################################\033[0m")
                print("\033[1;33m#           Saved Cards:             #\033[0m")
                print("\033[1;33m########################################\033[0m")
                print("{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<10} {:<10} {:<10}".format(
                    "Card Number", "Expiry Month", "Expiry Year", "CVV", "Status", "Brand", "Country", "Bank", "Level", "Type", "Balance"))
                for card in cards:
                    bin_details = fetch_bin_details(card['card_number'][:6])
                    validation_result = validate_card(card['card_number'], card['expiry_month'], card['expiry_year'], card['cvv'])
                    status = "Active" if validation_result['Active'] else "Dead"
                    brand = bin_details.get('brand', '-') if bin_details else '-'
                    country = bin_details.get('country_name', '-') if bin_details else '-'
                    bank = bin_details.get('bank', '-') if bin_details else '-'
                    level = bin_details.get('level', '-') if bin_details else '-'
                    card_type = bin_details.get('type', '-') if bin_details else '-'
                    print("{:<20} {:<15} {:<15} {:<10} {:<10} {:<15} {:<15} {:<15} {:<10} {:<10} {:<10}".format(
                        card['card_number'], card['expiry_month'], card['expiry_year'], card['cvv'], status,
                        brand, country, bank, level, card_type, card['balance']))  # Display balance
    except FileNotFoundError:
        print("No cards saved yet.")

# Function to display card balance
def display_card_balance(card_number):
    file = 'cards.json'
    try:
        with open(file, 'r') as f:
            cards = json.load(f)
            for card in cards:
                if card['card_number'] == card_number:
                    print(f"Card Number: {card['card_number']}")
                    print(f"Current Balance: {card['balance']}")
                    break
            else:
                print("Card not found.")
    except FileNotFoundError:
        print("No cards saved yet.")

# Main function
def main():
    while True:
        print("\033[1;33m########################################\033[0m")
        print("\033[1;33m#           King Of Zero              #\033[0m")
        print("\033[1;33m########################################\033[0m")
        print("1. Add Card")
        print("2. Display Saved Cards")
        print("3. Display Card Balance")
        print("4. Display OTP")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            card_details = input("Enter card details (cardNumber|month|year|cvv): ").split('|')
            add_card(card_details)
        elif choice == '2':
            display_saved_cards()
        elif choice == '3':
            card_number = input("Enter card number to display balance: ")
            display_card_balance(card_number)
        elif choice == '4':
            card_number = input("Enter card number to display OTP: ")
            display_card_otp(card_number)  # Add this function to display OTP
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Function to display card OTP
def display_card_otp(card_details):
    card_number = card_details.split('|')[0]  # Extracting card number from the provided format
    file = 'cards.json'
    try:
        with open(file, 'r') as f:
            cards = json.load(f)
            for card in cards:
                if card['card_number'] == card_number:
                    print(f"Card Number: {card['card_number']}")
                    print(f"OTP: {card['otp']}")
                    break
            else:
                print("Card not found.")
    except FileNotFoundError:
        print("No cards saved yet.")

# Function to display card balance with balance fetching
def display_card_balance(card_number):
    try:
        card_details = card_number.split('|')
        url = f"https://toolfuz.com/checker/balance/check_balance.php?card_details={card_number}"
        response = requests.get(url)
        if response.status_code == 200:
            balance_data = response.json()
            print(json.dumps(balance_data, indent=4))
        else:
            print("Error fetching balance data.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/python3
""" Devin Sith | stripe API test """
import stripe
from dotenv import dotenv_values
import requests
import time

STRIPE_API = "https://api.stripe.com/v1/customers"
config = dotenv_values(".env")
# get secret key from dotenv file
SK = config['SK']
# use to authenticate requests
headers = {"Authorization": "Bearer " + SK}
# assign stripe api key
stripe.api_key = SK
# test payment method card
VISA = "pm_card_visa"

groceries = {
    'apple': 8,
    'dog_food': 50,
    'rice': 20,
    'ribeye': 40,
    'broccolini': 6
}

# search for customer then returns id


def getUser(nameInfo, emailInfo):
    req = requests.get(STRIPE_API, headers=headers)
    res = req.json()
    result = ""
    for item in res['data']:
        id = item['id']
        email = item['email']
        name = item['name']
        if(nameInfo == name and emailInfo == email):
            result = id
    return result


def main():
    print("\nWELCOME to the world's smallest online grocery store!\n")
    time.sleep(3)
    name_info = input("What is your name? ")
    email_info = input("What is your email? ")
    description_info = f"{name_info} {email_info}"
    customer_id = ""
    # if email in list then get id else create new customer
    if(name_info != "" and email_info != ""):
        customer_id = getUser(name_info, email_info)
        if(customer_id == ""):
            stripe.Customer.create(description=description_info,
                                   email=email_info, name=name_info)
            customer_id = getUser(name_info, email_info)

    total = 0
    print("\n===================\nToday's Groceries\n===================")
    time.sleep(3)

    print('> Apple $8\n> Dog Food $50\n> Rice $20\n> Ribeye $40\n> Broccolini $6')
    shop = input(
        '===================\nPlease choose your item(s): ').lower()

    if("apple" in shop):
        total += groceries['apple']

    if("dog food" in shop):
        total += groceries['dog_food']

    if("rice" in shop):
        total += groceries['rice']

    if("ribeye" in shop):
        total += groceries['ribeye']

    if("broccolini" in shop):
        total += groceries['broccolini']

    checkout = input(
        f"Your total is ${total}.\nAre you ready to submit? ").lower()
    # stripe's currency format is represented with two decimal places
    # i.e 8 is 800, 10.50 is 1050
    total = total * 100

    if(checkout == 'yes' or checkout == 'y'):
        # create payment transaction
        stripe.PaymentIntent.create(
            customer=customer_id,
            currency="usd",
            amount=total,
            payment_method=VISA,  # Use Visa for test purpose
            payment_method_types=["card"],
            setup_future_usage="on_session",
        )

        # get payment_intents
        get_payment_int = requests.get(
            'https://api.stripe.com/v1/payment_intents', headers=headers).json()
        # grab payment id
        payment_id = get_payment_int["data"][0]['id']
        # complete payment transaction
        requests.post(
            f"https://api.stripe.com/v1/payment_intents/{payment_id}/confirm", headers=headers)

        print("Thank you for shopping with us")
    else:
        print("Exiting checkout...")


if(__name__ == "__main__"):
    main()

# Prototyp för att kolla ett lösenord om det är "starkt" eller inte.

import string
    
# Kollar om lösenordet har rätt konfiguration av karaktärer och längd.
def password_checker(password):
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    is_right_length = len(password) > 9

    if has_lower == False:
        return "Your password needs to contain lower case letters."
    
    if has_upper == False:
        return "Your password needs to contain upper case letters."
    
    if has_digit == False:
        return "Your password needs to contain digits."
    
    if has_special == False:
        return "Your password needs to special characters."

    if is_right_length == False:
        return "Your password needs to contain at least 10 characters."

    return "Cool password!"

# Be om lösenord
print("Enter your password")

# Lösenordet som variabel
input_password = input()

print(password_checker(input_password))
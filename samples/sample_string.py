def reverse_words(text):
    # No check, directly performing the task
    words = text.split()
    reversed_words = words[::-1]
    return " ".join(reversed_words)

def is_palindrome(text):
    # Instead of a complex one-liner, using a simple loop
    cleaned_text = ""
    for char in text:
        if char.isalnum():
            cleaned_text += char.lower()
            
    return cleaned_text == cleaned_text[::-1]

def mask_email(email):
    # Simple logic if there is '@', split,, otherwise return as is
    if "@" not in email:
        return email
    
    parts = email.split("@")
    username = parts[0]
    domain = parts[1]
    
    # No masking if the username is short
    if len(username) <= 2:
        return email
    
    # Concatenating strings 
    masked_username = username[0] + "***" + username[-1]
    return masked_username + "@" + domain

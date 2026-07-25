import random
import string

def generate_tracking_id():

    letters = string.ascii_uppercase
    numbers = string.digits

    random_part = ''.join(random.choices(letters + numbers, k=8))

    return "TRK" + random_part
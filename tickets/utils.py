import re

def RegexValidator(korean_name, english_name, birth, email, phone, gender, passport):
              
     KOREAN_NAME_REGEX  = "^[가-힣\s]+$"   
     ENGLISH_NAME_REGEX = "^[a-zA-Z\s]+$"
     BIRTH_REGEX        = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
     EMAIL_REGEX        = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
     PHONE_REGEX        = "^[0-9]{10,11}$"
     PASSPORT_REGEX     = "([a-zA-Z]{1}|[a-zA-Z]{2})\d{8}"

     if not re.search(KOREAN_NAME_REGEX, korean_name):
        return False

     if not re.search(ENGLISH_NAME_REGEX, english_name):
        return False

     if not re.search(BIRTH_REGEX, birth):
        return False

     if not re.search(EMAIL_REGEX, email):
        return False

     if not re.search(PHONE_REGEX, phone):
        return False

     if not gender=="남자" and not gender=="여자":
        return False

     if not re.search(PASSPORT_REGEX, passport):
        return False

     return True

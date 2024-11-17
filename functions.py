import re
def checkpasswordvalidity(password):
    if len(password)<6:
        return("the password must have atleast 6 characters")
    elif re.search(r"[a-z]",password):
         return "attleast 1 uppercase"
    elif re.search(r"[A-Z]",password):
         return "atleast 1 lowercase"
    elif re.search(r"[0-10]",password):
         return "atleast a number"
    elif re.search(r"[!@#$%^&*/]",password):
         return "atleast 1 special character"
    else:
         return True






  
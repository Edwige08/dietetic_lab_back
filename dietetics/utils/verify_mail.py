def verify_mail(mail):
    if "@" not in mail:
        return False
    else:
        if len(mail.split("@")) != 2 or len(mail.split("@")[0]) == 0 or len(mail.split("@")[1]) == 0 or "." not in mail.split("@")[1] or " " in mail.split("@")[0] or " " in mail.split("@")[1] : 
            return False
        else: 
            return True
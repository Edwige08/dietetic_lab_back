def verify_mail(mail):
    if "@" not in mail:
        return False
    else:
        email_parts = mail.split("@")
        if len(email_parts) != 2 or len(email_parts[0]) == 0 or len(email_parts[1]) == 0 or "." not in email_parts[1] or " " in email_parts[0] or " " in email_parts[1] : 
            return False
        else: 
            return True
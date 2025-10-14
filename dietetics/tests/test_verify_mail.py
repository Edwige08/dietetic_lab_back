from dietetics.utils.verify_mail import verify_mail

def test_valid_emails():
    assert verify_mail("firstname.lastname@domain.com") == True
    assert verify_mail("user@domain.com") == True
    assert verify_mail("contact@entreprise.fr") == True

def test_invalid_emails():
    assert verify_mail("test") == False
    assert verify_mail("test@") == False
    assert verify_mail("@domain.com") == False
    assert verify_mail("test@domain") == False
    assert verify_mail("test@@domain") == False
    assert verify_mail("test@test@domain") == False
    assert verify_mail("test @domain.com") == False
    assert verify_mail("test@ domain.com") == False
    assert verify_mail("") == False
from verify_email import verify_email

def verify_email_address(email):
    try:
        is_valid = verify_email(email)
        if is_valid:
            
            return "Yes"
        else:
            return "No"
    except Exception as e:
        print(f"Error verifying email: {e}")

if __name__ == "__main__":
    email_to_verify = "surya.k@valuehealthsol.com"
    print(verify_email_address(email_to_verify))

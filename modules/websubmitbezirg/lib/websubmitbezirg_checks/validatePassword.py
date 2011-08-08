def validatePassword(password):
    return password.isalnum() and len(password)>=8

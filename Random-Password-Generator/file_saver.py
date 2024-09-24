def save_password_to_file(password):
    with open("saved_passwords.txt", "a") as file:
        file.write(password + "\n")

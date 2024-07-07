import os

def main():
    print("configure git")
    username = input("What's your username? >>>")
    email = input("What's your email? >>>")
    token = input("What's your github token? >>>")
    
    os.system(f"git config user.name \"{username}\"")
    os.system(f"git config user.email \"{email}\"")
    os.system(f"git remote set-url origin https://{token}@github.com/user-11150/puel")
    
    print("Configure git was successfully!")

if __name__ == "__main__":
    main()

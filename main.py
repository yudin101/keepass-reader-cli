from pykeepass import PyKeePass, exceptions
import pyotp
import maskpass

try:
    file_name = input("Enter file name: ")
    file_name = file_name if file_name[-5:] == ".kdbx" else f"{file_name}.kdbx"

    password = maskpass.askpass(mask="")

    kp = PyKeePass(file_name, password=password)
except FileNotFoundError:
    print(f"\nError! File: {file_name} doesn't exist.")
    exit(1)
except exceptions.CredentialsError:
    print(f"\nError! Wrong Password!")
    exit(1)

kp_entries = kp.entries

for i, j in enumerate(kp_entries):
    print(f"[{i}]", j)

try:
    choice = int(input("\nEnter the corresponding number of the required entry: "))

    if choice > len(kp_entries):
        print("Error! Invalid Value!")
        exit(1)
except ValueError:
    print("Error! Invalid Value!")
    exit(1)

selected_choice = str(kp_entries[choice])
print(f"\n{selected_choice}")

entry_name = str(
    selected_choice[selected_choice.find("/") + 1 : selected_choice.find("(")]
).strip()
entry_details = kp.find_entries(title=entry_name, first=True)
print(f"\nEntry: {entry_name}")
print(f"Password: {entry_details.password}")
print(f"URL: {entry_details.url}")

otp_choice = input("\nShow OTP now? (y/n): ").upper()

if otp_choice == "Y":
    try:
        print(f"OTP: {pyotp.parse_uri(entry_details.otp).now()}")
    except TypeError:
        print("No OTP found!")

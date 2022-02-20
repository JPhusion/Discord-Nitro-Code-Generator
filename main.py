import ctypes
import string
import os
import time
import getpass

try:
    import board
    import neopixel
except Exception as e:
    print(e)

pixels = [0]

try:
    pixels = neopixel.NeoPixel(board.D18, 30)
    pixels[0] = (255, 0, 0)
except NameError:
    pass

USE_WEBHOOK = True

os.system('cls' if os.name == 'nt' else 'clear')

username = getpass.getuser()

start_time = time.time()

try:  # Check if the requrements have been installed
    from discord_webhook import DiscordWebhook  # Try to import discord_webhook
except ImportError:  # If it chould not be installed
    # Tell the user it has not been installed and how to install it
    input(
        f"Module discord_webhook not installed, to install run '{'py -3' if os.name == 'nt' else 'python3.8'} -m pip install discord_webhook'\nYou can ignore this error if you aren't going to use a webhook.\nPress enter to continue.")
    USE_WEBHOOK = False
try:  # Setup try statement to catch the error
    import requests  # Try to import requests
except ImportError:  # If it has not been installed
    # Tell the user it has not been installed and how to install it
    input(
        f"Module requests not installed, to install run '{'py -3' if os.name == 'nt' else 'python3.8'} -m pip install requests'\nPress enter to exit")
    exit()  # Exit the program
try:  # Setup try statement to catch the error
    import numpy  # Try to import requests
except ImportError:  # If it has not been installed
    # Tell the user it has not been installed and how to install it
    input(
        f"Module numpy not installed, to install run '{'py -3' if os.name == 'nt' else 'python3.8'} -m pip install numpy'\nPress enter to exit")
    exit()  # Exit the program

# check if user is connected to internet
url = "https://github.com"
try:
    response = requests.get(url)  # Get the responce from the url
    print("Internet check")
    time.sleep(.4)
except requests.exceptions.ConnectionError:
    # Tell the user
    input("You are not connected to internet, check your connection and try again.\nPress enter to exit")
    exit()  # Exit program


class NitroGen:  # Initialise the class
    def __init__(self):  # The initaliseaiton function
        self.fileName = "Nitro Codes.txt"  # Set the file name the codes are stored in

    def main(self):  # The main function contains the most important code
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        # Print who developed the code
        try:
            num = 10  # Ask the user for the amount of codes
        except ValueError:
            input("Specified input wasn't a number.\nPress enter to exit")
            exit()  # Exit program

        if USE_WEBHOOK:
            # Get the webhook url, if the user does not wish to use a webhook the message will be an empty string
            url = "https://canary.discord.com/api/webhooks/944758935959773184/rkbWqFU1VD0d5rGTDvuoa9krTeIElPhSG-6xhtfWhhofAnzOmyGbP3eMvMEoagX-l0aT"  # Get the answer
            # If the url is empty make it be None insted
            webhook = url if url != "" else None

            if webhook is not None:
                DiscordWebhook(  # Let the user know it has started logging the ids
                    url=url,
                    content=f"```Started checking urls from {username}```"
                ).execute()

        # print() # Print a newline for looks

        valid = []  # Keep track of valid codes
        invalid = 0  # Keep track of how many invalid codes was detected
        chars = []
        chars[:0] = string.ascii_letters + string.digits

        # generate codes faster than using random.choice
        call_counter = 10
        found = False
        while True:
            if call_counter / (time.time() - start_time) > 15:
                time.sleep(0.5)
            for i in range(2):
                pixels[0] = (0, 0, 0) if i % 2 == 0 else (
                    0, 0, 255) if not found else (0, 255, 0)
                c = numpy.random.choice(chars, size=[num, 19])
                for s in c:  # Loop over the amount of codes to check
                    try:
                        code = ''.join(x for x in s)
                        # Generate the url
                        url = f"https://discord.gift/{code}"

                        result = self.quickChecker(
                            url, webhook)  # Check the codes

                        call_counter += 1

                        if result:  # If the code was valid
                            # Add that code to the list of found codes
                            valid.append(url)
                            result = False
                            found = True
                            break
                        else:  # If the code was not valid
                            invalid += 1  # Increase the invalid counter by one
                    except KeyboardInterrupt:
                        print(
                            f"""\n===========================================\nValid: {len(valid)}, Invalid: {invalid}\nValid Codes: {', '.join(valid)}\n===========================================""")  # Exit the program
                        time.sleep(1)
                    except Exception as e:  # If the request fails
                        # Tell the user an error occurred
                        print(f" Error | {url} ", e)

                    if os.name == "nt":  # If the system is windows
                        ctypes.windll.kernel32.SetConsoleTitleW(
                            f"{len(valid)} Valid | {invalid} Invalid")  # Change the title
                        print("")
                    else:  # If it is a unix system
                        # Change the title
                        print(
                            f'\33]0;{len(valid)} Valid | {invalid} Invalid\a', end='', flush=True)

        # Tell the user the program finished
        print("\nThe end!")

    # Function used to print text a little more fancier
    def slowType(self, text: str, speed: float, newLine=True):
        for i in text:  # Loop over the message
            # Print the one charecter, flush is used to force python to print the char
            print(i, end="", flush=True)
        if newLine:  # Check if the newLine argument is set to True
            print()  # Print a final newline to make it act more like a normal print statement

    # Used to check a single code at a time
    def quickChecker(self, nitro: str, notify=None):
        # Generate the request url
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url=url)  # Get the response from discord

        if "You are being rate limited" in response.text:
            print("\nYou are being rate limited\n")
            print(response.text)
            print("\nChange your ip address to bypass the rate limit")
            exit()

        if response.status_code == 200:  # If the responce went through
            # Notify the user the code was valid
            pixels[0] = (0, 100, 0)
            print(f" Valid | {nitro} ", flush=True,
                  end="" if os.name == 'nt' else "\n")
            with open("Nitro Codes.txt", "w") as file:  # Open file to write
                # Write the nitro code to the file it will automatically add a newline
                file.write(nitro)

            if notify is not None:  # If a webhook has been added
                DiscordWebhook(  # Send the message to discord letting the user know there has been a valid nitro code
                    url=url,
                    content=f"Valid Nitro Code detected! <@651705531261779988> \n{nitro}"
                ).execute()

            return True  # Tell the main function the code was found

        # If the responce got ignored or is invalid ( such as a 404 or 405 )
        elif response.status_code in [404, 405]:
            # Tell the user it tested a code and it was invalid
            print(f" Invalid | {nitro} ", flush=True,
                  end="" if os.name == 'nt' else "\n")
            return False  # Tell the main function there was not a code found
        else:
            print(f" Limited | {nitro} ", flush=True,
                  end="" if os.name == 'nt' else "\n")
            return False


if __name__ == '__main__':
    Gen = NitroGen()  # Create the nitro generator object
    Gen.main()  # Run the main code

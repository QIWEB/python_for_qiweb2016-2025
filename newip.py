import os

def main():
    print "Running tests... ip chege"
    os.system("""(echo authenticate '"mypassword"'; echo signal newnym; echo quit) | nc localhost 9051""")


if __name__ == "__main__":
    main()


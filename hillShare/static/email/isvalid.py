def isValid(userid, password):
    with open('users.txt', 'r') as file:
        # read the file into lines
        lines = file.readlines() 

        # iterate through lines, splitting each line into strings
        for line in lines:
            strings = iter(line.split())

            # process each string pair, return True if match
            # otherwise when end of file reached, drop to return False
            while True:
                try:
                    fileUserId = strings.next()
                    filePassword = strings.next()

                    # we have a match
                    if (userid == fileUserId) and (password == filePassword):
                        return True

                except StopIteration:
                    break

    return False

def main():
    user=input("User name")
    pas=input("passWord")
    isValid('username:'+user,'password'+pas)


main()

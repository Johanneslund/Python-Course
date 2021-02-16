#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 2

"""

import argparse
import sys

__version__ = '1.0'
__desc__ = "A simple script used to authenticate spies!"


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT0179G Assignment 2 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('credentials', metavar='credentials', type=str,
                        help="Username and password as string value")

    args = parser.parse_args()

    if not authenticate_user(args.credentials):
        print("Authentication failed. Program exits...")
        sys.exit()

    print("Authentication successful. User may now access the system!")


def authenticate_user(credentials: str) -> bool:
    """Procedure for validating user credentials"""
    username = 'Chevy_Chase'  # Expected username. MAY NOT BE MODIFIED!!
    password = 'i0J0u0j0u0J0Zys0r0{'  # Expected password. MAY NOT BE MODIFIED!!
    user_tmp = pass_tmp = str()

    ''' PSEUDO CODE
    PARSE string value of 'credentials' into its components: username and password.
    SEND username for FORMATTING by utilizing devoted function. Store return value in 'user_tmp'.
    SEND password for decryption by utilizing devoted function. Store return value in 'pass_tmp'.
    VALIDATE that both values corresponds to expected credentials.
    RETURN outcome of validation as BOOLEAN VALUE.
    '''
    pass  # TODO: Replace with implementation!

    credentials = credentials.split()
    user_tmp = credentials[0] + ' ' + credentials[1]
    pass_tmp = credentials[2]

    user_tmp = format_username(user_tmp)
    pass_tmp = decrypt_password(pass_tmp)

    if user_tmp == username and pass_tmp == password:
        return True
    else:
        return False


def format_username(username: str) -> str:
    """Procedure to format user provided username"""

    ''' PSEUDO CODE
    FORMAT first letter of given name to be UPPERCASE.
    FORMAT first letter of surname to be UPPERCASE.
    REPLACE empty space between given name and surname with UNDERSCORE '_'
    RETURN formatted username as string value.
    '''
    pass  # TODO: Replace with implementation!

    username = username.split()

    newuser = ''

    r = 0
    k = 0

    for user in username:
        r = 0
        if k != 0:
            newuser += '_'

        k += 1

        for i in user:
            if r == 0:
                newuser += i.upper()
                r += 1
            else:
                newuser += i.lower()
                r += 1

    return newuser


def decrypt_password(password: str) -> str:
    """Procedure used to decrypt user provided password"""
    rot7, rot9 = 7, 9  # Rotation values. MAY NOT BE MODIFIED!!
    vowels = 'AEIOUaeiou'  # MAY NOT BE MODIFIED!!
    decrypted = str()

    ''' PSEUDO CODE
    REPEAT {
        DETERMINE if char IS VOWEL.
        DETERMINE ROTATION KEY to use.
        DETERMINE decryption value
        ADD decrypted value to decrypted string
    }
    RETURN decrypted string value
    '''
    pass  # TODO: Replace with implementation!

    flag = 0
    count = 0
    key = 0

    for i in password:

        if i in vowels:
            flag = 1
        if (count % 2) == 0:
            key = rot7
        else:
            key = rot9
        dValue = chr(ord(i) + key)
        if flag == 1:
            decrypted += '0' + dValue + '0'
        else:
            decrypted += dValue
        count += 1
        flag = 0
        key = 0

    return decrypted


if __name__ == "__main__":
    main()

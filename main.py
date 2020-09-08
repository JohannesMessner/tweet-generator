import model
import update_archive


def main():
    print_intro()
    user_id = 'realDonaldTrump'
    filename = user_id + '.csv'
    n = 2
    m = model.Model(n, filename)
    m.initialize()
    command = input()
    while command != 'q':
        if command == 't':
            print(m.generate_tweet())
        elif command.startswith('refresh data'):
            command_split = command.split()
            if len(command_split) <= 2:  # no authentication given -> use credentials-file
                auth_args = (None, None, None, None)
            elif len(command_split) == 6:  # use directly provided api tokens and secrets
                auth_args = command_split[2:]
            else:
                print('Wrong number of command arguments')
                continue
            try:
                update_archive.update_archive(user_id, *auth_args)
                m = model.Model(n, filename)
                m.initialize()
                print('Refresh done')
            except:
                print_authentication_fail()
        elif command.startswith('switch'):
            command_split = command.split()
            user_id = command_split[1]
            filename = user_id + '.csv'
            try:
                update_archive.update_archive(user_id)
                m = model.Model(n, filename)
                m.initialize()
                print('Refresh done')
            except:
                print_authentication_fail()

        elif command == 'help':
            print_help()
        command = input()


def print_authentication_fail():
    print('Twitter authentication failed')
    print('Enter Twitter api credentials directly or refer to the readme for further information')


def print_intro():
    print('Wanna generate some tweets?')
    print('Type "t" to generate a Trump-Tweet!')
    print('Type "help" for help and further information')


def print_help():
    print('The following command are available:')
    print('-------------------------------------')
    print('"t": \t \t Creates a new tweet.')
    print('"refresh data [<api_key> <api_secret> <access_token> <access_token_secret>]":'
          '\t Pulls data from Twitter and refreshes the language model of the currently simulated'
          'Twitter user.')
    print('switch <Twitter-handle>: \t Switches the model to a different twitter user.'
          'Pulls their tweets from the api. Requires a credentials-file (see readme).')
    print('"q": \t \t Quits the app.')


if __name__ == '__main__':
    main()
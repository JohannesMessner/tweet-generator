import model
import update_archive


def main():
    print('Hey, wanna generate some tweets?')
    print('Specify how closely the generated tweets should match the originals (1-3).')
    print('A low number results in more random tweets that might be garbage, a high number generates more proper'
          'sentences but might reproduce real tweets 1:1')
    n = int(input())
    print('You can also select who the tweets should emulate.')
    print('At the moment only Donald Trump is available, so type "realDonaldTrump"')
    filename = input() + '.csv'
    m = model.Model(n, filename)
    m.initialize()
    print_intro()
    command = input()
    while command != 'q':
        if command == 't':
            print(m.generate_tweet())
        elif command == 'refresh data':
            update_archive.update_archive()
            m = model.Model(n, filename)
            m.initialize()
            print('Refresh done')
        elif command == 'help':
            print_help()
        command = input()


def print_intro():
    print('Type "help" for help and further information')


def print_help():
    print('The following command are available:')
    print('-------------------------------------')
    print('"t": \t Creates a new tweet')
    print('"refresh data": \t Pulls data from Twitter and refreshes the language model')


if __name__ == '__main__':
    main()
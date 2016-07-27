from application.identifier import Identifier

if __name__ == '__main__':
    idf = Identifier()
    while raw_input('Hello!, to start listening press enter, to exit press q\n') != 'q':
        idf.guess()

from fa import FA


def main():
    fa = FA.from_file('number_FA.in')
    print(fa)
    print(fa.verify('numărul 28532131'))


if __name__ == '__main__':
    main()

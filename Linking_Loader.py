class Linking_Loader(object):
    source_code = ''
    beginning_address = int('4000', 16)
    load_map = dict()

    def __init__(self, file, beginning_address=None):
        self.beginning_address = beginning_address or self.beginning_address
        self.file = file
        f = open(file, 'r')
        self.source_code = f.read().upper().splitlines()
        f.close()
        self.source_code = list(filter(lambda a: a != '', self.source_code))
        self.build_load_map()

    def __repr__(self):
        return '<beginning_address:{}\n load_map:{}\n source_code:{}>'.format(self.beginning_address, self.load_map,
                                                                              self.source_code)

    def build_load_map(self):
        locctr = self.beginning_address
        for each in self.source_code:
            if (each[0] == 'H'):
                length = int(each[13:19], 16)
                self.load_map[each[1:7]] = (locctr, length)
                locctr += length
            elif (each[0] == 'D'):
                number = int((len(each) - 1) / 12)
                for i in range(0, number):
                    start = 12 * i + 1
                    mid = start + 6
                    end = mid + 6
                    self.load_map[each[start:mid]] = int(each[mid:end], 16)

    def show_load_map(self):
        def fillstr(string, sample):
            return string + sample[:len(sample) - len(string)]
        print('Control', 'Symbol ', sep='      ', end='\n')
        print('Section', 'Name   ', 'Address', 'Length', sep='      ', end='\n')
        print('---------------------------------------------', end='\n')
        locctr = 0
        for i, j in self.load_map.items():
            if (type(j) == tuple):
                locctr = j[0]
                print(i + ' ', '       ', fillstr(hex(j[0])[2:].upper(), '       '), hex(j[1])[2:].upper(),
                      sep='      ', end='\n')
            elif (type(j) == int):
                print('       ', i + ' ', fillstr(hex(locctr + j)[2:].upper(), '       '), sep='      ', end='\n')


if __name__ == '__main__':
    l = Linking_Loader(file='2.17.obj')
    print('Load Map : ')
    l.show_load_map()

class Linking_Loader(object):
    source_code = ''
    beginning_address = int('4000', 16)
    load_map = dict()
    memory_address = dict()

    def __init__(self, file, beginning_address=None):
        self.beginning_address = beginning_address or self.beginning_address
        self.file = file
        f = open(file, 'r')
        self.source_code = f.read().upper().splitlines()
        f.close()
        self.source_code = list(filter(lambda a: a != '', self.source_code))
        self.build_load_map()
        self.build_memory_address()

    def __repr__(self):
        return '<beginning_address:{}\n load_map:{}\n source_code:{}\nmemory_address:{}>'.format(self.beginning_address, self.load_map,
                                                                              self.source_code, self.memory_address)

    def build_memory_address(self):
        def fillstr(string, length):
            for count in range(0, length - len(string)):
                string = '0' + string
            return string
        def iskey_exist(key):
            for each in self.memory_address.keys():
                if key == each:
                    return True
            return False
        def putin(place, string):
            locctr = place - place % 16
            if(iskey_exist(locctr)):
                able = 32 - len(self.memory_address[locctr])
                if(len(string) > able):
                    self.memory_address[locctr] += string[:able]
                    putin(locctr + 16, string[able:])
                else:
                    self.memory_address[locctr] += string
            else:
                empty_num = (place - locctr) * 2
                contents = ''
                able = 32 - empty_num
                for i in range(0, empty_num):
                    contents += 'x'
                if(len(string) > able):
                    self.memory_address[locctr] = contents + string[:able]
                    putin(locctr + 16, string[able:])
                else:
                    self.memory_address[locctr] = contents + string
        begin = 0
        locctr = 0
        for each in self.source_code:
            if(each[0] == 'H'):
                begin = self.load_map[each[1:7]][0]
            elif(each[0] == 'T'):
                locctr = begin + int(each[1:7], 16)
                putin(locctr, each[9:9 + int(each[7:9], 16) * 2])
            elif(each[0] == 'M'):
                locctr = begin + int(each[1:7], 16)
                place = locctr % 16
                locctr -= place
                place *= 2
                length = int(each[7:9], 16)
                flag = each[9]
                sysbol = each[10:16]
                if(length % 2 == 1):
                    place += 1
                temp = self.memory_address[locctr]
                target = int(temp[place:place + length], 16)
                #print(temp[place:place + length], end='\n')
                if(type(self.load_map[sysbol]) == tuple):
                    if(flag == '+'):
                        target += self.load_map[sysbol][0]
                    elif(flag == '-'):
                        target -= self.load_map[sysbol][0]
                elif (type(self.load_map[sysbol]) == int):
                    if (flag == '+'):
                        target += self.load_map[sysbol]
                    elif (flag == '-'):
                        target -= self.load_map[sysbol]
                temp = temp[:place] + fillstr((hex(target)[2:]), length).upper() + temp[place + length:]
                self.memory_address[locctr] = temp

    def build_load_map(self):
        baklocctr = self.beginning_address
        locctr = self.beginning_address
        for each in self.source_code:
            if (each[0] == 'H'):
                length = int(each[13:19], 16)
                self.load_map[each[1:7]] = (locctr, length)
                baklocctr = locctr
                locctr += length
            elif (each[0] == 'D'):
                number = int((len(each) - 1) / 12)
                for i in range(0, number):
                    start = 12 * i + 1
                    mid = start + 6
                    end = mid + 6
                    self.load_map[each[start:mid]] = int(each[mid:end], 16) + baklocctr

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
                print('       ', i + ' ', fillstr(hex(j)[2:].upper(), '       '), sep='      ', end='\n')

    def show_memory_address(self):
        def fillstr(string, sample):
            return string + sample[:len(sample) - len(string)]
        def formet_memory_adress():
            count = len(self.memory_address.keys())
            for i, j in self.memory_address.items():
                count -= 1
                if(len(j) < 8):
                    if(count == 0):
                        self.memory_address[i] = (fillstr(j, 'xxxxxxxx'), 'xxxxxxxx', 'xxxxxxxx', 'xxxxxxxx')
                    else:
                        self.memory_address[i] = (fillstr(j, '--------'), '--------', '--------', '--------')
                elif(len(j) < 16):
                    if (count == 0):
                        self.memory_address[i] = (j[:8], fillstr(j[8:], 'xxxxxxxx'), 'xxxxxxxx', 'xxxxxxxx')
                    else:
                        self.memory_address[i] = (j[:8], fillstr(j[8:], '--------'), '--------', '--------')
                elif(len(j) < 24):
                    if (count == 0):
                        self.memory_address[i] = (j[:8], j[8:16], fillstr(j[16:], 'xxxxxxxx'), 'xxxxxxxx')
                    else:
                        self.memory_address[i] = (j[:8], j[8:16], fillstr(j[16:], '--------'), '--------')
                elif(len(j) < 32):
                    if (count == 0):
                        self.memory_address[i] = (j[:8], j[8:16], j[16:24], fillstr(j[24:], 'xxxxxxxx'))
                    else:
                        self.memory_address[i] = (j[:8], j[8:16], j[16:24], fillstr(j[24:], '--------'))
                else:
                    self.memory_address[i] = (j[:8], j[8:16], j[16:24], j[24:])
        formet_memory_adress()
        print('Memory', end='\n')
        print('Address', 'Contents', sep='   ', end='\n')
        print('----------------------------------------------', end='\n')
        for i, j in self.memory_address.items():
            print(fillstr(hex(i)[2:].upper(), '       '), end='   ')
            print(j[0], j[1], j[2], j[3], sep=' ', end='\n')

if __name__ == '__main__':
    l = Linking_Loader(file='2.17.obj')
    print('\nLoad Map : \n')
    l.show_load_map()
    print('\nMemory Address : \n')
    l.show_memory_address()
    print()

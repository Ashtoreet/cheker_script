class Key(object):
    """docstring for Key."""


    def __init__(self, key, name=None, ut=None):
        self.key = key
        self.name = name


    def determine_type_of_key(self):
        len_key = len(self.key)
        if len_key is 10:
            print('Это innul (инн юрлица): ', self.key)
            self.name = 'innul'
        elif len_key is 12:
            print('Это innfl (инн физлица): ', self.key)
            self.name = 'innfl'
        elif len_key is 13:
            print('Это ogrn (огрн): ', self.key)
            self.name = 'ogrn'
        elif len_key is 15:
            print('Это ogrnip (огрн Ип): ', self.key)
            self.name = 'ogrnip'
        else:
            return False
        return True



if __name__ == '__main__':
    innul = input('innul', )
    innfl = input('innfl', )
    key = Key(innfl)
    key.determine_type_of_key()

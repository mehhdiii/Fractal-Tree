import pickle

class rw:
    # A class which reads and writes data to the hardisk
    
    def __init__(self) -> None:
        pass

    def read(self, dir: str, filename):
        with open(filename) as file:
            data = pickle.load(file)

        return data


    def write(self, dir: str, filename, data):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
myobj = rw()
        

    



    
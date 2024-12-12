#from TrainModel import TrainModel
from TrainModel.TrainModel import TrainModel

class TrainList:
    def __init__(self):
        self.train_list = [] 

    #Add a train using the train controller shared list
    def add_train(self, tc_list):
        train_model = TrainModel(tc_list)
        train_model.ID = len(self.train_list)
        self.train_list.append(train_model)
        print("successfully added a train")
        print("Num trains: ", len(self.train_list))
    
    #Remove a train by name
    def remove_train(self, train_name):
        self.train_list = [train for train in self.train_list if train.name != train_name]

    #Return a train specified
    def get_train(self, train_name):
        for train in self.train_list:
            if train.name == train_name:
                return train
        return None


    def list_trains(self):
        return self.train_list

    #To get the length
    def __len__(self):
        return len(self.train_list)

    #For indexing
    def __getitem__(self, index):
        return self.train_list[index]

#from TrainModel import TrainModel
from TrainModel.TrainModel import TrainModel

class TrainList:
    def __init__(self):
        self.train_list = []  # This will hold the list of train objects

    def add_train(self):
        """Add a new TrainModel to the list."""
        train_model = TrainModel()
        train_model.ID = len(self.train_list)
        self.train_list.append(train_model)
    

    def remove_train(self, train_name):
        """Remove a train by name."""
        self.train_list = [train for train in self.train_list if train.name != train_name]

    def get_train(self, train_name):
        """Retrieve a train by name."""
        for train in self.train_list:
            if train.name == train_name:
                return train
        return None

    def list_trains(self):
        """List all trains in the train list."""
        return self.train_list

    def __len__(self):
        """Return the number of trains in the list."""
        return len(self.train_list)

    def __getitem__(self, index):
        """Allow indexing like train_list[0]."""
        return self.train_list[index]

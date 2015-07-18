class BioObject:
    #this is the central hierarchical object
    def __init__(self,pos,type):
        self.types = types      #type of Bioobject

    def add_subtype(self.sub):
        #add a Subobject (Bioobject) to the object
        
    def add_discrete_model(discrete_models):
        #add discrete model position
        self.discrete_models = discrete_model
        
    def add_continous_model(continous_model):
        #add a continous model
        self.continous_model = continous_model
        
    def create_discrete_instances():
        #this creates new instances from BioObject for each subobject
        self.subobjects = self.discrete_models.create_instances(self.pos)
        
    def get_contained_bioobjects():
        #returns all bioobjects contained in bioobject (optional: for bioobject being in given state)
        return self.subobjects

class BioObjectType:
    self.DiscreteModel = []
    self.ContinousModel = []
    
    

class DiscreteModel:
    #the discrete model defines relative position and type of each Object
    def __init__(self,pos,types):
        self.pos = pos        #relative positions of all BioObjects
        self.types = types     #type of each BioObject
    def create_instances(relpos):
        #this creates new instances from BioObject for each position in the DiscreteModel and returns them
        return [BioObject(pos+relpos,t) for pos,t in zip(self.pos,self.types)]
    def create_continous_model():
        #this creates a new continous model based on the positions of the BioObjects
        #....
        return ContinousModel()


class ContinousModel:
    def __init__(self,densities,types):
        self.types = types          #types of Bioobject
    def create_discrete_model():
        #this creates a new discrete model based on the Continous Model
        pass
        return DiscreteModel()
    def get_electron_density():
        #this returns the electron density of the model
        pass
    def get_number_density():
        #this returns the number density for each containing type
        pass
    def get_number_density(types)
        #this returns the number density for the given types

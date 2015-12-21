# requirements for a datastructure:
# hierarchical with link in both directions of the tree and possible with to branches ending in the same object
# we need to be able to map between concepts and individual representations (in both directions) (e.g. water might be just threaten in a course grained fashion or implicitly, but one should be able to switch to atomistic representation)
# objects might be defined explicitly (e.g. (relativ) position for each instance) or implicitly (e.g. a concentration within an volumen)
# the data need to able to be pushed into a larger repository, with possible detailed data stored locally
# one should be able to take concepts, copy them and use them in a different context, e.g. a lipid bilayer developed for HIV should be able to be used for a bacteria afterwards
# we might think how to incorpurate time dependence

#check XML for neurons: https://neuroml.org/examples
#check bioblender and pymol for visualisation



class BioObject:
    # a BioObject is an instance of a BioClass
    def init_pos(pos):
        #initialise the position of the BioObject
        self.pos = pos


class BioClass:
    # the bioclass defines the hierarchical relations
    # each BioClass is supposed to have one or BioModel
    # each BioClass is supposed to have one or many BioObject
    def init_pos(pos):
        self.level                    #level of abstraction
    def add_Classes()
    
    
class BioMaschine:
    # a Run is a instance of a BioModel

class BioModel:
    #a biomodel connects a class with is superior as well as its inferior class
    #it defines the attributes of the BioObjects
    #it might depend on attributes of other BioClasses (superiors, inferiors, neighboring on the same level of abstraction)
    def __init__(self):
        self.name                     #name of the model
    def create_instances(relpos):
        #this creates new instances from BioObject according to the model
        pass

class DiscreteModel(BioModel):
    #the discrete model defines relative position and type of each Object
    def __init__(self,pos,types):
        self.pos = pos        #relative positions of all BioObjects
    def create_instances(relpos):
        #this creates new instances from BioObject for each position in the DiscreteModel and returns them
    def get_electron_density():
        #this returns the electron density of the model
        pass
    def get_number_density(types):
        #this returns the number density for the given types
        pass
        return [BioObject(pos+relpos,t) for pos,t in zip(self.pos,self.types)]


class ContinousModel(BioModel):
    def __init__(self,densities,types):
        self.types = types          #types of Bioobject
        self.number_density = []    #a matrix defining the number density of each class
    def create_discrete_model():
        #this creates a new discrete model based on the Continous Model
        pass
        return DiscreteModel()
    def get_electron_density():
        #this returns the electron density of the model
        pass
    def get_number_density():
        #this returns the number density for each class defined by the model
        pass


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




def buildHIV():
    #creating of a droplet object
    HIVDROPLET = BioClass()
    #adding two BioClass
    WATER = BioClass()
    HIV = BioClass()
    HIVDROPLET.add_Classes([WATER,HIV])
    #defining components of HIV
    ENVELOPE = BioClass()
    INSIDE = BioClass()
    
    HIV.add_Classes([ENVELOPE,INSIDE])

    #defining components of ENVELOPE
    LIPIDS = BioClass()
    UPROTEIN = BioClass()
    MAMATRIX = BioClass()
    SUTMCOMPLEX = BioClass()
    NEF = BioClass()
    ENVELOPE.add_Classes([LIPIDS,UPROTEIN,MAMATRIX,SUTMCOMPLEX,NEF])

    #defining components of INSIDE
   
    OUTERVOLUMEN = BioClass()
    CAPSID = BioClass()
    
    INSIDE.add_Classes([OUTERVOLUMEN,CAPSID])

    #defining components of OUTERVOLUMEN
    CAPSIDPROTEIN = BioClass()
    REVTRANS = BioClass()
    INTEGRASE = BioClass()
    PROTEASE = BioClass()
    VIRPROTR = BioClass()
    VIRINFFAC = BioClass()

    OUTERVOLUMEN.add_Classes([CAPSIDPROTEIN,REVTRANS,INTEGRASE,PROTEASE,VIRPROTR,VIRINFFAC])

    #defining components of CAPSID
    INNERVOLUMEN = BioClass()
    CAPSIDHULL = BioClass()

    INSIDE.add_Classes([CAPSIDHULL,INNERVOLUMEN])

    #defining components of CAPSIDHULL
    INSIDE.add_Classes([CAPSIDPROTEIN])

    #defining components of CAPSIDHULL
    GENOME = BioClass()
    NUCLEOCAPSIDPROT = BioClass()
    TRANSACTTRANS = BioClass()
    
    INNERVOLUMEN.add_Classes([GENOME,NUCLEOCAPSIDPROT,TRANSACTTRANS])

    #defining models:
    
    
    

    
    #add a continous model to the droplet
    HIVdroplet.add_continous_model()
    #select a model describing a continum and single object within
    HIVdroplet.cmodel.load_type('objectincontinum')
    HIVdroplet.cmodel.continum.model('droplet')
    HIVdroplet.cmodel.continum.objectclass = Water
    HIVdroplet.cmodel.object = HIV
    HIVdroplet.cmodel.size = 200

    #adding atomic definition to water
    Water.load_type('molecule')
    Water.add_discrete_model()
    Water.dmodel.load_pdb('water.pdb')

    #defining components of HIV
    Envelope = BioObject()
    Outervolumen = BioObject()
    Capsid = BioObject()
    Innervolumen = BioObject()


    
    #creating of a droplet object
    HIVdroplet = BioObject()
    #adding two bioobjects
    Water = BioObjectClass()
    HIV = BioObject()
#    HIVdroplet.add_subobject([Water,HIV])
    #add a continous model to the droplet
    HIVdroplet.add_continous_model()
    #select a model describing a continum and single object within
    HIVdroplet.cmodel.load_type('objectincontinum')
    HIVdroplet.cmodel.continum.model('droplet')
    HIVdroplet.cmodel.continum.objectclass = Water
    HIVdroplet.cmodel.object = HIV
    HIVdroplet.cmodel.size = 200

    #adding atomic definition to water
    Water.load_type('molecule')
    Water.add_discrete_model()
    Water.dmodel.load_pdb('water.pdb')

    #defining components of HIV
    Envelope = BioObject()
    Outervolumen = BioObject()
    Capsid = BioObject()
    Innervolumen = BioObject()

    #add components to HIV
    HIV.add_subobjects([Envelope,Outervolumen,Capsid,Innervolumen])
    
    #envelope
    Envelope.add_continous_model()
    Envelope.cmodel.load_type('vesicle')
    Envelope.cmodel.diameter = 110
    #add lipids and membrane proteins
    Lipids  = BioObjectClass(load='lipids')
    
    
    Envelope.cmodel.
    
    
    
    HIVdroplet.add_
    HIVdroplet.cmodel.load_type('objectincontinum')
    #setting size of water droplet to 12
    HIVdroplet.cmodel.size = 12
    #specifing the object 
    HIV = BioObject()
    HIVdroplet.cmodel.size 
     
    

# Build scenario

# Define features for input object protein
class protein():
    # define protein info
    def __init__(self,pdbin):
	# primarykey = pdb_id_uniprot_id
        # pdb_id
	# uniprot_id
	# aa_seq
	# pfam_id
	# GO_id
	# GO_type
	# EC_id
	# KEGG_id
	# KEGG_pathway
	# prot_color (attribute a color to each KEGG pathway in /data)
	# gene_id
	# entrez_id
	# NT_seq
	pass

    # if protein complex, define chains (apply everythin for each chain)
    def prot_complex(self):
	# def an array of chains for chain_id
	pass

    # get and clean the PDB file from database
    def get_clean_pdb(self):
        # request pdb files from Protein Data bank
        PDB = 'ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb'+pdbin+'.ent.gz'
        wget.download(PDB)
        gzip.open('pdb'+pdbin+'.ent.gz', 'rb')
	# save coordinates in a dataframe or something

    # obtain aa sequence
    def get_aa_seq(self):
	# query from uniprot_id -> seq in website aa_seq

        # get seq from pdb file with possible gaps and mutations aa_seq_pdb
        p = PDBParser() 
        aa_seq_pdb = p.get_structure(pdbin, './PDB/pdb'+pdbin+'.ent')
        io = PDBIO()
        io.set_structure(aa_seq_pdb)
        io.save('./PDB/'+pdbin+'.pdb')
        print 'This is the sequence of '+pdbin+':\n', aa_seq_pdb
        return aa_seq_pdb 

    # define the ligands, inhibitors, effectors...
    def compounds_prot(self):
	# get KEEG_chemicals for that KEGG_id
	pass

    # Generate a modell of the protein '/home/celsa/Documents/Pompeu Fabra/SBI/steps.txt' 
    def model_prot(self):
        # development in further steps when aa_seq_pdb != aa_seq 
        print "1. Get seq of the protein \n2. Find other seqs similar \n3. Find structures \n3.a. Build modell \n3.b.1. Predict secondary structure in gap \n3.b.2. Build modell by secondary structure prediction"

    # generate the dataframe for user and server (json format)
    def gen_dataframe(self):
	# ids for user
	# all info in server
        pass

class lipid():
    def __init__(self, unitcell_struc):
	# list of lipids ids in /data
	# list of structures in /data
	# primary key integer
	# lip_id 
        # give color (by type of lipid get from /data)
	pass
    
    # get coordinates
    def lip_coord(self):
	#parse the pdb and get xyz coord
	pass

    # generate the dataframe for user and server (json format)
    def gen_dataframe(self):
        # ids for user
        # all info in server
        pass

class compounds():
    def __init__(self, chemid, protid):
	# def function (substrate, ligand, effector, inhibitor)
	# def color (make a list of important compounds and specific colors in /data and also colors for each function)
	pass

class nucleotide():
    def __init__(self, protid):
	# get gene_id
	# get entrez_id
	pass	

class item_cellcraft():
    def __init__(self, threshold, blocksize):
	# define threshold
	# get name of item
	# define blocksize
	pass

    # rotate item if needed to center 
    def move_item(self, refrot, reftrans):
	# transport item to ref position
	# get the rotated structures of item for given refs
	pass

    # define the volume that item will need 
    def vol_prot(self):
        # calculate the vol each needs
        pass

    # parse item throuh the grid
    def def_blocks(self):
        # generate a 3d grid for my coordinates
        # get volumen of my item to know boundaries according to blocksize units defined
        # use a 3d histogram (numpy 3d bin)
        # define empty or full by threshold
        pass

    # translate grid into cellcraft format
    def def_cellcraftinput(self):
        pass

    # define the item in cellpack format
    def def_cellpackinput(self):
	pass

    # define the moment the data is requested    
    def date_time(self):
        # date and time of the data generation



# use autopack/cellpack to generate it
class envelope():
    def __init__(self, unitcell_struc, items, percentage):
	# define unit cell (collada or whatever)
	# percentage
	# items (cellpack format)
	pass	

    # generate the package
    def gen_envelope(self):
	# parse through cellpack
	pass






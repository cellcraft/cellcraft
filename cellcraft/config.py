from collections import defaultdict

############# TODO
### generate an algorithm that predicts color and texture of blocks taking into account a) biological features (GOterms) b) n_chains c) type of complex (prot complex, membrane, dna...)
### it should be a method in ProteinComplex(), Membrane() and Dna() instead of particular of each item (Protein(),Lipid()...)

# colors EC id:color id
col = {'1': 6, '2': 1, '3': 9, '4': 2, '5': 5, '6': 4, '0': 7}

# testure path name:texture id
text = defaultdict(list)
names = ['Metabolism', 'Genetic Information Processing', 'Human Diseases', 'Drug Development',
         'Environmental Information Processing', 'Cellular Processes', 'Organismal Systems']

# texture 95 crystal, 159 full, 35 wool
textures = ['159', '35', '35', '35', '95', '95', '95']
for t, n in zip(textures, names):
    text[t].append(n)

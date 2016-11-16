# -*- coding: utf-8 -*-
"""
Define functions, constants and exceptions for PathWalue application.

Functions
---------
determine_intermediates :  find intermediate compounds
evaluate_input :  process PathWalue user input
evaluate_pathway :  evaluate pathway
filter_pathway :  filter pathways by enzymes
find_pathway :  find a pathway between reactions
format_compound :  collect compound data to ouput
format_pathway :  collect pathway data to output
format_output :  collect data to output
format_reaction :  collect reaction data to output
intersect_dict :  return an intersect of dict and an iterable of keys
initialize_graph :  initialize networkx.DiGraph for pathway searching
nbest_items :  return n highest value items
order_pathway_data :  collect pathway data for evaluation
pair_reactions :  pair reactions for pathway searching
get_content :  return contents of a text file
get_json :  return object written in a JSON file
get_names :  return filenames in a directory
write_json :  write an object to a JSON file
write_jsons :  write objects to JSON files

Constants
---------
DELIMITER_TSV :  tab character in tsv files
PATH_CHEBI :  directory path to ChEBI files
PATH_INTENZ :  directory path to IntEnz files
PATH_JSON :  directory path to JSON files
PATH_RHEA :  directory path to Rhea files
PATH_RD :  directory path to Rhea reaction data files
CHEBI_COMPOUNDS :  filename for ChEBI compound data
CHEBI_DATA :  filename for ChEBI chemical data
CHEBI_RELATIONS :  filename for ChEBI relation data
CHEBI_VERTICES :  filename for ChEBI vertex data
INTENZ :  filename for IntEnz data
FILE_CMP_CHARGES :  JSON filename for ChEBI ID to charge mapping
FILE_CMP_DEMANDS :  JSON filename for ChEBI ID to demand mapping
FILE_CMP_FORMULAE :  JSON filename for ChEBI ID to formula mapping
FILE_CMP_MASSES :  JSON filename for ChEBI ID to mass mapping
FILE_CMP_PARENTS :  JSON filename for ChEBI ID to parent ID mapping
FILE_CMP_PRICES :  JSON filename for ChEBI ID to price mapping
FILE_CMP_REACTIONS :  JSON filename for compound to reaction mapping
FILE_CMP_RELATIONS :  JSON filename for ChEBI ID to relations mapping
FILE_EC_NAMES :  JSON filename for EC number to enzyme name mapping
FILE_EC_REACTIONS :  JSON filename for EC number to Rhea ID mapping
FILE_RXN_COMPLEXITIES :  JSON filename for Rhea ID to complexity mapping
FILE_RXN_ECS :  JSON filename for Rhea ID to EC number mapping
FILE_RXN_EQUATIONS :  JSON filename for Rhea ID to equation mapping
FILE_RXN_STOICIOMETRICS :  JSON filename for Rhea ID to stoichiometrics
RHEA_RC :  filename for Rhea EC data

Exceptions
----------
ChEBIIDError :  given ChEBI ID is not recognized
ECNumberError :  given EC number is not recognized
RheaIDError :  given Rhea ID is not recognized
DirectoryNotFoundError :  given directory path is not recognized


PEP 257:
The docstring of a script (a stand-alone program) should be usable as
its "usage" message, printed when the script is invoked with incorrect
or missing arguments (or perhaps with a "-h" option, for "help"). Such
a docstring should document the script's function and command line
syntax, environment variables, and files. Usage messages can be fairly
elaborate (several screens full) and should be sufficient for a new
user to use the command properly, as well as a complete quick reference
to all options and arguments for the sophisticated user.

The docstring for a module should generally list the classes,
exceptions and functions (and any other objects) that are exported by
the module, with a one-line summary of each. (These summaries generally
give less detail than the summary line in the object's docstring.) The
docstring for a package (i.e., the docstring of the package's
__init__.py module) should also list the modules and subpackages
exported by the package.

The docstring for a function or method should summarize its behavior
and document its arguments, return value(s), side effects, exceptions
raised, and restrictions on when it can be called (all if applicable).
Optional arguments should be indicated. It should be documented whether
keyword arguments are part of the interface.

The docstring for a class should summarize its behavior and list the
public methods and instance variables. If the class is intended to be
subclassed, and has an additional interface for subclasses, this
interface should be listed separately (in the docstring). The class
constructor should be documented in the docstring for its __init__
method. Individual methods should be documented by their own docstring.

If a class subclasses another class and its behavior is mostly
inherited from that class, its docstring should mention this and
summarize the differences. Use the verb "override" to indicate that a
subclass method replaces a superclass method and does not call the
superclass method; use the verb "extend" to indicate that a subclass
method calls the superclass method (in addition to its own behavior).

"""

import collections as cl
import itertools as it
import heapq as hq  # Used in finding n max values from a list.
import math as m

import networkx as nx

import json
import os


# Constants.
DELIMITER_TSV = '\t'

# File extensions.
_EXTENSION_DAT = '.dat'
_EXTENSION_JSON = '.txt'
_EXTENSION_TSV = '.tsv'
_EXTENSION_RD = '.rd'

# Directory paths.
_BASE_DIR = os.path.normpath('P:/My Documents/Spyder/PathWalue/webapp')
_PATH_DATA = os.path.join(_BASE_DIR, 'data')
PATH_CHEBI = os.path.join(_PATH_DATA, 'chebi')
PATH_INTENZ = os.path.join(_PATH_DATA, 'intenz')
PATH_JSON = os.path.join(_PATH_DATA, 'json')
PATH_RHEA = os.path.join(_PATH_DATA, 'rhea')
PATH_RD = os.path.join(PATH_RHEA, 'rd')

# ChEBI files.
CHEBI_COMPOUNDS = 'compounds' + _EXTENSION_TSV
CHEBI_DATA = 'chemical_data' + _EXTENSION_TSV
CHEBI_RELATIONS = 'relation' + _EXTENSION_TSV
CHEBI_VERTICES = 'vertice' + _EXTENSION_TSV

# IntEnz files.
INTENZ = 'enzyme' + _EXTENSION_DAT

# JSON files.
_PREFIX_CMP = 'cmp_'
FILE_CMP_CHARGES = _PREFIX_CMP + 'charges' + _EXTENSION_JSON
FILE_CMP_DEMANDS = _PREFIX_CMP + 'demands' + _EXTENSION_JSON
FILE_CMP_FORMULAE = _PREFIX_CMP + 'formulae' + _EXTENSION_JSON
FILE_CMP_MASSES = _PREFIX_CMP + 'masses' + _EXTENSION_JSON
FILE_CMP_NAMES = _PREFIX_CMP + 'names' + _EXTENSION_JSON
FILE_CMP_PARENTS = _PREFIX_CMP + 'parents' + _EXTENSION_JSON
FILE_CMP_PRICES = _PREFIX_CMP + 'prices' + _EXTENSION_JSON
FILE_CMP_REACTIONS = _PREFIX_CMP + 'reactions' + _EXTENSION_JSON
FILE_CMP_RELATIONS = _PREFIX_CMP + 'relations' + _EXTENSION_JSON
FILE_CMP_VALUES = _PREFIX_CMP + 'values' + _EXTENSION_JSON

FILE_EC_NAMES = 'ec_names' + _EXTENSION_JSON
FILE_EC_REACTIONS = 'ec_reactions' + _EXTENSION_JSON

_PREFIX_RXN = 'rxn_'
FILE_RXN_COMPLEXITIES = _PREFIX_RXN + 'complexities' + _EXTENSION_JSON
FILE_RXN_ECS = _PREFIX_RXN + 'ecs' + _EXTENSION_JSON
FILE_RXN_EQUATIONS = _PREFIX_RXN + 'equations' + _EXTENSION_JSON
FILE_RXN_STOICHIOMETRICS = _PREFIX_RXN + 'stoichiometrics' + _EXTENSION_JSON

# Rhea files.
RHEA_EC = 'ec-rhea-dir' + _EXTENSION_TSV


_IGNORED_COMPOUNDS = set((
    '15377',  # H2O water
    '29242',  # AsH2O3
    '48597',  # AsHO4
    '15858',  # Br
    '16183',  # CH4 methane
    '17245',  # CO carbon monoxide
    '16526',  # CO2 carbon dioxide
    '17996',  # Cl chloride
    '85033',  # Co(1+) cobalt
    '49552',  # Cu(+) copper
    '29036',  # Cu(2+) copper
    '17051',  # F fluoride
    '29033',  # Fe(2+) iron
    '29034',  # Fe(3+) iron
    '15378',  # H(+) hydron
    '18276',  # H2
    '18407',  # HCN hydrogen cyanide
    '17544',  # HCO3 hydrogencarbonate
    '16240',  # H2O2 hydrogen peroxide
    '43473',  # HPO4 hydrogenphosphate
    '33019',  # HP2O7 diphosphate
    '29919',  # HS hydrosulfide
    '16382',  # I iodide
    '78619',  # iron(III) oxide-hydroxide(1-)
    '17997',  # N2
    '28938',  # NH4(+)
    '84879',  # NHO
    '16480',  # NO nitric oxide
    '17045',  # N2O dinitrogen oxide
    '16301',  # NO2(-) nitrite
    '17632',  # NO3(-) nitrate
    '29101',  # Na(+)
    '43474',  # PO4
    '15379',  # O2 dioxygen
    '18421',  # O2 superoxide
    '26833',  # S sulfur atom
    '17359',  # SO3 sulfite
    '16189',  # SO4 sulfate
    '29256',  # thiol
    '18036',  # triphosphate
    '58339',  # 3'-phosphonato-5'-adenylyl sulfate(4-)
    '58343',  # adenosine 3',5'-bismonophosphate(4-)
    # Factors
    '73299',  # cobalt(II)-factor III(8-)
    '85471',  # cobalt(II)-factor IV(6-)
    # Hormones
    '83274',  # juvenile hormone III carboxylate
    '15581',  # juvenile hormone II
    '27493',  # juvenile hormone III
    '83641',  # juvenile hormone I
    '87109',  # juvenile hormone I carboxylate
    # Residues
    '65264',  # dodecanoyl-pantetheine-4-phosphorylserine(1-) residue
    '82657',  # deoxyhypusine(2+) residue
    '78457',  # O-[S-(3R)-hydroxyhexanoylpantetheine-4'-phosphoryl]s... residue
    '74419',  # 2-thio-N(6)-L-threonylcarbamoyladenine 5'-monophosph... residue
    '79032',  # O-[S-(dihydromonacolin L carboxy)pantetheine-4'-phos... residue
    '87079',  # N-acetyl-beta-D-glucosaminyl-(1->3)-N-acetyl-alpha-D... residue
    '78461',  # O-[S-(3R)-hydroxyoctanoylpantetheine-4-phosphoryl]se... residue
    '74455',  # 5-methylaminomethyl-2-thiouridine 5'-monophosphate z... residue
    '88221',  # N(omega),N('omega)-dimethyl-L-arginine(1+) residue
    '74481',  # N(2)-methylguanosine 5'-monophosphate(1-) residue
    '29950',  # L-cysteine residue
    '83690',  # N-terminal N-acetyl-L-serine residue
    '64315',  # 4-demethylwyosine 5'-monophosphate(1-) residue
    '78449',  # O-(S-malonylpantetheine-4'-phosphoryl)serine(2-) residue
    '85305',  # S-3-[(2R)-phycourobilin]-L-cysteine(2-) residue
    '16044',  # L-methionine residue
    '29973',  # L-glutamate residue
    '82693',  # 2-[(3S)-3-carboxylato-3-(methylammonio)propyl]-L-his... residue
    '78470',  # O-[S-(3R)-hydroxydodecanoylpantetheine-4-phosphoryl]... residue
    '85958',  # 5'-(N(7)-methyl 5'-triphosphoguanosine)-2'-O-methyla... residue
    '78778',  # O-[S-(11Z)-hexadecenoylpantetheine-4'-phosphoryl]ser... residue
    '83111',  # N(6)-[(R)-S(8)-acetyldihydrolipoyl]-L-lysine residue
    '90675',  # ribonucleotide residue(1-)
    '83144',  # biotinyl-L-lysine residue
    '83561',  # N-terminal L-phenylalanyl-L-alpha-amino acid(1+) residue
    '83545',  # agmatidine 5'-phosphate(1+) residue
    '78458',  # O-[S-(2E)-hexenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '85027',  # 2'-phospho-nucleotide 5'-phosphate(3-) residue
    '30011',  # L-glutamine residue
    '79005',  # diphthine methyl ester residue
    '90516',  # L-leucinate residue
    '78598',  # N-terminal Nalpha-acetylamino-acid residue
    '82795',  # gamma-methyl L-glutamate residue
    '78454',  # O-(S-butanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '90975',  # O(4)-(N-acetyl-alpha-D-galactosaminyl)-trans-4-hydro... residue
    '74275',  # 7-[(3S)-(3-amino-3-methoxycarbonyl)propyl]wyosine 5'... residue
    '87080',  # N-acetyl-beta-D-glucosaminyl-(1->3)-N-acetyl-alpha-D... residue
    '74483',  # 5-methylcytidine 5'-monophosphate(1-) residue
    '83683',  # N-terminal N-acetyl-L-alanine residue
    '74491',  # N(1)-methyladenosine 5'-monophosphate(1-) residue
    '61976',  # N(6),N(6)-dimethyl-L-lysine(1+) residue
    '62836',  # 2-methylthio-N(6)-(cis-4-hydroxy-Delta(2)-isopenteny... residue
    '78467',  # O-[S-(2E)-decenoylpantetheine-4-phosphoryl]serine(1-) residue
    '85644',  # UMP 2',3'-cyclic phosphate(2-) residue
    '82883',  # nucleotide 5'-phosphate(1-) residue
    '82620',  # L-tyrosine-O-phosphate(2-) residue
    '74420',  # 2-methylthio-N(6)-L-threonylcarbamoyladenine 5'-mono... residue
    '45764',  # L-methionine (R)-S-oxide residue
    '82696',  # diphthine betaine residue
    '78818',  # O-(S-3-oxopentanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '74447',  # 5-methyluridine 5'-monophosphate(1-) residue
    '78809',  # N(6)-octanoyl-L-lysine residue
    '78466',  # O-[S-(3R)-hydroxydecanoylpantetheine-4-phosphoryl]se... residue
    '83562',  # N-terminal L-arginyl-L-alpha-amino acid(2+) residue
    '83556',  # N-terminal L-leucyl-L-alpha-amino acid(1+) residue
    '64837',  # N(pros)-phosphonato-L-histidine residue
    '74898',  # 3'-end 2'-O-methylribonucleotide(1-) residue
    '87131',  # O-(S-L-2-amino-6-adipoylpantetheine-4'-phosphoryl)-L... residue
    '82695',  # 2-[(3S)-3-carboxylato-3-(dimethylammonio)propyl]-L-h... residue
    '73550',  # 4-demethyl-7-(3-amino-3-carboxypropyl)wyosine 5'-mon... residue
    '78779',  # O-[S-(13Z)-3-oxooctadecenoylpantetheine-4'-phosphory... residue
    '73543',  # 7-[(3S)-3-amino-3-carboxypropyl]wyosine 5'-monophosp... residue
    '90783',  # C-terminal S-(Gly-Gly)-L-Cys zwitterion residue
    '90616',  # N(6)-methyl-dAMP(1-) residue
    '29999',  # L-serine residue
    '50347',  # L-asparagine residue
    '64479',  # O-(pantetheine-4'-phosphoryl)serine(1-) residue
    '83145',  # carboxybiotinyl-L-lysine(1-) residue
    '90615',  # dAMP(1-) residue
    '78823',  # O-(S-3-oxo-4-methylhexanoylpantetheine-4'-phosphoryl... residue
    '78599',  # (gamma-L-glutamyl) N-terminal alpha-amino-acid zwitt... residue
    '85448',  # 6-O-methyl dGMP(1-) residue
    '61965',  # trans-4-hydroxy-L-proline residue
    '86021',  # S-geranylgeranyl-L-cysteine residue
    '74257',  # FMN-L-threonine(2-) residue
    '90870',  # 3-iodo-L-tyrosine residue
    '83421',  # O-phospho-L-serine(2-) residue
    '78468',  # O-(S-decanoylpantetheine-4-phosphoryl)serine(1-) residue
    '74416',  # 2-thio-N(6)-dimethylallyladenine 5'-monophosphate(1-) residue
    '78450',  # O-(S-acetoacetylpantetheine-4'-phosphoryl)serine(1-) residue
    '83441',  # O-[S-(3R)-hydroxyicosanoylpantetheine-4-phosphoryl]s... residue
    '82612',  # S-methyl-L-cysteine residue
    '83100',  # N(6)-[(R)-dihydrolipoyl]-L-lysine residue
    '16692',  # diphthamide residue
    '90511',  # S-[(2E,6E)-farnesyl]-L-cysteine methyl ester residue
    '78475',  # O-[S-(2E)-tetradecenoylpantetheine-4-phosphoryl]seri... residue
    '61891',  # N(5)-methyl-L-glutamine residue
    '90602',  # uridylyl-L-tyrosine(1-) residue
    '78597',  # N-terminal alpha-amino-acid(1+) residue
    '61897',  # N(omega),N(omega)-dimethyl-L-arginine(1+) residue
    '29965',  # L-argininium residue
    '86110',  # O-[S-(6Z)-hexadecenoylpantetheine-4'-phosphoryl]seri... residue
    '74478',  # 2'-O-methyluridine 5'-monophosphate(1-) residue
    '83143',  # N(6)-[(R)-S(8)-ammoniomethyldihydrolipoyl]-L-lysine(1+) residue
    '85452',  # dCMP(1-) residue
    '29969',  # L-lysinium residue
    '74851',  # 5-(2-methoxy-2-oxoethyl)uridine 5'-monophosphate residue(1-)
    '78820',  # O-(S-3-oxo-4-methylpentanoylpantetheine-4'-phosphory... residue
    '82697',  # N-(ADP-D-ribosyl)diphthamide(1-) residue
    '83064',  # 3'-end ribonucleotide 2',3'-cyclic phosphate(2-) residue
    '83834',  # peptidylproline (omega=180) residue
    '74493',  # N(6),N(6)-dimethyladenosine 5'-monophosphate(1-) residue
    '82683',  # O-[2'-(5-phosphoribosyl)-3'-dephospho-CoA]-L-serine(3-) residue
    '83624',  # O-adenyl-L-tyrosine(1-) residue
    '83062',  # 3'-end ribonucleotide 3'-phosphate(3-) residue
    '87831',  # N(6)-malonyl-L-lysine(1-) residue
    '131803',  # L-allysine residue
    '65286',  # L-tyrosine-O-sulfate(1-) residue
    '78480',  # O-[S-(3R)-hydroxyhexadecanoylpantetheine-4'-phosphor... residue
    '78453',  # O-[S-(2E)-butenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '73544',  # wybutosine 5'-monophosphate(1-) residue
    '74480',  # N(7)-methylguanosine 5'-phosphate zwitterion residue
    '78824',  # O-(S-3-oxoheptanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '85445',  # dGMP(1-) residue
    '74445',  # 2'-O-methylguanosine 5'-monophosphate(1-) residue
    '74454',  # 5-aminomethyl-2-thiouridine 5'-monophosphate zwitterion residue
    '78296',  # (3S)-3-ammonio-3-(3-chloro-4,5-dihydroxyphenyl)propa... residue
    '30013',  # L-threonine residue
    '90510',  # S-[(2E,6E)-farnesyl]-L-cysteinate residue
    '84990',  # gamma-carboxy-L-glutamate(2-) residue
    '74882',  # 5-(carboxymethyl)uridine 5'-monophosphate(2-) residue
    '74900',  # N(4)-acetylcytidine 5'-monophosphate(1-) residue
    '61963',  # 3-disulfanyl-L-alanine residue
    '29961',  # L-aspartate residue
    '74508',  # 5-carboxymethylaminomethyluridine 5'-monophosphate(1-) residue
    '78462',  # O-[S-(2E)-octenoylpantetheine-4-phosphoryl]serine(1-) residue
    '131709',  # N(6)-(1-hydroxy-2-oxopropyl)-L-lysine residue(1+)
    '131913',  # O-[S-3,5-dihydroxy-4-methylanthranilyl]serine(1-) residue
    '61929',  # N(6)-methyl-L-lysinium residue
    '78456',  # O-(S-3-oxohexanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '78822',  # O-(S-3-oxo-5-methylhexanoylpantetheine-4'-phosphoryl... residue
    '87215',  # N-terminal 5-oxo-L-proline residue
    '90840',  # O-(N-acetyl-beta-D-glucosaminyl)-L-threonine residue
    '88222',  # N(5)-methyl-argininium(1+) residue
    '74151',  # S-palmitoyl-L-cysteine residue
    '78446',  # O-(S-acetylpantetheine-4'-phosphoryl)serine(1-) residue
    '78846',  # O-(S-pimeloylpantetheine-4'-phosphoryl)serine(2-) residue
    '78442',  # AMP 3'-end(1-) residue
    '83739',  # ferroheme c di-L-cysteine(2-) residue
    '78826',  # O-(S-3-oxononanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '83665',  # lysidine monophosphate zwitterion residue
    '78294',  # (3R)-3-hydroxy-L-argininium residue
    '90420',  # N(6)-(3-O-phospho-D-ribulosyl)-L-lysinium residue
    '87169',  # S-sulfo-L-cysteine(1-) residue
    '83142',  # N(6)-[(R)-S(8)-isobutyryldihydrolipoyl]-L-lysine residue
    '83440',  # O-(S-3-oxoicosanoylpantetheine-4'-phosphoryl)-L-seri... residue
    '82852',  # inosine 5'-phosphate(1-) residue
    '87075',  # N-acetyl-alpha-D-galactosaminyl-L-threonine residue
    '74543',  # 8-methyladenosine 5'-monophosphate(1-) residue
    '78488',  # O-[S-(3R)-hydroxyoctadecanoylpantetheine-4'-phosphor... residue
    '44120',  # L-methionine (S)-S-oxide residue
    '61930',  # N(6)-acetyl-L-lysine residue
    '87828',  # N(6)-glutaryl-L-lysine(1-) residue
    '83099',  # N(6)-[(R)-lipoyl]-L-lysine residue
    '74486',  # N(3)-methylpseudouridine 5'-monophosphate(1-) residue
    '62866',  # 2-methylthio-N(6)-(Delta(2)-isopentenyl)adenosine residue
    '83120',  # N(6)-[(R)-S(8)-succinyldihydrolipoyl]-L-lysine(1-) residue
    '83960',  # N(omega)-(ADP-D-ribosyl)-L-arginine(1-) residue
    '86299',  # O-[S-5-hexynoylpantetheine-4'-phosphoryl]serine(1-) residue
    '90873',  # dehydroalanine residue
    '90610',  # O-[S-2,3-dihydroxybenzoylpantetheine-4'-phosphoryl]-... residue
    '90838',  # O-(N-acetyl-beta-D-glucosaminyl)-L-serine residue
    '87830',  # N(6)-succinyl-L-lysine(1-) residue
    '90874',  # 3,3',5-triiodo-L-thyronine residue
    '83071',  # tRNA 3'-terminal nucleotidyl-cytidyl-cytidyl-adenosi... residue
    '74513',  # N(2),N(2)-dimethylguanosine 5'-monophosphate(1-) residue
    '87078',  # N-acetyl-alpha-D-galactosaminyl-L-serine residue
    '90418',  # N(6)-D-ribulosyl-L-lysinium residue
    '16367',  # N(tele)-methyl-L-histidine residue
    '78477',  # O-(S-tetradecanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '78483',  # O-(S-hexadecanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '83226',  # N(omega)-phospho-L-arginine(1-) residue
    '75591',  # 3-hydroxy-L-aspartate residue
    '85643',  # 3'-terminal pUpU(2-) residue
    '76179',  # O-(S-acylpantetheine-4'-phosphoryl)serine(1-) residue
    '65315',  # UMP(1-) residue
    '78495',  # O-(S-octadecanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '50342',  # L-proline residue
    '74890',  # N(1)-methylpseudouridine 5'-monophosphate(1-) residue
    '78489',  # O-[S-(2E)-octadecenoylpantetheine-4'-phosphoryl]seri... residue
    '83833',  # peptidylproline (omega=0) residue
    '74506',  # N(4)-methylcytidine 5'-monophosphate(1-) residue
    '78481',  # O-[S-(2E)-hexadecenoylpantetheine-4'-phosphoryl]seri... residue
    '74495',  # 2'-O-methylcytidine 5'-monophosphate(1-) residue
    '78827',  # O-[S-(3R)-3-hydroxyacylpantetheine-4'-phosphoryl]ser... residue
    '82831',  # queuosine 5'-phosphate zwitterion residue
    '74511',  # 5-carboxymethylaminomethyl-2'-O-methyluridine 5'-mon... residue
    '131710',  # S-(1-hydroxy-2-oxopropyl)-L-cysteine residue
    '78487',  # O-(S-3-oxooctadecanoylpantetheine-4'-phosphoryl)seri... residue
    '131912',  # O-[S-3-hydroxy-4-methylanthranilyl]serine(1-) residue
    '82764',  # O-[S-2-methylbutanoylpantetheine-4'-phosphoryl]serin... residue
    '85339',  # O-[S-(L-alloisoleucyl)pantetheine-4'-phosphoryl]seri... residue
    '74497',  # 2-methyladenosine 5'-monophosphate(1-) residue
    '78464',  # O-(S-3-oxodecanoylpantetheine-4-phosphoryl)serine(1-) residue
    '82930',  # 3-(3-amino-3-carboxypropyl)uridine 5'-phosphate(1-) residue
    '78460',  # O-(S-3-oxooctanoylpantetheine-4-phosphoryl)serine(1-) residue
    '74418',  # N(6)-L-threonylcarbamoyladenine 5'-monophosphate(2-) residue
    '83697',  # N(5)-alkyl-L-glutamine residue
    '90676',  # 2'-O-methylribonucleotide(1-) residue
    '131610',  # O-(beta-L-arabinofuranosyl)-trans-4-hydroxy-L-proline residue
    '85959',  # 5'-(N(7)-methyl 5'-triphosphoguanosine)-N(7),2'-O-di... residue
    '29979',  # L-histidine residue
    '90871',  # 3,5-diiodo-L-tyrosine residue
    '85288',  # S-3-[(2R)-phycoviolobilin]-L-cysteine(2-) residue
    '78463',  # O-(S-octanoylpantetheine-4-phosphoryl)serine(1-) residue
    '82850',  # 7-cyano-7-carbaguanine 5'-phosphate(1-) residue
    '83151',  # glycyl-AMP(1-) residue
    '29998',  # D-serine residue
    '82748',  # CMP(1-) residue
    '78459',  # O-(S-hexanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '78469',  # O-(S-3-oxododecanoylpantetheine-4-phosphoryl)serine(1-) residue
    '83586',  # N(tele)-phosphonato-L-histidine residue
    '82735',  # O-[S-(6-methoxycarbonylhexanoyl)pantetheine-4'-phosp... residue
    '15989',  # L-methionine S-oxide residue
    '74502',  # N(3)-methyluridine 5'-monophosphate(1-) residue
    '65280',  # N(omega)-methyl-argininium(1+) residue
    '74449',  # N(6)-methyladenosine 5'-monophosphate(1-) residue
    '83989',  # O-[S-(9Z)-hexadecenoylpantetheine-4'-phosphoryl]seri... residue
    '85961',  # 5'-triphosphoguanosine(3-) residue
    '78472',  # O-[S-(2E)-dodecenoylpantetheine-4-phosphoryl]serine(1-) residue
    '78798',  # O-[S-(3Z)-decenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '85189',  # O-[(9Z)-hexadecenoyl]-L-serine residue
    '90619',  # C-terminal N-glycylaminoethanethioic S-acid residue
    '90872',  # L-thyroxine residue
    '78845',  # O-[S-(methoxycarbonylacetyl)pantetheine-4'-phosphory... residue
    '85919',  # O-[S-(4Z)-hexadecenoylpantetheine-4'-phosphoryl]seri... residue
    '61977',  # O-phosphonato-L-threonine(2-) residue
    '78784',  # O-[S-(2E)-2-enoylpantetheine-4'-phosphoryl]-L-serine... residue
    '86019',  # S-[(2E,6E)-farnesyl]-L-cysteine residue
    '78474',  # O-[S-(3R)-hydroxytetradecanoylpantetheine-4-phosphor... residue
    '85454',  # 5-methyl dCMP(1-) residue
    '73542',  # N(1)-methylguanosine 5'-monophosphate(1-) residue
    '74477',  # 2'-O-methyladenosine 5'-monophosphate(1-) residue
    '82833',  # 7-aminomethyl-7-carbaguanine 5'-phosphate zwitterion residue
    '78776',  # O-(S-3-oxoacylpantetheine-4'-phosphoryl)-L-serine(1-) residue
    '74415',  # N(6)-dimethylallyladenine 5'-monophosphate(1-) residue
    '73603',  # 7-(2-hydroxy-3-amino-3-carboxypropyl)wyosine 5'-mono... residue
    '74417',  # 2-methylthio-N(6)-dimethylallyladenine 5'-monophosph... residue
    '85501',  # N(4)-(beta-D-glucosyl)-L-asparagine residue
    '82834',  # epoxyqueuosine 5'-phosphate zwitterion residue
    '65314',  # pseudouridine 5'-phosphate(1-) residue
    '86298',  # O-[S-5-hexenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '85280',  # S-3-[(2R)-phycocyanobilin]-L-cysteine(2-) residue
    '73995',  # 2-[(3S)-3-amino-3-carboxypropyl]-L-histidine zwitterion residue
    '90778',  # C-terminal Gly-Gly(1-) residue
    '74896',  # 3'-end ribonucleotide(1-) residue
    '74269',  # GMP(1-) residue
    '46858',  # L-tyrosine residue
    '78473',  # O-(S-3-oxotetradecanoylpantetheine-4-phosphoryl)seri... residue
    '90596',  # L-beta-isoaspartate residue
    '83397',  # L-citrulline residue
    '85279',  # S-3-[(2R)-phycoerythrobilin]-L-cysteine(2-) residue
    '74411',  # AMP(1-) residue
    '90598',  # L-aspartic acid alpha-methyl ester residue
    '78451',  # O-[S-(3R)-hydroxybutanoylpantetheine-4'-phosphoryl]s... residue
    '78297',  # (3S)-3-ammonio-3-(3-chloro-4-hydroxyphenyl)propanoyl residue
    '85428',  # trans-3-hydroxy-L-proline residue
    '50058',  # L-cystine residue
    '78785',  # O-(S-2,3-saturated acylpantetheine-4'-phosphoryl)ser... residue
    '78478',  # O-(S-3-oxohexadecanoylpantetheine-4'-phosphoryl)seri... residue
    '78783',  # O-(S-oleoylpantetheine-4'-phosphoryl)serine(1-) residue
    # Deoxyribonucleotides
    '61404',  # dATP(4-)
    '57667',  # dADP(3-)
    '58245',  # dAMP(2-)
    '61481',  # dCTP(4-)
    '58593',  # dCDP(3-)
    '57566',  # dCMP(2-)
    '61429',  # dGTP(4-)
    '58595',  # dGDP(4-)
    '57673',  # dGMP(4-)
    '61382',  # dITP(4-)
    '37568',  # dTTP(4-)
    '58369',  # dTDP(3-)
    '63528',  # dTMP(2-)
    '61555',  # dUTP(4-)
    '60471',  # dUDP(3-)
    '246422',  # dUMP(2-)
    # Ribonucleotides
    '30616',  # ATP(4-)
    '456216',  # ADP(3-)
    '456215',  # AMP(2-)
    '37563',  # CTP(4-)
    '58069',  # CDP(3-)
    '60377',  # CMP(2-)
    '37565',  # GTP(4-)
    '58189',  # GDP(3-)
    '58115',  # GMP(2-)
    '61402',  # ITP(4-)
    '58280',  # IDP(3-)
    '58053',  # IMP(2-)
    '46398',  # UTP(4-)
    '58223',  # UDP(3-)
    '57865',  # UMP(2-)
    '61314',  # XTP(4-)
    '59884',  # XDP(3-)
    '57464',  # XMP(2-)
    # Nucleosides
    '73316',  # 2'-deoxyribonucleoside 5'-diphosphate(3-)
    '131705',  # 2'-deoxynucleoside 3'-monophosphate(2-)
    '65317',  # 2'-deoxynucleoside 5'-monophosphate(2-)
    '58043',  # nucleoside 5'-monophosphate(2-)
    '61557',  # nucleoside triphosphate(4-)
    '58464',  # nucleoside 3',5'-cyclic phosphate anion
    '18274',  # 2'-deoxyribonucleoside
    '66949',  # nucleoside 3'-phosphate(2-)
    '83402',  # nucleoside 3',5'-bisphosphate(4-)
    '57930',  # nucleoside diphosphate(3-)
    '33838',  # nucleoside
    '13197',  # ribonucleoside 3'-monophosphate(2-)
    '61560',  # 2'-deoxyribonucleoside 5'-triphosphate(4-)
    '18254',  # ribonucleoside
    '57867',  # nucleoside 5'-phosphate dianion
    '78552',  # ribonucleoside 2'-monophosphate(2-)
    # Nucleotides
    '71310',  # Mo(VI)-molybdopterin guanine dinucleotide(2-)
    '66954',  # 2',3'-cyclic nucleotide(1-)
    '83064',  # 3'-end ribonucleotide 2',3'-cyclic phosphate(2-) residue
    '57439',  # (3Z)-phytochromobilin(2-)
    '62727',  # molybdopterin adenine dinucleotide(3-)
    '57502',  # nicotinate D-ribonucleotide(2-)
    '71308',  # Mo(VI)-molybdopterin cytosine dinucleotide(2-)
    '75967',  # nicotinate-adenine dinucleotide phosphate(4-)
    # Cofactors and -enzymes
    '16509',  # 1,4-benzoquinone
    '57530',  # 1,5-dihydrocoenzyme F420(4-)
    '16810',  # 2-oxoglutarate(2-)
    '175763',  # 2-trans,6-trans-farnesyl diphosphate(3-)
    '28889',  # 5,6,7,8-tetrahydropteridine
    '57454',  # 10-formyltetrahydrofolate(2-)
    '57288',  # acetyl-CoA(4-)
    '58342',  # acyl-CoA(4-)
    '64876',  # bacillthiol(1-)
    '60488',  # cob(I)alamin(1-)
    '16304',  # cob(II)alamin
    '28911',  # cob(III)alamin
    '57287',  # CoA(4-)
    '58319',  # coenzyme M(1-)
    '59920',  # coenzyme F420-1(4-)
    '57922',  # coenzyme gamma-F420-2(5-)
    '58596',  # coenzyme B(3-)
    '59923',  # coenzyme alpha-F420-3(6-)
    '83348',  # chlorophyllide a(2-)
    '71302',  # MoO2-molybdopterin cofactor(2-)
    '71305',  # WO2-molybdopterin cofactor(2-)
    '57692',  # FAD(3-)
    '58307',  # FADH2(2-)
    '33737',  # Fe2S2 di-mu-sulfido-diiron(2+)
    '33738',  # Fe2S2 di-mu-sulfido-diiron(1+)
    '57618',  # FMNH2
    '58210',  # FMN(3-)
    '57925',  # glutathionate(1-)
    '17594',  # hydroquinone
    '57384',  # malonyl-CoA(5-)
    '57540',  # NAD
    '57945',  # NADH
    '58349',  # NADP(3-)
    '57783',  # NADPH(4-)
    '17154',  # nicotinamide
    '16768',  # mycothiol
    '57387',  # oleoyl-CoA(4-)
    '57379',  # palmitoyl-CoA(4-)
    '18067',  # phylloquinone
    '28026',  # plastoquinol-9
    '28377',  # plastoquinone-9
    '59648',  # precursor Z(1-)
    '87467',  # prenyl-FMNH2(2-)
    '17310',  # pyridoxal
    '16709',  # pyridoxine
    '58442',  # pyrroloquinoline quinone(3-)
    '77660',  # pyrroloquinoline quinol(4-)
    '43711',  # (R)-dihydrolipoamide
    '76202',  # riboflavin cyclic 4',5'-phosphate(2-)
    '57856',  # S-adenosyl-L-homocysteine zwitterion
    '59789',  # S-adenosyl-L-methionine zwitterion
    '71177',  # tetrahydromonapterin
    '33723',  # tetra-mu3-suldifo-tetrairon(1+)
    '33722',  # tetra-mu3-suldifo-tetrairon(2+)
    # Porphyrins
    '62626',  # uroporphyrinogen I(8-)
    '62631',  # coproporphyrinogen I(4-)
    '131725',  # coproporphyrin III(4-)
    '60489',  # magnesium 13(1)-hydroxyprotoporphyrin 13-monomethyl ester(1-)
    '57307',  # protoporphyrinogen(2-)
    '57306',  # protoporphyrin(2-)
    '60490',  # magnesium 13(1)-oxoprotoporphyrin 13-monomethyl ester(1-)
    '57845',  # preuroporphyrinogen(8-)
    '60492',  # magnesium protoporphyrin(2-)
    '60491',  # magnesium protoporphyrin 13-monomethyl ester(1-)
    '57308',  # uroporphyrinogen III(8-)
    '57309',  # coproporphyrinogen III(4-)
    # Groups
    '60068',  # alpha-N-acetylneuraminyl-2,3-beta-D-galactosyl-1,3... group(1-)
    '18018',  # D-galactosyl-(1->4)-beta-D-glucosyl group
    '83148',  # glycino(1-) group
    '29917',  # thiol group
    '15876',  # beta-D-galactosyl-1,3-(N-acetyl-beta-D-glucosaminyl-1,... group
    '68550',  # triphosphate group(4-)
    '77037',  # N,N-dimethyl-L-alanyl group
    '78503',  # C-terminal-gamma-L-glutamyl-L-2-aminoadipate(3-) group
    '16361',  # alpha-N-acetylneuraminyl-2,3-beta-D-galactosyl group
    '17723',  # beta-D-galactosyl-1,3-(N-acetyl-D-glucosaminyl-1,6)-N-... group
    '78532',  # 3'-(L-prolyl)adenylyl zwitterionic group
    '17806',  # N-acetyl-beta-D-galactosaminyl group
    '78531',  # 3'-(L-phenylalanyl)adenylyl(1-) group
    '68546',  # phosphate group(2-)
    '68549',  # diphosphate group(3-)
    '16124',  # alpha-L-fucosyl-(1->2)-beta-D-galactosyl group
    '78517',  # 3'-(L-cysteinyl)adenylyl zwitterionic group
    '11936',  # N-acetyl-beta-D-glucosaminyl-(1->4)-beta-D-mannosyl group
    '16198',  # N-acetyl-beta-D-glucosaminyl-1,6-beta-D-galactosyl-1,4... group
    '75185',  # alpha-D-mannosyl group
    '78521',  # 3'-(L-glutaminyl)adenylyl zwitterionic group
    '79333',  # 3'-(D-alpha-aminoacyl)adenylyl zwitterionic group
    '11714',  # 3-(2,4-bis[N-acetyl-beta-D-glucosaminyl]-alpha-D-manno... group
    '17227',  # D-galactosyl-(1->3)-beta-D-galactosyl-(1->4)-beta-D-gl... group
    '17571',  # beta-D-galactosyl-(1->4)-N-acetyl-D-glucosaminyl group
    '78520',  # 3'-(L-glutamate)adenylyl(1-) group
    '12357',  # beta-D-galactosyl-(1->4)-N-acetyl-beta-D-glucosaminyl group
    '32591',  # alpha-D-mannosyl-(1->3)-beta-D-mannosyl group
    '78529',  # 3'-(L-lysyl)adenylyl(1+) group
    '49298',  # N-formyl-L-methionyl group
    '18914',  # beta-D-galactosyl-(1->3)-[alpha-L-fucosyl-(1->4)]-N-ac... group
    '12193',  # alpha-D-mannosyl-(1->6)-beta-D-mannosyl group
    '22783',  # beta-D-galactosyl-(1->3)-N-acetyl-D-galactosaminyl group
    '78499',  # C-terminal-gamma-L-glutamyl-L-2-aminoadipate 6-phospha... group
    '88115',  # N(2)-L-glutamino(1-) group
    '78530',  # 3'-(L-methionyl)adenylyl zwitterionic group
    '74432',  # N(2),N(2),N(7)-trimethylguanosine 5'-triphosphate(2-) group
    '5484',  # alpha-D-galactosyl-(1->3)-[alpha-L-fucosyl-(1->2)]-D-ga... group
    '64722',  # L-glutaminiumyl group
    '78516',  # 3'-(L-aspartate)adenylyl(1-) group
    '85224',  # alpha-hydroxyglycino(1-) group
    '32875',  # methyl group
    '16250',  # N-acetyl-beta-D-glucosaminyl-(1->3)-N-acetyl-D-galacto... group
    '12384',  # beta-D-mannosyl group
    '75191',  # N-acetyl-beta-D-galactosaminyl-(1->3)-N-acetyl-bet... group(2-)
    '78844',  # 3'-(N-formyl-L-methionyl)adenylyl(1-) group
    '17182',  # N-acetyl-beta-D-glucosaminyl-(1->2)-alpha-D-mannosyl-(... group
    '17651',  # 6-(2,6-bis[N-acetyl-beta-D-glucosaminyl]-alpha-D-manno... group
    '78527',  # 3'-(L-histidyl)adenylyl(1-) group
    '16478',  # N-acetyl-beta-D-glucosaminyl-1,6-(N-acetyl-beta-D-gluc... group
    '64428',  # H group
    '78515',  # 3'-(L-asparaginyl)adenylyl(1-) group
    '78551',  # 3'-(O-phosphonato-L-seryl)adenylyl(2-) group
    '78526',  # C-terminal-gamma-L-glutamyl-L-lysine(1-) group
    '78522',  # 3'-glycyladenylyl zwitterionic group
    '79073',  # CHOH group
    '78573',  # 3'-(L-selenocysteinyl)adenylyl(1-) group
    '17483',  # alpha-N-acetylneuraminyl-2,8-alpha-N-acetylneuraminyl-... group
    '32602',  # 2,4,6-tris(N-acetyl-beta-D-glucosaminyl)-alpha-D-mannosyl group
    '78537',  # 3'-(L-valyl)adenylyl zwitterionic group
    '78497',  # 3'-(L-alanyl)adenylyl zwitterionic group
    '64731',  # L-methioniniumyl group
    '55471',  # N-acetyl-beta-D-glucosaminyl group
    '23019',  # carbonyl group
    '16289',  # beta-D-galactosyl group
    '43176',  # hydroxy group
    '17581',  # N-acetyl-beta-D-glucosaminyl-1,3-beta-D-galactosyl-1,3... group
    '78535',  # 3'-(L-tryptophyl)adenylyl(1-) group
    '16059',  # N-acetyl-beta-D-glucosaminyl-1,3-beta-D-galactosyl-1,4... group
    '17785',  # alpha-D-Galp-(1->3)-beta-D-Galp-(1->4)-D-GlcpNAc-yl group
    '16117',  # beta-D-galactosyl-(1->3)-N-acetyl-alpha-D-galactosaminyl group
    '75189',  # N-acetyl-beta-D-galactosaminyl-(1->3)-N-acetyl-beta-D-... group
    '78494',  # 3'-(L-leucyl)adenylyl zwitterionic group
    '90517',  # methyl L-leucinato group
    '78533',  # 3'-(L-seryl)adenylyl(1-) group
    '75187',  # N-acetyl-beta-D-glucosaminyl-(1->4)-alpha-D-mannosyl group
    '32618',  # N-acetyl-beta-D-glucosaminyl-(1->2)-alpha-D-mannosyl-(... group
    '32601',  # N-acetyl-beta-D-glucosaminyl-1,6-(N-acetyl-beta-D-gluc... group
    '78501',  # C-terminal-gamma-L-glutamyl-L-2-aminoadipate semialdeh... group
    '74429',  # 7-methylguanosine 5'-triphosphate(2-) group
    '60105',  # alpha-N-acetylneuraminyl-(2->3)-beta-D-galactosyl-(1->... group
    '16901',  # alpha-N-acetylneuraminyl-2,3-beta-D-galactosyl-1,3-N-a... group
    '64718',  # L-alaniniumyl group
    '48563',  # methylsulfanyl group
    '78723',  # 3'-(D-tyrosyl)adenylyl(1-) group
    '78528',  # 3'-(L-isoleucyl)adenylyl zwitterionic group
    '78536',  # 3'-(L-tyrosyl)adenylyl(1-) group
    '78513',  # 3'-(L-arginyl)adenylyl(1+) group
    '64738',  # L-seriniumyl group
    '78525',  # L-glutamo(2-) group
    '62190',  # N-acetyl-beta-D-galactosaminyl-(1->4)-N-acetyl-beta-D-... group
    '78556',  # 3'-(L-pyrrolysyl)adenylyl zwitterionic group
    '18915',  # beta-D-galactosyl-(1->3)-N-acetyl-D-glucosaminyl group
    '78534',  # 3'-(L-threonyl)adenylyl(1-) group
    # Miscellaneous
    '30212',  # photon
    ))


class DirectoryNotFoundError(OSError):
    pass


class ChEBIIDError(KeyError):
    pass


class ECNumberError(KeyError):
    pass


class RheaIDError(KeyError):
    pass


def determine_intermediates(substrates, products):
    """
    Return pathway intermediates.

    Parameters
    ----------
    substrates, products : dict
        Must contain keys 'chebi' and 'number'.

    Returns
    -------
    dict
        ChEBI ID string to tuple of 2 numeric values. First value is
        the amount of occurrences in substrates and the second in
        products.

    """
    substrate_iter = ([s['chebi']] * s['number'] for s in substrates)
    product_iter = ([p['chebi']] * p['number'] for p in products)
    counter_s = cl.Counter(it.chain.from_iterable(substrate_iter))
    counter_p = cl.Counter(it.chain.from_iterable(product_iter))
    intermediate_set = set(counter_s) & set(counter_p)
    intermediates = {i: (counter_s[i], counter_p[i]) for i in intermediate_set}
    return intermediates


def evaluate_input(n, graph, compounds=[], enzymes=[], context={}):
    """
    Evaluate user input.

    Parameters
    ----------
    n : int
        The amount of results to be returned. Must be at least 1.
    compounds : list or tuple
        ChEBI ID strings. Order matters.
    enzymes : list or tuple
        EC number strings. Order doesn't matter.

    Returns
    -------
    list
        Tuples of value, pathway -pairs.

    Raises
    ------
    ChEBIIDError
        If a ChEBI ID in `compounds` is not recognized.
    ECNumberError
        If an EC number in `enzymes` is not recognized.
    TypeError
        If `n` is not int or if `compounds` or `enzymes` is neither
        list nor tuple.
    ValueError
        If `n` is less than 1.

    """
    if not isinstance(n, int):
        raise TypeError('`n` not int')

    ec_reactions = context['ec_reactions']
    compound_reactions = context['compound_reactions']
    complexities = context['complexities']
    demands = context['demands']
    prices = context['prices']
    stoichiometrics = context['stoichiometrics']

    pathways = set()
    start = None
    goal = None
    sources = [None]
    targets = [None]
    # Determine search and filter parameters.
    if compounds:
        start = compounds[0]
        goal = compounds[-1]
        if start == 'any':
            compounds = compounds[1:]
            if goal == 'any':
                pass
            else:
                targets = compound_reactions[goal][1]
        else:
            sources = compound_reactions[start][0]
            if goal == 'any':
                compounds = compounds[:-1]
            else:
                targets = compound_reactions[goal][1]
    else:
        sources.extend(e for ec in enzymes for e in ec_reactions[ec])
        targets = sources
    # Find pathways.
    for source, target in it.product(sources, targets):
        pws = find_pathway(graph, source, target)
        filtered_pws = filter_pathways(
            pws, source=start, target=goal, compounds=compounds,
            enzymes=enzymes, context=context)
        pathways.update(filtered_pws)

    # Evaluate pathways.
    pathways = list(pathways)
    pathway_data = order_pathway_data(pathways, stoichiometrics,
                                      complexities, demands, prices)
    values = [evaluate_pathway(s, c) for s, c in pathway_data]
    return nbest_items(n, values, pathways)


def evaluate_pathway(steps, compounds):
    """
    Evaluate pathway.

    Evaluates the pathway by calculating values of start and goal
    compounds and intermediate reaction steps. Start and goal compounds
    are determined by the reaction steps.

    Parameters
    ----------
    steps : collections.OrderedDict
        Keys are Rhea ID strings and values are dicts of substrate and
        product ChEBI ID-stoichiometric number -pairs. Order matches
        the order of reaction steps.
    compounds : dict
        Keys are ChEBI ID strings and value are tuples of compound
        demands and prices.

    Returns
    -------
    number
        Pathway's value.

    Raises
    ------
    TypeError
        If `steps` is not an instance of collections.OrderedDict.
        If `compounds` is not a dict.

    """
    values_reactions = (data[0] for data in steps.values())
    substrates_all = set(s for step in steps.values() for s in step[1])
    products_all = set(p for step in steps.values() for p in step[2])
    substrates = substrates_all - products_all
    products = products_all - substrates_all
    values_reactants = (compounds[s][1] * compounds[s][0] for s in substrates)
    values_products = (compounds[p][1] * compounds[p][0] for p in products)
    amount_reactions = len(steps)

    # Evaluate total value of products and reactants.
    p = sum(values_products)
    r = sum(values_reactants)
    # Evaluate pathway's total complexity factor.
    c = sum(values_reactions)
    # Evaluate and return pathway's value.
    value = m.ceil((p - r) * (c + 1) / amount_reactions)
    return value


def filter_pathways(
        pathways,
        source=None,
        target=None,
        compounds=[],
        enzymes=[],
        context={},
        ):
    """
    Yield pathways that meet filtering conditions.

    Parameters
    ----------
    pathways : iterable
        Lists of Rhea ID strings.
    source : string
        ChEBI ID of pathway's source compound. Filters pathways that
        have reactions producing `source`.
    target : string
        ChEBI ID of pathway's target compound. Filters pathways that
        have reactions consuming `target`.
    compounds : iterable
        CheBI ID strings. Filters pathways that don't have all
        compounds.
    enzymes : iterable
        EC number strings. Filters pathways that don't have all enzymes.
    context : dict
        Key `reaction_ecs` maps to a dict of Rhea ID string keys to EC
        number string list values.
        Key `stoichiometrics` maps to a dict of Rhea ID string keys to
        a list of dicts of substrates and products.

    Yields
    ------
    list
        Pathway reaction lists that meet the filtering conditions of
        given arguments.

    """
    reaction_ecs = context['reaction_ecs']
    stoichiometrics = context['stoichiometrics']
    for pathway in pathways:
        compounds_pw = set(['any'])
        enzymes_pw = set()
        for i, reaction in enumerate(pathway):
            substrates, products = stoichiometrics[reaction]
            if target in substrates:
                break
            elif source in products:
                break
            elif i >= 2:
                prepre_s, prepre_p = stoichiometrics[pathway[i - 2]]
                pre_s, pre_p = stoichiometrics[pathway[i - 1]]
                discard_substrates_1 = any(s in prepre_s for s in substrates)
                discard_substrates_2 = any(s in pre_p for s in substrates)
                if discard_substrates_1 and discard_substrates_2:
                    break
                discard_products_1 = any(p in prepre_p for p in products)
                discard_products_2 = any(p in pre_s for p in products)
                if discard_products_1 and discard_products_2:
                    break
            compounds_pw.update(substrates.keys())
            compounds_pw.update(products.keys())
            try:
                enzymes_pw.update(reaction_ecs[reaction])
            except KeyError:
                pass
        else:
            if not set(enzymes) <= enzymes_pw:
                continue
            elif not set(compounds) <= compounds_pw:
                continue
            yield tuple(pathway)


def find_pathway(graph, source=None, target=None):
    """
    Yield pathway lists.

    Parameters
    ----------
    graph : networkx graph object
        Use `initialize_graph_reaction` to create graph.
    reactions : iterable of 1 or 2
        `graph` node IDs to search pathways for.

    Yields
    ------
    list
        Pathways from source to target nodes. If length of `reactions`
        is 1, the ID in `reactions` is used as a source and as a
        target. If length of `reactions` is 2, the first item is used as
        the source and the second item is used as the target.

    Raises
    ------
    ValueError
        If length of `reactions` is neither 1 nor 2.

    """
    if target is None:
        if source is None:
            pass
        else:
            try:
                paths = nx.single_source_shortest_path(graph, source).values()
            except KeyError:
                pass
            else:
                for path in paths:
                    yield path
    elif source is None:
        with nx.utils.reversed(graph):
            try:
                paths = nx.single_source_shortest_path(graph, target)
            except KeyError:
                paths = []
        for target in paths:
            yield list(reversed(paths[target]))
    else:
        try:
            yield nx.bidirectional_shortest_path(graph, source, target)
        except nx.NetworkXNoPath:
            pass


def format_compound(compound, context={}):
    """
    Format chebi data with context to a dict.

    Parameters
    ----------
    compound : dict
        ChEBI ID str to stoichiometric number int.
    context : dict
        Must have a 'compounds' key that maps to a dict of ChEBI ID strs
        to compound names.

    Returns
    -------
    dict
        Compound data keyed by strings: 'chebi', 'number' and 'name'.

    """
    data = {}
    try:
        [[chebi, number]] = compound.items()
    except ValueError:  # Empty `compound`.
        pass
    else:
        data['chebi'] = chebi
        data['number'] = number
        data['name'] = context.get('compounds', {}).get(data['chebi'], '')
    finally:
        return data


def format_output(results, data):
    """
    Format `evaluate_input` results.

    Parameters
    ----------
    results : iterable
        tuples of value, pathway -pairs.

    Returns
    -------
    list
        Pathway dicts.

    """
    output = []
    for value, reactions in results:
        output.append(format_pathway(value, reactions, data))
    return output


def format_pathway(value, reactions=[], context={}):
    """
    Format pathway data with context to a dict.

    Parameters
    ----------
    value : number
        Pathways value.
    reactions : iterable
        Rhea ID strings.
    context : dict
        Accessory data. Must have keys 'compounds', 'enzymes',
        'equations', 'reactions', 'stoichiometrics' that map to data
        dicts.

    Returns
    -------
    dict
        Pathway data. Has keys 'value', 'reactions', 'substrates',
        'products' and 'intermediates'.

    """
    data = {}
    data['value'] = value
    data['reactions'] = [format_reaction(r, context) for r in reactions]
    data['substrates'] = []
    data['products'] = []
    data['intermediates'] = []
    substrates = []
    products = []
    for reaction in data['reactions']:
        substrates_reaction = reaction['substrates']
        products_reaction = reaction['products']
        for s, v_s in substrates_reaction.items():
            substrates.append(format_compound({s: v_s}, context))
        for p, v_p in products_reaction.items():
            products.append(format_compound({p: v_p}, context))
    intermediates = determine_intermediates(substrates, products)
    for i, v_i in intermediates.items():
        data['intermediates'].append(format_compound({i: v_i}, context))
    for s in substrates:
        is_intermediate = s['chebi'] in intermediates
        duplicates = any(s['chebi'] == d['chebi'] for d in data['substrates'])
        if not is_intermediate and not duplicates:
            data['substrates'].append(s)
    for p in products:
        is_intermediate = p['chebi'] in intermediates
        is_duplicate = any(p['chebi'] == d['chebi'] for d in data['products'])
        if not is_intermediate and not is_duplicate:
            data['products'].append(p)
    return data


def format_reaction(reaction, context={}):
    """
    Format reaction data with context to a dict.

    Parameters
    ----------
    reaction : str
        Rhea ID.
    context : dict
        Accessory data. Must have keys 'equations', 'reactions',
        'enzymes' and 'stoichiometrics' that map to data dicts.

    Returns
    -------
    dict
        Reaction data. Has keys 'rhea', 'equation', 'enzymes',
        'products' and 'substrates'.

    """
    data = {}
    data['rhea'] = reaction
    data['equation'] = context.get('equations', {}).get(reaction, '')
    enzymes = context.get('reaction_ecs', {}).get(reaction, [])
    enzyme_names = {
        ec: context.get('enzymes', {}).get(ec, '') for ec in enzymes}
    data['enzymes'] = {ec: enzyme_names[ec] for ec in enzymes}
    substrates, products = context.get(
        'stoichiometrics', {}).get(reaction, ({}, {}))
    data['products'] = products
    data['substrates'] = substrates
    return data


def intersect_dict(target, filter_to={}):
    """
    Return dict without keys that aren't present in the iterable.

    Parameters
    ----------
    target : dict
        key: value -pairs.
    filter_to : iterable
        Keys that are to be kept in `target`.

    Returns
    -------
    dict
        `target` without keys that aren't present in `filter_to`.

    """
    for key in target.copy():
        if key not in filter_to:
            target.pop(key)
    return target


def initialize_graph(
        reaction_stoichiometrics={},
        compound_reactions={},
        reactions_ignored=set(),
        compounds_ignored=set(),
        ):
    """
    Initialize graph to find pathways.

    Parameters
    ----------
    reaction_stoichiometrics : dict
        Rhea ID string keys, substrate and product dict values.
    compounds_reactions : dict
        ChEBI ID string keys, consumer and producer list values.
    reactions_ignored : set
        Rhea ID strings.
    compounds_ignored : set
        ChEBI ID strings.

    Returns
    -------
    nx.DiGraph object

    """
    graph = nx.DiGraph()
    # Create edges.
    for reaction in set(reaction_stoichiometrics) - reactions_ignored:
        substrates, products = reaction_stoichiometrics[reaction]
        for product in set(products) - compounds_ignored:
            consumers, __ = compound_reactions[product]
            weight = len(consumers)
            for consumer in set(consumers) - reactions_ignored:
                # Ignore opposite direction of reaction.
                __, consumer_products = reaction_stoichiometrics[consumer]
                if consumer_products == substrates:
                    continue
                graph.add_edge(reaction, consumer, weight=weight)
    return graph


def nbest_items(n, values, items):
    """
    Return n best items.

    Parameters
    ----------
    n : int
        The amount of best value-item -pairs to be returned.
    values : iterable
        Values of items in `items`. Indices must match.
    items : iterable
        Items to be compared by values in `values`. Indices must match.

    Returns
    -------
    list
        tuples of value-item -pairs in descending value-order.

    Raises
    ------
    TypeError
        If `n` or items in `values` are non-numeric.
    ValueError
        If `n` is less than 1.

    """
    if not isinstance(n, (float, int)):
        raise TypeError('`n` non-numeric')
    elif n < 1:
        raise ValueError('`n` less than 1')
    elif not all((isinstance(value, (float, int)) for value in values)):
        raise TypeError('nonnumerical item in `values`')
    maxes = hq.nlargest(n, values)
    indices_max = [ix for ix, value in enumerate(values) if value in maxes]
    items_max = [items[index_max] for index_max in indices_max]
    values_max = [values[index_max] for index_max in indices_max]
    return sorted(list(zip(values_max, items_max)), reverse=True)[:n]


def order_pathway_data(
        pathways,
        stoichiometrics={},
        complexities={},
        demands={},
        prices={},
        ):
    """
    Yield ordered pathway dicts.

    Parameters
    ----------
    pathways : iterable
        Lists or tuples of ordered reaction Rhea ID strings.

    Yields
    ------
    tuple
        [0] collections.OrderedDict of Rhea ID string keys and value
        lists of reaction complexities and dicts of reactant and
        product ChEBI ID strings keys and stoichiometric number values.
        [1] Dict of ChEBI ID string keys and value tuples of compound
        demand and price.

    """
    for pw in pathways:
        steps = cl.OrderedDict()
        compounds = {}
        for step in pw:
            reactants, products = stoichiometrics[step]
            complexity = complexities[step]
            steps[step] = [complexity, reactants, products]
            compounds.update(
                (r, (demands[r], prices[r])) for r in reactants)
            compounds.update(
                (p, (demands[p], prices[p])) for p in products)
        yield steps, compounds


def get_content(path, filename):
    """
    Return content of a text file.

    Parameters
    ----------
    path : str
        Directory path to file.
    filename : str
        Name of the file. Name must include extension.

    Returns
    -------
    list
        Contents of the file. List elements correspond to text file
        rows.

    Raises
    ------
    FileNotFoundError
        If the path or file does not exist.
    TypeError
        If path or filename is not str.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename)) as file:
        return file.readlines()


def get_json(path, filename):
    """
    Return data object from a JSON formatted file.

    Parameters
    ----------
    path : str
        Directory path to file.
    filename : str
        Name of the file. Name must include extension.

    Returns
    -------
    object
        Object contained in the JSON file.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename)) as file:
        return json.load(file)


def get_names(path):
    """
    Return a list of filenames in a directory.

    Parameters
    ----------
    path : str
        Directory path.

    Returns
    -------
    list
        String names of the files. Names also contain the file
        extensions.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    # os.walk yields tuple of 3: dirpath, dirnames and filenames.
    try:
        __, __, filenames = os.walk(path).__next__()
    except StopIteration:
        raise DirectoryNotFoundError('directory `{}` not found'.format(path))
    else:
        return filenames


def write_json(python_object, path, filename):
    """
    Save object data in a JSON formatted file.

    Parameters
    ----------
    python_object : obj
        Object to be saved in the JSON file.
    path : str
        Directory path to file.
    filename : str
        Name of the target JSON file. Filename must not contain path or
        extension.

    Returns
    -------
    None

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename), 'w') as file:
        json.dump(python_object, file)


def write_jsons(data, path, filenames):
    """
    Save objects in JSON formatted files.

    Parameters
    ----------
    data : list
        Objects to be saved in the files. Object index must correspond to
        filename index.
    path : str
        Directory path to file.
    filenames : list
        Names of the target JSON files. Filename index must correspond
        to object index.

    Returns
    -------
    None

    """
    if not isinstance(data, (list, tuple)):
        raise TypeError('`data` must be list or tuple')
    elif not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filenames, (list, tuple)):
        raise TypeError('`filenames` must be list or tuple')
    for object_, filename in zip(data, filenames):
        write_json(object_, path, filename)


def main():
    """
    Empty main function.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    pass


if __name__ == '__main__':
    main()

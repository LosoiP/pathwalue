'use strict';
/**
 * @fileOverview JavaScript for PathWalue-application.
 *
 * @author Pauli Losoi
 *
 * @requires Lodash
 * @requires jQuery
 * @requires JSNetworkX
 * @requires Select2
 */

var IGNORED_COMPOUNDS = [
    '15377',  // H2O water
    '29242',  // AsH2O3
    '48597',  // AsHO4
    '15858',  // Br
    '16183',  // CH4 methane
    '17245',  // CO carbon monoxide
    '16526',  // CO2 carbon dioxide
    '17996',  // Cl chloride
    '85033',  // Co(1+) cobalt
    '49552',  // Cu(+) copper
    '29036',  // Cu(2+) copper
    '17051',  // F fluoride
    '29033',  // Fe(2+) iron
    '29034',  // Fe(3+) iron
    '15378',  // H(+) hydron
    '18276',  // H2
    '18407',  // HCN hydrogen cyanide
    '17544',  // HCO3 hydrogencarbonate
    '16240',  // H2O2 hydrogen peroxide
    '43473',  // HPO4 hydrogenphosphate
    '33019',  // HP2O7 diphosphate
    '29919',  // HS hydrosulfide
    '16382',  // I iodide
    '78619',  // iron(III) oxide-hydroxide(1-)
    '17997',  // N2
    '28938',  // NH4(+)
    '84879',  // NHO
    '16480',  // NO nitric oxide
    '17045',  // N2O dinitrogen oxide
    '16301',  // NO2(-) nitrite
    '17632',  // NO3(-) nitrate
    '29101',  // Na(+)
    '43474',  // PO4
    '15379',  // O2 dioxygen
    '18421',  // O2 superoxide
    '26833',  // S sulfur atom
    '17359',  // SO3 sulfite
    '16189',  // SO4 sulfate
    '29256',  // thiol
    '18036',  // triphosphate
    '58339',  // 3'-phosphonato-5'-adenylyl sulfate(4-)
    '58343',  // adenosine 3',5'-bismonophosphate(4-)
    // Factors
    '73299',  // cobalt(II)-factor III(8-)
    '85471',  // cobalt(II)-factor IV(6-)
    // Hormones
    '83274',  // juvenile hormone III carboxylate
    '15581',  // juvenile hormone II
    '27493',  // juvenile hormone III
    '83641',  // juvenile hormone I
    '87109',  // juvenile hormone I carboxylate
    // Residues
    '65264',  // dodecanoyl-pantetheine-4-phosphorylserine(1-) residue
    '82657',  // deoxyhypusine(2+) residue
    '78457',  // O-[S-(3R)-hydroxyhexanoylpantetheine-4'-phosphoryl]... residue
    '74419',  // 2-thio-N(6)-L-threonylcarbamoyladenine 5'-monophosp... residue
    '79032',  // O-[S-(dihydromonacolin L carboxy)pantetheine-4'-pho... residue
    '87079',  // N-acetyl-beta-D-glucosaminyl-(1->3)-N-acetyl-alpha-... residue
    '78461',  // O-[S-(3R)-hydroxyoctanoylpantetheine-4-phosphoryl]s... residue
    '74455',  // 5-methylaminomethyl-2-thiouridine 5'-monophosphate ... residue
    '88221',  // N(omega),N('omega)-dimethyl-L-arginine(1+) residue
    '74481',  // N(2)-methylguanosine 5'-monophosphate(1-) residue
    '29950',  // L-cysteine residue
    '83690',  // N-terminal N-acetyl-L-serine residue
    '64315',  // 4-demethylwyosine 5'-monophosphate(1-) residue
    '78449',  // O-(S-malonylpantetheine-4'-phosphoryl)serine(2-) residue
    '85305',  // S-3-[(2R)-phycourobilin]-L-cysteine(2-) residue
    '16044',  // L-methionine residue
    '29973',  // L-glutamate residue
    '82693',  // 2-[(3S)-3-carboxylato-3-(methylammonio)propyl]-L-hi... residue
    '78470',  // O-[S-(3R)-hydroxydodecanoylpantetheine-4-phosphoryl... residue
    '85958',  // 5'-(N(7)-methyl 5'-triphosphoguanosine)-2'-O-methyl... residue
    '78778',  // O-[S-(11Z)-hexadecenoylpantetheine-4'-phosphoryl]se... residue
    '83111',  // N(6)-[(R)-S(8)-acetyldihydrolipoyl]-L-lysine residue
    '90675',  // ribonucleotide residue(1-)
    '83144',  // biotinyl-L-lysine residue
    '83561',  // N-terminal L-phenylalanyl-L-alpha-amino acid(1+) residue
    '83545',  // agmatidine 5'-phosphate(1+) residue
    '78458',  // O-[S-(2E)-hexenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '85027',  // 2'-phospho-nucleotide 5'-phosphate(3-) residue
    '30011',  // L-glutamine residue
    '79005',  // diphthine methyl ester residue
    '90516',  // L-leucinate residue
    '78598',  // N-terminal Nalpha-acetylamino-acid residue
    '82795',  // gamma-methyl L-glutamate residue
    '78454',  // O-(S-butanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '90975',  // O(4)-(N-acetyl-alpha-D-galactosaminyl)-trans-4-hydr... residue
    '74275',  // 7-[(3S)-(3-amino-3-methoxycarbonyl)propyl]wyosine 5... residue
    '87080',  // N-acetyl-beta-D-glucosaminyl-(1->3)-N-acetyl-alpha-... residue
    '74483',  // 5-methylcytidine 5'-monophosphate(1-) residue
    '83683',  // N-terminal N-acetyl-L-alanine residue
    '74491',  // N(1)-methyladenosine 5'-monophosphate(1-) residue
    '61976',  // N(6),N(6)-dimethyl-L-lysine(1+) residue
    '62836',  // 2-methylthio-N(6)-(cis-4-hydroxy-Delta(2)-isopenten... residue
    '78467',  // O-[S-(2E)-decenoylpantetheine-4-phosphoryl]serine(1-) residue
    '85644',  // UMP 2',3'-cyclic phosphate(2-) residue
    '82883',  // nucleotide 5'-phosphate(1-) residue
    '82620',  // L-tyrosine-O-phosphate(2-) residue
    '74420',  // 2-methylthio-N(6)-L-threonylcarbamoyladenine 5'-mon... residue
    '45764',  // L-methionine (R)-S-oxide residue
    '82696',  // diphthine betaine residue
    '78818',  // O-(S-3-oxopentanoylpantetheine-4'-phosphoryl)serine... residue
    '74447',  // 5-methyluridine 5'-monophosphate(1-) residue
    '78809',  // N(6)-octanoyl-L-lysine residue
    '78466',  // O-[S-(3R)-hydroxydecanoylpantetheine-4-phosphoryl]s... residue
    '83562',  // N-terminal L-arginyl-L-alpha-amino acid(2+) residue
    '83556',  // N-terminal L-leucyl-L-alpha-amino acid(1+) residue
    '64837',  // N(pros)-phosphonato-L-histidine residue
    '74898',  // 3'-end 2'-O-methylribonucleotide(1-) residue
    '87131',  // O-(S-L-2-amino-6-adipoylpantetheine-4'-phosphoryl)-... residue
    '82695',  // 2-[(3S)-3-carboxylato-3-(dimethylammonio)propyl]-L-... residue
    '73550',  // 4-demethyl-7-(3-amino-3-carboxypropyl)wyosine 5'-mo... residue
    '78779',  // O-[S-(13Z)-3-oxooctadecenoylpantetheine-4'-phosphor... residue
    '73543',  // 7-[(3S)-3-amino-3-carboxypropyl]wyosine 5'-monophos... residue
    '90783',  // C-terminal S-(Gly-Gly)-L-Cys zwitterion residue
    '90616',  // N(6)-methyl-dAMP(1-) residue
    '29999',  // L-serine residue
    '50347',  // L-asparagine residue
    '64479',  // O-(pantetheine-4'-phosphoryl)serine(1-) residue
    '83145',  // carboxybiotinyl-L-lysine(1-) residue
    '90615',  // dAMP(1-) residue
    '78823',  // O-(S-3-oxo-4-methylhexanoylpantetheine-4'-phosphory... residue
    '78599',  // (gamma-L-glutamyl) N-terminal alpha-amino-acid zwit... residue
    '85448',  // 6-O-methyl dGMP(1-) residue
    '61965',  // trans-4-hydroxy-L-proline residue
    '86021',  // S-geranylgeranyl-L-cysteine residue
    '74257',  // FMN-L-threonine(2-) residue
    '90870',  // 3-iodo-L-tyrosine residue
    '83421',  // O-phospho-L-serine(2-) residue
    '78468',  // O-(S-decanoylpantetheine-4-phosphoryl)serine(1-) residue
    '74416',  // 2-thio-N(6)-dimethylallyladenine 5'-monophosphate(1-) residue
    '78450',  // O-(S-acetoacetylpantetheine-4'-phosphoryl)serine(1-) residue
    '83441',  // O-[S-(3R)-hydroxyicosanoylpantetheine-4-phosphoryl]... residue
    '82612',  // S-methyl-L-cysteine residue
    '83100',  // N(6)-[(R)-dihydrolipoyl]-L-lysine residue
    '16692',  // diphthamide residue
    '90511',  // S-[(2E,6E)-farnesyl]-L-cysteine methyl ester residue
    '78475',  // O-[S-(2E)-tetradecenoylpantetheine-4-phosphoryl]ser... residue
    '61891',  // N(5)-methyl-L-glutamine residue
    '90602',  // uridylyl-L-tyrosine(1-) residue
    '78597',  // N-terminal alpha-amino-acid(1+) residue
    '61897',  // N(omega),N(omega)-dimethyl-L-arginine(1+) residue
    '29965',  // L-argininium residue
    '86110',  // O-[S-(6Z)-hexadecenoylpantetheine-4'-phosphoryl]ser... residue
    '74478',  // 2'-O-methyluridine 5'-monophosphate(1-) residue
    '83143',  // N(6)-[(R)-S(8)-ammoniomethyldihydrolipoyl]-L-lysine... residue
    '85452',  // dCMP(1-) residue
    '29969',  // L-lysinium residue
    '74851',  // 5-(2-methoxy-2-oxoethyl)uridine 5'-monophosphate residue(1-)
    '78820',  // O-(S-3-oxo-4-methylpentanoylpantetheine-4'-phosphor... residue
    '82697',  // N-(ADP-D-ribosyl)diphthamide(1-) residue
    '83064',  // 3'-end ribonucleotide 2',3'-cyclic phosphate(2-) residue
    '83834',  // peptidylproline (omega=180) residue
    '74493',  // N(6),N(6)-dimethyladenosine 5'-monophosphate(1-) residue
    '82683',  // O-[2'-(5-phosphoribosyl)-3'-dephospho-CoA]-L-serine... residue
    '83624',  // O-adenyl-L-tyrosine(1-) residue
    '83062',  // 3'-end ribonucleotide 3'-phosphate(3-) residue
    '87831',  // N(6)-malonyl-L-lysine(1-) residue
    '131803',  // L-allysine residue
    '65286',  // L-tyrosine-O-sulfate(1-) residue
    '78480',  // O-[S-(3R)-hydroxyhexadecanoylpantetheine-4'-phospho... residue
    '78453',  // O-[S-(2E)-butenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '73544',  // wybutosine 5'-monophosphate(1-) residue
    '74480',  // N(7)-methylguanosine 5'-phosphate zwitterion residue
    '78824',  // O-(S-3-oxoheptanoylpantetheine-4'-phosphoryl)serine... residue
    '85445',  // dGMP(1-) residue
    '74445',  // 2'-O-methylguanosine 5'-monophosphate(1-) residue
    '74454',  // 5-aminomethyl-2-thiouridine 5'-monophosphate zwitterio residue
    '78296',  // (3S)-3-ammonio-3-(3-chloro-4,5-dihydroxyphenyl)prop... residue
    '30013',  // L-threonine residue
    '90510',  // S-[(2E,6E)-farnesyl]-L-cysteinate residue
    '84990',  // gamma-carboxy-L-glutamate(2-) residue
    '74882',  // 5-(carboxymethyl)uridine 5'-monophosphate(2-) residue
    '74900',  // N(4)-acetylcytidine 5'-monophosphate(1-) residue
    '61963',  // 3-disulfanyl-L-alanine residue
    '29961',  // L-aspartate residue
    '74508',  // 5-carboxymethylaminomethyluridine 5'-monophosphate(1-) residue
    '78462',  // O-[S-(2E)-octenoylpantetheine-4-phosphoryl]serine(1-) residue
    '131709',  // N(6)-(1-hydroxy-2-oxopropyl)-L-lysine residue(1+)
    '131913',  // O-[S-3,5-dihydroxy-4-methylanthranilyl]serine(1-) residue
    '61929',  // N(6)-methyl-L-lysinium residue
    '78456',  // O-(S-3-oxohexanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '78822',  // O-(S-3-oxo-5-methylhexanoylpantetheine-4'-phosphory... residue
    '87215',  // N-terminal 5-oxo-L-proline residue
    '90840',  // O-(N-acetyl-beta-D-glucosaminyl)-L-threonine residue
    '88222',  // N(5)-methyl-argininium(1+) residue
    '74151',  // S-palmitoyl-L-cysteine residue
    '78446',  // O-(S-acetylpantetheine-4'-phosphoryl)serine(1-) residue
    '78846',  // O-(S-pimeloylpantetheine-4'-phosphoryl)serine(2-) residue
    '78442',  // AMP 3'-end(1-) residue
    '83739',  // ferroheme c di-L-cysteine(2-) residue
    '78826',  // O-(S-3-oxononanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '83665',  // lysidine monophosphate zwitterion residue
    '78294',  // (3R)-3-hydroxy-L-argininium residue
    '90420',  // N(6)-(3-O-phospho-D-ribulosyl)-L-lysinium residue
    '87169',  // S-sulfo-L-cysteine(1-) residue
    '83142',  // N(6)-[(R)-S(8)-isobutyryldihydrolipoyl]-L-lysine residue
    '83440',  // O-(S-3-oxoicosanoylpantetheine-4'-phosphoryl)-L-ser... residue
    '82852',  // inosine 5'-phosphate(1-) residue
    '87075',  // N-acetyl-alpha-D-galactosaminyl-L-threonine residue
    '74543',  // 8-methyladenosine 5'-monophosphate(1-) residue
    '78488',  // O-[S-(3R)-hydroxyoctadecanoylpantetheine-4'-phospho... residue
    '44120',  // L-methionine (S)-S-oxide residue
    '61930',  // N(6)-acetyl-L-lysine residue
    '87828',  // N(6)-glutaryl-L-lysine(1-) residue
    '83099',  // N(6)-[(R)-lipoyl]-L-lysine residue
    '74486',  // N(3)-methylpseudouridine 5'-monophosphate(1-) residue
    '62866',  // 2-methylthio-N(6)-(Delta(2)-isopentenyl)adenosine residue
    '83120',  // N(6)-[(R)-S(8)-succinyldihydrolipoyl]-L-lysine(1-) residue
    '83960',  // N(omega)-(ADP-D-ribosyl)-L-arginine(1-) residue
    '86299',  // O-[S-5-hexynoylpantetheine-4'-phosphoryl]serine(1-) residue
    '90873',  // dehydroalanine residue
    '90610',  // O-[S-2,3-dihydroxybenzoylpantetheine-4'-phosphoryl]... residue
    '90838',  // O-(N-acetyl-beta-D-glucosaminyl)-L-serine residue
    '87830',  // N(6)-succinyl-L-lysine(1-) residue
    '90874',  // 3,3',5-triiodo-L-thyronine residue
    '83071',  // tRNA 3'-terminal nucleotidyl-cytidyl-cytidyl-adenos... residue
    '74513',  // N(2),N(2)-dimethylguanosine 5'-monophosphate(1-) residue
    '87078',  // N-acetyl-alpha-D-galactosaminyl-L-serine residue
    '90418',  // N(6)-D-ribulosyl-L-lysinium residue
    '16367',  // N(tele)-methyl-L-histidine residue
    '78477',  // O-(S-tetradecanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '78483',  // O-(S-hexadecanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '83226',  // N(omega)-phospho-L-arginine(1-) residue
    '75591',  // 3-hydroxy-L-aspartate residue
    '85643',  // 3'-terminal pUpU(2-) residue
    '76179',  // O-(S-acylpantetheine-4'-phosphoryl)serine(1-) residue
    '65315',  // UMP(1-) residue
    '78495',  // O-(S-octadecanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '50342',  // L-proline residue
    '74890',  // N(1)-methylpseudouridine 5'-monophosphate(1-) residue
    '78489',  // O-[S-(2E)-octadecenoylpantetheine-4'-phosphoryl]ser... residue
    '83833',  // peptidylproline (omega=0) residue
    '74506',  // N(4)-methylcytidine 5'-monophosphate(1-) residue
    '78481',  // O-[S-(2E)-hexadecenoylpantetheine-4'-phosphoryl]ser... residue
    '74495',  // 2'-O-methylcytidine 5'-monophosphate(1-) residue
    '78827',  // O-[S-(3R)-3-hydroxyacylpantetheine-4'-phosphoryl]se... residue
    '82831',  // queuosine 5'-phosphate zwitterion residue
    '74511',  // 5-carboxymethylaminomethyl-2'-O-methyluridine 5'-mo... residue
    '131710',  // S-(1-hydroxy-2-oxopropyl)-L-cysteine residue
    '78487',  // O-(S-3-oxooctadecanoylpantetheine-4'-phosphoryl)ser... residue
    '131912',  // O-[S-3-hydroxy-4-methylanthranilyl]serine(1-) residue
    '82764',  // O-[S-2-methylbutanoylpantetheine-4'-phosphoryl]seri... residue
    '85339',  // O-[S-(L-alloisoleucyl)pantetheine-4'-phosphoryl]ser... residue
    '74497',  // 2-methyladenosine 5'-monophosphate(1-) residue
    '78464',  // O-(S-3-oxodecanoylpantetheine-4-phosphoryl)serine(1-) residue
    '82930',  // 3-(3-amino-3-carboxypropyl)uridine 5'-phosphate(1-) residue
    '78460',  // O-(S-3-oxooctanoylpantetheine-4-phosphoryl)serine(1-) residue
    '74418',  // N(6)-L-threonylcarbamoyladenine 5'-monophosphate(2-) residue
    '83697',  // N(5)-alkyl-L-glutamine residue
    '90676',  // 2'-O-methylribonucleotide(1-) residue
    '131610',  // O-(beta-L-arabinofuranosyl)-trans-4-hydroxy-L-proline residue
    '85959',  // 5'-(N(7)-methyl 5'-triphosphoguanosine)-N(7),2'-O-d... residue
    '29979',  // L-histidine residue
    '90871',  // 3,5-diiodo-L-tyrosine residue
    '85288',  // S-3-[(2R)-phycoviolobilin]-L-cysteine(2-) residue
    '78463',  // O-(S-octanoylpantetheine-4-phosphoryl)serine(1-) residue
    '82850',  // 7-cyano-7-carbaguanine 5'-phosphate(1-) residue
    '83151',  // glycyl-AMP(1-) residue
    '29998',  // D-serine residue
    '82748',  // CMP(1-) residue
    '78459',  // O-(S-hexanoylpantetheine-4'-phosphoryl)serine(1-) residue
    '78469',  // O-(S-3-oxododecanoylpantetheine-4-phosphoryl)serine... residue
    '83586',  // N(tele)-phosphonato-L-histidine residue
    '82735',  // O-[S-(6-methoxycarbonylhexanoyl)pantetheine-4'-phos... residue
    '15989',  // L-methionine S-oxide residue
    '74502',  // N(3)-methyluridine 5'-monophosphate(1-) residue
    '65280',  // N(omega)-methyl-argininium(1+) residue
    '74449',  // N(6)-methyladenosine 5'-monophosphate(1-) residue
    '83989',  // O-[S-(9Z)-hexadecenoylpantetheine-4'-phosphoryl]ser... residue
    '85961',  // 5'-triphosphoguanosine(3-) residue
    '78472',  // O-[S-(2E)-dodecenoylpantetheine-4-phosphoryl]serine... residue
    '78798',  // O-[S-(3Z)-decenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '85189',  // O-[(9Z)-hexadecenoyl]-L-serine residue
    '90619',  // C-terminal N-glycylaminoethanethioic S-acid residue
    '90872',  // L-thyroxine residue
    '78845',  // O-[S-(methoxycarbonylacetyl)pantetheine-4'-phosphor... residue
    '85919',  // O-[S-(4Z)-hexadecenoylpantetheine-4'-phosphoryl]ser... residue
    '61977',  // O-phosphonato-L-threonine(2-) residue
    '78784',  // O-[S-(2E)-2-enoylpantetheine-4'-phosphoryl]-L-serin... residue
    '86019',  // S-[(2E,6E)-farnesyl]-L-cysteine residue
    '78474',  // O-[S-(3R)-hydroxytetradecanoylpantetheine-4-phospho... residue
    '85454',  // 5-methyl dCMP(1-) residue
    '73542',  // N(1)-methylguanosine 5'-monophosphate(1-) residue
    '74477',  // 2'-O-methyladenosine 5'-monophosphate(1-) residue
    '82833',  // 7-aminomethyl-7-carbaguanine 5'-phosphate zwitterion residue
    '78776',  // O-(S-3-oxoacylpantetheine-4'-phosphoryl)-L-serine(1-) residue
    '74415',  // N(6)-dimethylallyladenine 5'-monophosphate(1-) residue
    '73603',  // 7-(2-hydroxy-3-amino-3-carboxypropyl)wyosine 5'-mon... residue
    '74417',  // 2-methylthio-N(6)-dimethylallyladenine 5'-monophosp... residue
    '85501',  // N(4)-(beta-D-glucosyl)-L-asparagine residue
    '82834',  // epoxyqueuosine 5'-phosphate zwitterion residue
    '65314',  // pseudouridine 5'-phosphate(1-) residue
    '86298',  // O-[S-5-hexenoylpantetheine-4'-phosphoryl]serine(1-) residue
    '85280',  // S-3-[(2R)-phycocyanobilin]-L-cysteine(2-) residue
    '73995',  // 2-[(3S)-3-amino-3-carboxypropyl]-L-histidine zwitterion residue
    '90778',  // C-terminal Gly-Gly(1-) residue
    '74896',  // 3'-end ribonucleotide(1-) residue
    '74269',  // GMP(1-) residue
    '46858',  // L-tyrosine residue
    '78473',  // O-(S-3-oxotetradecanoylpantetheine-4-phosphoryl)ser... residue
    '90596',  // L-beta-isoaspartate residue
    '83397',  // L-citrulline residue
    '85279',  // S-3-[(2R)-phycoerythrobilin]-L-cysteine(2-) residue
    '74411',  // AMP(1-) residue
    '90598',  // L-aspartic acid alpha-methyl ester residue
    '78451',  // O-[S-(3R)-hydroxybutanoylpantetheine-4'-phosphoryl]... residue
    '78297',  // (3S)-3-ammonio-3-(3-chloro-4-hydroxyphenyl)propanoyl residue
    '85428',  // trans-3-hydroxy-L-proline residue
    '50058',  // L-cystine residue
    '78785',  // O-(S-2,3-saturated acylpantetheine-4'-phosphoryl)se... residue
    '78478',  // O-(S-3-oxohexadecanoylpantetheine-4'-phosphoryl)ser... residue
    '78783',  // O-(S-oleoylpantetheine-4'-phosphoryl)serine(1-) residue
    // Deoxyribonucleotides
    '61404',  // dATP(4-)
    '57667',  // dADP(3-)
    '58245',  // dAMP(2-)
    '61481',  // dCTP(4-)
    '58593',  // dCDP(3-)
    '57566',  // dCMP(2-)
    '61429',  // dGTP(4-)
    '58595',  // dGDP(4-)
    '57673',  // dGMP(4-)
    '61382',  // dITP(4-)
    '37568',  // dTTP(4-)
    '58369',  // dTDP(3-)
    '63528',  // dTMP(2-)
    '61555',  // dUTP(4-)
    '60471',  // dUDP(3-)
    '246422',  // dUMP(2-)
    // Ribonucleotides
    '30616',  // ATP(4-)
    '456216',  // ADP(3-)
    '456215',  // AMP(2-)
    '37563',  // CTP(4-)
    '58069',  // CDP(3-)
    '60377',  // CMP(2-)
    '37565',  // GTP(4-)
    '58189',  // GDP(3-)
    '58115',  // GMP(2-)
    '61402',  // ITP(4-)
    '58280',  // IDP(3-)
    '58053',  // IMP(2-)
    '46398',  // UTP(4-)
    '58223',  // UDP(3-)
    '57865',  // UMP(2-)
    '61314',  // XTP(4-)
    '59884',  // XDP(3-)
    '57464',  // XMP(2-)
    // Nucleosides
    '73316',  // 2'-deoxyribonucleoside 5'-diphosphate(3-)
    '131705',  // 2'-deoxynucleoside 3'-monophosphate(2-)
    '65317',  // 2'-deoxynucleoside 5'-monophosphate(2-)
    '58043',  // nucleoside 5'-monophosphate(2-)
    '61557',  // nucleoside triphosphate(4-)
    '58464',  // nucleoside 3',5'-cyclic phosphate anion
    '18274',  // 2'-deoxyribonucleoside
    '66949',  // nucleoside 3'-phosphate(2-)
    '83402',  // nucleoside 3',5'-bisphosphate(4-)
    '57930',  // nucleoside diphosphate(3-)
    '33838',  // nucleoside
    '13197',  // ribonucleoside 3'-monophosphate(2-)
    '61560',  // 2'-deoxyribonucleoside 5'-triphosphate(4-)
    '18254',  // ribonucleoside
    '57867',  // nucleoside 5'-phosphate dianion
    '78552',  // ribonucleoside 2'-monophosphate(2-)
    // Nucleotides
    '71310',  // Mo(VI)-molybdopterin guanine dinucleotide(2-)
    '66954',  // 2',3'-cyclic nucleotide(1-)
    '83064',  // 3'-end ribonucleotide 2',3'-cyclic phosphate(2-) residue
    '57439',  // (3Z)-phytochromobilin(2-)
    '62727',  // molybdopterin adenine dinucleotide(3-)
    '57502',  // nicotinate D-ribonucleotide(2-)
    '71308',  // Mo(VI)-molybdopterin cytosine dinucleotide(2-)
    '75967',  // nicotinate-adenine dinucleotide phosphate(4-)
    // Cofactors and -enzymes
    '16509',  // 1,4-benzoquinone
    '57530',  // 1,5-dihydrocoenzyme F420(4-)
    '16810',  // 2-oxoglutarate(2-)
    '175763',  // 2-trans,6-trans-farnesyl diphosphate(3-)
    '28889',  // 5,6,7,8-tetrahydropteridine
    '57454',  // 10-formyltetrahydrofolate(2-)
    '57288',  // acetyl-CoA(4-)
    '58342',  // acyl-CoA(4-)
    '64876',  // bacillthiol(1-)
    '60488',  // cob(I)alamin(1-)
    '16304',  // cob(II)alamin
    '28911',  // cob(III)alamin
    '57287',  // CoA(4-)
    '58319',  // coenzyme M(1-)
    '59920',  // coenzyme F420-1(4-)
    '57922',  // coenzyme gamma-F420-2(5-)
    '58596',  // coenzyme B(3-)
    '59923',  // coenzyme alpha-F420-3(6-)
    '83348',  // chlorophyllide a(2-)
    '71302',  // MoO2-molybdopterin cofactor(2-)
    '71305',  // WO2-molybdopterin cofactor(2-)
    '57692',  // FAD(3-)
    '58307',  // FADH2(2-)
    '33737',  // Fe2S2 di-mu-sulfido-diiron(2+)
    '33738',  // Fe2S2 di-mu-sulfido-diiron(1+)
    '57618',  // FMNH2
    '58210',  // FMN(3-)
    '57925',  // glutathionate(1-)
    '17594',  // hydroquinone
    '57384',  // malonyl-CoA(5-)
    '57540',  // NAD
    '57945',  // NADH
    '58349',  // NADP(3-)
    '57783',  // NADPH(4-)
    '17154',  // nicotinamide
    '16768',  // mycothiol
    '57387',  // oleoyl-CoA(4-)
    '57379',  // palmitoyl-CoA(4-)
    '18067',  // phylloquinone
    '28026',  // plastoquinol-9
    '28377',  // plastoquinone-9
    '59648',  // precursor Z(1-)
    '87467',  // prenyl-FMNH2(2-)
    '17310',  // pyridoxal
    '16709',  // pyridoxine
    '58442',  // pyrroloquinoline quinone(3-)
    '77660',  // pyrroloquinoline quinol(4-)
    '43711',  // (R)-dihydrolipoamide
    '76202',  // riboflavin cyclic 4',5'-phosphate(2-)
    '57856',  // S-adenosyl-L-homocysteine zwitterion
    '59789',  // S-adenosyl-L-methionine zwitterion
    '71177',  // tetrahydromonapterin
    '33723',  // tetra-mu3-suldifo-tetrairon(1+)
    '33722',  // tetra-mu3-suldifo-tetrairon(2+)
    // Porphyrins
    '62626',  // uroporphyrinogen I(8-)
    '62631',  // coproporphyrinogen I(4-)
    '131725',  // coproporphyrin III(4-)
    '60489',  // magnesium 13(1)-hydroxyprotoporphyrin 13-monomethyl ester(1-)
    '57307',  // protoporphyrinogen(2-)
    '57306',  // protoporphyrin(2-)
    '60490',  // magnesium 13(1)-oxoprotoporphyrin 13-monomethyl ester(1-)
    '57845',  // preuroporphyrinogen(8-)
    '60492',  // magnesium protoporphyrin(2-)
    '60491',  // magnesium protoporphyrin 13-monomethyl ester(1-)
    '57308',  // uroporphyrinogen III(8-)
    '57309',  // coproporphyrinogen III(4-)
    // Groups
    '60068',  // alpha-N-acetylneuraminyl-2,3-beta-D-galactosyl-1,3... group(1-)
    '18018',  // D-galactosyl-(1->4)-beta-D-glucosyl group
    '83148',  // glycino(1-) group
    '29917',  // thiol group
    '15876',  // beta-D-galactosyl-1,3-(N-acetyl-beta-D-glucosaminyl-1... group
    '68550',  // triphosphate group(4-)
    '77037',  // N,N-dimethyl-L-alanyl group
    '78503',  // C-terminal-gamma-L-glutamyl-L-2-aminoadipate(3-) group
    '16361',  // alpha-N-acetylneuraminyl-2,3-beta-D-galactosyl group
    '17723',  // beta-D-galactosyl-1,3-(N-acetyl-D-glucosaminyl-1,6)-N... group
    '78532',  // 3'-(L-prolyl)adenylyl zwitterionic group
    '17806',  // N-acetyl-beta-D-galactosaminyl group
    '78531',  // 3'-(L-phenylalanyl)adenylyl(1-) group
    '68546',  // phosphate group(2-)
    '68549',  // diphosphate group(3-)
    '16124',  // alpha-L-fucosyl-(1->2)-beta-D-galactosyl group
    '78517',  // 3'-(L-cysteinyl)adenylyl zwitterionic group
    '11936',  // N-acetyl-beta-D-glucosaminyl-(1->4)-beta-D-mannosyl group
    '16198',  // N-acetyl-beta-D-glucosaminyl-1,6-beta-D-galactosyl-1,... group
    '75185',  // alpha-D-mannosyl group
    '78521',  // 3'-(L-glutaminyl)adenylyl zwitterionic group
    '79333',  // 3'-(D-alpha-aminoacyl)adenylyl zwitterionic group
    '11714',  // 3-(2,4-bis[N-acetyl-beta-D-glucosaminyl]-alpha-D-mann... group
    '17227',  // D-galactosyl-(1->3)-beta-D-galactosyl-(1->4)-beta-D-g... group
    '17571',  // beta-D-galactosyl-(1->4)-N-acetyl-D-glucosaminyl group
    '78520',  // 3'-(L-glutamate)adenylyl(1-) group
    '12357',  // beta-D-galactosyl-(1->4)-N-acetyl-beta-D-glucosaminyl group
    '32591',  // alpha-D-mannosyl-(1->3)-beta-D-mannosyl group
    '78529',  // 3'-(L-lysyl)adenylyl(1+) group
    '49298',  // N-formyl-L-methionyl group
    '18914',  // beta-D-galactosyl-(1->3)-[alpha-L-fucosyl-(1->4)]-N-a... group
    '12193',  // alpha-D-mannosyl-(1->6)-beta-D-mannosyl group
    '22783',  // beta-D-galactosyl-(1->3)-N-acetyl-D-galactosaminyl group
    '78499',  // C-terminal-gamma-L-glutamyl-L-2-aminoadipate 6-phosph... group
    '88115',  // N(2)-L-glutamino(1-) group
    '78530',  // 3'-(L-methionyl)adenylyl zwitterionic group
    '74432',  // N(2),N(2),N(7)-trimethylguanosine 5'-triphosphate(2-) group
    '5484',  // alpha-D-galactosyl-(1->3)-[alpha-L-fucosyl-(1->2)]-D-g... group
    '64722',  // L-glutaminiumyl group
    '78516',  // 3'-(L-aspartate)adenylyl(1-) group
    '85224',  // alpha-hydroxyglycino(1-) group
    '32875',  // methyl group
    '16250',  // N-acetyl-beta-D-glucosaminyl-(1->3)-N-acetyl-D-galact... group
    '12384',  // beta-D-mannosyl group
    '75191',  // N-acetyl-beta-D-galactosaminyl-(1->3)-N-acetyl-be... group(2-)
    '78844',  // 3'-(N-formyl-L-methionyl)adenylyl(1-) group
    '17182',  // N-acetyl-beta-D-glucosaminyl-(1->2)-alpha-D-mannosyl-... group
    '17651',  // 6-(2,6-bis[N-acetyl-beta-D-glucosaminyl]-alpha-D-mann... group
    '78527',  // 3'-(L-histidyl)adenylyl(1-) group
    '16478',  // N-acetyl-beta-D-glucosaminyl-1,6-(N-acetyl-beta-D-glu... group
    '64428',  // H group
    '78515',  // 3'-(L-asparaginyl)adenylyl(1-) group
    '78551',  // 3'-(O-phosphonato-L-seryl)adenylyl(2-) group
    '78526',  // C-terminal-gamma-L-glutamyl-L-lysine(1-) group
    '78522',  // 3'-glycyladenylyl zwitterionic group
    '79073',  // CHOH group
    '78573',  // 3'-(L-selenocysteinyl)adenylyl(1-) group
    '17483',  // alpha-N-acetylneuraminyl-2,8-alpha-N-acetylneuraminyl... group
    '32602',  // 2,4,6-tris(N-acetyl-beta-D-glucosaminyl)-alpha-D-mann... group
    '78537',  // 3'-(L-valyl)adenylyl zwitterionic group
    '78497',  // 3'-(L-alanyl)adenylyl zwitterionic group
    '64731',  // L-methioniniumyl group
    '55471',  // N-acetyl-beta-D-glucosaminyl group
    '23019',  // carbonyl group
    '16289',  // beta-D-galactosyl group
    '43176',  // hydroxy group
    '17581',  // N-acetyl-beta-D-glucosaminyl-1,3-beta-D-galactosyl-1,... group
    '78535',  // 3'-(L-tryptophyl)adenylyl(1-) group
    '16059',  // N-acetyl-beta-D-glucosaminyl-1,3-beta-D-galactosyl-1,... group
    '17785',  // alpha-D-Galp-(1->3)-beta-D-Galp-(1->4)-D-GlcpNAc-yl group
    '16117',  // beta-D-galactosyl-(1->3)-N-acetyl-alpha-D-galactosaminyl group
    '75189',  // N-acetyl-beta-D-galactosaminyl-(1->3)-N-acetyl-beta-D... group
    '78494',  // 3'-(L-leucyl)adenylyl zwitterionic group
    '90517',  // methyl L-leucinato group
    '78533',  // 3'-(L-seryl)adenylyl(1-) group
    '75187',  // N-acetyl-beta-D-glucosaminyl-(1->4)-alpha-D-mannosyl group
    '32618',  // N-acetyl-beta-D-glucosaminyl-(1->2)-alpha-D-mannosyl-... group
    '32601',  // N-acetyl-beta-D-glucosaminyl-1,6-(N-acetyl-beta-D-glu... group
    '78501',  // C-terminal-gamma-L-glutamyl-L-2-aminoadipate semialde... group
    '74429',  // 7-methylguanosine 5'-triphosphate(2-) group
    '60105',  // alpha-N-acetylneuraminyl-(2->3)-beta-D-galactosyl-(1-... group
    '16901',  // alpha-N-acetylneuraminyl-2,3-beta-D-galactosyl-1,3-N-... group
    '64718',  // L-alaniniumyl group
    '48563',  // methylsulfanyl group
    '78723',  // 3'-(D-tyrosyl)adenylyl(1-) group
    '78528',  // 3'-(L-isoleucyl)adenylyl zwitterionic group
    '78536',  // 3'-(L-tyrosyl)adenylyl(1-) group
    '78513',  // 3'-(L-arginyl)adenylyl(1+) group
    '64738',  // L-seriniumyl group
    '78525',  // L-glutamo(2-) group
    '62190',  // N-acetyl-beta-D-galactosaminyl-(1->4)-N-acetyl-beta-D... group
    '78556',  // 3'-(L-pyrrolysyl)adenylyl zwitterionic group
    '18915',  // beta-D-galactosyl-(1->3)-N-acetyl-D-glucosaminyl group
    '78534',  // 3'-(L-threonyl)adenylyl(1-) group
    // Miscellaneous
    '30212',  // photon
];


/**
 * Return a new HTML element with attributes.
 * @param {HTMLElement} documentObject the document.
 * @param {string} tagName the HTML element tag name.
 * @param {object} attributes the attributes to the HTML element.
 *
 * @returns {HTMLElement} HTML element.
 */
function createHTMLElement(documentObject, tagName, attributes) {
    var element = documentObject.createElement(tagName);
    _.forOwn(attributes, function(value, key) {
        element[key] = value;
    });
    return element;
}


/**
 * Search and return best scoring pathways.
 * @param {jsnx.DiGraph} G
 * @param {number} n
 * @param {array} C
 * @param {array} E
 * @param {object} context
 *
 * @returns {array}
 */
function evaluateInput(G, n, C, E, Fl, context) {
    var pathways = [];
    var ecReactions = context['ec_reactions'];
    var compoundReactions = context['compound_reactions'];
    var complexities = context['complexities'];
    var demands = context['demands'];
    var prices = context['prices'];
    var stoichiometrics = context['stoichiometrics'];
    var start = null;
    var goal = null;
    var sources = [null];
    var targets = [null];
    var pws;
    var filterPws;
    var pathway;
    var data;
    var values = [];
    var i;
    var iLen;
    var lenSources;
    var lenTargets;
    var maxSources;
    var maxTargets;
    var maxPw;
    var maxFilter;
    var a = 1000;
    var b = 1000;
    var c = 5;
    var filter = {compounds: C, enzymes: E, source: '', target: '', links: Fl};
    // Determine search and filter parameters.
    if (C.length > 1) {
        start = C[0];
        goal = _.last(C);
        if (start === 'any') {
            C = C.slice(1);  // affects filter
            start = null;
            if (goal === 'any') {  // too wide to implement
                return [];
            } else {
                targets = compoundReactions[goal][1];
            }
        } else {
            sources = compoundReactions[start][0];
            if (goal === 'any') {
                C = C.slice(0, -1);  // affects filter
                goal = null;
            } else {
                targets = compoundReactions[goal][1];
            }
        }
        filter.source = start;
        filter.target = goal;
    } else {
        _.forEach(E, function(ec) {
            sources.push.apply(sources, ecReactions[ec]);
        });
        sources = _.uniqWith(sources, _.isEqual);
        targets = sources;
    }
    // Find pathways.
    // Constrain search to optimize performance.
    lenSources = sources.length;
    lenTargets = targets.length;
    maxSources = Math.ceil(Math.sqrt(a * lenSources / lenTargets));
    maxTargets = Math.ceil(Math.sqrt(a * lenTargets / lenSources));
    if (maxSources > 50) {
        maxSources = 50;
    }
    if (maxTargets > 50) {
        maxTargets > 50;
    }
    if (lenSources > maxSources) {
        lenSources = maxSources;
    }
    if (lenTargets > maxTargets) {
        lenTargets = maxTargets;
    }
    maxPw = Math.ceil(b / (lenSources * lenTargets));
    maxFilter = n + Math.ceil(maxPw / c);
    // Store shortest path from each source to each target in pathways.
    _.forEach(sources.slice(0, maxSources), function(s, i) {
        _.forEach(targets.slice(0, maxTargets), function(t, j) {
            pws = _.take(findPathway(G, s, t), maxPw);
            filterPws = _.take(
                filterPathways(pws, filter, context), maxFilter);
            pathways.push.apply(pathways, filterPws);
        });
    });
    // Evaluate pathways.
    pathways = _.uniqWith(pathways, function(a, b) {
        if (a.length === b.length) {
            for (i = 0, iLen = a.length; i < iLen; i++) {
                if (a[i] !== b[i]) {
                    return false
                }
            }
            return true
        } else {
            return false;
        }
    });
    // Fetch data for evaluate function.
    data = orderPathwayData(
        pathways, stoichiometrics, complexities, demands, prices);
    _.forEach(_.zip(data[0], data[1]), function(SC) {
        values.push(evaluatePathway(SC[0], SC[1]));
    });
    return _.sortBy(_.zip(values, pathways), function (pw) {return - pw[0];}).slice(0, n);
}


/**
 * Return pathway value.
 * @param {array} steps
 * @param {object} compounds
 *
 * @returns {number}
 */
function evaluatePathway(steps, compounds) {
    var rxns = [];
    var pros = [];
    var subs = [];
    var substratesAll = [];
    var productsAll = [];
    _.forEach(steps, function(step) {
        rxns.push(step[0]);
        substratesAll.push.apply(substratesAll, step[1]);
        productsAll.push.apply(productsAll, step[2]);
    });
    _.forEach(_.difference(substratesAll, productsAll), function(s) {
        try {  // FIND OUT WHY COMPOUND[X] CAN BE UNDEFINED.
            subs.push(compounds[s][0] * compounds[s][1]);
        }
        catch (error) {
            ;
        }
    });
    _.forEach(_.difference(productsAll, substratesAll), function(p) {
        try {
            pros.push(compounds[p][0] * compounds[p][1]);
        }
        catch (error) {
            ;
        }
    });
    return Math.ceil((_.sum(pros)-_.sum(subs))*(_.sum(rxns)+1)/steps.length);
}


/**
 * Return pathways that meet filtering conditions.
 * @param {array} pathways pathway arrays.
 * @param {object} filter filter object.
 * @param {object} context context object.
 *
 * @returns {array} Approved pathways.
 */
function filterPathways(pathways, filter, context) {
    var rxnEcs = context.reaction_ecs;
    var S = context.stoichiometrics;
    var C = filter.compounds;
    var E = filter.enzymes;
    var s = filter.source;
    var t = filter.target;
    var Fl = filter.links;
    var compounds;
    var enzymes;
    var approved;
    var substrates;
    var products;
    var prepreC;
    var preC;
    var discard1;
    var discard2;
    var intersectProsSubs;
    var intersectFilterSubs;
    var intersectAll;
    return _.remove(pathways, function(pathway) {
        approved = true;
        compounds = ['any'];
        enzymes = [];
        _.forEach(pathway, function(reaction, i, pw) {
            substrates = _.keys(S[reaction][0]);
            products = _.keys(S[reaction][1]);
            // Check if target is consumed.
            if (_.includes(substrates, t)) {
                approved = false;
                return false;
            // Check if source is produced.
            } else if (_.includes(products, s)) {
                approved = false;
                return false;
            // Check for forbidden links.
            } else if (i >= 1) {
                preC = _.keys(S[pw[i - 1]][1]);  // products
                intersectProsSubs = _.intersection(preC, substrates);
                intersectFilterSubs = _.intersection(Fl, substrates);
                intersectAll = _.intersection(preC, intersectFilterSubs);
                if (intersectAll.length >= intersectProsSubs.length) {
                    approved = false;
                    return false;
                }
                // Check for repetitive consuming and producing.
                if (i >= 2) {
                    prepreC = _.keys(S[pw[i - 2]][0]);  // substrates
                    discard1 = _.intersection(prepreC, substrates);
                    discard2 = _.intersection(preC, substrates);  // products
                    if (discard1.length !== 0 && discard2.length !== 0) {
                        approved = false;
                        return false;
                    }
                    prepreC = _.keys(S[pw[i - 2]][1]);  // products
                    preC = _.keys(S[pw[i - 1]][0]);  // substrates
                    discard1 = _.intersection(prepreC, products);
                    discard2 = _.intersection(preC, products);
                    if (discard1.length !== 0 && discard2.length !== 0) {
                        approved = false;
                        return false;
                    }
                }
            }
            compounds.push(substrates);
            compounds.push(products);
            enzymes.push(rxnEcs[reaction]);
            });
        // Check for compounds and enzymes.
        if (_.intersection(C, _.flattenDeep(compounds)).length !== C.length) {
            approved = false;
        } else if (_.intersection(E, _.flattenDeep(enzymes)).length !== E.length) {
            approved = false;
        }
        if (approved) {
            return true;
        }
    });
}


/**
 * Return pathways from source to target.
 * @param {object} G jsnx.DiGraph object
 * @param {string} source pathway source Rhea ID.
 * @param {string} target pathway target Rhea ID.
 *
 * @returns {array} Rhea ID arrays.
 */
function findPathway(G, source, target) {
    var pathway;
    var pathwaysAll;
    var optParameters = {};
    if (source !== null) {
        optParameters['source'] = source;
        if (target !== null) {  // source to target
            optParameters['target'] = target;
            try {
                pathway = [jsnx.shortestPath(G, optParameters)];
            }
            catch (error) {
                ;
            }
        } else {  // source to all targets
            try {
                pathwaysAll = jsnx.shortestPath(G, optParameters);
            }
            catch (error) {
                ;
            }
        }
    } else if (target !== null) {  // all sources to target
        optParameters['target'] = target;
        try {
            pathwaysAll = jsnx.shortestPath(G, optParameters);
        }
        catch (error) {
            ;
        }
    } 
    // all sources to all targets not implemented
    if (pathwaysAll !== undefined) {
        return _.values(pathwaysAll._stringValues);
    } else {
    return pathway;
    }
}


/**
 * Format output for showing results.
 */
function formatOutput(document, results, context) {
    var ol = createHTMLElement(document, 'OL');
    if (results === undefined) {
        ol.innerHTML = 'Invalid search parameters. Please enter either at '
            + 'least 2 compounds or at least 1 enzyme.';
    } else if (results.length === 0) {
        ol.innerHTML = 'No pathways were found.';
    } else {
        _.forEach(results, function(pw) {
            ol.appendChild(formatPathway(document, pw, context));
        });
    }
    return ol;
}


/**
 * Format a compound entry in results.
 */
function formatCompound(document, chebi, context) {
    var liMain = createHTMLElement(document, 'LI');
    liMain.innerHTML = 'ChEBI:' + chebi + ' ' + context.compounds[chebi];
    return liMain;
}


/**
 * Format a list tag.
 */
function formatList(document, listTag, title, container, f, context) {
    var liMain = createHTMLElement(document, 'LI');
    var list = createHTMLElement(document, listTag);
    liMain.innerHTML = title;
    _.forEach(container, function(c) {
        list.appendChild(f(document, c, context));
    });
    liMain.appendChild(list);
    return liMain;
}


/**
 * Format a pathway entry in results.
 */
function formatPathway(document, pathway, context) {
    var li;
    var ul;
    var ol;
    var liMain = createHTMLElement(document, 'LI');
    var ulMain = createHTMLElement(document, 'UL');
    var S = [];
    var I;
    var P = [];
    var namesS;
    var namesP;
    var totalReaction = 'totalReaction';
    var pwPoints = pathway[0];
    // Group compounds to S, I and P.
    _.forEach(pathway[1], function(rhea) {
        S.push.apply(S, _.keys(context.stoichiometrics[rhea][0]));
    });
    _.forEach(pathway[1], function(rhea) {
        P.push.apply(P, _.keys(context.stoichiometrics[rhea][1]));
    });
    I = _.uniq(_.intersection(S, P));
    S = _.uniq(_.difference(S, I));
    P = _.uniq(_.difference(P, I));
    // Total reaction
    namesS = _.map(S, function(chebi) {return context.compounds[chebi];});
    namesP = _.map(P, function(chebi) {return context.compounds[chebi];});
    totalReaction = namesS.join(' + ') + ' => ' + namesP.join(' + ');
    liMain.innerHTML = 'Total reaction: <b>' + totalReaction + '</b>';
    // Points
    li = createHTMLElement(document, 'LI');
    li.innerHTML = 'Score: ' + pwPoints;
    ulMain.appendChild(li);
    // Substrates
    li = formatList(document, 'UL', 'Substrates:', S, formatCompound, context);
    ulMain.appendChild(li);
    // Intermediates
    li = formatList(document, 'UL', 'Intermediates:', I, formatCompound,
        context);
    ulMain.appendChild(li);
    // Products
    li = formatList(document, 'UL', 'Products:', P, formatCompound, context);
    ulMain.appendChild(li);
    // Reaction steps
    li = formatList(document, 'OL', 'Reaction steps:', pathway[1],
        formatReaction, context);
    ulMain.appendChild(li);
    
    liMain.appendChild(ulMain);
    liMain.innerHTML += '<br>'
    return liMain;
}


/**
 * Format a reaction entry in results.
 */
function formatReaction(document, rhea, context) {
    var liMain = createHTMLElement(document, 'LI');
    var dl = createHTMLElement(document, 'DL');
    var dt = createHTMLElement(document, 'DT');
    var dd = createHTMLElement(document, 'DD');
    var enzymes = context.reaction_ecs[rhea];
    var substrates = _.keys(context.stoichiometrics[rhea][0]);
    var products = _.keys(context.stoichiometrics[rhea][1]);
    dt.innerHTML = '<b>' + context.equations[rhea] + '</b>';
    dl.appendChild(dt);
    dd.innerHTML = 'Rhea:' + rhea;
    dl.appendChild(dd);
    _.forEach(enzymes, function(ec) {
        dd = createHTMLElement(document, 'DD');
        dd.innerHTML = 'EC:' + ec + ' ' + context.enzymes[ec];
        dl.appendChild(dd);
    });
    _.forEach(substrates, function(chebi) {
        dd = createHTMLElement(document, 'DD');
        dd.innerHTML = 'Substrate ChEBI:' + chebi + ' ' + context.compounds[chebi];
        dl.appendChild(dd);
    });
    _.forEach(products, function(chebi) {
        dd = createHTMLElement(document, 'DD');
        dd.innerHTML = 'Product ChEBI:' + chebi + ' ' + context.compounds[chebi];
        dl.appendChild(dd);
    });
    liMain.appendChild(dl)
    return liMain;
}


/**
 * Return values from a form of input and 2 select fields.
 * @param {HTMLElement} form the HTML form element.
 *
 * @returns {object} selected values of form. Keys: 'compounds',
   'enzymes' and 'nResults'.
 */
function getInputValues(form) {
    var selectNodes = form.getElementsByTagName('SELECT');
    var nodeNResults = selectNodes[0];
    var nodeCompounds = selectNodes[1];
    var nodeEnzymes = selectNodes[2];
    var nodeFilterLinks = selectNodes[3];
    var nResults = Number(getMultiselectValues(nodeNResults));
    var compounds = getMultiselectValues(nodeCompounds);
    var enzymes = getMultiselectValues(nodeEnzymes);
    var filterLinks = getMultiselectValues(nodeFilterLinks);
    var result = {
        compounds: compounds,
        enzymes: enzymes,
        filterLinks: filterLinks,
        nResults: nResults,
    };
    return result;
}


/**
 * Return all selected values of a select element.
 * @param {HTMLElement} select the HTML select element.
 *
 * @returns {array} selected values of the select element.
 */
function getMultiselectValues(select) {
    var result = [];
    var options = select && select.options;
    var option;
    for (var i = 0, iLen = options.length; i < iLen; i++) {
        option = options[i];
        if (option.selected) {
            result.push(option.value);
        }
    }
    return result;
}


/**
 * Return an initialized jsnx.DiGraph.
 * @param {object} S stoichiometrics object.
 * @param {object} C compounds object.
 * @param {object} I ignored compounds array.
 *
 * @returns {object} jsnx.DiGraph.
 */
function initializeGraph(S, C, I) {
    var G = new jsnx.DiGraph();
    _.forOwn(S, function(rxnCompounds, reaction) {
        _.forOwn(rxnCompounds[1], function(empty, product) {
            // Check that the product is not an ignore compound.
            if (!_.includes(I, product)) {
                _.forEach(C[product][0], function(consumerRxn) {
                    // Check that target is not opposite of source.
                    if (!_.isEqual(S[consumerRxn][1], rxnCompounds[0])) {
                        G.addEdge(reaction, consumerRxn);
                    }
                });
            }
        });
    });
    return G;
}


/**
 * Initialize HTML form at Input section.
 */
function initializeForm(rheaChebis, chebiNames, rheaEcs, ecNames) {
    var compounds = [{id: 'any', text: 'any ChEBI'}];
    var enzymes = [];
    var nResults = [];
    var i = 1;
    var iLen = 20;
    for (; i <= iLen; i++) {
        nResults.push({id:i, text:i});
    }
    _.forEach(rheaChebis, function(chebi) {
        compounds.push({id: chebi, text: chebi + ' ' + chebiNames[chebi]});
    });
    _.forEach(rheaEcs, function(ec) {
        enzymes.push({id: ec, text: ec + ' ' + ecNames[ec]});
    });
    $('#idNResults').select2({
        data: nResults,
    });
    $('#idSelectCompounds').select2({
        data: compounds,
    });
    $('#idSelectEnzymes').select2({
        data: enzymes,
    });
    $('#idSelectFilterLinks').select2({
        data: compounds,
    });
    return;
}




/**
 * Return data for pathway evaluation.
 * @param {array} pathways
 * @param {object} S
 * @param {object} C
 * @param {object} D
 * @param {object} P
 *
 * @returns {array}
 */
function orderPathwayData(pathways, S, C, D, P) {
    var steps = [];
    var stepsPw;
    var compounds = [];
    var compoundsPw;
    var reaction = [];
    var substrates = [];
    var products = [];
    var subs;
    var pros;
    _.forEach(pathways, function(pw) {
        stepsPw = [];
        compoundsPw = {};
        _.forEach(pw, function (rxn) {
            substrates = _.keys(S[rxn][0]);
            products = _.keys(S[rxn][1]);
            _.forEach(substrates, function(s) {
                compoundsPw[s] = [D[s], P[s]];
            });
            _.forEach(products, function(p) {
                compoundsPw[p] = [D[p], P[p]];
            });
            stepsPw.push([C[rxn], substrates, products]);
        });
        steps.push(stepsPw);
        compounds.push(compoundsPw);
    });
    return [steps, compounds];
}


/**
 * Submit and evaluate input and return output.
 */
function submitSearch() {
    var outputSlot = document.getElementById('outputDiv');
    var form = document.getElementById('inputForm');
    var tmp = document.createElement('div');
    var input = getInputValues(form);
    var results;
    var lenChildren = outputSlot.childNodes.length;
    var nIsValid = validateInputN(input.nResults);
    var cEIsValid = validateInputCE(input.compounds, input.enzymes);
    if (validateInputN(nIsValid) && cEIsValid) {
        results = evaluateInput(
            GRAPH, input.nResults, input.compounds, input.enzymes,
            input.filterLinks, CONTEXT);
    }
    tmp.appendChild(formatOutput(document, results, CONTEXT));
    outputSlot.innerHTML = tmp.innerHTML;
    return;
};


/**
 * Return a boolean of the validity of two fields.
 * @param {array} compounds array of chosen compounds.
 * @param {array} enzymes array of chosen enzymes.
 *
 * @returns {boolean} false if both compounds and enzymes are empty
    arrays. Returns true otherwise.
 */
function validateInputCE(compounds, enzymes) {
    var isValid;
    var lenCompounds = compounds.length;
    var lenEnzymes = enzymes.length;
    if (lenCompounds >= 2) {
        isValid = true;
    } else if (lenEnzymes >= 1) {
        isValid = true;
    } else {
        isValid = false;
    }
    return isValid;
}


/**
 * Return a boolean of the validity of the numeric field.
 * @param {number} n the number in the field.
 *
 * @returns {boolean} true if 1 < n < 20. Returns false otherwise.
 */
function validateInputN(n) {
    var isValid;
    if (isNaN(n) || n < 1 || n > 20) {
        isValid = false;
    } else {
        isValid = true;
    }
    return isValid;
}

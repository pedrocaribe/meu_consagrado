# Import main modules
import discord

# Import secondary modules
from math import floor
from itertools import cycle


admin = '<@380901552195371020>'
member_admin = 'veritasaequitas1'
role_msg_id = 914303897277976606
emoji_id = '👍'
units = ['B', 'KiB','MiB','GiB','TiB']

bot_cogs = [
            'cogs.cog_modCommands',
            'cogs.cog_cs50Commands',
            'cogs.cog_generalCommands',
            'cogs.cog_Music',
            'cogs.cog_ownerCommands',
            'cogs.cog_System',
            'cogs.cog_chatgpt_ai',
            'cogs.cog_Game',
            'cogs.cog_Study'
            ]

monitor_errors = [
                'attribute',
                'TypeError',
                'RuntimeWarning',
                'was never awaited',
                'ERROR'
                ]

ignore_errors = [
                'Need 11 character',
                'Already playing audio'
                ]

fraseMeio = [
            'meu Magnata',
            'meu Feiticeiro',
            'meu Imperador',
            'meu Diplomata',
            'meu Embaixador',
            'meu Almirante',
            'meu Comendador',
            'meu Engenheiro',
            'meu Bacharel',
            'meu Chanceler',
            'meu Eclesiasta',
            'meu Paladino',
            'meu Estivador',
            'meu Menestrel',
            'meu Comensal',
            'meu Suserano',
            'meu Leviatã',
            'meu Kylo Ren',
            'meu Cangaceiro',
            'meu Sambarilove',
            'meu Dig Dig Joy',
            'meu Aliado',
            'meu Querido',
            'meu Parceiro',
            'meu Aliado',
            'meu Bom',
            'meu Rei',
            'meu Amigo',
            'meu Doutrinador',
            'meu Queridão',
            'gente boa',
            'meu Mestre',
            'Fera',
            'meu Patrão',
            'Chapa',
            'meu Chapa',
            'Chefia',
            'Campeão'
            ]

fraseFinal = [
            'Pegue os limões que a vida te dá e faça uma bela caipirinha!',
            'Barriga de porco e um choppinho gelado, vai??',
            'Desce uma que o dia ta começando!',
            'OOOOOOOOOOOOOOOPA VÊ MAIS UM BALDE PRA GENTE AQUI...',
            'Desce aquela porçãozinha de fritas e uma gelada??',
            '3 cachacinhas pra aquecer ou nem?'

            ]

status = cycle([
                'Feito em Python',
                'Coded in Python',
                'By Pedro Caribé',
                'Pythonic Way',
                'Sugestões?',
                'Suggestions?',
                'Dúvidas? %help'
                ])

arbitragem = '''Como é possível a arbitragem?

As apostas de arbitragem são possíveis quando há uma discrepância entre as probabilidades que permitem obter lucro cobrindo todos os resultados. __*Normalmente*__, esta é uma aposta binária – com apenas dois resultados. Um exemplo seria uma partida de tênis, onde apenas dois resultados são possíveis.
As oportunidades de arbitragem geralmente surgem quando as casas de apostas discordam das probabilidades ou cometem um erro ao precificar um mercado.
A arbitragem está muito longe do jogo tradicional. __É mais um processo matemático para garantir o lucro__.
Muitos sistemas de apostas de futebol e estratégias de corridas de cavalos são sustentados pelas teorias associadas à arbitragem.
Fora isso, toda casa de apostas considerada boa pode ser utilizada para fazer a aplicação da arbitragem. Contudo, algumas, são melhores que outras.

Essas casas geralmente são as que disponibilizam odds promocionais ou aprimoradas. Sendo assim, indicamos que aplique a arbitragem nas seguintes plataformas: **__Betano, Bet365 e Betway__**.'''

languages = [
    ('aa', 'Afar'),
    ('ab', 'Abkhazian'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('an', 'Aragonese'),
    ('hy', 'Armenian'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ae', 'Avestan'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('ba', 'Bashkir'),
    ('bm', 'Bambara'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bh', 'Bihari languages'),
    ('bi', 'Bislama'),
    ('bo', 'Tibetan'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('my', 'Burmese'),
    ('ca', 'Catalan; Valencian'),
    ('cs', 'Czech'),
    ('ch', 'Chamorro'),
    ('ce', 'Chechen'),
    ('zh', 'Chinese'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cv', 'Chuvash'),
    ('kw', 'Cornish'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('cy', 'Welsh'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dv', 'Divehi; Dhivehi; Maldivian'),
    ('nl', 'Dutch; Flemish'),
    ('dz', 'Dzongkha'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('ee', 'Ewe'),
    ('fo', 'Faroese'),
    ('fa', 'Persian'),
    ('fj', 'Fijian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('fy', 'Western Frisian'),
    ('ff', 'Fulah'),
    ('Ga', 'Georgian'),
    ('de', 'German'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('ga', 'Irish'),
    ('gl', 'Galician'),
    ('gv', 'Manx'),
    ('el', 'Greek, Modern (1453-)'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian; Haitian Creole'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hz', 'Herero'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('hy', 'Armenian'),
    ('ig', 'Igbo'),
    ('is', 'Icelandic'),
    ('io', 'Ido'),
    ('ii', 'Sichuan Yi; Nuosu'),
    ('iu', 'Inuktitut'),
    ('ie', 'Interlingue; Occidental'),
    ('ia', 'Interlingua (International Auxiliary Language Association)'),
    ('id', 'Indonesian'),
    ('ik', 'Inupiaq'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('jv', 'Javanese'),
    ('ja', 'Japanese'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('kn', 'Kannada'),
    ('ks', 'Kashmiri'),
    ('ka', 'Georgian'),
    ('kr', 'Kanuri'),
    ('kk', 'Kazakh'),
    ('km', 'Central Khmer'),
    ('ki', 'Kikuyu; Gikuyu'),
    ('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('kv', 'Komi'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('kj', 'Kuanyama; Kwanyama'),
    ('ku', 'Kurdish'),
    ('lo', 'Lao'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('li', 'Limburgan; Limburger; Limburgish'),
    ('ln', 'Lingala'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('lu', 'Luba-Katanga'),
    ('lg', 'Ganda'),
    ('mk', 'Macedonian'),
    ('mh', 'Marshallese'),
    ('ml', 'Malayalam'),
    ('mi', 'Maori'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('Mi', 'Micmac'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('mt', 'Maltese'),
    ('mn', 'Mongolian'),
    ('mi', 'Maori'),
    ('ms', 'Malay'),
    ('my', 'Burmese'),
    ('na', 'Nauru'),
    ('nv', 'Navajo; Navaho'),
    ('nr', 'Ndebele, South; South Ndebele'),
    ('nd', 'Ndebele, North; North Ndebele'),
    ('ng', 'Ndonga'),
    ('ne', 'Nepali'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'),
    ('no', 'Norwegian'),
    ('oc', 'Occitan (post 1500)'),
    ('oj', 'Ojibwa'),
    ('or', 'Oriya'),
    ('om', 'Oromo'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('fa', 'Persian'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ps', 'Pushto; Pashto'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('rn', 'Rundi'),
    ('ru', 'Russian'),
    ('sg', 'Sango'),
    ('sa', 'Sanskrit'),
    ('si', 'Sinhala; Sinhalese'),
    ('sk', 'Slovak'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('se', 'Northern Sami'),
    ('sm', 'Samoan'),
    ('sn', 'Shona'),
    ('sd', 'Sindhi'),
    ('so', 'Somali'),
    ('st', 'Sotho, Southern'),
    ('es', 'Spanish; Castilian'),
    ('sq', 'Albanian'),
    ('sc', 'Sardinian'),
    ('sr', 'Serbian'),
    ('ss', 'Swati'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('ty', 'Tahitian'),
    ('ta', 'Tamil'),
    ('tt', 'Tatar'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('tl', 'Tagalog'),
    ('th', 'Thai'),
    ('bo', 'Tibetan'),
    ('ti', 'Tigrinya'),
    ('to', 'Tonga (Tonga Islands)'),
    ('tn', 'Tswana'),
    ('ts', 'Tsonga'),
    ('tk', 'Turkmen'),
    ('tr', 'Turkish'),
    ('tw', 'Twi'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('vo', 'Volapük'),
    ('cy', 'Welsh'),
    ('wa', 'Walloon'),
    ('wo', 'Wolof'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu')
]

def humanizer(size, d_unit):
    for unit in units:
        if unit == d_unit:
            break
        size /= 1024.0
    return f'{size:.{2}f}{unit}'


def get_size(size):
    for unit in ['B', 'KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f'{size:.{2}f}{unit}'


def digitExtractedProcessed(card_number):
    a = floor(floor(card_number % 100) // 10) * 2
    if a > 9:
        a = a // 10 + a % 10
    return a


def digitExtractedProcessed2(card_number):
    a = (floor(card_number % 100) // 10)
    return a


def reduceCardN(card_number):
    rdCardN = 0
    if card_number > 134:
        rdCardN = card_number // 100
    elif card_number < 100:
        rdCardN = card_number // 10
    else:
        rdCardN = card_number
    return rdCardN


def lastDigitExtractedProcessed(card_number):
    a = card_number % 10
    return a
import bs4, pandas, time, requests, datetime


def get_price_info(finnkode):
    url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=' + finnkode
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    element = soup.find_all(name='div', class_='panel')
    text = str(element[2].text).strip().replace('\xa0','').split('kr')
    price = int(text[0].replace('\n','').replace(' ','').replace('Prisantydning',''))
    expenses = int(text[1].replace('\n','').replace(' ','').replace('Omkostninger',''))
    total_price = int(text[2].replace('\n','').replace(' ','').replace('Totalpris',''))
    municipality_tax = int(text[3].replace('\n','').replace(' ','').replace('Kommunaleavg.',''))
 
    return price, expenses, total_price, municipality_tax


def get_object_info(finnkode):
    url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=' + finnkode
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    element = soup.find_all(name='dl', class_='definition-list--cols1to2')
    lst = element[0].text.strip().split('\n')
    sum = 0
    list_values = []
    list_keys = []
    for i in lst:
        if sum%2 == 0:
            list_keys.append(i)
            sum += 1
        else:
            list_values.append(i)
            sum += 1

    lst = list(zip(list_keys,list_values))

    boligtype = lst[0][1]
    eierform = lst[1][1]
    sov = lst[2][1]
    pri_rom = lst[3][1]
    bolig_areal = lst[4][1]
    bygg_aar = lst[5][1]
    energi = lst[7][1]
    tomt_areal = lst[9][1]

    if 'Selveier' in eierform:
        eierform = 'Selveier'

    sov = int(sov)
    pri_rom_tmp = pri_rom.split(' ')
    pri_rom = int(pri_rom_tmp[0])
    bolig_areal_tmp = bolig_areal.split(' ')
    bolig_areal = int(bolig_areal_tmp[0])
    bygg_aar = int(bygg_aar)
    energi = energi.replace(' ','').split('-')
    energi_bokstav = energi[0]
    energi_farge = energi[1]
    tomt_areal_tmp = tomt_areal.split(' ')
    tomt_areal= int(tomt_areal_tmp[0])
    tomt_eieform = tomt_areal_tmp[2].replace('(','').replace(')','')

    return boligtype, eierform, sov, pri_rom, bolig_areal, bygg_aar, energi_bokstav, energi_farge, tomt_areal, tomt_eieform


def get_address_info(finnkode):
    url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=' + finnkode
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    element = soup.find_all(name='p', class_='u-mh16')
    adresse = element[0].text
    adresse_tmp = adresse.split(',')
    gate = adresse_tmp[0]
    post_nr_tmp = adresse_tmp[1].split(' ')
    post_nr = int(post_nr_tmp[1])
    post_sted = post_nr_tmp[2]

    return gate, post_nr, post_sted



def get_visning_info(finnkode):
    url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=' + finnkode
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    element = soup.find_all(name='dl', class_='u-mb0')
    temp_visning_dato = element[0].text
    visnigsdato = temp_visning_dato.replace('\n','').split('\xa0')
    visning_tidspunkt = visnigsdato[1]
    visning = visnigsdato[0].replace(' ','').split('.')
    visning_dag = int(visning[1])
    visning_mnd = get_month(visning[2].lower())
    now = datetime.datetime.now()
    visning_aar = now.year
    visning_objekt=[visning_aar, visning_mnd, visning_dag, visning_tidspunkt]
    

    return visning_objekt


def get_month(visnings_mnd):
    if visnings_mnd == 'januar':
        visnings_mnd = 1
        return visnings_mnd
    elif visnings_mnd == 'februar':
        visnings_mnd = 2
        return visnings_mnd
    elif visnings_mnd == 'mars':
        visnings_mnd = 3
        return visnings_mnd
    elif visnings_mnd == 'april':
        visnings_mnd = 4
        return visnings_mnd
    elif visnings_mnd == 'mai':
        visnings_mnd = 5
        return visnings_mnd
    elif visnings_mnd == 'juni':
        visnings_mnd = 6
        return visnings_mnd
    elif visnings_mnd == 'juli':
        visnings_mnd = 7
        return visnings_mnd
    elif visnings_mnd == 'august':
        visnings_mnd = 8
        return visnings_mnd
    elif visnings_mnd == 'september':
        visnings_mnd = 9
        return visnings_mnd
    elif visnings_mnd == 'oktober':
        visnings_mnd = 10
        return visnings_mnd
    elif visnings_mnd == 'november':
        visnings_mnd = 11
        return visnings_mnd
    elif visnings_mnd == 'desember':
        visnings_mnd = 12
        return visnings_mnd
    else:
        print("Error: Ingen valg passet input string")

x = get_price_info(finnkode=str(242042295))

y = get_object_info(finnkode=str(242042295))

z = get_address_info(finnkode=str(242042295))

w = get_visning_info(finnkode=str(242042295))

print(x)
print(y)
print(z)
print(w)

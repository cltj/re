import bs4, pandas, time, requests


def get_panel_1_info(finnkode):
    url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=' + finnkode
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    element = soup.find_all(name='div', class_='panel')
    p = str(element[2].text).strip().replace('\xa0','').split('kr')
    n = p[0].replace('\n','').replace(' ','').replace('Prisantydning','')
    o = p[1].replace('\n','').replace(' ','').replace('Omkostninger','')
    t = p[2].replace('\n','').replace(' ','').replace('Totalpris','')
    k = p[3].replace('\n','').replace(' ','').replace('Kommunaleavg.','')
    price = int(n)
    cost = int(o)
    total_price = int(t)
    yearly_municipality_expense = int(k)


    return price, cost, total_price, yearly_municipality_expense


def get_panel_2_info(finnkode):
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


def get_panel_3_info(finnkode):
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

x = get_panel_1_info(finnkode=str(242042295))

y = get_panel_2_info(finnkode=str(242042295))

z = get_panel_3_info(finnkode=str(242042295))
print(x+y+z)

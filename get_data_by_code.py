import bs4, pandas, time, requests, datetime

def get_sales_object_soup(finn_code):
    """
    Gets the soup
    param: finn_code (str)
    return: soup
    """
    url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=' + finn_code
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    return soup


def get_price_info(soup):
    """
    Gets price information and convert to integers
    param: soup
    return: price, expenses, total_price, municipality_tax
    """
    element = soup.find_all(name='div', class_='panel')
    text = str(element[2].text).strip().replace('\xa0','').split('kr')
    price = int(text[0].replace('\n','').replace(' ','').replace('Prisantydning',''))
    expenses = int(text[1].replace('\n','').replace(' ','').replace('Omkostninger',''))
    total_price = int(text[2].replace('\n','').replace(' ','').replace('Totalpris',''))
    municipality_tax = int(text[3].replace('\n','').replace(' ','').replace('Kommunaleavg.',''))
 
    return price, expenses, total_price, municipality_tax


def get_object_info(soup):
    """
    Gets and coverts all data for the sales object
    param: soup
    return: 18 datapoints from the sales object
    """
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

    house_type = lst[0][1]
    form_of_ownership = lst[1][1]
    bedroom = lst[2][1]
    prime_living_area = lst[3][1]
    total_living_area = lst[4][1]
    build_year = lst[5][1]
    energy = lst[7][1]
    plot_area = lst[9][1]

    if 'Selveier' in form_of_ownership:
        form_of_ownership = 'Selveier'

    bedroom = int(bedroom)
    prime_living_area_tmp = prime_living_area.split(' ')
    prime_living_area = int(prime_living_area_tmp[0])
    total_living_area_tmp = total_living_area.split(' ')
    total_living_area = int(total_living_area_tmp[0])
    build_year = int(build_year)
    energy = energy.replace(' ','').split('-')
    energy_letter= energy[0]
    energy_color = energy[1]
    plot_area_tmp = plot_area.split(' ')
    plot_area = int(plot_area_tmp[0])
    plot_owner_form = plot_area_tmp[2].replace('(','').replace(')','')

    more_key_info = []
    element = soup.find_all(name='div', class_='u-display-none')
    for elem in element[1].contents:
        if len(elem) > 4:
            more_key_info.append(elem.text.strip().split('\n'))

    for item in more_key_info:
        if item[0].lower() == 'bruttoareal':
            gross_area_tmp = item[1].split(' ')
            gross_area = int(gross_area_tmp[0])
        elif item[0].lower() == 'formuesverdi':
            wealth_value_tmp = item[1].replace('\xa0','').split(' ')
            wealth_value = int(wealth_value_tmp[0])
        elif item[0].lower() == 'arealbeskrivelse':
            area_description = item[1]
        elif len(item) == 3:
            municipality_number_tmp = item[0].replace(' ','').split(':')
            municipality_number = int(municipality_number_tmp[1])
            gards_nummer_tmp = item[1].replace(' ','').split(':')
            gards_nummer = int(gards_nummer_tmp[1])
            bruks_nummer_tmp = item[2].replace(' ','').split(':')
            bruks_nummer = int(bruks_nummer_tmp[1])
        elif item[0].lower() == 'omkostninger':
            expenses_text = item[1]
        else:
            facilities = item

    return house_type, form_of_ownership, bedroom, prime_living_area, total_living_area, build_year, energy_letter, energy_color, plot_area, plot_owner_form, gross_area, wealth_value, area_description, municipality_number, gards_nummer, bruks_nummer, expenses_text, facilities


def get_address_info(soup):
    """
    Gets the address information for the sales object
    param: soup
    return: street, post_number, post_place
    """
    element = soup.find_all(name='p', class_='u-mh16')
    address = element[0].text
    address_tmp = address.split(',')
    street = address_tmp[0]
    post_nr_tmp = address_tmp[1].split(' ')
    post_number = int(post_nr_tmp[1])
    post_place = post_nr_tmp[2]

    return street, post_number, post_place


def get_showing_info(soup):
    """
    Gets and formats the date of open house (showing)
    Uses helper function 'get_month' to find number eq to str <month>(ex. januar)
    param: soup
    raturn showing_date
    """
    element = soup.find_all(name='dl', class_='u-mb0')
    tmp_showing_date = element[0].text
    showingdate = tmp_showing_date.replace('\n','').split('\xa0')
    showing_time = showingdate[1]
    showing = showingdate[0].replace(' ','').split('.')
    showing_day = int(showing[1])
    showing_month = get_month(showing[2].lower())
    now = datetime.datetime.now()
    showing_year = now.year
    showing_date = datetime.date(showing_year, showing_month, showing_day)
    

    return showing_date


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

#soup = get_sales_object_soup(finn_code=str(242042295))
#x = get_price_info(soup)
#y = get_object_info(soup)
#z = get_address_info(soup)
#w = get_showing_info(soup)

#print(x)
#print(y)
#print(z)
#print(w)

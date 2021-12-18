import bs4, pandas, time, requests


def get_codes(page_number):
    url = 'https://www.finn.no/realestate/homes/search.html?location=1.22030.22105&page='+ str(page_number) +'&sort=PUBLISHED_DESC'
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    error_page = soup.find_all(name='div', class_='u-mv64')
    if not error_page:
        
        element = soup.find_all(name='h2', class_='ads__unit__content__title')
        codes = []
        for i in element:
            code = i.next.attrs['id']
            codes.append(int(code))

        lst_len = len(codes)
        if lst_len > 1:
            return codes
        else:
            return 0
    else:
        return 0


page_numbers = [1,2,3,4,5,6,7,8,9,10,11,12]
lillestrom_codes = []
for i in page_numbers:
    codes = get_codes(i)
    if codes == 0:
        print('Page ' + str(i) + ' not found. Terminating program')
        break
    else:
        lillestrom_codes.append(codes)

lst = []
for i in lillestrom_codes:
    for j in i:
        if j not in lst:
            lst.append(j)
        else:
            pass

print(len(lst))

import requests
from bs4 import BeautifulSoup as bs
import re
import csv


def scrape_page(base_url):
    page = requests.get(base_url)
    soup = bs(page.text)
    next_page = ''
    letters = soup.find('div', 'letterlinks').find_all('a')
    for letter in letters:
        letter_link = letter['href']
        letter_page = requests.get('http://www.behindthename.com'+letter_link)
        letter_soup = bs(letter_page.text)
        try:
            next_page = letter_soup.find('center').find_all('a', 'sidelink')[-1]
        except:
            pass
        while next_page:
            titles_blocks = letter_soup.find_all('div', 'browsename')
            for titles_block in titles_blocks:
                name_link = titles_block.find('b').find('a')['href']
                name_page = requests.get('http://www.behindthename.com'+name_link)
                name_soup = bs(name_page.text)
                given_name = name_soup.find('div', 'namemain').text.split('Given Name')[-1].strip().encode('utf-8')
                variants = ''
                try:
                    variants = name_soup.find('span', text=re.compile('VARIANTS:')).find_next('span').text.strip().encode('utf-8')
                except: pass
                print variants
                other_languages = ''
                try:
                    other_languages = name_soup.find('span', text=re.compile('OTHER LANGUAGES:')).find_next('span').text.strip().encode('utf-8')
                except: pass
                diminutives = ''
                try:
                    diminutives = name_soup.find('span', text=re.compile('DIMINUTIVES:')).find_next('span').text.strip().encode('utf-8')
                except: pass
                print diminutives
                feminine_forms = ''
                try:
                    feminine_forms = name_soup.find('span', text=re.compile('FEMININE FORMS:')).find_next('span').text.strip().encode('utf-8')
                except: pass
                print given_name
                yield given_name, variants, other_languages, diminutives, feminine_forms
            try:
                next_page = letter_soup.find('center').find_all('a', 'sidelink')[-1].text
            except:
                break
            if 'Next' not in next_page:
                break
            else:
                next_page_link = 'http://www.behindthename.com' + letter_soup.find('center').find_all('a', 'sidelink')[-1]['href']
            letter_page = requests.get(next_page_link)
            letter_soup = bs(letter_page.text)


if __name__ == '__main__':
     with open('behindthenames.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(['Given Name', 'Variants,', 'Other Languages', 'Diminutives', 'Feminine Forms'])
        start_url = 'http://www.behindthename.com/names/list.php'
        s = scrape_page(start_url)
        for l in s:
             write.writerow([l[0], l[1], l[2], l[3], l[4]])



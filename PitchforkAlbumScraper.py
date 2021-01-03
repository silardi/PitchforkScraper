from selenium import webdriver
import bs4


def get_pitchfork_albums(review_url):
    driver = webdriver.Firefox()
    driver.get(review_url)
    albums = driver.find_elements_by_class_name('review__title-album')
    album_list = []
    artist_album_list = []
    score_list = []

    for album in albums:
        album_list.append(album.text)
        album_list = album_list[0:5]  # revises list to include first 5 albums on page only

    for title in album_list:
        album_words = title.split()
        # last word in album title is used as selenium selector
        # last word is used to avoid searching for common first words like "the"
        # the search may fail if two or more album titles both contain the same last word
        album_match = driver.find_element_by_partial_link_text(str(album_words[-1]))
        artist_album_list.append(album_match.text)
        album_match.click()
        source = driver.page_source
        soup = bs4.BeautifulSoup(source, features="html.parser")
        elems = soup.find_all(class_="score")
        score = elems[0].text.strip()
        score_list.append(score)
        driver.back()

    # prints out artist, album title and score for each album
    counter = 0
    for value in artist_album_list:
        new_val = value.replace("\n", "\nAlbum:  ")
        print("Artist: " + new_val)
        print("Score:  " + score_list[counter])
        counter += 1
        print("")


get_pitchfork_albums('https://pitchfork.com/reviews/best/albums/?page=1')

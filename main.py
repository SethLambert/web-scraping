from selenium import webdriver
import csv
import time

chrome_driver_path = "C:\install\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
time.sleep(5)

url = 'https://www.rottentomatoes.com/browse/movies_at_home/sort:popular'
driver.get(url)
time.sleep(5)

streaming_services = ['peacock', 'netflix', 'hulu', 'amazon_prime', 'disney_plus', 'max_us', 'paramount_plus']

for service in streaming_services:
    bubble = driver.find_element("css selector", f'where-to-watch-bubble[value="{service}"]')
    # activate service sort
    bubble.click()
    time.sleep(10)
    
    #scrape and save movies
    movie_element_list = driver.find_elements("css selector", 'a[data-qa="discovery-media-list-item-caption"]')
    movie_list = [movie_element_list[i].text for i in range(len(movie_element_list))]

    field_names=['Title','Critic_Score','Audience_Score']
    movies = []
    for movie in movie_list:
        movie_details = {
            'Title': movie.splitlines()[2],
            'Critic_Score': movie.splitlines()[0],
            'Audience_Score': movie.splitlines()[1]
        }
        movies.append(movie_details)
        
    with open(f'{service}_Movies.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(movies)
    
    #deactivate service sort
    bubble.click()
    time.sleep(5)
    

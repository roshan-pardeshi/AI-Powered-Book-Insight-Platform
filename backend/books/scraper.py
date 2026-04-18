import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from books.models import Book

def scrape_books(url, pages=2):
    """
    Scrape book data from a website using Selenium.
    This is a generic scraper; adjust selectors based on the actual site.
    """
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    books_data = []

    try:
        for page in range(1, pages + 1):
            page_url = f"{url}?page={page}" if page > 1 else url
            driver.get(page_url)
            time.sleep(3)  # Wait for page to load

            # Adjust selectors based on the website structure
            # Example selectors for a book listing site
            book_elements = driver.find_elements(By.CSS_SELECTOR, ".book-item")  # Adjust selector

            for book_elem in book_elements:
                try:
                    title = book_elem.find_element(By.CSS_SELECTOR, ".book-title").text
                    author = book_elem.find_element(By.CSS_SELECTOR, ".book-author").text
                    rating = float(book_elem.find_element(By.CSS_SELECTOR, ".book-rating").text)
                    description = book_elem.find_element(By.CSS_SELECTOR, ".book-description").text
                    book_url = book_elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    books_data.append({
                        'title': title,
                        'author': author,
                        'rating': rating,
                        'description': description,
                        'url': book_url
                    })
                except Exception as e:
                    print(f"Error parsing book: {e}")
                    continue

    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

    return books_data

def save_books_to_db(books_data):
    """
    Save scraped book data to the database.
    """
    for book_data in books_data:
        Book.objects.get_or_create(
            title=book_data['title'],
            defaults=book_data
        )
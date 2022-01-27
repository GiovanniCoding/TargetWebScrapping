# Target Web Scraping Example

Example of the use of libraries to obtain data through Web Scraping, for this exercise we mainly use Selenium to be able to interact with browsing and the web page.

## Scraped Data

The solution is saved in a dictionary for each of the requested fields.

* Price
    * To obtain the price, regular expressions were used to clean it and keep only the numerical value.
* Description
    * The article description was obtained as plain text.
* Specifications
* Highlights
* Questions
* Images urls
* Title

## Required Libraries
* Selenium == 4.1.0
* webdriver_manager == 3.5.2

```bash
pip install foobar
```
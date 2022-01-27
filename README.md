# Target Web Scraping Example

Example of the use of libraries to obtain data through Web Scraping, for this exercise we mainly use Selenium to be able to interact with browsing and the web page.

## Scraped Data

The solution is saved in a dictionary for each of the requested fields.

* Price
    * To obtain the price, regular expressions were used to clean it and keep only the numerical value.
* Title
    * The article title was obtained as plain text.
* Description
    * The article description was obtained as plain text.
* Specifications
    * The item specifications were stored in a dictionary, where each of the keys in the dictionary represents the characteristics and the value represents the specification.
* Highlights
    * The hilisegsd were stored in a list, where each item in the highlights list is a list entry.
* Questions
    * The questions were stored in a list, where each element of the list is a tuple containing 2 elements:
        * The first element is the question.
        * The second element is a list where each of the list elements is an answer for the question, this was done in this way to get all the answers in questions that have more than one answer. In case of questions that do not have any answers, this list is empty. We opted to leave out data such as username and date, although if necessary, these can be easily added.
* Images urls
    * For the images, it was decided to only add the images relevant to the current product, the urls of each of the images were stored in a list.

The structure designed to save the data was designed to maintain order and efficient access to information.

Although the clear advantages of creating a function for each of the fields to be extracted were considered, such as extracting fields exclusively, I consider that separation is not necessary for demonstration purposes.

## Required Libraries
* Selenium == 4.1.0
* webdriver_manager == 3.5.2
# LocalCart

Table of contents:
I. Manually test the website UI and features
II. Running Unit and Functional Tests
III. Running Automated UI Tests with Selenium


WARNING: Google Maps API has some fairly small usage limits for non-paying users that may cause errors if too many or too large of tests are used with LocalCart's search and resolve list features. Avoid testing too large of sample sizes.

I. Manually test the website

To best test the full functionality of the site, use the Heroku App to do the following tests. Refresh at any point to show that the backend is responding correctly and storing changes:

A. Merchant and Inventory Checking:
1. Create a merchant account using the register link.
2. Log in as the merchant.
3. Use the interface to create a store. Make sure the address used is a real address.
4. Then edit the inventory manually or with the provided CSV file. Add items that will be searched for in later manual tests.
5. Repeat this process (Steps 1-4) for multiple merchants at multiple locations. Make sure that these locations are not too far from each other in order to later test the search algorithm.

B. Customer View, List, and Search checking
6. Create a customer account.
7. Log in as the customer.
8. From the home page select the View Shopping List tab.
9. Enter a New List Name and click Add List+. Make as many lists as needed. The list currently selected is used as the "Active List" that items will be added to. 
10. Use the Search and Search Location fields in the home page to check a few queries related to the items that were previously put into the merchant's inventory.
11. Examine that the map markers are placed correctly in red for the search results. A blue marker will appear for the Search Location.
12. Select a map marker to display directions.
13. Add an item to the cart. It should now be shown on the map in green and in the View Shopping Cart menu.
14. Start a new search and see that the current list markers are still displayed.

C. Resolve List checking
15. Go to the View Shopping List menu.
16. On any existing or new list, use Item Name field and Add Item button to add text-only items to the list. Make sure that these search queries have relevant entries in the inventories constructed earlier (otherwise the search algorithm will not return results for those items without matches)
17. Input a Location in the Location field at the bottom of the Shopping List menu and then select resolve list.
18. If the search algorithm finds a matching local store item, the items will be replaced with the best choice. Otherwise, an error will display.

D. Store and Review checking
19. Select the store name in any search result to open a new tab to that store.
20. On this page, you can view the inventory of the selected store and add items to the cart.
21. Select the Reviews tab and leave a review. The review requires a rating number as well.




II. Running Unit and Functional Tests


First ensure all packages in requirements.txt have been obtained.

Obtain the code from GitHub. Ensure that in settings.py, DEBUG = True and line 88 is commented. These setting changes are necessary for running locally with sqlite3. 
line 88 :DATABASES['default'] =  dj_database_url.config()

Run the server locally using:
./manage.py runserver

While the server is running, use a separate terminal to run tests and see coverage using:
./manage.py test

This should run all of the unit and functional test that were created and provide a coverage report.

To otherwise use the application locally, send GET and POST requests using curl or a browser.




III. Running Automated UI Tests with Selenium

To run automated UI tests:
	
1. Download Selenium IDE plugin (v2.9.0) in Firefox (http://docs.seleniumhq.org/download/) 
2. Click on “Selenium IDE” in upper-right part of browser
3. File-->Open Test Suite-->testing/AutomatedUITests/iter3/TestSuite
4. Change speed to “Slow”
5. Actions-->Play entire test suite


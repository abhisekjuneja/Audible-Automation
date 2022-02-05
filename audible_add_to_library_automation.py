from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time

# Store the Script Execution Start Time
scriptStartTime = time.time()

# AMAZON ACCOUNT CREDENTIAL
AMAZON_EMAIL = "hohn.doe@gmail.com"
AMAZON_PASWD = "EnterPasswordHere"

# Create a Firefox Selenium Web Driver Object
firefoxDriver = webdriver.Firefox()

""" AMAZON AUDIBLE SIGN-IN """

# Construct the Address for Audible (IN) Sign-In Page
audibleIndiaSignInPageAddress = "https://www.amazon.in/ap/signin?"
audibleIndiaSignInPageAddress += "clientContext=259-8217305-2726058"
audibleIndiaSignInPageAddress += "&openid.pape.max_auth_age=900"
audibleIndiaSignInPageAddress += "&openid.return_to=https%3A%2F%2Fwww.audible.in%2F"
audibleIndiaSignInPageAddress += "&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select"
audibleIndiaSignInPageAddress += "&openid.assoc_handle=amzn_audible_in"
audibleIndiaSignInPageAddress += "&openid.mode=checkid_setup"
audibleIndiaSignInPageAddress += "&siteState=audibleid.userType%3Damzn%2Caudibleid.mode%3Did_res&marketPlaceId=AJO3FBRUE6J4S"
audibleIndiaSignInPageAddress += "&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select"
audibleIndiaSignInPageAddress += "&pageId=amzn_audible_in&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
audibleIndiaSignInPageAddress += "&pf_rd_p=1b60255c-ac96-4bc2-a0c8-6e6d0e32515d"
audibleIndiaSignInPageAddress += "&pf_rd_r=A7Y32NNYCEJMK0N5GS5D"

print("Opening Audible (IN) Sign-in Page...", end="")
# Navigate to the Audible (IN) Sign-In Page
firefoxDriver.get(audibleIndiaSignInPageAddress)
print("Done!")

# Insert Amazon Login Credentials to the Login Form
firefoxDriver.find_element(By.ID, "ap_email").send_keys(AMAZON_EMAIL)
firefoxDriver.find_element(By.ID, "ap_password").send_keys(AMAZON_PASWD)

# Sign into Audible (IN)
print("Signing into Audible (IN)...", end="")
firefoxDriver.find_element(By.ID, "signInSubmit").click()
print("Done!")

""" AUDIBLE GREAT COURSES - ADD TO LIBRARY """

# Construct the Address for the Search Results Page
audibleFilteredSearchHomePage = "https://www.audible.in/search?" # Base Audible (IN) Search Page
audibleFilteredSearchHomePage += "audible_programs=22940210031" # Limit to Audible Plus Catalogue
audibleFilteredSearchHomePage += "&keywords=the+great+courses" # Keyword = "The Great Courses"

# Navigate to the Search Results Page
print("Searching the Audible Plus Catalogue for 'The Great Courses' Titles...", end="")
firefoxDriver.get(audibleFilteredSearchHomePage)
print("Done!")

# Fetch the 'Results Summary' Sub-Heading Text (1 - X of Y Results)
resultsSummarySubheadingText = firefoxDriver.find_element(By.CLASS_NAME, "resultsSummarySubheading").text.strip()

# Calculate the Number of Pages that the Search Results are Split-into
totalSearchResults = int(re.findall("\d+", resultsSummarySubheadingText)[2])
resultsPerPage = 50
searchResultsPageCount = totalSearchResults // 50
searchResultsPageCount += 1 if (totalSearchResults % resultsPerPage != 0) else 0
print(f"There are [{totalSearchResults}] Search Results spread over [{searchResultsPageCount}] Pages!")

# Iterate over the Number of Pages that Contains Search Results
for i in range(searchResultsPageCount):
	# 'i' ranges from 0 to 'searchResultsPageCount' - 1
	# So, 'pageNumber' ranges from 1 to 'searchResultsPageCount'
	pageNumber = i + 1

	# Construct the Address for the Search Result Page (Paginated)
	searchResultPageAddress = "https://www.audible.in/search?" # Base Audible (IN) Search Page 
	searchResultPageAddress += "audible_programs=22940210031" # Limit to Audible Plus Catalogue
	searchResultPageAddress += "&keywords=the+great+courses" # Keyword = "The Great Courses"
	searchResultPageAddress += "&pageSize=" + str(resultsPerPage) # Results Per Page = 50 (Maximum Allowed by Audible)
	searchResultPageAddress += "&page=" + str(pageNumber)

	# Navigate to the Search Result Page Web
	print(f"Opening Page [{pageNumber}] of [{searchResultsPageCount}]...", end="")
	firefoxDriver.get(searchResultPageAddress)
	firefoxDriver.implicitly_wait(5)
	print("Done!")

	# Obtain the Initial List of 'Add to Library' Buttons for the Search Result Titles
	addToLibraryButtonList = firefoxDriver.find_elements(By.CLASS_NAME, "discovery-add-to-library-button")

	# Keep a Track of the Total Titles in the Page & the Titles that have been Added to the Library
	totalSearchResultsInPage, totalBooksAddedToLibrary = len(addToLibraryButtonList), 0

	# Iterate over the List of 'Add to Library' Buttons
	while len(addToLibraryButtonList) > 0:
		# Click the 'Add to Library' Button & Refresh the Page
		print(f"Page [{pageNumber}] of [{searchResultsPageCount}] :: Adding to Library [{totalBooksAddedToLibrary + 1}] of [{totalSearchResultsInPage}]...", end="")
		addToLibraryButton = firefoxDriver.find_element(By.CLASS_NAME, "discovery-add-to-library-button")
		addToLibraryButton.click()
		totalBooksAddedToLibrary += 1
		print("Done!")

		# Refresh the Current Search Result Page
		firefoxDriver.refresh()
		
		# Re-Obtain the List of 'Add to Library' Buttons for the Search Result Titles
		addToLibraryButtonList = firefoxDriver.find_elements(By.CLASS_NAME, "discovery-add-to-library-button")

# Store the Script Execution End Time
scriptEndTime = time.time()

# Publish the Script Execution Results and the Time Taken for Completion
print(f"Process Completed! Time taken for Execution: {str(scriptEndTime - scriptStartTime)} Seconds")

# Close the Firefox Selenium Web Driver Object
driver.quit()
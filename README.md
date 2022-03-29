# ACS-API-Wrapper
Wrapper for American Community Survey API to quickly download data as a csv file

## Folder Structure
  -  data - Contains files with lists of all ACS variables and scripts to sort these variables into various files. 
  -  fetch-data - Contains a script to download ACS data given a config file. 
  -  site-frontend - Contains code for a website that allows users to generate the above config file. 

## How to Download ACS Data
1. Visit https://acs-data.netlify.app/ and use the searchbar to search for ACS tables you would like to include in your data set. 
2. Once you have selected all of the columns you would like to include, press the download button to download the config file. 
3. Make sure to replace the `api_key` field with your own api key. If you don't have one, you can obtain one here: https://api.census.gov/data/key_signup.html. 
4. Clone this repo and run `cd ACS-API-Wrapper`.
6. Run `python fetch-data/main.py config.yaml data.csv`. 

### Important Note: The Census Bureau does not make all of its variables available for all geographies. If your data set includes one of these variables, the script will fill those columns with empty values.  

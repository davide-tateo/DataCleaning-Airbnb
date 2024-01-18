import numpy as np
import pandas as pd


### CREATING PANDAS DATAFRAME FROM CSV ###
listing = pd.read_csv('csv/AirBnbListings.csv')


# These functions were used at the start of the project to get insights on the original dataset
#print(listing.head(3))
#print(listing.info())
#print(listing.describe())



### DATA CLEANING ###


## DROPPING COLUMNS/ROWS ##
# Dropping columns not relevant to our analysis
listing.drop(['last_scraped','scrape_id','picture_url','neighbourhood_group_cleansed','calendar_updated','host_verifications','license',
              'host_about','maximum_maximum_nights','bathrooms','minimum_maximum_nights','maximum_minimum_nights','minimum_minimum_nights','description',
              'neighborhood_overview','host_thumbnail_url','host_picture_url','host_total_listings_count','host_url','listing_url',
              "calculated_host_listings_count_entire_homes",'calculated_host_listings_count_private_rooms','calculated_host_listings_count_shared_rooms'], axis=1, inplace=True)
# Dropping row with mostly null values
listing.drop(2551, inplace=True)


## DROPPING DUPLICATE VALUES ##
# count how many duplicate rows we have (it will print 0 so we won't use 'listing = listing.drop_duplicates()' as it's unnecessary)
print(listing.duplicated().sum())


## CLEANING LISTING NEIGHBOURHOOD INFORMATION ##
# Correcting geographical mistake
listing.loc[listing['neighbourhood'].str.contains('Gentofte', case=False, na=False), 'neighbourhood_cleansed'] = 'Gentofte'
listing.loc[12054, 'neighbourhood_cleansed'] = "Charlottenlund"
condition = np.logical_and(listing['neighbourhood'].str.contains('Hellerup', na=False),listing['neighbourhood_cleansed'] == "sterbro")
listing.loc[condition, 'neighbourhood_cleansed'] = 'Hellerup'
# Deleting the column neighbourhood and renaming neighbourhood_cleansed as neighbourhood
del listing['neighbourhood']
listing.rename(columns={'neighbourhood_cleansed':'neighbourhood'}, inplace=True)
# Correcting spelling mistakes
listing['neighbourhood'].replace({'Brnshj-Husum': 'Broenshoej-Husum', 'Nrrebro': 'Noerrebro', 'Vanlse': 'Vanloese', 'sterbro': 'Oesterbro', 'Amager st': 'Amager Oest'}, inplace=True)
# Checking that this part of the code is working
#print(listing.loc[12054])
#print(listing['neighbourhood'].tail(60))


## CLEANING HOST NEIGHBOURHOOD AND HOST LOCATION ##
# Filling blanks in host_neighbourhood if it's Copenhagen/Koebenhavn according to host_location
condition = np.logical_and(np.logical_or(listing['host_location'].str.contains('enha', na=False),listing['host_location'].str.contains('kbh', case = False, na=False)),listing['host_neighbourhood'].isna())
listing.loc[condition, 'host_neighbourhood'] = 'Copenhagen'
# Checking that this part of the code is working
#print(listing['host_neighbourhood'].head(60))
# Cleaning host_location specifying denmark or dividing by continent # 
# Denmark
DKlocation = ['nmark', 'gade', 'lufthavn', 'kbh', 'plads', 'vej', 'Greenland', 'enha', 'Alle', 'dk', 'kyst']
listing.loc[listing['host_location'].str.contains('|'.join(DKlocation), case=False, na=False), 'host_location'] = 'Denmark'
# Rest of Europe
europelocation_caseF =['Sweden','Italy','Norway','Spain', 'Germany','Romania','Hungary','United Kingdom','Lithuania', 'Croatia','Poland','Austria','Belgium',
                    'Netherlands', 'Switzerland','Fr', 'Portugal', 'Bulgaria', 'Iceland', 'Luxembourg', 'Estonia', 'Latvia', 'Greece','Moldova', 'London', 'UK']
europelocation_caseT = ['G','DE', 'S','IT', 'NL', 'NO','BA','CH']
listing.loc[listing['host_location'].str.contains('|'.join(europelocation_caseF), case=False, na=False), 'host_location'] = 'Europe'
listing.loc[listing['host_location'].str.contains('|'.join(europelocation_caseT), na=False), 'host_location'] = 'Europe'
# Africa
africalocation = ['Egypt','Africa', 'Kenya']
listing.loc[listing['host_location'].str.contains('|'.join(africalocation), case=False, na=False), 'host_location'] = 'Africa'
# Asia
asialocation_caseF = ['Th', 'Hong Kong','India', 'Emirate', 'Uzbekistan', 'Turkey', 'China']
asialocation_caseT = ['J', 'IL']
listing.loc[listing['host_location'].str.contains('|'.join(asialocation_caseF), case=False, na=False), 'host_location'] = 'Asia'
listing.loc[listing['host_location'].str.contains('|'.join(asialocation_caseT), na=False), 'host_location'] = 'Asia'
# Oceania
oceanialocation = ['New Zealand', 'Au']
listing.loc[listing['host_location'].str.contains('|'.join(oceanialocation), case=False, na=False), 'host_location'] = 'Oceania'
# Americas
americaslocation = ['United States', 'Peru', 'Argentina', 'Canada', 'Brazil', 'Mexico', 'Paraguay', 'Guatemala', 'Chile', 'Puerto Rico']
listing.loc[listing['host_location'].str.contains('|'.join(americaslocation), case=False, na=False), 'host_location'] = 'Americas'
listing.loc[listing['host_location'].str.contains('AR', na=False), 'host_location'] = 'Americas'
# Checking that this part of the code is working, i.e., the only possible values are the ones we decided
#unique_values = listing['host_location'].unique()
#print(unique_values)
# Inserting NotDenmark in host_neighbourhood whenever host_location is not denmark
condition = np.logical_not(listing['host_location'].str.contains('Denmark',na=False))
listing.loc[condition, 'host_neighbourhood'] = 'NotDenmark'
# Checking that this part of the code is working
#print(listing['host_location'].tail(50))
#print(listing['host_neighbourhood'].head(50))
#print(listing.loc[2672])


## CLEANING BATHROOM INFORMATION ##
# Extract numeric part form bathrooms_text and store in new column bathrooms_number
listing['bathrooms_number'] = listing['bathrooms_text'].str.extract('(\d+(\.\d+)?)', expand=False)[0]
# Set 'bathrooms_number' to 0.5 for entries containing the word "half", as it's not extracted by the previous line because it's not made of digits
listing.loc[listing['bathrooms_text'].str.contains('half', case=False, na=False), 'bathrooms_number'] = 0.5
# Convert 'bathrooms_number' to numeric
listing['bathrooms_number'] = pd.to_numeric(listing['bathrooms_number'])
# Create boolean column shared_bath, depending on the presence of "shared" in bathrooms_text
listing['shared_bath'] = listing['bathrooms_text'].str.contains('shared', case=False, na=False)
# Converting boolean to integer value (either 0 or 1)
listing['shared_bath'] = listing['shared_bath'].astype(int)
# Dropping column bathrooms_text
listing.drop('bathrooms_text', axis=1, inplace=True)
# Checking that this part of the code is working
#print(listing['bathrooms_number'].head())
#print(listing['shared_bath'].head())


## TRANSFORMING EXISTING BOOLEANS ##
# Transforming string into boolean & converting boolean into integer value (either 0 or 1)
bool_to_num = ['host_is_superhost', 'host_has_profile_pic', 'host_identity_verified', 'has_availability', 'instant_bookable']
for column in bool_to_num:
    listing[column] = listing[column].str.contains('t')
    listing[column] = listing[column].astype(int)
# Checking that this part of the code is working
#print(listing['host_is_superhost'].head(2))
#print(listing.loc[12054])


## CLEANING PRICE INFORMATION ##
# Removing  the dollar symbol and the commas, then converting to numeric
listing['price'] = listing['price'].str.replace('$', '')
listing['price'] = listing['price'].str.replace(',', '')
listing['price'] = pd.to_numeric(listing['price'], errors='coerce')
# Deleting rows where price = 0
listing.drop(listing[listing['price'] == 0].index, inplace=True)
# Checking that this part of the code is working
#print(listing['price'].describe())


## CLEANING BEDROOMS INFORMATION ##
# Correcting a row with a wrong bedroom number. Info retrieved from the column "decription".
bedrooms_to_correct = listing['bedrooms'].idxmax()
listing.at[bedrooms_to_correct, 'bedrooms'] = 3
# Checking that this part of the code is working
#print(listing.loc[bedrooms_to_correct])




### CREATING TABLE WITH INFORMATION ABOUT THE CLEANED DATASET ###
# Create a new dataframe with description of the now cleaned dataset
descript = listing.describe(include='all')
descript.drop(['id', 'name', 'host_since', 'host_id', 'host_name','latitude', 'property_type', 'longitude','amenities', 'last_review', 'first_review','calendar_last_scraped'], axis=1, inplace=True)
# Transposing the descript DataFrame
descript_T = descript.T
# Resetting the index and renaming the columns 
descript_T.reset_index(inplace=True)
descript_T.columns = ['Column_name', 'Count', 'Unique', 'Top', 'Freq', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
# Creating new columns with metrics
descript_T['Freq%'] = (descript_T['Freq'] / descript_T['Count'])*100
descript_T['Nullcount'] = listing.shape[0] - descript_T['Count']
descript_T['Nullcount%'] = descript_T['Nullcount']*100 / listing.shape[0]
descript_T['True%'] = (descript_T['Mean'][(descript_T['Min'] == 0) & (descript_T['Max'] == 1)])*100
# Rounding columns to the 3rd decimal digit
columns_to_round = ['Freq%','Mean', 'Std', 'Nullcount%', 'True%']
for column in columns_to_round:
    descript_T[column] = descript_T[column].apply(np.round, decimals=3)
# Rearranging column order
descript_T = descript_T[['Column_name', 'Count', 'Nullcount', 'Nullcount%', 'Unique', 'Top', 'Freq', 'Freq%', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max', 'True%']]
# Setting the count datatype as integer
descript_T['Count'].astype(int)
# Saving dataframe as csv file
descript_T.to_csv('Description_cleaned_AirBnbListings.csv', index=False)




### FILLING NULL VALUES TO AVOID ERRORS IN PGADMIN ###
# Dividing the columns to fill in lists depending on what we will be filling with
columns_to_fill_with_0 = ['bedrooms','bathrooms_number','beds','review_scores_rating','review_scores_accuracy', 'review_scores_cleanliness',
                        'review_scores_checkin', 'review_scores_communication','review_scores_location', 'review_scores_value']
columns_to_fill_with_0001 = ['host_response_rate', 'host_acceptance_rate']
# Fill missing values with 0
for column in columns_to_fill_with_0:
    listing[column].fillna(0, inplace=True)
# Fill missing values with 0.001
for column in columns_to_fill_with_0001:
    listing[column].fillna(0.001, inplace=True)
# Fill missing values with 'N/A' 
listing['host_response_time'].fillna('N/A', inplace=True)



### SAVING CLEANED DATASET AS CSV FILE ###
listing.to_csv('cleaned_AirBnbListings.csv', index=False)



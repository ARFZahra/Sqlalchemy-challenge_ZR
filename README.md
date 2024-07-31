# Sqlalchemy-challenge_ZR


SQLAlchemy Challenge:  This challenge was divided into two main parts:
Part 1: Analyze and Explore the Climate Data

We used climate_starter.ipynb and hawaii.sqlite to perform climate analysis and data exploration. This part involved following analyses:

Precipitation Analysis
•	Identified the most recent date in the dataset.
•	Queried the previous 12 months of precipitation data from that date.
•	Selected only the "date" and "prcp" values.
•	Loaded the query results into a Pandas DataFrame and explicitly set the column names.
•	Sorted the DataFrame by "date" and plotted the results.
•	Used Pandas to print the summary statistics for the precipitation data.

Station Analysis
•	Designed a query to calculate the total number of stations in the dataset.
•	Designed a query to find the most active stations by:
•	Listing the stations and their observation counts in descending order.
•	Identifying the station with the greatest number of observations.
•	Using the most active station ID, calculated the lowest, highest, and average temperatures.
•	Designed a query to get the previous 12 months of temperature observation (TOBS) data:
•	Filtered by the station with the greatest number of observations.
•	Queried the previous 12 months of TOBS data for that station.
•	Plotted the results as a histogram with 12 bins.


Part 2: Design Climate APP
We developed a Flask API by creating following app for query climate data as below. 

/api/v1.0/precipitation
Queried precipitation data, converting the results into a dictionary with the date as the key and prcp as the value.
Returned the JSON representation of the dictionary.

/api/v1.0/stations
Returned a JSON list of stations from the dataset.

/api/v1.0/tobs
Queried the dates and temperature observations (TOBS) of the most active station for the previous year.
Returned a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
Returned a JSON list of the minimum temperature, average temperature, and maximum temperature for a specified start or start-end range.
For a specified start, calculated MIN, AVG, and MAX for all dates greater than or equal to the start date.
For a specified start and end date, calculated TMIN, TAVG, and TMAX for the dates within the range, inclusive.





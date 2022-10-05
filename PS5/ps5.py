# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Jordan Gallivan

import pylab
import re
import numpy
import scipy


# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def gen_years(start_year,end_year, n=1):
    '''
    returns a list of years between start and end, incremented by n

    '''
    year_list = []
    for year in range(start_year, end_year+1,n):
        year_list.append(year)
    
    return year_list

def daily_temps(climate, city, start_year, end_year, month, day):
    '''
    Parameters
    ----------
    climate : Climate Class.
    city : string
        city you wish to pull the daily temperatures for.
    start_year : int
        starting year.
    end_year : int
        ending year.
    month : he month to get the data for (int, where January = 1,
        December = 12)
    day : int
        the day you want to pull data for each year.

    returns array of daily temperatures
    '''
    city = city.upper()
    temps=[]
    for year in range(start_year, end_year+1):
        temps.append(climate.get_daily_temp(city, month, day, year))
    return pylab.array(temps)


def annual_avg_temps(climate, city, start_year, end_year):
    '''
    Parameters
    ----------
    climate : Climate Class.
    city : string
        city you wish to pull the annual average temperatures for.
    start_year : int
        starting year.
    end_year : int
        ending year.

    returns array of average temperatures where each element corresponds to start_year+i 
    '''
    city = city.upper()
    years = gen_years(start_year, end_year)
    annual_avg=[]
    for year in years:
        year_temps = climate.get_yearly_temp(city, year)
        annual_avg.append(sum(year_temps)/len(year_temps))
    
    return pylab.array(annual_avg)


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def leap_year(year):
    if year%4 == 0:
        if year%100 == 0:
            if year%400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return True
    
def day_to_month_year(day, year):
    '''
    

    Parameters
    ----------
    day : int
        day between 1 and 366.
    year : int
        any year.
    --------- 
    returns:
    tuple (day(int), month(int), year(int))
    '''
    day_dict = {}
    
    for i in range(365):
        if i>=334:
            day_dict[i+1] = 12
        elif i>=304:
            day_dict[i+1] = 11
        elif i>=273:
            day_dict[i+1] = 10
        elif i>=243:
            day_dict[i+1] = 9
        elif i >= 212:
            day_dict[i+1] = 8
        elif i >= 181:
            day_dict[i+1] = 7
        elif i >= 151:
            day_dict[i+1] = 6
        elif i >= 120:
            day_dict[i+1] = 5
        elif i >= 90:
            day_dict[i+1] = 4
        elif i >= 59:
            day_dict[i+1] = 3
        elif i >= 31:
            day_dict[i+1] = 2
        else:
            day_dict[i+1] = 1
    
    if leap_year(year):
        if day == 29:
            month = 2
        elif day >= 60:
            month = day_dict[day-1]
    else:
        month = day_dict(day)
        
    return day, month, year

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for n in degs:
        models.append(pylab.polyfit(x,y,n))
        
    return models


# print(generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2]))

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """

    error = ((y - estimated)**2).sum()
    variability = ((y - numpy.mean(y))**2).sum()
    return 1- (error/variability)
    
    

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    x_label = 'Years'
    y_label = 'Degrees Celsius'

    # iterate through the models (different degree polynomials)
    # i+1 = degree of polynomial
    for i in range(len(models)):

        estimated = pylab.polyval(models[i], x) # generate estimate data
        
        r_sq = r_squared(y, estimated)  # get R^2
        r_sq_str = str(round(r_sq,2))   # convert R^2 to string
        
        # ploting
        pylab.figure(i)
        pylab.plot(x,y,'b.')
        pylab.plot(x,estimated, 'r-')
        pylab.xlabel(x_label)
        pylab.ylabel(y_label)
        title = str(i+1) + "Degree Polynomial Fit" + "\n" + "R^2: " + r_sq_str
        
        # linear caveat // update tilte with Ratio of SE to slope
        if i == 0:
            se_slope = se_over_slope(x, y, estimated, models[i])
            se_slope_str = str(round(se_slope,2))
            title = title + "\n" + 'Ratio of SE to slope: ' + se_slope_str
        
        pylab.title(title)
    
    return

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    start_year = years[0]
    end_year = years[-1]
    city_dict = {}  # dictionary with key: city : value(array of annual averages)
    
    # generate city_dict values for each city in multi_cities
    for city in multi_cities:
        upper_city = city.upper()
        city_dict[city] = annual_avg_temps(climate, upper_city, start_year, end_year)
    
    multi_city_an_avg = []
    year_temps = []
    for n in range(len(years)):
        for city in multi_cities:
            year_temps.append(city_dict[city][n])
        multi_city_an_avg.append(sum(year_temps)/len(year_temps))
        year_temps=[]
    
    return pylab.array(multi_city_an_avg)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    mvg_avg = []
    for i in range(len(y)):
        if i == 0:
            mvg_avg.append(y[0])
        elif i < (window_length-1):
            mvg_avg.append(sum(y[:i+1])/(i+1))
        else:
            mvg_avg.append(sum( y[(i-window_length+1) : (i+1)] ) / window_length)
            
    return pylab.array(mvg_avg)
            
        
    
    
    
    
    return

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    
    num = ((y-estimated)**2).sum()
    
    return (num/len(y))**0.5
    
    
    

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    start_year = years[0]
    end_year = years[-1]
    city_dict = {}  # dictionary with key: city : value(array of daily temps for given year)
    year_daily_avg = []
    day_sum = 0
    stddev = []
    
    ### Start pseudo code
    # loop through years
    # loop through multi_cities
    # pull yearly data for each city and add to city_dict ###### needs to be reset
    # average daily temps across each city
    # append that into a list ######  Needs to be reset
    # get stddev for daily averages for that year
    # append that into a list  #### 
    ### End pseudo code
    
    for year in years:
        for city in multi_cities:
            upper_city = city.upper()
            city_dict[city] = climate.get_yearly_temp(upper_city, year) # add a list of daily temps
                                                                        # to each city
        for j in range(len(city_dict[multi_cities[0]])):  # using any city to gen length of that year
            for city in multi_cities:
                day_sum += city_dict[city][j]
            year_daily_avg.append(day_sum/len(multi_cities))
            day_sum = 0 # reset day_sum
        
        
        # calculate stddev for that year's daily averages
        mean = sum(year_daily_avg)/len(year_daily_avg)
        year_daily_avg = pylab.array(year_daily_avg)
        var = (((year_daily_avg - mean)**2).sum())/len(year_daily_avg)
        stddev.append(var**0.5)
        
        # reset 
        year_daily_avg = [] # reset year_daily_avg
        city_dict = {}      # reset city_dict
    
    
    # for city in multi_cities:
    #     #generate city_dict values for each city in multi_cities
    #     upper_city = city.upper()
    #     city_dict[city] = annual_avg_temps(climate, upper_city, start_year, end_year)
        
    return pylab.array(stddev)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    x_label = 'Years'
    y_label = 'Degrees Celsius'

    # iterate through the models (different degree polynomials)
    # i+1 = degree of polynomial
    for i in range(len(models)):
               
        estimated = pylab.polyval(models[i], x) # generate estimate data
        

        
        rmse_data = rmse(y, estimated)
        rmse_str = str(round(rmse_data,2))
        
        # ploting
        pylab.figure(i)
        pylab.plot(x,y,'b.')
        pylab.plot(x,estimated, 'r-')
        pylab.xlabel(x_label)
        pylab.ylabel(y_label)
        title = str(len(models[i])-1) + " Degree Polynomial Fit" + "\n" + "RMSE: " + rmse_str
        

        
        pylab.title(title)
    
    return

if __name__ == '__main__':
    
    climate = Climate("data.csv")
    
    # def plot_two_data(x1, y1, x2, y2, xlabel, ylabel, title):
    #     '''
    #     x1, y1, x2, y2 : list or array, len(x1) must equal len(y1) and same for x2,y2
        
    #     Takes in two data sets and plots them both on one figure
    #         x1/y1 represented as blue dots
    #         x2,y2 represented as a red line
    #     '''
    #     pylab.figure(0)
    #     pylab.plot(x1,y1, 'b.')
    #     pylab.plot(x2,y2, 'r-')
    #     pylab.xlabel(xlabel)
    #     pylab.ylabel(ylabel)
    #     pylab.title(title)
    



    

                
    
    
    city = "NEW YORK"
    start_year = 1961
    end_year = 2009
    month = 1
    day = 10
    years = gen_years(start_year, end_year)
    years_array = pylab.array(years)
    
    # January 10th from 1961-2009
    act_temps = daily_temps(climate, city, start_year, end_year, month, day)
    
    #annual average from 1961-2009
    # act_temps = annual_avg_temps(climate, city, start_year, end_year)
    
    #annual average across multiple cities
    year_avg = gen_cities_avg(climate, CITIES, years)
    
    #moving average
    # act_temps = moving_average(year_avg, 5)
    
    # stadard 
    act_temps = gen_std_devs(climate, CITIES, years)
    
    
    models = generate_models(years_array, act_temps, [1])
    evaluate_models_on_training(years_array, act_temps, models)
    
    
    
    
    

    # Part B
    # TODO: replace this line with your code

    # Part C
    # TODO: replace this line with your code

    # Part D.2
    # start_year = 2010
    # end_year = 2015
    # month = 1
    # day = 10
    # years = gen_years(start_year, end_year)
    # years_array = pylab.array(years)
    
    # year_avg_d2 = gen_cities_avg(climate, CITIES, years)
    
    # #moving average
    # act_temps_d2 = moving_average(year_avg_d2, 5)
    
    # evaluate_models_on_testing(years_array, act_temps_d2, models)
    

    # Part E
    # TODO: replace this line with your code

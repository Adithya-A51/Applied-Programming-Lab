import csv


def get_city_temperatures(filename, city_name):
    temperature_data = {}

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            # Check if this row matches our city
            if row["City"] == city_name:
                # Extract year-month from date (format: 1849-01-01 -> 1849-01)
                date_str = row["dt"]
                year_month = date_str[:7]  # Take first 7 characters (YYYY-MM)

                # Get temperature, handle missing values
                temp_str = row["AverageTemperature"]
                if temp_str and temp_str.strip():  # Check if not empty
                    try:
                        temperature = float(temp_str)
                        temperature_data[year_month] = temperature
                    except ValueError:
                        continue

    return temperature_data


def get_average_temp(filename):
    temp_data = {}
    city_data = get_available_cities(filename)

    # Prepare accumulators for each city
    sums = {city: 0 for city in city_data}
    counts = {city: 0 for city in city_data}
    countries = {city: "" for city in city_data}

    # Read file once
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row["City"]
            if city in city_data:  # process only required cities
                countries[city] = row["Country"]
                temp_str = row["AverageTemperature"]
                if temp_str and temp_str.strip():
                    try:
                        temperature = float(temp_str)
                        sums[city] += temperature
                        counts[city] += 1
                    except ValueError:
                        continue

    # Final averages
    for city in city_data:
        if counts[city] > 0:
            temp_data[city] = [sums[city] / counts[city], countries[city]]

    return temp_data


def get_available_cities(filename, limit=None):
    cities = set()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cities.add(row["City"])
            if limit and len(cities) >= limit:
                break

    return sorted(list(cities))


# =============================================================================
# ASSIGNMENT: Build a Temperature Data API
# =============================================================================
# Students should implement these 5 functions to create a complete API


def find_temperature_extremes(filename, city_name):
    max_temp = float("-inf")
    min_temp = float("inf")
    max_month = None
    min_month = None

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["City"] == city_name:
                temp_str = row["AverageTemperature"]
                if temp_str and temp_str.strip():  # Check if not empty
                    try:
                        temperature = float(temp_str)
                        # Updating x_temp
                        if temperature > max_temp:
                            max_temp = temperature
                            max_month = row["dt"][:7]

                        if temperature < min_temp:
                            min_temp = temperature
                            min_month = row["dt"][:7]

                    except ValueError:
                        # Skip rows with invalid temperature data
                        continue

        return {
            "hottest": {"date": max_month, "temperature": max_temp},
            "coldest": {"date": min_month, "temperature": min_temp},
        }


def get_seasonal_averages(filename, city_name, season):
    temp_data = get_city_temperatures(filename, city_name)  # Getting temp_data
    # Sets for the different seasons
    if season == "spring":
        months = {"03", "04", "05"}
    elif season == "summer":
        months = {"06", "07", "08"}
    elif season == "autumn":
        months = {"09", "10", "11"}
    else:
        months = {"12", "01", "02"}

    temp_sum = 0
    count = 0
    for ym in temp_data:
        temp = temp_data[ym]
        if ym[5:] in months:  # Checking if the data is part of the season
            temp_sum += temp
            count += 1

    return {
        "city": city_name,
        "season": season,
        "average_temperature": temp_sum / count,
    }


def compare_decades(filename, city_name, decade1, decade2):
    if decade1 % 10 or decade2 % 10:
        raise ValueError("Invalid decade values")

    temp_data = get_city_temperatures(filename, city_name)
    decade1_end = decade1 + 10
    decade2_end = decade2 + 10
    tempd1 = 0
    countd1 = 0
    tempd2 = 0
    countd2 = 0

    for ym in temp_data:
        temp = temp_data[ym]
        if int(ym[:4]) >= decade1 and int(ym[:4]) < decade1_end:
            tempd1 += temp
            countd1 += 1
        elif int(ym[:4]) >= decade2 and int(ym[:4]) < decade2_end:
            tempd2 += temp
            countd2 += 1

    trend = ""
    difference = tempd2 / countd2 - tempd1 / countd1
    # Keeping threshold for heating or cooling as 0.05 degrees
    if difference < -0.05:
        trend = "cooling"

    elif difference > -0.05:
        trend = "warming"

    else:
        trend = "stable"
    return {
        "city": city_name,
        "decade1": {
            "period": str(decade1) + "s",
            "avg_temp": tempd1 / countd1,
            "data_points": countd1,
        },
        "decade2": {
            "period": str(decade2) + "s",
            "avg_temp": tempd2 / countd2,
            "data_points": countd2,
        },
        "difference": difference,
        "trend": trend,
    }


def find_similar_cities(filename, target_city, tolerance=2.0):

    temp_data = get_average_temp(filename)
    cities = get_available_cities(filename)
    target_avg = temp_data[target_city]
    similar = []

    for city in cities:
        if city != target_city:
            city_avg = temp_data[city]
            if abs(target_avg[0] - city_avg[0]) <= tolerance:
                similar.append(
                    {
                        "city": city,
                        "country": city_avg[1],
                        "avg_temp": city_avg[0],
                        "difference": abs(target_avg[0] - city_avg[0]),
                    }
                )

    return {
        "target_city": target_city,
        "target_avg_temp": target_avg[0],
        "similar_cities": similar,
        "tolerance": tolerance,
    }


def get_temperature_trends(filename, city_name, window_size=5):
    year_temps = {}
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["City"] == city_name:
                year = row["dt"][:4]
                temp_str = row["AverageTemperature"]
                if temp_str and temp_str.strip():  # Check if not empty
                    try:
                        temperature = float(temp_str)
                        year_temps.setdefault(year, []).append(temperature)
                    except ValueError:
                        # Skip rows with invalid temperature data
                        continue

        annual_means = {
            year: sum(temps) / len(temps) for year, temps in year_temps.items()
        }

        years = [year for year in year_temps.keys()]
        temps = [temp for temp in year_temps.values()]
        annual_temps = [temp for temp in annual_means.values()]
        moving_averages = {}
        for i in range(window_size - 1, len(years)):
            temp_window = temps[i - (window_size - 1) : i + 1]
            moving_averages[years[i]] = sum(
                sum(sublist) for sublist in temp_window
            ) / sum(len(sublist) for sublist in temp_window)

        overall_slope = (annual_temps[-1] - annual_temps[0]) / (
            int(years[-1]) - int(years[0])
        )
        values = [annual_means[year] for year in annual_means]
        warming_periods = []
        cooling_periods = []
        start = years[0]
        prev_temp = values[0]
        trend = None

        for i in range(1, len(years)):
            rate = values[i] - prev_temp
            if rate > 0:
                if trend != "warming":
                    if trend == "cooling":
                        cooling_periods.append(
                            {
                                "start": start,
                                "end": years[i - 1],
                                "rate": (values[i - 1] - values[years.index(start)])
                                / (int(years[i - 1]) - int(start) + 1),
                            }
                        )
                        start = years[i - 1]
                    trend = "warming"
            elif rate < 0:
                if trend != "cooling":
                    if trend == "warming":
                        warming_periods.append(
                            {
                                "start": start,
                                "end": years[i - 1],
                                "rate": (values[i - 1] - values[years.index(start)])
                                / (int(years[i - 1]) - int(start) + 1),
                            }
                        )
                        start = years[i - 1]
                    trend = "cooling"
                prev_temp = values[i]

        # To capture last trend period
        if trend == "warming":
            warming_periods.append(
                {
                    "start": start,
                    "end": years[-1],
                    "rate": (values[-1] - values[years.index(start)])
                    / (int(years[-1]) - int(start) + 1),
                }
            )
        elif trend == "cooling":
            cooling_periods.append(
                {
                    "start": start,
                    "end": years[-1],
                    "rate": (values[-1] - values[years.index(start)])
                    / (int(years[-1]) - int(start) + 1),
                }
            )

        return {
            "city": city_name,
            "raw_annual_data": annual_means,
            "moving_averages": moving_averages,
            "trend_analysis": {
                "overall_slope": overall_slope,
                "warming_periods": warming_periods,
                "cooling_periods": cooling_periods,
            },
        }


# =============================================================================
# TESTING CODE
# =============================================================================


def test_api_functions():
    """
    Test all API functions with sample data.
    """
    filename = "GlobalLandTemperaturesByMajorCity.csv"
    test_city = "Kano"

    print("Testing Temperature Data API")
    print("=" * 40)

    # Test basic function
    temps = get_city_temperatures(filename, test_city)
    print(f"Basic function: Found {len(temps)} temperature records")

    # Test extremes
    extremes = find_temperature_extremes(filename, test_city)
    print(f"Extremes: Hottest = {extremes['hottest']['temperature']}°C")

    # Test seasonal averages
    summer_avg = get_seasonal_averages(filename, test_city, "summer")
    print(f"Seasonal: Summer average = {summer_avg['average_temperature']:.1f}°C")

    # Test decade comparison
    comparison = compare_decades(filename, test_city, 1980, 2000)
    print(f"Decades: Temperature change = {comparison['difference']:.2f}°C")

    # Test similar cities
    similar = find_similar_cities(filename, test_city, tolerance=5.0)
    print(f"Similar cities: Found {len(similar['similar_cities'])} matches")

    # Test trends
    trends = get_temperature_trends(filename, test_city)
    print(
        f"Trends: Overall slope = {trends['trend_analysis']['overall_slope']:.4f}°C/year"
    )


if __name__ == "__main__":
    test_api_functions()

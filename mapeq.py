import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import simplekml

# Convert latitude and longitude to Cartesian coordinates
def latlon_to_cartesian(lat, lon):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return x, y, z

# Convert Cartesian coordinates to latitude and longitude
def cartesian_to_latlon(x, y, z):
    lon = np.degrees(np.arctan2(y, x))
    hyp = np.sqrt(x**2 + y**2)
    lat = np.degrees(np.arctan2(z, hyp))
    return lat, lon

# Coordinates and names of the ancient sites
site_coordinates = [
    (51.1789, -1.8262, 'Stonehenge'), (29.9792, 31.1342, 'Great Pyramid of Giza'), (-13.5096, -71.9817, 'Sacsayhuamán'),
    (-13.1631, -72.5450, 'Machu Picchu'), (34.0058, 36.2039, 'Baalbek'), (37.2231, 38.9222, 'Gobekli Tepe'),
    (-27.1127, -109.3497, 'Easter Island'), (9.1545, -83.8612, 'Guayabo'), (47.5936, -3.0834, 'Carnac'),
    (51.4285, -1.8541, 'Avebury'), (53.6947, -6.4758, 'Newgrange'), (59.0481, -3.3430, 'Ring of Brodgar'),
    (27.3294, 68.1384, 'Mohenjo-daro'), (-20.2670, 30.9333, 'Great Zimbabwe'), (-16.5540, -68.6720, 'Tiwanaku'),
    (13.6910, -14.8974, 'Senegambian Stone Circles'), (34.0058, 36.2039, 'Baalbek'), (43.3776, 44.1563, 'Vainakh Towers'),
    (59.3520, -2.9154, 'Maeshowe'), (20.6843, -88.5678, 'Chichen Itza'), (17.4820, -92.0372, 'Palenque'),
    (19.6925, -98.8438, 'Cantona'), (17.0465, -96.7675, 'Monte Alban'), (17.2220, -89.6237, 'Tikal'),
    (17.7561, -89.9102, 'Caracol'), (31.8707, 35.4420, 'Jericho'), (40.0218, 34.6070, 'Hattusa'),
    (37.7281, 22.7544, 'Mycenae'), (35.2982, 25.1594, 'Knossos'), (37.9715, 23.7257, 'Athens'),
    (35.8495, 14.5326, 'Tarxien Temples'), (40.4319, 116.5704, 'Great Wall of China'), (34.3853, 109.2786, 'Terracotta Army'),
    (8.3114, 80.4037, 'Anuradhapura'), (7.9403, 81.0184, 'Polonnaruwa'), (7.9569, 80.7603, 'Sigiriya'),
    (13.4125, 103.8667, 'Angkor Wat'), (-7.6079, 110.2038, 'Borobudur'), (6.8428, 158.3348, 'Nan Madol'),
    (30.3285, 35.4444, 'Petra'), (39.9578, 26.2385, 'Troy'), (38.4828, 22.5010, 'Delphi'),
    (40.8360, 23.8537, 'Amphipolis'), (14.1320, 38.7200, 'Aksum'), (22.5091, 30.7194, 'Abu Simbel'),
    (25.7402, 32.6014, 'Luxor Temple'), (16.9370, 33.7430, 'Jebel Barkal'), (29.4731, 31.1557, 'Dahshur'),
    (39.0259, -83.4301, 'Serpent Mound')
]

# Create figure and axis
fig, ax = plt.subplots(figsize=(20, 10))

# Create a Basemap instance
m = Basemap(projection='mill', resolution='c', ax=ax)

# Draw coastlines and countries
m.drawcoastlines()
m.drawcountries()

# Plot ancient sites
lats = [site[0] for site in site_coordinates]
lons = [site[1] for site in site_coordinates]
x, y = m(lons, lats)
m.scatter(x, y, color='red', s=50, label="Ancient Sites")

# Plot the Earth's actual equator
equator_lat = [0] * 360
equator_lon = np.linspace(-180, 180, 360)
eq_x, eq_y = m(equator_lon, equator_lat)
m.plot(eq_x, eq_y, color='blue', linewidth=2, label="Earth's Equator")

# Define function to compute the great circle through two points
def great_circle(lat1, lon1, lat2, lon2, num_points=360):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    delta_lon = lon2 - lon1
    delta_sigma = np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(delta_lon))
    sigma = np.linspace(0, delta_sigma, num_points)
    x = np.sin((1 - sigma) * delta_sigma) / np.sin(delta_sigma) * np.cos(lat1) * np.cos(lon1) + \
        np.sin(sigma * delta_sigma) / np.sin(delta_sigma) * np.cos(lat2) * np.cos(lon2)
    y = np.sin((1 - sigma) * delta_sigma) / np.sin(delta_sigma) * np.cos(lat1) * np.sin(lon1) + \
        np.sin(sigma * delta_sigma) / np.sin(delta_sigma) * np.cos(lat2) * np.sin(lon2)
    z = np.sin((1 - sigma) * delta_sigma) / np.sin(delta_sigma) * np.sin(lat1) + \
        np.sin(sigma * delta_sigma) / np.sin(delta_sigma) * np.sin(lat2)
    return cartesian_to_latlon(x, y, z)

# Coordinates for Easter Island and the Great Pyramid of Giza
easter_island = (-27.1127, -109.3497)
great_pyramid = (29.9792, 31.1342)

# Compute the great circle (equator) passing through Easter Island and the Great Pyramid
green_lat_range, green_lon_range = great_circle(easter_island[0], easter_island[1], great_pyramid[0], great_pyramid[1])

# Split the green_lat_range and green_lon_range at the discontinuity
green_lat_range = np.array(green_lat_range)
green_lon_range = np.array(green_lon_range)
green_lat_range, green_lon_range = np.unwrap(green_lat_range, axis=0), np.unwrap(green_lon_range, axis=0)

# Plot the great circle
green_eq_x, green_eq_y = m(green_lon_range, green_lat_range)
m.plot(green_eq_x, green_eq_y, color='green', linewidth=2, label="Easter Island to Giza Equator")

# Title and legend
plt.title("Top 50 Ancient Sites and Equators")
plt.legend(loc='lower left')

# Show the plot
plt.show()

# Export to KML
kml = simplekml.Kml()

# Add ancient sites to KML
for lat, lon, name in site_coordinates:
    pnt = kml.newpoint(name=name, coords=[(lon, lat)])
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'

# Add Earth's equator to KML
equator_line = kml.newlinestring(name="Earth's Equator")
equator_line.coords = list(zip(equator_lon, equator_lat))
equator_line.style.linestyle.color = simplekml.Color.blue
equator_line.style.linestyle.width = 2

# Add Easter Island to Great Pyramid equator to KML
green_line = kml.newlinestring(name="Easter Island to Giza Equator")
green_line.coords = list(zip(green_lon_range, green_lat_range))
green_line.style.linestyle.color = simplekml.Color.green
green_line.style.linestyle.width = 2

# Save KML file
kml.save("ancient_sites_and_equators.kml")

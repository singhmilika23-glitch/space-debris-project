from skyfield.api import load
import matplotlib.pyplot as plt
import numpy as np

# Close old figures
plt.close('all')

ts = load.timescale()

stations_url = 'https://celestrak.org/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)

t = ts.now()

x = []
y = []
names = []

close_pairs = []

# Use dark background
plt.style.use('dark_background')

# Collect positions
for sat in satellites[:10]:

    pos = sat.at(t).position.km

    x.append(pos[0])
    y.append(pos[1])
    names.append(sat.name)

# Collision detection
for i in range(10):
    for j in range(i + 1, 10):

        pos1 = satellites[i].at(t).position.km
        pos2 = satellites[j].at(t).position.km

        distance = np.linalg.norm(pos1 - pos2)

        # Larger threshold so warnings appear
        if distance < 5000:
            close_pairs.append((i, j, distance))

# ONE figure only
plt.figure(figsize=(10,10))

# Plot satellites
plt.scatter(x, y, color='cyan', s=60)

# Labels
for i, name in enumerate(names):
    plt.text(x[i], y[i], name, fontsize=7)

# Draw warning lines
for pair in close_pairs:

    i, j, distance = pair

    plt.plot(
        [x[i], x[j]],
        [y[i], y[j]],
        color='red',
        linewidth=2
    )

    print(f"WARNING: {names[i]} ↔ {names[j]}")
    print(f"Distance: {distance:.2f} km\n")

plt.title("Satellite Collision Detection System")
plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.grid(True)

plt.show()
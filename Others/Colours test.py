import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random


# Your code to generate random colors
supported_colors = list(mcolors.CSS4_COLORS)
n = random.randint(10, 99999)
print(n)
n = 86128
random.seed(n)
random_colors = random.sample(supported_colors, 20)

# Plotting the colors
fig, ax = plt.subplots(1, 1, figsize=(10, 1))
ax.imshow([[mcolors.hex2color(color) for color in random_colors]], aspect='auto', extent=[0, len(random_colors), 0, 1])
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
plt.show()
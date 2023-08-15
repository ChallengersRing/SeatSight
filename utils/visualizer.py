import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Bounding box coordinates
chair_bounding_boxes = [
    [143, 270, 176, 328],
]

person_bounding_boxes = [
    [157, 212, 250, 352],
    [86, 227, 161, 322],
]

# Combine chair and person bounding boxes
bounding_boxes = chair_bounding_boxes + person_bounding_boxes

# Create a figure and axis
fig, ax = plt.subplots()

# Loop through the combined bounding boxes and create rectangle patches
for i, bbox in enumerate(bounding_boxes):
    if i < len(chair_bounding_boxes):
        label = 'Chair'
        color = 'r'
    else:
        label = 'Person'
        color = 'g'

    bbox_rect = patches.Rectangle((bbox[0], bbox[3]), bbox[2] - bbox[0], bbox[3] - bbox[1], linewidth=2, edgecolor=color, facecolor='none', label=label)
    ax.add_patch(bbox_rect)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Detected Objects')

# Set legend
ax.legend()

# Calculate axis limits
# x_min = min(bbox[0] for bbox in bounding_boxes)
# y_min = min(bbox[1] for bbox in bounding_boxes)
# x_max = max(bbox[2] for bbox in bounding_boxes)
# y_max = max(bbox[3] for bbox in bounding_boxes)

# Add some padding
# padding = 20
# ax.set_xlim(x_min - padding, x_max + padding)
# ax.set_ylim(y_min - padding, y_max + padding)

# Set axis limits based on your bounding boxes
ax.set_xlim(0, 400)
ax.set_ylim(0, 500)

# Show the plot
plt.show()

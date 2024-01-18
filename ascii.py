import numpy as np
from PIL import Image

def find_complementary_color(rgb_color):
    # Invert the RGB values to get the complementary color
    comp_color = (255 - rgb_color[0], 255 - rgb_color[1], 255 - rgb_color[2])
    return comp_color

def image_to_colored_ascii_html_with_bg(image_path, output_html_path, scale=0.2, char_density=0.5):
    # Characters for ASCII art, sorted by perceived brightness
    ascii_chars = np.array(list('fCLti1G '))
    num_chars = len(ascii_chars)

    # Load the image from the provided path
    image = Image.open(image_path)

    # Resize the image according to the scale while maintaining aspect ratio
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width
    new_width = int(original_width * scale)
    new_height = int(aspect_ratio * new_width * char_density)
    image = image.resize((new_width, new_height))

    # Convert the image to RGB if it's not already in that format
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get the RGB values from the image and calculate the average color
    rgb_values = np.array(image)
    average_color = np.mean(rgb_values, axis=(0, 1)).astype(int)
    bg_color = find_complementary_color(average_color)

    # Flatten the array for processing
    rgb_values = rgb_values.reshape((-1, 3))  

    # Normalize the RGB values to 0-1 range
    rgb_values_normalized = rgb_values / 255.0

    # Calculate the luminance (brightness) of each pixel
    luminance = 0.2126 * rgb_values_normalized[:, 0] + 0.7152 * rgb_values_normalized[:, 1] + 0.0722 * rgb_values_normalized[:, 2]

    # Map luminance to ASCII characters
    char_indices = (luminance * (num_chars - 1)).astype(int)
    ascii_art = ascii_chars[char_indices]

    # Begin constructing the HTML string
    html_string = f'<html><head></head><body style="font-family: monospace; white-space: pre; line-height: 0.8; background-color: rgb{bg_color};">'

    # Convert ASCII art and RGB values to HTML
    for i, char in enumerate(ascii_art):
        color = tuple(rgb_values[i])
        html_string += f'<span style="color: rgb{color};">{char}</span>'
        if (i + 1) % new_width == 0:
            html_string += '<br>'

    # Close the HTML string
    html_string += '</body></html>'

    # Save the HTML to the specified path
    with open(output_html_path, 'w') as html_file:
        html_file.write(html_string)

    return output_html_path

# Paths for the input and output files
input_image_path = 'path_to_your_image.png'  # Replace with your image path
output_html_file_path = 'path_to_your_output_html.html'  # Replace with your desired output path

# Call the function to convert the image and get the HTML file path with dynamic background
html_file_path_with_bg = image_to_colored_ascii_html_with_bg(input_image_path, output_html_file_path)
print(f"HTML file with ASCII art generated at: {html_file_path_with_bg}")

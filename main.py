import os
import openai
import requests
from PIL import Image, ImageDraw, ImageFont
import io

openai.api_key = "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"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="In a JSON object, give me a bizarre and interesting animal fact that is estimated to be 20-25 words long in the following format\n \nAnimal: \"Name here\";\nFact: \"Fact Here\";\n\n\n",
    temperature=0.7,
    max_tokens=50,
    top_p=0.8,
    frequency_penalty=0.2,
    presence_penalty=0.2
)

generated_text = response.choices[0].text.strip()

# Split the generated text into lines
lines = generated_text.split('\n')

# Initialize variables to store animal name and fact
animal_name = ""
fact = ""

# Loop through the lines to find the Animal and Fact lines
for line in lines:
    if line.startswith("Animal:"):
        animal_name = line[len("Animal:"):].strip()
    elif line.startswith("Fact:"):
        fact = line[len("Fact:"):].strip()

# Generate Image
response = openai.Image.create(
    prompt="picture of a " + animal_name,
    n=1,
    size="256x256"
)
image_url = response['data'][0]['url']

# Download the image
image_response = requests.get(image_url)
img = Image.open(io.BytesIO(image_response.content))

# Create a drawing object
draw = ImageDraw.Draw(img)

import textwrap

# Define the font and size
font_size = 16
font = ImageFont.truetype("fonts/first.ttf", size=font_size)

# Define the text and maximum width
text = fact
max_width = 200  # Adjust this based on the available space

# Wrap the text to fit within the maximum width
wrapper = textwrap.TextWrapper(width=20)  # Adjust the width as needed
wrapped_text = wrapper.fill(text)

# Calculate the position to center the wrapped text horizontally and adjust the vertical position
text_width, text_height = draw.textsize(wrapped_text, font=font)
horizontal_position = (256 - text_width) / 2
vertical_position = (256 - text_height) / 4  # Adjust this value to control vertical placement

# Set the text color
text_color = (255, 255, 255)  # White color

# Add the wrapped text to the image
draw.text((horizontal_position, vertical_position), wrapped_text, fill=text_color, font=font)


# Save the modified image
img.save("output_image.jpg")

# Print the extracted animal name and fact
print("Animal:", animal_name)
print("Fact:", fact)
print("Image:", image_url)

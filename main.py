import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Replace 'YOUR_API_KEY' with your actual DeepAI API key
API_KEY = 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'


def generate_image_from_text(text, options):
    # API endpoint for the DeepAI Text2Image service
    API_ENDPOINT = 'https://api.deepai.org/api/text2img'

    # Set up the headers with your API key
    headers = {
        'api-key': API_KEY
    }

    # Define the text you want to convert into an image
    data = {
        'text': text,
        'grid_size': options['grid_size'],
        'width': options['width'],
        'height': options['height'],
        'image_generator_version': options['image_generator_version'],
        'negative_prompt': options['negative_prompt']
    }

    # Make the API request
    response = requests.post(API_ENDPOINT, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response to get the image URL
        result = response.json()
        image_url = result.get('output_url')

        # Download the image
        image_response = requests.get(image_url)

        # Open and return the image using PIL
        if image_response.status_code == 200:
            image_data = BytesIO(image_response.content)
            return Image.open(image_data)

    return None


def generate_image():
    text = text_entry.get("1.0", "end-1c")

    if text:
        options = {
            'grid_size': grid_size_var.get(),
            'width': width_var.get(),
            'height': height_var.get(),
            'image_generator_version': image_generator_var.get(),
            'negative_prompt': negative_prompt_var.get()
        }

        generated_image = generate_image_from_text(text, options)

        if generated_image:
            generated_image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(generated_image)
            image_label.config(image=photo)
            image_label.photo = photo
        else:
            messagebox.showerror("Error", "Failed to generate the image.")
    else:
        messagebox.showwarning("Warning", "Please enter text.")


# Create the main window
root = tk.Tk()
root.title("Text to Image Converter")

# Create a Text widget for entering text
text_entry = tk.Text(root, width=40, height=10)
text_entry.pack(pady=10)

# Create a frame for options
options_frame = tk.Frame(root)
options_frame.pack()

# Create option labels and input fields
grid_size_label = tk.Label(options_frame, text="Grid Size:")
grid_size_label.grid(row=0, column=0, padx=5, pady=5)
grid_size_var = tk.StringVar()
grid_size_var.set("2")
grid_size_entry = tk.Entry(options_frame, textvariable=grid_size_var)
grid_size_entry.grid(row=0, column=1, padx=5, pady=5)

width_label = tk.Label(options_frame, text="Width:")
width_label.grid(row=1, column=0, padx=5, pady=5)
width_var = tk.StringVar()
width_var.set("512")
width_entry = tk.Entry(options_frame, textvariable=width_var)
width_entry.grid(row=1, column=1, padx=5, pady=5)

height_label = tk.Label(options_frame, text="Height:")
height_label.grid(row=2, column=0, padx=5, pady=5)
height_var = tk.StringVar()
height_var.set("512")
height_entry = tk.Entry(options_frame, textvariable=height_var)
height_entry.grid(row=2, column=1, padx=5, pady=5)

image_generator_label = tk.Label(options_frame, text="Image Generator Version:")
image_generator_label.grid(row=3, column=0, padx=5, pady=5)
image_generator_var = tk.StringVar()
image_generator_var.set("standard")
image_generator_entry = tk.Entry(options_frame, textvariable=image_generator_var)
image_generator_entry.grid(row=3, column=1, padx=5, pady=5)

negative_prompt_label = tk.Label(options_frame, text="Negative Prompt:")
negative_prompt_label.grid(row=4, column=0, padx=5, pady=5)
negative_prompt_var = tk.StringVar()
negative_prompt_entry = tk.Entry(options_frame, textvariable=negative_prompt_var)
negative_prompt_entry.grid(row=4, column=1, padx=5, pady=5)

# Create a button to generate the image
generate_button = tk.Button(root, text="Generate Image", command=generate_image)
generate_button.pack()

# Create a label to display the generated image
image_label = tk.Label(root)
image_label.pack()

# Start the Tkinter main loop
root.mainloop()

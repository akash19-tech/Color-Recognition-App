import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Function to recognize color based on RGB values
def recognize_color(R, G, B, csv):
    minimum = 10000
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to load the uploaded image
def load_image():
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')  # Convert to RGB for consistency
        return np.array(image)
    return None

# Add custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #e9ecef;  /* Light background */
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            color: #343a40;
            font-size: 42px;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            color: #6c757d;
            font-size: 24px;
            margin-bottom: 30px;
        }
        .color-output {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.9);  /* White background with slight transparency */
            border: 2px solid #007bff;  /* Blue border for the box */
            color: #007bff;  /* Blue text color */
            margin: 10px;  /* Margin for spacing */
        }
        .color-box {
            display: inline-block;
            width: 50px;
            height: 50px;
            margin: 5px;
            border: 2px solid #343a40;
            border-radius: 5px;
        }
        .button {
            background-color: #007bff;  /* Blue button */
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 10px;
        }
        .button:hover {
            background-color: #0056b3;  /* Darker blue on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Main app
def main():
    add_custom_css()  # Apply custom CSS styles

    st.markdown("<h1 class='title'>Color Recognition App</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Upload an image and click to detect colors!</h2>", unsafe_allow_html=True)

    # Ensure 'colors.csv' path is correct, adjust if necessary
    csv_file_path = 'colors.csv'  # Replace with the correct path if needed
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv(csv_file_path, names=index, header=None)

    # Upload and display the image
    img = load_image()

    if img is not None:
        # Create a drawable canvas where users can click on the image
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",  # Transparent background
            stroke_width=1,
            background_image=Image.fromarray(img),  # Ensure this line displays the image on canvas
            update_streamlit=True,
            height=img.shape[0],  # Set the canvas height to image height
            width=img.shape[1],  # Set the canvas width to image width
            drawing_mode="freedraw",
            key="canvas",
        )

        if canvas_result.json_data is not None:
            # Extracting the X, Y coordinates where the user clicked
            for obj in canvas_result.json_data["objects"]:
                x, y = int(obj["left"]), int(obj["top"])

                # Check if the click is within the image bounds
                if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                    # Get the RGB values of the selected pixel
                    b, g, r = img[y, x]
                    color_name = recognize_color(r, g, b, csv)
                    
                    # Display color info
                    st.markdown(f"<div class='color-output'>Color at ({x},{y}): {color_name} (R={r}, G={g}, B={b})</div>", unsafe_allow_html=True)
                else:
                    st.error("Clicked outside the image bounds!")
    else:
        st.warning("Please upload an image to proceed.")

if __name__ == '__main__':
    main()


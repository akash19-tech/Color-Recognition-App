import streamlit as st
import cv2
import pandas as pd
import numpy as np
from PIL import Image

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

# Upload image function
def load_image():
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        return np.array(image)
    return None

# Main app
def main():
    st.title("Color Recognition App")
    st.write("Upload an image and click on the image to detect colors.")
    
    # Load CSV file containing color data
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('colors.csv', names=index, header=None)

    # Upload and display the image
    img = load_image()
    
    if img is not None:
        st.image(img, caption="Uploaded Image", use_column_width=True)
        
        # Select a pixel and show its color information
        if st.button("Detect Color"):
            x, y = st.slider("Select X coordinate", 0, img.shape[1]), st.slider("Select Y coordinate", 0, img.shape[0])
            
            b, g, r = img[y, x]
            color_name = recognize_color(r, g, b, csv)
            
            st.write(f"Color at ({x},{y}): {color_name} (R={r}, G={g}, B={b})")
            st.write(f"Hex: #{r:02x}{g:02x}{b:02x}".upper())

if __name__ == '__main__':
    main()

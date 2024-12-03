import base64

# Open the token.pickle file in binary mode
with open("token.pickle", "rb") as file:
    # Encode the file content into Base64
    encoded = base64.b64encode(file.read()).decode("utf-8")

# Write the Base64 string to a new file
with open("token.pickle.b64", "w") as out_file:
    out_file.write(encoded)

print("Base64 encoding complete! Saved as token.pickle.b64")

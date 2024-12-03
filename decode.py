import base64

with open("token.pickle.b64", "r") as file:
    encoded = file.read()

# Decode the Base64 string
with open("decoded_token.pickle", "wb") as out_file:
    out_file.write(base64.b64decode(encoded))

print("Decoding complete. Check the output file: decoded_token.pickle")

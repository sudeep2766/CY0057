from PIL import Image


def hide_message(input_image, output_image, message):
    image = Image.open(input_image).convert("RGB")

    # Add a delimiter so we know where the message ends
    message += "#####"
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    pixels = list(image.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message is too large for this image.")

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel
        new_pixel = [r, g, b]

        for i in range(3):
            if bit_index < len(binary_message):
                # Replace the least significant bit
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[bit_index])
                bit_index += 1

        new_pixels.append(tuple(new_pixel))

    image.putdata(new_pixels)
    image.save(output_image)

    print("Message hidden successfully.")


def extract_message(image_path):
    image = Image.open(image_path).convert("RGB")

    binary_message = ""

    for pixel in image.getdata():
        for value in pixel:
            binary_message += str(value & 1)

    # Convert binary to text
    message = ""

    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]

        if len(byte) < 8:
            break

        char = chr(int(byte, 2))
        message += char

        if message.endswith("#####"):
            return message[:-5]

    return message


# # Example
hide_message(
    "Land.jpeg",
    "secret.jpeg",
    "This is my secret message!"
)

# message = extract_message("secret.jpeg")
# print("Hidden message:", message)

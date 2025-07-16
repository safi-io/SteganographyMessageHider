from PIL import Image

# Encoding Logic
def stego_encode(image_path, message, output_path):
    img = Image.open(image_path)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # Null terminator
    binary_message = ''.join([format(ord(c), '08b') for c in message])
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx >= len(binary_message):
                break

            r, g, b = img.getpixel((x, y))

            if idx + 3 <= len(binary_message):
                r = (r & ~1) | int(binary_message[idx])
                g = (g & ~1) | int(binary_message[idx + 1])
                b = (b & ~1) | int(binary_message[idx + 2])
                idx += 3
            else:
                if idx < len(binary_message):
                    r = (r & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < len(binary_message):
                    g = (g & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < len(binary_message):
                    b = (b & ~1) | int(binary_message[idx])
                    idx += 1

            encoded.putpixel((x, y), (r, g, b))

    encoded.save(output_path, format='PNG')  # Always save as PNG

# Decoding Logic
def stego_decode(image_path):
    img = Image.open(image_path)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    width, height = img.size
    binary_data = ''

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == chr(0):  # Null terminator
            break
        chars.append(char)

    return ''.join(chars)
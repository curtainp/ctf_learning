from PIL import Image, ImageChops

# refer to https://crypto.stackexchange.com/questions/88430/how-to-decrypt-two-images-encrypted-using-xor-with-the-same-key
img1 = Image.open('lemur.png')
img2 = Image.open('flag.png')

img3 = ImageChops.add(ImageChops.subtract(img1, img2), ImageChops.subtract(img2, img1))

# from pwn import xor

# xor_bytes = xor(img1.tobytes(), img2.tobytes())
# img3 = Image.frombytes(img2.mode, img2.size, xor_bytes)

img3.show()

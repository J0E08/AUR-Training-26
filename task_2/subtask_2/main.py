from PIL import Image
def main():
 image = Image.open("img.png")
 bw_image = image.convert("L")
 bw_image.show()
 bw_image.save("bw.png")
 #just added another command to save the picture

main()
from PIL import Image # type: ignore
def main():
 image = Image.open("img.png")
 bw_image = image.convert("L")
 bw_image.save("bw.png")
 print("bw.pg is saved in Subtask_2")
 bw_image.show()
 
main()
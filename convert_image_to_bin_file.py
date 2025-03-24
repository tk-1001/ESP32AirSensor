from PIL import Image
import argparse

def image_to_bitmap(image: Image.Image, mode: str = 'bw', threshold: int = 128, output_path=None) -> list:
    if mode == 'bw':
        # Convert to grayscale
        image_in_grayscale = image.convert("L")

        width, height = image_in_grayscale.size

        bw_image = image_in_grayscale.point(lambda x: 0 if x < threshold else 255, '1')
        bw_image.save(output_path)
        bitmap = []

        for y in range(height):
            row = []
            for x in range(width):
                pixel_value = image_in_grayscale.getpixel((x, y))
                binary_value = 1 if pixel_value >= threshold else 0
                row.append(binary_value)
            bitmap.append(row)

        return bitmap
    elif mode == 'color':
        raise NotImplemented("The feature was not implemented yet.")
    else:
        raise ValueError("Invalid mode. Choose 'bw' for black and white or 'color' for indexed color.")

def create_bin_file(splash_screen_image, path_to_file):
    with open(path_to_file, 'w') as f:
        for y in range(0, 447):
            for x in range(0, 599):
                f.write(str(splash_screen_image[y][x]))
            f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a splash screen image to binary file')
    parser.add_argument('image', help='Path to image jpeg file')
    parser.add_argument('threshold', help='Threshold for black and white')
    args = parser.parse_args()


    image_to_process = Image.open(args.image)

    image_bitmap = image_to_bitmap(image_to_process,'bw', int(args.threshold), output_path=args.image[:5]+'_bw.png')

    create_bin_file(image_bitmap, args.image[:3]+'.bin')

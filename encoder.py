import base64
from PIL import Image
import os
import numpy as np
import cv2

def image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        base64_data = base64.b64encode(img_file.read()).decode('utf-8')
    return base64_data

def get_file_size(filename):
    return os.path.getsize('images/' + filename + '.webp')

def compress_image(filename, compression=50):
    img = Image.open('images/' + filename + '.webp')
    img_cpy = img.copy()
    img_cpy.save('images/compressed/' + filename + '.webp', quality=compression)

# Generate QR Code manually by writng to OpenCV Canvas
    
def generate_qr_matrix(data, qr_matrix):
    # Array is np.zeros(960, 540, 3, dtype=np.uint8)
    # Max hex possible is 7f7f7f

    encoded_data = data.encode('ascii')

    # To create a distinction between one image and the next, we add a pure white pixel
    encoded_data_bytearray = bytearray(encoded_data)
    for _ in range(3 - (len(encoded_data_bytearray) % 3)):
        encoded_data_bytearray.append(255)
    encoded_data = bytes(encoded_data_bytearray)

    for i in range(0, len(encoded_data), 3):
        for n in range(3):
            # print((i // 3) // 960, (i // 3) % 960)
            # This takes care of creating four pixels of each color
            qr_matrix[2 * ((i // 3) // 960)][2 * ((i // 3) % 960)][n] = encoded_data[i + n]
            qr_matrix[2 * ((i // 3) // 960) + 1][2 * ((i // 3) % 960)][n] = encoded_data[i + n]
            qr_matrix[2 * ((i // 3) // 960)][2 * ((i // 3) % 960) + 1][n] = encoded_data[i + n]
            qr_matrix[2 * ((i // 3) // 960) + 1][2 * ((i // 3) % 960) + 1][n] = encoded_data[i + n]
        
    return qr_matrix

def encode_image(filename, show=True):
    image_text = image_to_base64('images/compressed/' + filename + '.webp')
    qr_matrix = np.zeros((1080, 1920, 3), dtype=np.uint8)
    qr_matrix = generate_qr_matrix(image_text, qr_matrix)
    print(qr_matrix)
    cv2.imwrite('images/encoded/' + filename + '.png', qr_matrix)

    if show:
        cv2.imshow("Final Image", qr_matrix)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def generate_video(output_path):
    images = [img for img in os.listdir('images/encoded') if img.endswith('.png')]
    images.sort()

    video_path = os.path.join('images', output_path)

    fps = 25.0                  # frame rate in fps
    image_duration = 25         # duration of each image in frames

    img = cv2.imread(os.path.join('images/encoded', images[0]))
    height, width, _ = img.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image in images:
        for _ in range(image_duration):
            img = cv2.imread(os.path.join('images/encoded', image))
            video_writer.write(img)

    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    images = sorted([img.split('.')[0] for img in os.listdir('images') if img.endswith('.webp')])
    for image in images:
        compress_image(image)
        encode_image(image, show=False)
    generate_video(output_path='output_video.mp4')

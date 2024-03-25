import cv2
import base64

def base64_to_image(base64_data, output_path):
    img_data = base64.b64decode(base64_data)
    with open(output_path, 'wb') as img_file:
        img_file.write(img_data)

def decode_qr_code(image_path):
    qr_image = cv2.imread(image_path)
    qr_decoder = cv2.QRCodeDetector()
    decoded_data, _, _ = qr_decoder.detectAndDecode(qr_image)
    return decoded_data

def decode_qr_code_to_image(image_path):
    decoded_text = decode_qr_code(image_path)
    base64_to_image(decoded_text, 'decoded_image.png')

def qr_matrix_to_text(qr_matrix):
    downsampled_qr_matrix = qr_matrix[::2, ::2]
    encoded_list = downsampled_qr_matrix.flatten()

    ascii_string = ''
    for num in encoded_list:
        if num < 128:               # Not only the number 255
            ascii_string += chr(num)
        else:
            break

    print(downsampled_qr_matrix)
    print(len(ascii_string))

    base64_to_image(ascii_string, 'img.png')

def read_video(input_path):
    video_cap = cv2.VideoCapture(input_path)

    # fps = video_cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    image_duration = 25              # duration of each image in frames
    frame_count = 0
    image_index = 0

    while True:
        ret, frame = video_cap.read()
        if not ret:
            break  # Break the loop if there are no more frames
        
        if frame_count % image_duration == 0:
            print(frame.shape)
            qr_matrix_to_text(frame)
            image_index += 1
        
        frame_count += 1
        if frame_count >= total_frames:
            break
    
    video_cap.release()

if __name__ == '__main__':
    read_video('images/output_video.mp4')

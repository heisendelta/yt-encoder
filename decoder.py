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

if __name__ == '__main__':
    decode_qr_code_to_image('qr.png')

Version 1 is where each image is ASCII encoded, then each number from that is converted into a RGB color. This color is stored on four pixel to avoid compression, and each image is shown for a minimum of 4 frames (as recommended in that YT Video).

However, the returned array sized are vastly different (115032 to 1103 when flattened), so there might be some youtube compression. The videos look similar but even if one of the colors are off by one hexadecimal value, the image can no longer be furnished.

Maybe using colors like this might not be the best option, try using QR codes so you don't have to worry about error correction. Each images takes up multiple QR codes and fit multiple QR codes onto each 1920x1080 canvas.

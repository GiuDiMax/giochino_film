from google_images_download import google_images_download
response = google_images_download.googleimagesdownload()
arguments = {"keywords": "house", "limit": 50, "print_urls": True}
absolute_image_paths = response.download(arguments)
print(absolute_image_paths)
# Speed test code is not included on the repo due to it not being created by me:
# It can be downloaded here:
#       https://github.com/sivel/speedtest-cli
#
# I've changed it slightly to include the method "get_all()" this just returns the value of the download
# And upload
import speedtest as speed

# TODO: Create automatic tests that generate data on download speed when latency is increase
#   Might need to run the packet script as another process?
#       - Data to be exported to a CSV file

print('Speed test starting!')

download, upload = speed.get_all()

download_speed_in_Mbps = download / 1000000
upload_speed_in_Mbps = upload / 1000000

print("Download: {:.2f}Mbps - Upload: {:.2f}Mbps".format(download_speed_in_Mbps, upload_speed_in_Mbps))



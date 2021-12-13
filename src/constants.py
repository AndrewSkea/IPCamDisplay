# Passwords for the RTSP Camera feed 
cam_passes = {
    "CAM ID 1": "PASS 1",
    "CAM ID 2": "PASS 2",
    "CAM ID 3": "PASS 3",
    "CAM ID 4": "PASS 4",
}

cam_ips = {}
# # If you know the STATIS ip addresses of your 
# # cameras, uncomment and fill out
# # If you don't, update the get_urls function
# # to suit your nmap search for the cameras IPs
# cam_ips = {
#     "CAM ID 1": "IP 1",
#     "CAM ID 2": "IP 2",
#     "CAM ID 3": "IP 3",
#     "CAM ID 4": "IP 4",
# }

# Desired Frames Per Second
desired_fps = 10 

# Resolution
width = 768
height = 480

# Base IP mask. If unsure, leave as is
base_ip = "192.168.8.0"

# API settings
host = "0.0.0.0"
port = "8080"
debug=True

import os
import platform
import time

from board import SCL, SDA
import busio
import adafruit_ssd1306
import humanize
import psutil
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

interface = os.getenv('PIHOLE_OLED_INTERFACE', 'eth0')
# Mount point for disk usage info
mount_point = os.getenv('PIHOLE_OLED_MOUNT_POINT', '/')
# There is no reset pin on the SSD1306 0.96"


# Create the I2C interface for the Oled Display
i2c = busio.I2C(SCL, SDA)

#Init the display with the Size 128x32. My screen is a 0,96" Oled display with a resolution of 128x32

disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

width = disp.width
height = disp.height

disp.show()

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#fonts

font = ImageFont.truetype('/home/pi/DisplayPiHole/SF_Pixelate.ttf', 8)
font2 = ImageFont.truetype('/home/pi/DisplayPiHole/SF_Pixelate.ttf', 40)
font3 = ImageFont.truetype('/home/pi/DisplayPiHole/SF_Pixelate.ttf', 10)

sleep = 1  # seconds

hostname = platform.node()

try:

    while True:

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        addr = psutil.net_if_addrs()[interface][0]
        draw.text(
            (0, 0),
            "Pi: %s" % addr.address.rjust(15),
            font=font3,
            fill=255
        )

        uptime = datetime.now() - datetime.fromtimestamp(
            psutil.boot_time()
        )
        draw.text(
            (0, 12),
            "Up: %s" % humanize.naturaltime(uptime),
            font=font3,
            fill=255
        )

        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                temp = entry.current
                draw.text(
                    (0, 24),
                    "Temp: %s °C" % temp,
                    font=font3,
                    fill=255
                )

        disp.image(image)
        disp.show()
        time.sleep(5)

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        for x in range(0,10,1):

            if x < 10:

                draw.rectangle((0, 0, width, height), outline=0, fill=0)

                draw.text((0, 0), "Pi Status:", font=font, fill=255)

                cpu = int(psutil.cpu_percent(percpu=False))
                draw.text((0, 8), "CPU", font=font, fill=255)
                draw.text((26, 8), "%s%%" % cpu, font=font, fill=255)
                draw.rectangle(
                    (50, 8, 126, 8 + 6),
                    outline=255,
                    fill=0
                )
                draw.rectangle(
                    (50, 8, 50 + cpu, 8 + 6),
                    outline=255,
                    fill=255
                )

                mem = int(psutil.virtual_memory().percent)
                draw.text((0, 16), "RAM", font=font, fill=255)
                draw.text((26, 16), "%s%%" % mem, font=font, fill=255)
                draw.rectangle(
                    (50, 16, 126, 16 + 6),
                    outline=255,
                    fill=0
                )
                draw.rectangle(
                    (50, 16, 50 + mem, 16 + 6),
                    outline=255,
                    fill=255
                )

                disk = int(psutil.disk_usage(mount_point).percent)
                draw.text((0, 24), "Disk", font=font, fill=255)
                draw.text((26, 24), "%s%%" % disk, font=font, fill=255)
                draw.rectangle(
                    (50, 24, 126, 24 + 6),
                    outline=255,
                    fill=0
                )
                draw.rectangle(
                    (50, 24, 50 + disk, 24 + 6),
                    outline=255,
                    fill=255
                )

                disp.image(image)
                disp.show()
                time.sleep(1)

                x = x+1
            else:
                pass

        req = requests.get('http://pi.hole/admin/api.php')
        data = req.json()

        for x in range(128, -1, -16):
            # Draw a black filled box to clear image.
            draw.rectangle((0, 0, width, height), outline=0, fill=0)

            # Display large Pi-Hole ads blocked percentage
            draw.text((x, 0), "%s%%" % req.json()["ads_percentage_today"], font=font2, fill=255)
            disp.image(image)
            disp.show()

        time.sleep(3)

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        draw.text(
            (0, 0),
            "Pi-hole (%s)" % data["status"],
            font=font,
            fill=255
        )

        draw.line((0, 7, width, 7), fill=255)

        draw.text(
            (0,8),
            "Blocked: %d (%d%%)" % (
                data["ads_blocked_today"],
                data["ads_percentage_today"]
            ),
            font=font,
            fill=255
        )
        draw.text(
            (0, 16),
            "Queries: %d" % data["dns_queries_today"],
            font=font,
            fill=255
        )

        draw.line((0, 50, width, 50), fill=255)

        draw.text(
            (0, 25),
            "Blocklist: %d" % data["domains_being_blocked"],
            font=font,
            fill=255
        )

        disp.image(image)
        disp.show()
        time.sleep(5)

except (KeyboardInterrupt, SystemExit):
    print("Exiting...")
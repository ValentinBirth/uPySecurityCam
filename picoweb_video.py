import picoweb
import utime
import camera
import gc
import machine


def camera_init():
    camera.deinit()
    camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
                format=camera.JPEG, framesize=camera.FRAME_VGA, 
                xclk_freq=camera.XCLK_20MHz,
                href=23, vsync=25, reset=-1, pwdn=-1,
                sioc=27, siod=26, xclk=21, pclk=22, fb_location=camera.PSRAM)

    camera.framesize(camera.FRAME_VGA)
    # The options are the following:
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA
    
    camera.flip(1)                       # Flip up and down window: 0-1
    camera.mirror(1)                     # Flip window left and right: 0-1
    camera.saturation(0)                 # saturation: -2,2 (default 0). -2 grayscale 
    camera.brightness(0)                 # brightness: -2,2 (default 0). 2 brightness
    camera.contrast(0)                   # contrast: -2,2 (default 0). 2 highcontrast
    camera.quality(10)                   # quality: # 10-63 lower number means higher quality    
    camera.speffect(camera.EFFECT_NONE)
    camera.whitebalance(camera.WB_NONE)

index_web="""
HTTP/1.0 200 OK\r\n
<html>
  <head>
    <title>Security Cam</title>
  </head>
  <body>
    <h1>Security Cam Video Feed</h1>
    <img src="/video" margin-top:100px; style="transform:rotate(180deg)"; />
   <br>
   <table class="tg">
<tbody>
  <tr>
    <td class="tg-0lax"></td>
    <td class="tg-0lax"><button class="btn" aria-label="Login Button" id="cam_up">Up</button></td>
    <td class="tg-0lax"></td>
  </tr>
  <tr>
    <td class="tg-0lax"><button class="btn" aria-label="Login Button" id="cam_left">Left</button></td>
    <td class="tg-0lax"></td>
    <td class="tg-0lax"><button class="btn" aria-label="Login Button" id="cam_right">Right</button></td>
  </tr>
  <tr>
    <td class="tg-0lax"></td>
    <td class="tg-0lax"><button class="btn" aria-label="Login Button" id="cam_down">Down</button></td>
    <td class="tg-0lax"></td>
  </tr>
</tbody>
</table>
  </body>
</html>
"""

# HTTP Response
def index(req, resp):
    yield from resp.awrite(index_web)

def send_frame():
    buf = camera.capture()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n'
           + buf + b'\r\n')
    del buf
    gc.collect()
        
def video(req, resp):
    yield from picoweb.start_response(resp, content_type="multipart/x-mixed-replace; boundary=frame")
    while True:
        yield from resp.awrite(next(send_frame()))
        gc.collect()

ROUTES = [
    ("/", index),
    ("/video", video),
]


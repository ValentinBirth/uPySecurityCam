import picoweb
import camera
import gc
import ulogging as logging

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

def runServer() -> None:
  logging.basicConfig(level=logging.INFO)
  camera_init()
  app = picoweb.WebApp(__name__, ROUTES)
  app.run(debug=1, port=80, host="0.0.0.0")
  # debug values:
  # -1 disable all logging
  # 0 (False) normal logging: requests and errors
  # 1 (True) debug logging
  # 2 extra debug logging

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


index_web="""
HTTP/1.0 200 OK\r\n
<html>

  <head>
    <title>Security Cam</title>
    <style>
      body {
        display: flex;
        background: #2f2f2f;
        justify-content: center;
        align-content: center;
        align-items: center;
      }

      .btn-wraper {
        width: strech;
        margin: 0 auto;
        padding: 2px;
        display: block;
        position: relative;
        border-radius: 25px;
        background-color: #52b7f8;
        text-align: center
      }

      .btn {
        width: strech;
        padding: 5px;
        border: none;
        outline: none;
        line-height: 1.2;
        text-transform: uppercase;
        text-align: center;
        align-items: center;
        font-family: Poppins-Medium;
        font-size: 1em;
        color: #393939;
        background-color: transparent;
        cursor: pointer;
      }

      .wrap {
        min-width: fit-content;
        min-height: fit-content;
        overflow: hidden;
        position: relative;
        background: #393939;
        border-radius: 10px;
        padding: 10px;
        border: #52b7f8 solid 5px;
        color: #52b7f8;
        font-family: Poppins-Regular;
        font-size: 1em;
        line-height: 1.2;
        box-shadow: 0 5px 10px 0px rgb(0 0 0 / 10%);
      }

      .background {
        width: 90vw;
        height: 90vh;
        display: flex;
        flex-wrap: nowrap;
        flex-direction: column;
        justify-content: center;
        align-content: center;
        align-items: center;
        background: #2f2f2f;
        overflow: hidden;

        .title {
          display: block;
          padding-bottom: 5px;
          padding-top: 5px;
          text-align: center;
          font-size: 2em;
        }

    </style>
  </head>

  <body>
    <div class="background" id="background">
      <h1 class="title">Security Cam Video Feed</h1>
      <div class="wrap" id="main-feed-wrap">
        <img src="/video" margin-top:100px; style="transform:rotate(180deg)" ; />
      </div>
      <br>
      <div class="wrap" id="main-camcontrol-wrap">
        <table class="tg">
          <tbody>
            <tr>
              <td class="tg-0lax"></td>
              <td class="tg-0lax">
                <div class="btn-wraper" id="up-btn-wraper">
                  <button class="btn" aria-label="Up Button" id="cam_up">Up</button>
                </div>
              </td>
              <td class="tg-0lax"></td>
            </tr>
            <tr>
              <td class="tg-0lax">
                <div class="btn-wraper" id="left-btn-wraper">
                  <button class="btn" aria-label="Left Button" id="cam_left">Left</button>
                </div>
              </td>
              <td class="tg-0lax"></td>
              <td class="tg-0lax">
                <div class="btn-wraper" id="right-btn-wraper">
                  <button class="btn" aria-label="Right Button" id="cam_right">Right</button>
                </div>
              </td>
            </tr>
            <tr>
              <td class="tg-0lax"></td>
              <td class="tg-0lax">
                <div class="btn-wraper" id="down-btn-wraper">
                  <button class="btn" aria-label="Down Button" id="cam_down">Down</button>
                </div>
              </td>
              <td class="tg-0lax"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </body>

</html>

"""

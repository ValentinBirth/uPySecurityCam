import picoweb_video
import ulogging as logging
import picoweb

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    picoweb_video.camera_init()
    app = picoweb.WebApp(__name__, picoweb_video.ROUTES)
    app.run(debug=1, port=80, host="0.0.0.0")
    # debug values:
    # -1 disable all logging
    # 0 (False) normal logging: requests and errors
    # 1 (True) debug logging
    # 2 extra debug logging




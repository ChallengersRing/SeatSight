from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json
import cv2
import base64
from .views import detector
from .tools import process_frame

class SocketConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.cap = cv2.VideoCapture(0)
        self.keep_sending = True

    async def connect(self):
        await self.accept()
        print(self.websocket_connect,self.channel_name)
        # asyncio.create_task(self.send_data_stream())
        # await self.send_data_stream()
        print("Connected..................")
        
    async def disconnect(self, close_code):
        self.keep_sending = False
        print("Disconnected................",close_code)
        # self.cap.release()
        # cv2.destroyAllWindows()
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        print("text_data:.........",text_data)
        pret, frame = self.cap.read()
        response_data = process_frame(detector, bytes_data, False)
        json_data = json.dumps(response_data)
        await self.send(json_data)
        
    async def send_data_stream(self):
        while self.keep_sending:
            if not self.cap.isOpened():
                print("Error opening video stream or file")

            ret, frame = self.cap.read()
            if ret:
                img, listData = detector.predict(frame)
                # cv2.imshow("SeatSight", img)
                # if cv2.waitKey(25) & 0xFF == ord('q'): 
                #     break

                data = {
                    # "Detected classes:":listData[0],
                    "Chair available:":(listData[3] + listData[4]),
                    "No of People:":listData[2],
                    "Occupied Chair:":listData[3],
                    "Vacant Chair:":listData[4]
                }
                retval, encoded_image = cv2.imencode('.jpeg', img)
                base64_image = base64.b64encode(encoded_image).decode('utf-8')
                response_data = {
                        "data": data,
                        "image": base64_image
                    }
                print("send_data_stream1..................")
                json_data = json.dumps(response_data)
                await self.send(json_data)
            else:
                break
            await asyncio.sleep(0.2)
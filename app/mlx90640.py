import adafruit_mlx90640
import board
import busio
import numpy as np


class mlx90640:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mlx = adafruit_mlx90640.MLX90640(self.i2c)
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
        self.frame = [0] * 768
        self.temp = 0
        self.ta = 0

    def getimage(self):
        self.ta = self.mlx.getFrame(self.frame)
        self.temp = np.max(self.frame)*0.82731-0.07654*self.ta + 10.83260
        print("temp is %0.2f " % self.temp)
        print("ta is %0.2f " % self.ta)
        return self.temp


# if __name__ == '__main__':
#     a = mlx90640()
#     while True:
#         a.getimage()

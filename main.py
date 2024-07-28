import cv2 as cv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import io

url = "https://www.google.com/fbx?fbx=minesweeper"
browser = webdriver.Firefox()
browser.get(url)
canvas = browser.find_element(By.CLASS_NAME, 'ecwpfc')
screenshot = canvas.screenshot_as_png
image = Image.open(io.BytesIO(screenshot))


pixels = image.load()

width, height = image.size
# 540, 420
print(f'Width: {width}, Height: {height}')
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # print(f'Pixel ({x}, {y}): R={r}, G={g}, B={b}, A={a}')


# https://www.google.com/fbx?fbx=minesweeper
# squares are 24x24 pixels
# beginner: 10x8
# medium: 18x14
# advanced: 24x20



class Board:
    def __init__(self, xp, yp, xt, yt):
        self.xp = xp
        self.yp = yp
        self.xt = xt
        self.yt = yt
        self.w = round(xp / xt)
        self.h = round(yp / yt)
        
        




beginner = Board(width, height, 10, 8)
medium = Board(width, height,18, 14)
advanced = Board(width, height, 24, 20)

def click_tile(x: int, y: int):
    actions = ActionChains(browser)
    print(-520/2+24*x, -420/2+24*y)
    actions.move_to_element_with_offset(canvas, -520/2+medium.w*x, -420/2+medium.h*y).click().perform()
    

click_tile(0, 0)
click_tile(17, 13)


unknown = -2
flag = -1
colors = {
    '#aad751': unknown,
    '#a2d149': unknown,
    '#f23607': flag,
    '#e63307': flag,
    '#e5c29f': 0,
    '#d7b899': 0,
    '#1976d2': 1,
    '#388e3c': 2,
    '#d32f2f': 3,
    '#7b1fa2': 4,
    '#ff8f00': 5,
    '#0097a7': 6,
    '#424242': 7,
  }

relative_positions = [
      [.6, .4], [.5, .5], [.6, .6], [.5, .58], [.5, .3],
      [.45, .45], [.4, .6], [.5, .4],
]

# def get_tile(x: int, y: int) -> int:
    # px = x * 

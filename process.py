import numpy as np
import matplotlib.pyplot as plt
import random
import math
from PIL import Image
from scipy import special, optimize, constants


pi = constants.pi

def sinc(x):
    if x==0:
        return 1
    return math.sin(x)/x

def imgFilter(x, a):
    if x == 0:
        return 1
    else:
        x = pi*x
        return (math.sin(x)/x)*(math.sin(x/a)*a/x)
        #return sinc(pi*x)*sinc(pi*x/a)

def process(original, width, height, a):
    resultArr = np.zeros((height*2, width*2), dtype='uint8')
    #it = np.nditer(resultArr, flags=['multi_index'], op_flags=['readwrite'])
    #while not it.finished:
        #i = it.multi_index[0]
        #j = it.multi_index[1]
        #if i%2 == 0 and j%2 == 0:
            #it[0] = original[i/2][j/2]
        #else:
            #it[0] = 222
        #it.iternext()

    #newImg = Image.fromarray(resultArr, 'L')
    #newImg.show()

    it = np.nditer(resultArr, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        i = it.multi_index[0]
        j = it.multi_index[1]
        if i%2 == 0 and j%2 == 0:
            it[0] = original[i/2][j/2]
            it.iternext()
            continue
        i2 = i/2.
        j2 = j/2.
        startRow = max(math.ceil(i2)-a+1, 0)
        finishRow = min(math.ceil(i2)+a, height)
        startCol = max(math.ceil(j2)-a+1, 0)
        finishCol = min(math.ceil(j2)+a, width)
        result = 0
        row = startRow
        while row < finishRow:
            col = startCol
            filteredCell = imgFilter(i2-row, a)
            while col < finishCol:
                result += original[row][col]*filteredCell*imgFilter(j2-col, a)
                col += 1
            row += 1

        if result > 255:
            it[0] = 255
        elif result < 0:
            it[0] = 0
        else:
            it[0] = int(result)

        it.iternext()

    return resultArr


def main():
    img = Image.open('img/cat-band.png').convert('L')
    width = img.size[0]
    height = img.size[1]
    print 'image size:', width, height

    originalArr = np.array(np.uint8(img))

    newImg = Image.fromarray(originalArr, 'L')
    newImg.show()

    resultArr = process(originalArr, width, height, 4)
    resultArr2 = process(resultArr, width*2, height*2, 4)

    newImg = Image.fromarray(resultArr2, 'L')
    newImg.show()


if __name__ == "__main__":
    main()

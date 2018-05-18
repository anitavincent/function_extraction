# receives a binary image where 0.0 means YES
# returns lowest x,y active pixel, also the cropped
# image discarding padding inactive pixels


def crop_binary(image):

    padding = 3

    maxX = -1
    maxY = -1
    baseX = 99999999999999999999
    baseY = 99999999999999999999

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if image[i][j] > 0.0:
                if i < baseY:
                    baseY = i
                if i > maxY:
                    maxY = i
                if j < baseX:
                    baseX = j
                if j > maxX:
                    maxX = j

    # didn find any contour pixel, just crop 1 pixel
    if maxX == -1:
        return 0, 0, image[0:2, 0:2]

    if baseY - padding >= 0:
        baseY -= padding
    if maxY + padding <= image.shape[0]:
        maxY += padding
    if baseX - padding >= 0:
        baseX -= padding
    if maxX + padding <= image.shape[1]:
        maxX + padding

    return baseY, baseX, image[baseY:maxY, baseX:maxX]

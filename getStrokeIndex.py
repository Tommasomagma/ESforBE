
#imageIndexLs = output from openAi
#indexMap = output from drawStroke(strokes) in getImage.py
def mapIndex(imageIndexLs, indexMap):

    #List in which we will store stroke indeces we return to FE
    strokeIndexLs = []

    #For each image index we get from openAi we find the stroke indeces it represents
    for imageIndex in imageIndexLs:
        for strokeIndex in indexMap[imageIndex]:
            strokeIndexLs.append(strokeIndex)
    
    return strokeIndexLs



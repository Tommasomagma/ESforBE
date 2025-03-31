from PIL import Image, ImageDraw, ImageFont

def drawStroke(strokes):

    #Define size of image
    size = 800

    # Create canvas with fixed dimensions
    canvas_size = (size, size)
    image = Image.new('RGB', canvas_size, 'white')
    draw = ImageDraw.Draw(image)

    # Calculate bounds across all strokes
    all_x = [x for stroke in strokes for x in stroke['x']]
    all_y = [y for stroke in strokes for y in stroke['y']]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Set padding and scale
    padding = 30
    content_width = max_x - min_x + padding * 2
    content_height = max_y - min_y + padding * 2
    scale = min((size - padding * 2) / content_width, (size - padding * 2) / content_height)

    # Center the content
    translate_x = (size - content_width * scale) / 2 - min_x * scale
    translate_y = (size - content_height * scale) / 2 - min_y * scale

    # Draw all strokes
    for i, stroke in enumerate(strokes):

        scaled_x = [(x * scale + translate_x) for x in stroke['x']]
        scaled_y = [(y * scale + translate_y) for y in stroke['y']]

        #Increase size of dots for better visibility for Gemini
        if len(scaled_x) < 3:
            x = scaled_x[0]
            y = scaled_y[0] 
            draw.ellipse([x-5, y-5, x+5, y+5], fill='black')
        else:
            for i in range(len(scaled_x) - 1):
                draw.line([(scaled_x[i], scaled_y[i]), (scaled_x[i + 1], scaled_y[i + 1])], fill='black', width=3)

    # Add index numbers 
    try:
        font = ImageFont.truetype("ARIAL.TTF", 20)
    except OSError:
        print(OSError)
        font = ImageFont.load_default()

    # Index map will contain all indeces that we write out in the image as keys
    # The value for each key/index will be a list of the strokes that are represented by that index in the image
    indexMap = {}
    currentIndexLoc = []
    currentIndex = -1
    strokeCount = -1

    for stroke in strokes:
        location = getIndexLocation(stroke)
        scaled_x = location['x'] * scale + translate_x
        scaled_y = location['y'] * scale + translate_y
        strokeCount += 1

        # Draw the index number
        if checkIndexDist(currentIndexLoc, scaled_x, scaled_y) == True:
            currentIndex += 1
            draw.text((scaled_x, scaled_y), str(currentIndex), fill="red", font=font, anchor="mm")
            currentIndexLoc.append([scaled_x, scaled_y])
            #If we have drawn a new index we create a new object in indexMap
            indexMap[currentIndex] = [strokeCount]
        else:
            #If the current stroke is to close to another we map it to the last index we wrote in the image
            indexMap[currentIndex].append(strokeCount)

    #Return the image and the mapping from each index in the image to each stroke on the drawboard
    return image, indexMap


# Function checking if index is too close to other index to written in image
def checkIndexDist(currentIndexLoc, x, y):

    # Check if any point in currentIndexLoc is within 50 pixels of (x,y)
    for point in currentIndexLoc:
        # Calculate Euclidean distance between points
        dist = ((point[0] - x)**2 + (point[1] - y)**2)**0.5
        if dist <= 50:
            return False

    return True


# Function which returns the location in which the index of the stroke should be written
def getIndexLocation(stroke):

    x = max(stroke["x"]) + 10
    y = max(stroke["y"]) + 10

    return {"x": x, "y": y}
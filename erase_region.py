import numpy as np
import cv2
import pyvips
import sys
# ============================================================================

CANVAS_SIZE = (600,800)

FINAL_LINE_COLOR = (0, 255, 0)
WORKING_LINE_COLOR = (127, 127, 127)

# ============================================================================

class PolygonDrawer(object):
    def __init__(self, window_name, filename):
        self.window_name = window_name # Name for our window
        self.fill_color = (0,0, 255)
        self.done = False # Flag signalling we're done
        self.current = (0, 0) # Current position, so we can draw the line-in-progress
        self.points = [] # List of points defining our polygon
        self.canvas = cv2.imread(filename)

    def on_mouse(self, event, x, y, buttons, user_param):
        # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)

        if self.done: # Nothing more to do
            return

        if event == cv2.EVENT_MOUSEMOVE:
            # We want to be able to draw the line-in-progress, so update current mouse position
            self.current = (x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.fill_color = self.canvas[y, x]
            print(self.fill_color)
            #self.fill_color = self.fill_color.astype(np.int32, copy=False)


    def run(self):
        # Let's create our working window and set a mouse callback to handle events
        #cv2.namedWindow(self.window_name, flags=cv2.CV_WINDOW_AUTOSIZE)
        
        cv2.imshow(self.window_name, self.canvas)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while(not self.done):
            # This is our drawing loop, we just continuously draw new images
            # and show them in the named window
            #canvas = np.zeros(CANVAS_SIZE, np.uint8)
            if (len(self.points) > 0):
                # Draw all the current polygon segments
                cv2.polylines(self.canvas, np.array([self.points]), False, FINAL_LINE_COLOR, 2)
                # And  also show what the current segment would look like
                #cv2.line(canvas, self.points[-1], self.current, WORKING_LINE_COLOR)
            # Update the window
            cv2.imshow(self.window_name, self.canvas)
            # And wait 50ms before next iteration (this will pump window messages meanwhile)
            if cv2.waitKey(50) == 27: # ESC hit
                self.done = True

        # User finised entering the polygon points, so let's make the final drawing
        #canvas = np.zeros(CANVAS_SIZE, np.uint8)
        # of a filled polygon
        height, width, channels = self.canvas.shape
        mask_img = np.zeros((height, width, 3), np.uint8)
        if (len(self.points) > 0):
            cv2.fillPoly(mask_img, np.array([self.points]), color = (255,255,255))
        # And show it
        cv2.imshow(self.window_name, self.canvas)
        # Waiting for the user to press any key
        cv2.waitKey()

        cv2.destroyWindow(self.window_name)

        background_img = mask_img.copy()
        self.fill_color = (255, 255, 255) - self.fill_color
        for i in range(height):
            for j in range(width):
                if background_img[i,j,0] > 250:
                    background_img[i,j] = self.fill_color

        return mask_img, background_img

# ============================================================================

if __name__ == "__main__":
    i = int(sys.argv[1])
    filename = '%03d'%(i)+'.tif-new.tif'
    vipimg = pyvips.Image.new_from_file(filename)
    rsi = vipimg.resize(0.05)
    rsi.write_to_file("hello.tif",predictor='horizontal', compression='deflate')

    pd = PolygonDrawer("Polygon",'hello.tif')
    image, bimg= pd.run()
    cv2.imwrite("mask.jpg", image)
    cv2.imwrite("bimg.jpg", bimg)

    wb = pyvips.Image.new_from_file("mask.jpg")
    bb = pyvips.Image.new_from_file("bimg.jpg")

    wb = wb.resize(20)
    bb = bb.resize(20)

    vipimg = vipimg.boolean(wb, 'or')
    vipimg = vipimg.boolean(bb, 'eor')
    vipimg.write_to_file('output.tif',predictor='horizontal', compression='deflate')

    print("Polygon = %s" % pd.points)
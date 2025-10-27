"""
ROI Finder Tool for ValTimer
This tool helps you find the correct ROI (Region of Interest) coordinates 
for Spike detection at different resolutions.

Usage:
1. Run this script while Valorant is running
2. Go into a custom game and plant the Spike
3. Press 'c' to capture and save the current screen
4. Draw a rectangle around the Spike icon in the saved image
5. The tool will output the ROI coordinates

Controls:
- Click and drag to draw rectangle around Spike icon
- Press 'r' to reset the selection
- Press 's' to save the ROI coordinates
- Press 'q' to quit
"""

import cv2
import numpy as np
import mss
from PIL import Image
import json
from datetime import datetime

class ROIFinder:
    def __init__(self):
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.roi = None
        self.image = None
        self.clone = None
        
    def capture_screen(self):
        """Capture full screen"""
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            screenshot = sct.grab(monitor)
            
            # Convert to numpy array
            img = np.array(screenshot)
            # Convert BGRA to BGR
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img, monitor
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for drawing rectangle"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)
            self.end_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.end_point = (x, y)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_point = (x, y)
            
    def draw_rectangle(self):
        """Draw current rectangle on image"""
        temp_image = self.clone.copy()
        
        if self.start_point and self.end_point:
            cv2.rectangle(temp_image, self.start_point, self.end_point, (0, 255, 0), 2)
            
            # Show dimensions
            width = abs(self.end_point[0] - self.start_point[0])
            height = abs(self.end_point[1] - self.start_point[1])
            left = min(self.start_point[0], self.end_point[0])
            top = min(self.start_point[1], self.end_point[1])
            
            text = f"W:{width} H:{height} L:{left} T:{top}"
            cv2.putText(temp_image, text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return temp_image
    
    def get_roi_dict(self):
        """Get ROI as dictionary"""
        if not self.start_point or not self.end_point:
            return None
            
        left = min(self.start_point[0], self.end_point[0])
        top = min(self.start_point[1], self.end_point[1])
        width = abs(self.end_point[0] - self.start_point[0])
        height = abs(self.end_point[1] - self.start_point[1])
        
        return {
            'left': left,
            'top': top,
            'width': width,
            'height': height
        }
    
    def run(self):
        """Main loop"""
        print("=" * 60)
        print("ROI Finder Tool for ValTimer")
        print("=" * 60)
        print("\nInstructions:")
        print("1. Go to Valorant and plant the Spike")
        print("2. Alt+Tab back here and press 'c' to capture screen")
        print("3. Draw a rectangle around the Spike icon")
        print("4. Press 's' to save ROI coordinates")
        print("5. Press 'q' to quit")
        print("\nControls:")
        print("  c = Capture screen")
        print("  r = Reset selection")
        print("  s = Save ROI")
        print("  q = Quit")
        print("=" * 60)
        
        while True:
            key = input("\nPress 'c' to capture screen (or 'q' to quit): ").lower()
            
            if key == 'q':
                print("Exiting...")
                break
                
            if key == 'c':
                print("\nCapturing screen...")
                self.image, monitor = self.capture_screen()
                self.clone = self.image.copy()
                
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                cv2.imwrite(filename, self.image)
                print(f"Screenshot saved as: {filename}")
                print(f"Resolution: {monitor['width']}x{monitor['height']}")
                
                # Create window
                cv2.namedWindow('ROI Finder', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('ROI Finder', 1280, 720)
                cv2.setMouseCallback('ROI Finder', self.mouse_callback)
                
                print("\nDraw a rectangle around the Spike icon...")
                print("Press 'r' to reset, 's' to save, 'q' to quit")
                
                while True:
                    # Draw rectangle
                    display_image = self.draw_rectangle()
                    cv2.imshow('ROI Finder', display_image)
                    
                    key = cv2.waitKey(1) & 0xFF
                    
                    if key == ord('r'):
                        # Reset
                        self.start_point = None
                        self.end_point = None
                        print("\nSelection reset. Draw again...")
                        
                    elif key == ord('s'):
                        # Save ROI
                        roi = self.get_roi_dict()
                        if roi:
                            print("\n" + "=" * 60)
                            print("ROI COORDINATES:")
                            print("=" * 60)
                            print(f"Resolution: {monitor['width']}x{monitor['height']}")
                            print(f"\nROI Dictionary:")
                            print(json.dumps(roi, indent=2))
                            print(f"\nPython Code:")
                            print(f"roi = {roi}")
                            print("=" * 60)
                            
                            # Save to file
                            output_file = f"roi_{monitor['width']}x{monitor['height']}_{timestamp}.json"
                            with open(output_file, 'w') as f:
                                json.dump({
                                    'resolution': f"{monitor['width']}x{monitor['height']}",
                                    'roi': roi,
                                    'timestamp': timestamp
                                }, f, indent=2)
                            print(f"\nROI saved to: {output_file}")
                            
                            # Extract and save ROI region
                            roi_image = self.image[roi['top']:roi['top']+roi['height'], 
                                                  roi['left']:roi['left']+roi['width']]
                            roi_filename = f"roi_region_{timestamp}.png"
                            cv2.imwrite(roi_filename, roi_image)
                            print(f"ROI region saved as: {roi_filename}")
                            print("\nYou can now use these coordinates in timer_valo.py")
                        else:
                            print("\nNo ROI selected! Draw a rectangle first.")
                            
                    elif key == ord('q'):
                        cv2.destroyAllWindows()
                        break
                        
        cv2.destroyAllWindows()
        print("\nThank you for using ROI Finder!")

if __name__ == '__main__':
    finder = ROIFinder()
    finder.run()

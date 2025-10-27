"""
Simple ROI Position Finder for ValTimer
This tool helps you find the correct ROI coordinates for the Spike icon
at different resolutions.

Usage:
1. Run this script
2. Select your resolution
3. Capture a screenshot when Spike is planted
4. Draw a rectangle around the Spike icon
5. Get the ROI coordinates to add to timer_valo.py

The output coordinates can be directly copied into RESOLUTION_SETTINGS.
"""

import cv2
import numpy as np
import mss
import json
from datetime import datetime

class SimpleROIFinder:
    def __init__(self):
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.image = None
        self.clone = None
        self.window_name = 'ROI Finder - Draw rectangle around Spike icon'
        
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events"""
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
        """Draw rectangle and show coordinates"""
        temp_image = self.clone.copy()
        
        if self.start_point and self.end_point:
            # Draw rectangle
            cv2.rectangle(temp_image, self.start_point, self.end_point, (0, 255, 0), 2)
            
            # Calculate ROI
            left = min(self.start_point[0], self.end_point[0])
            top = min(self.start_point[1], self.end_point[1])
            width = abs(self.end_point[0] - self.start_point[0])
            height = abs(self.end_point[1] - self.start_point[1])
            
            # Display info
            info = [
                f"ROI Coordinates:",
                f"Left: {left}",
                f"Top: {top}",
                f"Width: {width}",
                f"Height: {height}",
                "",
                "Press 's' to save",
                "Press 'r' to reset",
                "Press 'q' to quit"
            ]
            
            y_pos = 30
            for line in info:
                cv2.putText(temp_image, line, (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_pos += 25
        else:
            cv2.putText(temp_image, "Draw a rectangle around the Spike icon",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
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
    
    def capture_and_find_roi(self):
        """Main function to capture screen and find ROI"""
        # Get screen info
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            resolution = f"{monitor['width']}x{monitor['height']}"
            
            print("=" * 70)
            print("Simple ROI Finder for ValTimer")
            print("=" * 70)
            print(f"Screen Resolution: {resolution}")
            print(f"\nInstructions:")
            print("1. Go to Valorant and plant the Spike")
            print("2. Alt+Tab back here and press Enter to capture")
            print("3. Draw a rectangle around the Spike icon")
            print("4. Press 's' to save the ROI coordinates")
            print("=" * 70)
            
            input("\nPress Enter when Spike is planted and visible...")
            
            # Capture screen
            print("\n📸 Capturing screen...")
            screenshot = sct.grab(monitor)
            self.image = np.array(screenshot)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)
            self.clone = self.image.copy()
            
            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_file = f"screenshot_{resolution}_{timestamp}.png"
            cv2.imwrite(screenshot_file, self.image)
            print(f"✅ Screenshot saved: {screenshot_file}")
            
            # Create window
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_name, 1280, 720)
            cv2.setMouseCallback(self.window_name, self.mouse_callback)
            
            print("\n🖱️  Draw a rectangle around the Spike icon...")
            print("   - Click and drag to draw")
            print("   - Press 'r' to reset")
            print("   - Press 's' to save")
            print("   - Press 'q' to quit\n")
            
            while True:
                display = self.draw_rectangle()
                cv2.imshow(self.window_name, display)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('r'):
                    # Reset
                    self.start_point = None
                    self.end_point = None
                    print("🔄 Selection reset")
                    
                elif key == ord('s'):
                    # Save
                    roi = self.get_roi_dict()
                    if roi:
                        self.save_roi(roi, resolution, timestamp)
                    else:
                        print("⚠️  No ROI selected! Draw a rectangle first.")
                        
                elif key == ord('q'):
                    break
            
            cv2.destroyAllWindows()
    
    def save_roi(self, roi, resolution, timestamp):
        """Save ROI data"""
        print("\n" + "=" * 70)
        print("✅ ROI COORDINATES FOUND!")
        print("=" * 70)
        print(f"Resolution: {resolution}")
        print(f"\nROI Dictionary:")
        print(json.dumps(roi, indent=2))
        
        # Generate code for timer_valo.py
        print("\n" + "=" * 70)
        print("📋 Copy this to timer_valo.py RESOLUTION_SETTINGS:")
        print("=" * 70)
        
        # Determine resolution name
        if resolution == "1920x1080":
            res_name = "1k"
        elif resolution == "2560x1440":
            res_name = "2k"
        elif resolution == "1440x1080":
            res_name = "4:3"
        else:
            res_name = f"custom_{resolution}"
        
        print(f"""
'{res_name}': {{
    'name': '{resolution}',
    'roi': {roi}
}},
""")
        
        print("=" * 70)
        
        # Save to JSON file
        output_file = f"roi_{resolution}_{timestamp}.json"
        data = {
            'resolution': resolution,
            'resolution_name': res_name,
            'roi': roi,
            'timestamp': timestamp,
            'for_timer_valo': {
                res_name: {
                    'name': resolution,
                    'roi': roi
                }
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 ROI data saved to: {output_file}")
        
        # Extract and save ROI region
        roi_image = self.image[roi['top']:roi['top']+roi['height'], 
                              roi['left']:roi['left']+roi['width']]
        roi_image_file = f"roi_region_{resolution}_{timestamp}.png"
        cv2.imwrite(roi_image_file, roi_image)
        print(f"🖼️  ROI region saved as: {roi_image_file}")
        
        print("\n✅ Done! You can now add this ROI to timer_valo.py")
        print("=" * 70)

def main():
    """Main menu"""
    print("\n" + "=" * 70)
    print("         Simple ROI Position Finder for ValTimer")
    print("=" * 70)
    print("\nThis tool helps you find the Spike icon position for any resolution.")
    print("The output can be directly added to RESOLUTION_SETTINGS in timer_valo.py")
    print("\n" + "=" * 70)
    
    # Detect current resolution
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        resolution = f"{monitor['width']}x{monitor['height']}"
        print(f"\n✅ Detected Resolution: {resolution}")
    
    print("\nWhat would you like to do?")
    print("1. Find ROI for current resolution")
    print("2. Exit")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == '1':
        finder = SimpleROIFinder()
        finder.capture_and_find_roi()
    else:
        print("Goodbye!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

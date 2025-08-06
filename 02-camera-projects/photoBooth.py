import cv2
import time
from datetime import datetime
import os

class PhotoBooth:
    def __init__(self):
        # Init camera
        self.cap = cv2.VideoCapture(0)  # 0 is first camera
        if not self.cap.isOpened():
            print("Could not open camera")
            exit(1)
        
        # Set camera res for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Photo counter
        self.photo_count = 0
        
        # Create photos directory if it doesn't exist
        self.photos_dir = "photos"
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)
            print(f"Created {self.photos_dir} directory")
    
    def say(self, message):
        """Print message (no audio for now)"""
        print(f"🔊 {message}")
    
    def take_photo(self, frame):
        """Take and save photo"""
        self.photo_count += 1
        
        # Creates filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.photos_dir}/photo_{self.photo_count:03d}_{timestamp}.jpg"
        
        # Save photo
        success = cv2.imwrite(filename, frame)
        if success:
            print(f"Photo saved: {filename}")
            return True
        else:
            print("Error saving photo")
            return False
    
    def add_photo_overlay(self, frame):
        """Add helpful text overlay to the camera feed"""
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Add instructions at the top
        cv2.putText(frame, "PI PHOTO BOOTH 📸", (20, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, "Press SPACE to take photo", (20, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit", (20, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add photo counter at bottom
        cv2.putText(frame, f"Photos taken: {self.photo_count}", (20, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def run(self):
        """Main photo booth loop"""
        print("\n Starting Pi Photo Booth")
        print("=" * 40)
        self.say("Welcome to the Pi Photo Booth")
        
        print("Controls:")
        print(" Space = Take Photo")
        print(" Q or ESC = Quit")
        print("=" * 40)
        
        try:
            while True:
                # Read frame from camera
                ret, frame = self.cap.read()
                if not ret:
                    print("Could not read from camera")
                    break
                
                frame = cv2.flip(frame, 1)  # Flip frame horizontally
                frame = self.add_photo_overlay(frame)  # Add overlay info
                cv2.imshow("Pi photo booth", frame)  # Display Frame
                
                key = cv2.waitKey(1) & 0xFF  # Check for key presses
                
                if key == ord(' '):  # Space bar
                    print("Taking photo")
                    self.take_photo(frame)  # take photo w current frame
                    time.sleep(0.5)
                    
                elif key == ord('q') or key == 27:
                    break
                    
        except KeyboardInterrupt:
            print("Booth stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up session and show summary"""
        self.cap.release()  # Release camera
        cv2.destroyAllWindows()
        
        # Session Summary
        print(f"\n Photo Booth Session Complete!")
        print(f" Total photos taken: {self.photo_count}")
        
        if self.photo_count > 0:
            print(f" Photos saved in: {self.photos_dir}/")
            self.say(f"Session complete! You took {self.photo_count} amazing photos!")
        else:
            self.say("Thanks for trying the photo booth!")
        
        print(" Thanks for using Pi Photo Booth!")

# Main execution
if __name__ == "__main__":
    booth = PhotoBooth()
    booth.run()
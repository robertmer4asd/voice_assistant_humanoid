import cv2
import pygame
import sys

class SplashScreen:
    def __init__(self, image_path, duration):
        self.image_path = image_path
        self.duration = duration
        self.screen_width = 882
        self.screen_height = 568

    def show(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Splash Screen Example")

        try:
            # Load the image
            splash_image = pygame.image.load(self.image_path)
            splash_image.set_alpha(0)  # Set initial transparency to fully transparent
        except pygame.error as e:
            print("Error loading splash image:", e)
            pygame.quit()
            sys.exit(1)

        splash_rect = splash_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        clock = pygame.time.Clock()
        fade_speed = 255 / (self.duration * 60)  # Calculate the speed for fading in

        # Fade in
        for alpha in range(256):
            splash_image.set_alpha(alpha)
            screen.fill((0, 0, 0))  # Clear the screen
            screen.blit(splash_image, splash_rect)
            pygame.display.flip()
            clock.tick(60)

        pygame.time.delay(int((self.duration - 2) * 1000))  # Display image for middle duration

        # Fade out
        for alpha in range(255, -1, -1):
            splash_image.set_alpha(alpha)
            screen.fill((0, 0, 0))  # Clear the screen
            screen.blit(splash_image, splash_rect)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

def detect_faces(frame, face_cascade):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return frame

def main():
    image_path = "splash.jpg"  # Replace with your splash image file path
    duration = 3  # duration is in seconds

    splash = SplashScreen(image_path, duration)
    splash.show()

    # After splash screen, continue with the main application
    pygame.init()
    main_screen = pygame.display.set_mode((882, 568))
    pygame.display.set_caption("Main Application")
    smiley_image = pygame.image.load("smiley.jpeg")  # Replace with your smiley face image file path

    # Calculate the position to move the smiley face image to the right
    smiley_rect = smiley_image.get_rect(center=(3 * main_screen.get_width() // 4, main_screen.get_height() // 2))

    # Load pre-trained cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()

        if ret:
            # Perform face detection on the captured frame
            frame_with_faces = detect_faces(frame, face_cascade)

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)
            # Convert the frame to pygame surface
            frame_pygame = pygame.image.frombuffer(frame_rgb.tostring(), frame_with_faces.shape[1::-1], "RGB")
            # Resize the frame to fit in the main application window
            frame_pygame = pygame.transform.scale(frame_pygame, (main_screen.get_width() // 2, main_screen.get_height()))

            # Display the frame in the main application window
            main_screen.fill((255, 255, 255))  # Fill the screen with white
            main_screen.blit(smiley_image, smiley_rect)  # Draw smiley face at calculated position
            main_screen.blit(frame_pygame, (0, 0))  # Display the frame on the left side of the screen

            pygame.display.flip()

        # Check for key press events
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()

import cv2
import mediapipe as mp
import pygame
import sys
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Initialize Pygame for the game interface
pygame.init()
width, height = 900, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hand Gesture Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
GREEN = (60, 255, 60)
BLUE = (60, 60, 255)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (210, 180, 140)
DINO_GREEN = (34, 139, 34)
CACTUS_GREEN = (0, 100, 0)
CLOUD_WHITE = (240, 240, 240)
SUN_YELLOW = (255, 223, 0)

# Fonts
font_small = pygame.font.SysFont('Arial', 28)
font_medium = pygame.font.SysFont('Arial', 36, bold=True)
font_large = pygame.font.SysFont('Arial', 72, bold=True)
font_title = pygame.font.SysFont('Arial', 90, bold=True)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Dino properties
dino_x, dino_y = 100, 350
dino_width, dino_height = 50, 60
dino = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
gravity = 0.8
velocity = 0
is_jumping = False
score = 0
game_speed = 8

# Obstacle properties
obstacle_width, obstacle_height = 30, 60
obstacle = pygame.Rect(width, 340, obstacle_width, obstacle_height)

# Clouds
clouds = [
    {'x': 100, 'y': 80, 'speed': 1},
    {'x': 400, 'y': 120, 'speed': 0.8},
    {'x': 700, 'y': 60, 'speed': 1.2}
]

# Animation
dino_leg_frame = 0
frame_counter = 0

# Clock
clock = pygame.time.Clock()

# OpenCV camera
cap = cv2.VideoCapture(0)

def draw_dino(x, y, leg_frame):
    """Draw a cute dinosaur"""
    # Body
    pygame.draw.ellipse(screen, DINO_GREEN, (x, y + 20, 35, 30))
    # Head
    pygame.draw.circle(screen, DINO_GREEN, (x + 35, y + 15), 18)
    # Eye
    pygame.draw.circle(screen, WHITE, (x + 42, y + 12), 6)
    pygame.draw.circle(screen, BLACK, (x + 44, y + 12), 3)
    # Mouth
    pygame.draw.line(screen, BLACK, (x + 48, y + 20), (x + 52, y + 22), 2)
    # Tail
    points = [(x, y + 35), (x - 15, y + 25), (x - 10, y + 40)]
    pygame.draw.polygon(screen, DINO_GREEN, points)
    # Legs (animated)
    if leg_frame % 2 == 0:
        pygame.draw.rect(screen, DINO_GREEN, (x + 8, y + 45, 8, 15))
        pygame.draw.rect(screen, DINO_GREEN, (x + 22, y + 48, 8, 12))
    else:
        pygame.draw.rect(screen, DINO_GREEN, (x + 8, y + 48, 8, 12))
        pygame.draw.rect(screen, DINO_GREEN, (x + 22, y + 45, 8, 15))
    # Arms
    pygame.draw.rect(screen, DINO_GREEN, (x + 10, y + 25, 6, 12))

def draw_cactus(x, y):
    """Draw a cactus obstacle"""
    # Main body
    pygame.draw.rect(screen, CACTUS_GREEN, (x + 10, y, 10, 60))
    # Left arm
    pygame.draw.rect(screen, CACTUS_GREEN, (x, y + 20, 10, 3))
    pygame.draw.rect(screen, CACTUS_GREEN, (x, y + 20, 3, 20))
    # Right arm
    pygame.draw.rect(screen, CACTUS_GREEN, (x + 20, y + 30, 10, 3))
    pygame.draw.rect(screen, CACTUS_GREEN, (x + 27, y + 30, 3, 15))
    # Spikes
    for i in range(0, 60, 10):
        pygame.draw.line(screen, CACTUS_GREEN, (x + 9, y + i + 5), (x + 6, y + i + 5), 2)
        pygame.draw.line(screen, CACTUS_GREEN, (x + 21, y + i + 5), (x + 24, y + i + 5), 2)

def draw_cloud(x, y):
    """Draw a cloud"""
    pygame.draw.circle(screen, CLOUD_WHITE, (x, y), 20)
    pygame.draw.circle(screen, CLOUD_WHITE, (x + 25, y), 25)
    pygame.draw.circle(screen, CLOUD_WHITE, (x + 50, y), 20)
    pygame.draw.ellipse(screen, CLOUD_WHITE, (x, y - 10, 50, 30))

def draw_ground():
    """Draw ground with grass details"""
    pygame.draw.rect(screen, GROUND_COLOR, (0, 400, width, 100))
    pygame.draw.line(screen, BLACK, (0, 400), (width, 400), 3)
    # Grass patches
    for i in range(0, width, 60):
        for j in range(3):
            offset = (frame_counter + i) % width
            pygame.draw.line(screen, GREEN, (offset + j * 15, 400), (offset + j * 15 - 5, 395), 2)

def draw_sun():
    """Draw a sun"""
    pygame.draw.circle(screen, SUN_YELLOW, (width - 100, 80), 40)
    # Sun rays
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        start_x = width - 100 + math.cos(rad) * 50
        start_y = 80 + math.sin(rad) * 50
        end_x = width - 100 + math.cos(rad) * 70
        end_y = 80 + math.sin(rad) * 70
        pygame.draw.line(screen, SUN_YELLOW, (start_x, start_y), (end_x, end_y), 3)

def draw_button(text, x, y, w, h, color, hover_color, mouse_pos):
    """Draw a button and return if it's clicked"""
    button_rect = pygame.Rect(x, y, w, h)
    is_hover = button_rect.collidepoint(mouse_pos)
    
    # Draw button
    pygame.draw.rect(screen, hover_color if is_hover else color, button_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_rect, 3, border_radius=15)
    
    # Draw text
    text_surface = font_medium.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    return is_hover

def draw_menu(mouse_pos):
    """Draw the start menu"""
    # Background
    screen.fill(SKY_BLUE)
    draw_sun()
    
    # Moving clouds
    for cloud in clouds:
        draw_cloud(int(cloud['x']), int(cloud['y']))
        cloud['x'] -= cloud['speed'] * 0.5
        if cloud['x'] < -100:
            cloud['x'] = width + 50
    
    draw_ground()
    
    # Title
    title_text = font_title.render("DINO RUN", True, DINO_GREEN)
    title_rect = title_text.get_rect(center=(width // 2, 120))
    # Shadow effect
    shadow_text = font_title.render("DINO RUN", True, BLACK)
    screen.blit(shadow_text, (title_rect.x + 4, title_rect.y + 4))
    screen.blit(title_text, title_rect)
    
    # Dino preview
    draw_dino(width // 2 - 80, 200, dino_leg_frame)
    
    # Instructions
    instruction_text = font_small.render("Close your fist to JUMP!", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(width // 2, 300))
    screen.blit(instruction_text, instruction_rect)
    
    # Start button
    button_clicked = draw_button("START GAME", width // 2 - 100, 350, 200, 60, GREEN, DINO_GREEN, mouse_pos)
    
    return button_clicked

def draw_game_over_screen(mouse_pos):
    """Draw game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = font_large.render("GAME OVER!", True, RED)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 80))
    screen.blit(game_over_text, game_over_rect)
    
    # Score
    score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(width // 2, height // 2 - 10))
    screen.blit(score_text, score_rect)
    
    # Restart button
    restart_clicked = draw_button("RESTART", width // 2 - 100, height // 2 + 50, 200, 60, BLUE, (30, 30, 200), mouse_pos)
    
    # Quit button
    quit_clicked = draw_button("QUIT", width // 2 - 100, height // 2 + 130, 200, 60, RED, (200, 30, 30), mouse_pos)
    
    return restart_clicked, quit_clicked

def count_fingers(hand_landmarks, handedness):
    """Count extended fingers based on hand landmarks"""
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    thumb_tip = 4
    thumb_ip = 3
    
    fingers = []
    
    is_right_hand = handedness == "Right"
    
    # Thumb
    if is_right_hand:
        if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_ip].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_ip].x:
            fingers.append(1)
        else:
            fingers.append(0)
    
    # Other fingers
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return sum(fingers)

def reset_game():
    """Reset game variables"""
    global dino, velocity, is_jumping, score, game_speed, obstacle
    dino.y = dino_y
    velocity = 0
    is_jumping = False
    score = 0
    game_speed = 8
    obstacle.x = width

# Main game loop
print("Starting Hand Gesture Dino Game!")
print("Controls:")
print("- Show 0 fingers (closed fist) to JUMP")
print("- Press 'q' in camera window to quit")

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                if draw_button("START GAME", width // 2 - 100, 350, 200, 60, GREEN, DINO_GREEN, mouse_pos):
                    game_state = PLAYING
                    reset_game()
            elif game_state == GAME_OVER:
                restart_clicked, quit_clicked = draw_game_over_screen(mouse_pos)
                if restart_clicked:
                    game_state = PLAYING
                    reset_game()
                if quit_clicked:
                    running = False
    
    # Process camera frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from camera")
        break
    
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    finger_count = None
    jump_status = "Open hand"
    hand_detected = False
    
    if results.multi_hand_landmarks and results.multi_handedness:
        hand_detected = True
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_type = handedness.classification[0].label
            finger_count = count_fingers(hand_landmarks, hand_type)
            
            if game_state == PLAYING and finger_count == 0:
                jump_status = "JUMPING!"
                # Allow jump if dino is on the ground (with small tolerance)
                if dino.y >= dino_y - 5:
                    velocity = -16
                    is_jumping = True
            elif finger_count == 0:
                jump_status = "Ready to jump!"
            else:
                jump_status = f"{finger_count} fingers"
    
    # Update animation frame
    frame_counter += 1
    if frame_counter % 10 == 0:
        dino_leg_frame = (dino_leg_frame + 1) % 2
    
    # Game logic based on state
    if game_state == MENU:
        screen.fill(SKY_BLUE)
        draw_sun()
        for cloud in clouds:
            draw_cloud(int(cloud['x']), int(cloud['y']))
            cloud['x'] -= cloud['speed'] * 0.5
            if cloud['x'] < -100:
                cloud['x'] = width + 50
        draw_ground()
        
        # Draw menu
        button_clicked = draw_menu(mouse_pos)
        
    elif game_state == PLAYING:
        # Physics
        velocity += gravity
        dino.y += velocity
        
        if dino.y >= dino_y:
            dino.y = dino_y
            velocity = 0
            is_jumping = False
        
        if dino.y < 0:
            dino.y = 0
            velocity = 0
        
        # Move obstacle
        obstacle.x -= game_speed
        if obstacle.x < -obstacle_width:
            obstacle.x = width
            score += 1
            game_speed = min(8 + score * 0.3, 18)
        
        # Check collision
        if dino.colliderect(obstacle):
            game_state = GAME_OVER
            print(f"Game Over! Final Score: {score}")
        
        # Drawing
        screen.fill(SKY_BLUE)
        draw_sun()
        
        # Move and draw clouds
        for cloud in clouds:
            draw_cloud(int(cloud['x']), int(cloud['y']))
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -100:
                cloud['x'] = width + 50
        
        draw_ground()
        draw_dino(dino.x, dino.y, dino_leg_frame)
        draw_cactus(obstacle.x, obstacle.y)
        
        # UI
        score_text = font_medium.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        if finger_count is not None:
            finger_text = font_small.render(f"Fingers: {finger_count}", True, BLUE)
            screen.blit(finger_text, (width - 180, 20))
            
            status_color = RED if finger_count == 0 else BLACK
            status_text = font_small.render(jump_status, True, status_color)
            screen.blit(status_text, (20, 60))
    
    elif game_state == GAME_OVER:
        # Keep drawing game background
        screen.fill(SKY_BLUE)
        draw_sun()
        for cloud in clouds:
            draw_cloud(int(cloud['x']), int(cloud['y']))
        draw_ground()
        draw_dino(dino.x, dino.y, 0)
        draw_cactus(obstacle.x, obstacle.y)
        
        # Draw game over overlay
        restart_clicked, quit_clicked = draw_game_over_screen(mouse_pos)
    
    pygame.display.flip()
    
    # Show camera window with info
    if game_state == PLAYING:
        status = f"Playing - Score: {score}"
    elif game_state == MENU:
        status = "Click START to begin"
    else:
        status = "GAME OVER"
    
    cv2.putText(frame, status, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Fingers: {finger_count if finger_count is not None else 'No hand'}", 
                (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, jump_status, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Hand Gesture Control", frame)
    
    clock.tick(30)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
print("Game closed. Thanks for playing!")
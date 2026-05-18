import pygame
import random
import sys
import os 

# 1. INISIALISASI
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Traffic Racer")
clock = pygame.time.Clock()

# --- INISIALISASI FONT ---
font_score = pygame.font.SysFont("consolas", 24, bold=True)
font_highscore = pygame.font.SysFont("consolas", 18) 
font_gameover = pygame.font.SysFont("impact", 54) 
font_title = pygame.font.SysFont("impact", 42)
font_retry = pygame.font.SysFont("consolas", 18)
font_total = pygame.font.SysFont("consolas", 22, bold=True)

# Definisi Warna (Sama persis dengan referensi Game Over)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GRASS = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 204, 0)
DARK_BLUE = (20, 30, 50) 
ORANGE = (255, 100, 0)    

# --- UKURAN ASET ---
player_width, player_height = 60, 110

# =========================================================================
# --- LOAD GAMBAR ASET DARI FOLDER 'mobil' ---
player_img = pygame.image.load('mobil/mobil_pemain.png')
player_img = pygame.transform.scale(player_img, (player_width, player_height))

enemy_filenames = [
    'mobil_musuh1.png', 
    'mobil_musuh2.png', 
    'mobil_musuh3.png', 
    'mobil_musuh4.png', 
    'mobil_musuh5.png',
    'mobil_musuh6.png',
    'mobil_musuh7.png'
]

enemy_car_images = []
for filename in enemy_filenames:
    img = pygame.image.load(f'mobil/{filename}')
    img = pygame.transform.scale(img, (player_width, player_height))
    enemy_car_images.append(img)
# =========================================================================

# --- SISTEM HIGH SCORE ---
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0 

# Posisi X disesuaikan untuk mobil selebar 60px
player_x = 170  
player_y = HEIGHT - 130
player_speed = 3

# Variabel Lingkungan & Kecepatan Base
base_road_speed = 3
base_enemy_speed = 4
road_speed = base_road_speed
enemy_speed = base_enemy_speed

line_offset = 0
bushes_y = [-50, 250, 550]

# Titik koordinat tengah jalur untuk mobil selebar 60px
lane_centers = [70, 170, 270] 
enemies = []        
spawn_timer = 0     

# --- VARIABEL STATUS GAME ---
score = 0
game_over = False
in_menu = True   # <--- Status saat berada di menu utama

# 2. GAME LOOP UTAMA
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- LOGIKA INPUT TOMBOL SPASI ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if in_menu:
                    in_menu = False # Keluar dari menu, mulai game
                elif game_over:
                    game_over = False
                    enemies.clear()
                    player_x = 170 
                    score = 0
                    spawn_timer = 0
                    road_speed = base_road_speed
                    enemy_speed = base_enemy_speed

    keys = pygame.key.get_pressed()
    
    # --- LOGIKA UPDATE ---
    if in_menu:
        # Saat di menu, jalanan dan semak tetap bergerak pelan sebagai animasi background
        line_offset = (line_offset + 2) % 100
        for i in range(len(bushes_y)):
            bushes_y[i] += 2
            if bushes_y[i] > HEIGHT + 50:
                bushes_y[i] = -100

    elif not game_over:
        # Logika utama saat game berjalan
        difficulty_level = score // 150
        road_speed = min(base_road_speed + (difficulty_level * 0.5), 8)
        enemy_speed = min(base_enemy_speed + (difficulty_level * 0.5), 10)

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 55:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width - 55:
            player_x += player_speed

        line_offset = (line_offset + road_speed) % 100
        for i in range(len(bushes_y)):
            bushes_y[i] += road_speed
            if bushes_y[i] > HEIGHT + 50:
                bushes_y[i] = -100

        spawn_timer += 1
        if spawn_timer > max(40, 100 - (difficulty_level * 5)): 
            lane_x = random.choice(lane_centers) 
            random_car_img = random.choice(enemy_car_images)
            enemies.append([lane_x, -110, player_width, player_height, random_car_img])
            spawn_timer = 0 

        for enemy in enemies[:]: 
            enemy[1] += enemy_speed 
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score += 10 

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        player_hitbox = player_rect.inflate(-4, -7) 
        
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy[2], enemy[3])
            enemy_hitbox = enemy_rect.inflate(-4, -7)
            
            if player_hitbox.colliderect(enemy_hitbox):
                game_over = True 
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))
                break

    # --- C. RENDER ---
    # Gambar environment (selalu digambar terlepas dari status game)
    screen.fill(GRAY)
    pygame.draw.rect(screen, GRASS, (0, 0, 50, HEIGHT))
    pygame.draw.rect(screen, GRASS, (WIDTH - 50, 0, 50, HEIGHT))
    pygame.draw.rect(screen, YELLOW, (50, 0, 5, HEIGHT))
    pygame.draw.rect(screen, YELLOW, (WIDTH - 55, 0, 5, HEIGHT))

    for by in bushes_y:
        pygame.draw.circle(screen, DARK_GREEN, (25, by), 18)       
        pygame.draw.circle(screen, DARK_GREEN, (WIDTH - 25, by + 120), 18) 

    for i in range(-1, HEIGHT // 100 + 1):
        line_y = i * 100 + line_offset
        pygame.draw.rect(screen, WHITE, (145, line_y, 10, 50)) 
        pygame.draw.rect(screen, WHITE, (245, line_y, 10, 50)) 

    # --- D. RENDER OBJEK & UI ---
    if not in_menu:
        # Jika game sedang berjalan atau Game Over, gambar mobil dan UI Skor
        for enemy in enemies:
            screen.blit(enemy[4], (enemy[0], enemy[1]))
            
        screen.blit(player_img, (player_x, player_y))

        score_surface = font_score.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (60, 15))
        
        hs_surface = font_highscore.render(f"High Score: {high_score}", True, YELLOW)
        screen.blit(hs_surface, (60, 45))

    # Tampilan Layar MENU UTAMA
    if in_menu:
        # 1. Buat Overlay Dimming
        overlay = pygame.Surface((WIDTH, HEIGHT)) 
        overlay.set_alpha(150) # Sikit lebih gelap
        overlay.fill((0, 0, 0))                   
        screen.blit(overlay, (0, 0))              

        # 2. Gambar Kotak Pop-up
        popup_rect = pygame.Rect(40, HEIGHT//2 - 110, 320, 220)
        pygame.draw.rect(screen, DARK_BLUE, popup_rect, border_radius=15)
        # Gambar border putih untuk pop-up
        pygame.draw.rect(screen, WHITE, popup_rect, width=3, border_radius=15)
        
        # 3. Teks Judul Utama "TRAFFIC RACER"
        title_surface = font_title.render("TRAFFIC RACER", True, ORANGE)
        title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(title_surface, title_rect)

        # 4. Teks Subtitle (White)
        welcome_surface = font_total.render("Siap Balapan?", True, WHITE)
        welcome_rect = welcome_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
        screen.blit(welcome_surface, welcome_rect)

        # 5. Info High Score 
        menu_hs_surface = font_total.render(f"Rekor Terbaik: {high_score}", True, YELLOW)
        menu_hs_rect = menu_hs_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        screen.blit(menu_hs_surface, menu_hs_rect)
        
        # 6. Teks Instruksi Mulai
        start_surface = font_retry.render("Tekan SPASI untuk Mulai", True, WHITE)
        start_rect = start_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 85))
        screen.blit(start_surface, start_rect)

    # Tampilan Layar GAME OVER
    if game_over and not in_menu:
        overlay = pygame.Surface((WIDTH, HEIGHT)) 
        overlay.set_alpha(150)                    
        overlay.fill((0, 0, 0))                   
        screen.blit(overlay, (0, 0))              

        popup_rect = pygame.Rect(40, HEIGHT//2 - 110, 320, 220)
        pygame.draw.rect(screen, DARK_BLUE, popup_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, popup_rect, width=3, border_radius=15)
        
        go_surface = font_gameover.render("GAME OVER", True, ORANGE)
        go_rect = go_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(go_surface, go_rect)

        total_surface = font_total.render(f"Score Anda: {score}", True, WHITE)
        total_rect = total_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
        screen.blit(total_surface, total_rect)

        best_surface = font_total.render(f"Best Score: {high_score}", True, YELLOW)
        best_rect = best_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        screen.blit(best_surface, best_rect)
        
        retry_surface = font_retry.render("Tekan SPASI untuk Ulangi", True, WHITE)
        retry_rect = retry_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 85))
        screen.blit(retry_surface, retry_rect)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
sys.exit()
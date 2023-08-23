import arcade
import pymunk

# Globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 20
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2

class PongGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Pong")
        
        self.ball = None
        self.paddle1 = None
        self.paddle2 = None
        self.paddle1_vel = 0
        self.paddle2_vel = 0
        self.l_score = 0
        self.r_score = 0
        
        arcade.set_background_color(arcade.color.BLACK)
        
        self.space = pymunk.Space()
        self.space.gravity = 0, 0
        
        self.init_game()
        
        self.game_started = False 
        self.ball_image = arcade.load_texture("img/pelota.png")  # Load the ball image
        self.paddle_image = arcade.load_texture("img/bate.png")
        
    def init_game(self):
        self.paddle1_pos = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.paddle1_shape = pymunk.Poly.create_box(self.paddle1_pos, (PAD_WIDTH, PAD_HEIGHT))
        self.paddle1_shape.elasticity = 1.0
        self.paddle1_shape.filter = pymunk.ShapeFilter(categories=0b01)
        
        self.paddle2_pos = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.paddle2_shape = pymunk.Poly.create_box(self.paddle2_pos, (PAD_WIDTH, PAD_HEIGHT))
        self.paddle2_shape.elasticity = 1.0
        self.paddle2_shape.filter = pymunk.ShapeFilter(categories=0b10)
        
        self.ball_body = pymunk.Body()
        self.ball_shape = pymunk.Circle(self.ball_body, BALL_RADIUS)
        self.ball_shape.elasticity = 1.0
        self.ball_shape.filter = pymunk.ShapeFilter(categories=0b11)
        self.ball_body.position = WIDTH // 2, HEIGHT // 2
        
        self.space.add(self.paddle1_pos, self.paddle1_shape, self.paddle2_pos, self.paddle2_shape, self.ball_body, self.ball_shape)
        
        self.ball_body.velocity = (100, 100)
        
    def on_draw(self):
        arcade.start_render()
        
        if not self.game_started:
            arcade.draw_text("Press Enter to Start", WIDTH // 2, HEIGHT // 2, arcade.color.WHITE, 20, anchor_x="center")
            
        else:
            self.paddle1_shape.body.position = HALF_PAD_WIDTH, self.paddle1_pos.position.y
            self.paddle2_shape.body.position = WIDTH - HALF_PAD_WIDTH, self.paddle2_pos.position.y
            
            arcade.draw_texture_rectangle(HALF_PAD_WIDTH, self.paddle1_pos.position.y, PAD_WIDTH, PAD_HEIGHT, self.paddle_image)
            arcade.draw_texture_rectangle(WIDTH - HALF_PAD_WIDTH, self.paddle2_pos.position.y, PAD_WIDTH, PAD_HEIGHT, self.paddle_image)
            arcade.draw_texture_rectangle(self.ball_body.position.x, self.ball_body.position.y, BALL_RADIUS * 2, BALL_RADIUS * 2, self.ball_image)

            
            arcade.draw_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, arcade.color.WHITE)
            
            arcade.draw_text(f"Score {self.l_score}", 170, 350, arcade.color.GREEN, 20)
            arcade.draw_text(f"Score {self.r_score}", WIDTH - 260, 350, arcade.color.WHITE, 20)
        
    def update(self, delta_time):
        self.ball_body.position += self.ball_body.velocity * delta_time
        
        if self.ball_body.position.y <= BALL_RADIUS or self.ball_body.position.y >= HEIGHT - BALL_RADIUS:
            self.ball_body.velocity = self.ball_body.velocity[0], -self.ball_body.velocity[1]
            
        if self.paddle1_pos.position.y + HALF_PAD_HEIGHT + 1 <= self.ball_body.position.y <= self.paddle1_pos.position.y + HALF_PAD_HEIGHT - 1:
            if self.ball_body.position.x <= HALF_PAD_WIDTH + BALL_RADIUS:
                self.ball_body.velocity = -self.ball_body.velocity[0], self.ball_body.velocity[1]
                
        if self.paddle2_pos.position.y + HALF_PAD_HEIGHT + 1 <= self.ball_body.position.y <= self.paddle2_pos.position.y + HALF_PAD_HEIGHT - 1:
            if self.ball_body.position.x >= WIDTH - HALF_PAD_WIDTH - BALL_RADIUS:
                self.ball_body.velocity = -self.ball_body.velocity[0], self.ball_body.velocity[1]
                
        if self.ball_body.position.x < BALL_RADIUS:
            self.r_score += 1
            self.reset_ball()
            
        if self.ball_body.position.x > WIDTH - BALL_RADIUS:
            self.l_score += 1
            self.reset_ball()
            
        # Increase ball's velocity over time
        self.ball_body.velocity *= 1.001

    def reset_ball(self):
        self.ball_body.position = WIDTH // 2, HEIGHT // 2
        initial_velocity = (100, 100)
        self.ball_body.velocity = initial_velocity
            
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.ENTER:
            self.game_started = True

        if key == arcade.key.W:
            self.paddle1_vel = 80
        elif key == arcade.key.S:
            self.paddle1_vel = -80
        elif key == arcade.key.UP:
            self.paddle2_vel = 80
        elif key == arcade.key.DOWN:
            self.paddle2_vel = -80
            
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.paddle1_vel = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.paddle2_vel = 0
            
    def on_update(self, delta_time):
        self.paddle1_pos.position = HALF_PAD_WIDTH, max(HALF_PAD_HEIGHT, min(HEIGHT - HALF_PAD_HEIGHT, self.paddle1_pos.position.y + self.paddle1_vel * delta_time))
        self.paddle2_pos.position = WIDTH - HALF_PAD_WIDTH, max(HALF_PAD_HEIGHT, min(HEIGHT - HALF_PAD_HEIGHT, self.paddle2_pos.position.y + self.paddle2_vel * delta_time))
        
        self.space.step(delta_time)
        
if __name__ == "__main__":
    window = PongGame()
    arcade.run()


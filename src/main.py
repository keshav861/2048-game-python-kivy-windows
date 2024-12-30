from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.properties import NumericProperty, DictProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from random import choice, randint, random
import json
import os
import sys
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from functools import lru_cache
import gc

# Update the resource path handling
import os

# Get the base directory (one level up from src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add resource path for bundled application
if hasattr(sys, '_MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS, 'assets/fonts'))
    font_path = os.path.join(sys._MEIPASS, 'assets/fonts')
else:
    font_path = os.path.join(BASE_DIR, 'assets', 'fonts')

# Update both font registrations with error handling
try:
    LabelBase.register(
        'FontAwesome', 
        os.path.join(font_path, 'Font Awesome 6 Free-Solid-900.otf')
    )
    
    LabelBase.register(
        '04B_19',
        os.path.join(font_path, '04B_19.TTF')
    )
except Exception as e:
    print(f"Error loading fonts: {e}")

TILE_COLORS = {
    '0': {
        'tile': (0.95, 0.95, 0.95, 0.1),  # Very light, almost invisible
        'bg': (0.85, 0.85, 0.85, 0.1),    # Light grey background
        'text': (0, 0, 0, 0)              # Invisible text for empty tiles
    },
    '2': {
        'tile': (0.95, 0.95, 0.9, 1),     # Light beige tile
        'bg': (0.90, 0.90, 0.85, 1),      # Slightly darker background
        'text': (0.4, 0.4, 0.4, 1)        # Dark grey text
    },
    '4': {
        'tile': (0.95, 0.92, 0.85, 1),
        'bg': (0.90, 0.87, 0.80, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '8': {
        'tile': (0.97, 0.7, 0.47, 1),
        'bg': (0.87, 0.6, 0.37, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '16': {
        'tile': (0.97, 0.6, 0.37, 1),
        'bg': (0.87, 0.5, 0.27, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '32': {
        'tile': (0.97, 0.5, 0.37, 1),
        'bg': (0.87, 0.4, 0.27, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '64': {
        'tile': (0.97, 0.4, 0.23, 1),
        'bg': (0.87, 0.3, 0.13, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '128': {
        'tile': (0.93, 0.81, 0.42, 1),
        'bg': (0.83, 0.71, 0.32, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '256': {
        'tile': (0.93, 0.79, 0.38, 1),
        'bg': (0.83, 0.69, 0.28, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '512': {
        'tile': (0.93, 0.77, 0.31, 1),
        'bg': (0.83, 0.67, 0.21, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '1024': {
        'tile': (0.93, 0.75, 0.24, 1),
        'bg': (0.83, 0.65, 0.14, 1),
        'text': (0.4, 0.4, 0.4, 1)
    },
    '2048': {
        'tile': (0.93, 0.73, 0.17, 1),
        'bg': (0.83, 0.63, 0.07, 1),
        'text': (0.4, 0.4, 0.4, 1)
    }
}

class DifficultyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.3, 0.1)
        self.background_color = (0, 0, 0, 0)
        self.font_name = '04B_19'
        self.font_size = '20sp'
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.93, 0.81, 0.42, 1)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )

class DifficultySelector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.size_hint = (0.4, 0.4)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        self.selected_index = 0
        
        # Initialize animations dictionary
        self.animations = {}
        self.current_cursor = None
        
        # Create outer container for responsive width
        self.container = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(None, 1)
        )
        self.container.bind(minimum_width=self.container.setter('width'))
        
        # Create difficulty options with centered layout
        self.options = []
        for text in ['Easy', 'Medium', 'Hard']:
            # Create a container for proper centering
            option = BoxLayout(
                orientation='horizontal',
                size_hint=(None, None),
                height=40,
                spacing=10,
                padding=[20, 0]
            )
            option.bind(minimum_width=option.setter('width'))
            
            cursor = Label(
                text='\uf0da',
                font_name='FontAwesome',
                font_size='24sp',
                color=(0.93, 0.81, 0.42, 1),
                size_hint=(None, 1),
                width=30,
                opacity=0
            )
            
            label = Label(
                text=text,
                font_name='04B_19',
                font_size='24sp',
                color=(0.93, 0.81, 0.42, 1),
                size_hint=(None, 1),
                width=100,  # Fixed width for consistency
                halign='left'
            )
            
            # Add widgets to option container
            option.add_widget(cursor)
            option.add_widget(label)
            
            self.options.append({'layout': option, 'cursor': cursor})
            self.container.add_widget(option)
        
        # Add container to main layout
        self.add_widget(self.container)
        
        # Bind to window size changes
        Window.bind(on_resize=self._on_window_resize)
        Clock.schedule_once(lambda dt: self._on_window_resize(Window, Window.width, Window.height), 0)
        
        # Start cursor animation after options are created
        Clock.schedule_once(lambda dt: self.start_cursor_animation(), 0)

    def _on_window_resize(self, instance, width, height):
        """Adjust layout based on window size"""
        # Calculate appropriate widths
        window_width = width
        is_mobile = height > width
        
        if is_mobile:
            # Mobile view - narrower width
            self.size_hint = (0.8, 0.4)
            self.container.pos_hint = {'center_x': 0.5}
        else:
            # Desktop view - wider width
            self.size_hint = (0.4, 0.4)
            self.container.pos_hint = {'center_x': 0.5}
        
        # Force layout update
        self.container.do_layout()

    def start_cursor_animation(self):
        # Stop previous animations
        if self.current_cursor:
            Animation.stop_all(self.current_cursor)
        
        # Hide all cursors
        for option in self.options:
            option['cursor'].opacity = 0
        
        # Show and animate selected cursor
        cursor = self.options[self.selected_index]['cursor']
        self.current_cursor = cursor
        cursor.opacity = 1
        
        # Create new animation
        anim = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        anim.repeat = True
        anim.start(cursor)

    def cleanup(self):
        # Stop all animations
        for option in self.options:
            Animation.stop_all(option['cursor'])

    def move_cursor(self, direction):
        # Update selection
        if direction == 'up':
            self.selected_index = (self.selected_index - 1) % 3
        else:
            self.selected_index = (self.selected_index + 1) % 3
        
        # Restart animation with new cursor
        self.start_cursor_animation()

    def get_selected_difficulty(self):
        return ['easy', 'medium', 'hard'][self.selected_index]

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # Title
        title = Label(
            text='2048',
            font_name='04B_19',
            font_size='120sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            color=(0.97, 0.7, 0.47, 1)
        )
        
        # Subtitle
        subtitle = Label(
            text='Select Difficulty',
            font_name='04B_19',
            font_size='30sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(0.93, 0.81, 0.42, 1)
        )
        
        # Difficulty selector
        self.difficulty_selector = DifficultySelector()
        
        # Add widgets
        self.layout.add_widget(title)
        self.layout.add_widget(subtitle)
        self.layout.add_widget(self.difficulty_selector)
        self.add_widget(self.layout)
        
        # Keyboard bindings
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        # Touch binding
        self.layout.bind(on_touch_down=self.on_touch_down)

    def on_enter(self):
        """Called when screen enters"""
        # Set up keyboard when screen is active
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self):
        """Called when screen is left"""
        # Cleanup animations and keyboard
        self.difficulty_selector.cleanup()
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.difficulty_selector.move_cursor('up')
        elif keycode[1] == 'down':
            self.difficulty_selector.move_cursor('down')
        elif keycode[1] == 'enter':
            self.start_game()
        return True

    def on_touch_down(self, touch):
        if not self.difficulty_selector.collide_point(touch.x, touch.y):
            return False
            
        # Calculate which option was touched
        relative_y = touch.y - self.difficulty_selector.y
        option_height = self.difficulty_selector.height / 3
        touched_index = int((self.difficulty_selector.height - relative_y) / option_height)
        
        if 0 <= touched_index < 3:
            # Update cursor position
            self.difficulty_selector.selected_index = touched_index
            self.difficulty_selector.start_cursor_animation()
            # Start game with selected difficulty
            Clock.schedule_once(lambda dt: self.start_game(), 0.1)

    def start_game(self, *args):
        app = App.get_running_app()
        new_difficulty = self.difficulty_selector.get_selected_difficulty()
        app.game.set_difficulty(new_difficulty)
        self.manager.current = 'game'

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # Create a vertical BoxLayout to manage spacing
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=50  # Increased spacing between elements
        )
        
        # Game Over text
        self.game_over_label = Label(
            text='GAME OVER!!',
            font_name='04B_19',
            font_size='80sp',
            size_hint=(1, 0.6),
            color=(0.97, 0.7, 0.47, 1)
        )
        
        # Add blinking animation
        def blink(dt):
            anim = Animation(opacity=0.5, duration=0.5) + Animation(opacity=1, duration=0.5)
            anim.start(self.game_over_label)
        Clock.schedule_interval(blink, 1.2)
        
        # Buttons layout with increased spacing
        buttons_layout = BoxLayout(
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5},
            spacing=30  # Increased spacing between buttons
        )
        
        restart_btn = ModernButton(
            text='Restart',
            font_size='24sp',
            color=(0.93, 0.81, 0.42, 1)
        )
        exit_btn = ModernButton(
            text='Main Menu',
            font_size='24sp',
            color=(0.93, 0.81, 0.42, 1)
        )
        
        restart_btn.bind(on_release=self.restart_game)
        exit_btn.bind(on_release=self.return_to_start)
        
        buttons_layout.add_widget(restart_btn)
        buttons_layout.add_widget(exit_btn)
        
        # Add widgets to content layout
        content_layout.add_widget(self.game_over_label)
        content_layout.add_widget(buttons_layout)
        
        # Add content layout to main layout
        self.layout.add_widget(content_layout)
        self.add_widget(self.layout)
        
        # Bind to window size changes for responsiveness
        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize(Window, Window.width, Window.height)

    def on_window_resize(self, window, width, height):
        """Adjust layout based on window size"""
        if width < height:
            # Portrait mode adjustments
            self.game_over_label.font_size = '60sp'
        else:
            # Landscape mode adjustments
            self.game_over_label.font_size = '80sp'

    def restart_game(self, *args):
        app = App.get_running_app()
        app.restart_game(None)  # Pass None as instance
        self.manager.current = 'game'

    def return_to_start(self, *args):
        app = App.get_running_app()
        # Reset game before returning to start
        app.game.reset_game()
        self.manager.current = 'start'

class RestartButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.background_color = (0, 0, 0, 0)
        self.font_name = 'FontAwesome'
        self.text = '\uf2f1'  # Font Awesome rotate-right icon unicode
        self.font_size = '24sp'
        self.color = (0.93, 0.77, 0.31, 1)  # Golden yellow color
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Background with golden gradient effect
            Color(0.97, 0.7, 0.47, 1)  # Lighter golden
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )
            # Add shadow effect
            Color(0.83, 0.63, 0.07, 0.2)
            RoundedRectangle(
                pos=(self.x + 2, self.y - 2),
                size=self.size,
                radius=[10]
            )

class ExitButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.background_color = (0, 0, 0, 0)
        self.font_name = 'FontAwesome'
        self.text = '\uf2d3'  # Font Awesome sign-out icon
        self.font_size = '24sp'
        self.color = (0.93, 0.77, 0.31, 1)
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.97, 0.7, 0.47, 1)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )
            Color(0.83, 0.63, 0.07, 0.2)
            RoundedRectangle(
                pos=(self.x + 2, self.y - 2),
                size=self.size,
                radius=[10]
            )

class GlassTile(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '40sp'
        self.text = ''
        self.font_name = 'Roboto'
        self.bold = True
        self.current_value = 0
        self.background_tile = None  # Store background widget reference
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        value = str(self.current_value) if self.current_value else '0'
        colors = TILE_COLORS.get(value, TILE_COLORS['0'])
        
        with self.canvas.before:
            # Draw tile background (darker shade)
            Color(*colors['bg'])
            RoundedRectangle(
                pos=(self.x, self.y),
                size=self.size,
                radius=[15]
            )
            # Draw actual tile
            Color(*colors['tile'])
            RoundedRectangle(
                pos=(self.x, self.y + 2),  # Slight offset for 3D effect
                size=self.size,
                radius=[15]
            )
        self.color = colors['text']

    def update_value(self, value):
        old_pos = self.pos[:]
        self.current_value = value
        
        if value == 0:
            self.text = ''
        else:
            self.text = str(value)
            # Scale animation for new tiles
            if not self.text:
                anim = Animation(scale=1.1, duration=0.1) + Animation(scale=1, duration=0.1)
                anim.start(self)
            # Merge animation
            elif value == self.current_value * 2:
                anim = Animation(scale=1.2, duration=0.1) + Animation(scale=1, duration=0.1)
                anim.start(self)

        # Position animation
        if self.pos != old_pos:
            anim = Animation(pos=self.pos, duration=0.15, t='in_out_quad')
            anim.start(self)
        
        self._update_canvas()

class Game2048(GridLayout):
    score = NumericProperty(0)
    best_score = NumericProperty(0)
    game_over = False
    won = False
    difficulty = 'easy'  # Add difficulty property

    @lru_cache(maxsize=None)
    def _get_tile_colors(self, value):
        """Cache tile colors for better performance"""
        value_str = str(value)
        return TILE_COLORS.get(value_str, TILE_COLORS['0'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize core properties
        self.cols = 4
        self.padding = [10]
        self.spacing = 10
        self._keyboard = None
        
        # Initialize scores
        self.scores_by_difficulty = {
            'easy': {'score': 0, 'best': 0},
            'medium': {'score': 0, 'best': 0},
            'hard': {'score': 0, 'best': 0}
        }
        self.load_best_scores()
        
        # Set up tiles
        self.tiles = [[GlassTile() for _ in range(4)] for _ in range(4)]
        for row in self.tiles:
            for tile in row:
                self.add_widget(tile)
        
        # Set up keyboard handling
        self.setup_keyboard()
        
        # Bind canvas updates
        self.bind(size=self._update_canvas, pos=self._update_canvas)
        
        # Initialize game
        self.reset_game()
        # Add garbage collection
        gc.collect()

    def setup_keyboard(self):
        """Set up keyboard bindings safely"""
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        """Handle keyboard cleanup safely"""
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def reset_game(self):
        """Improved reset logic"""
        self.game_over = False
        self.won = False
        self.score = 0
        
        # Reset current difficulty score
        if hasattr(self, 'scores_by_difficulty'):
            self.scores_by_difficulty[self.difficulty]['score'] = 0
        
        # Stop all animations and reset tiles
        for row in self.tiles:
            for tile in row:
                Animation.stop_all(tile)
                tile.opacity = 1
                tile.update_value(0)
        
        # Reset keyboard bindings
        self.setup_keyboard()
        
        # Add initial tiles with delay
        Clock.schedule_once(lambda dt: self.new_tile(), 0.1)
        Clock.schedule_once(lambda dt: self.new_tile(), 0.2)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Handle keyboard input with improved logic"""
        if self.game_over:
            return False

        key = keycode[1]
        moved = False

        # Add WASD support alongside arrow keys
        if key in ['up', 'w']:  # Up arrow or W
            moved = self.slide_up()
        elif key in ['down', 's']:  # Down arrow or S
            moved = self.slide_down()
        elif key in ['left', 'a']:  # Left arrow or A
            moved = self.slide_left()
        elif key in ['right', 'd']:  # Right arrow or D
            moved = self.slide_right()

        if moved:
            Clock.schedule_once(lambda dt: self.new_tile(), 0.2)
            Clock.schedule_once(lambda dt: self.check_game_state(), 0.3)
        elif not self._has_valid_moves():
            self.check_game_state()

        return True

    def on_enter(self):
        """Called when entering game screen"""
        self.setup_keyboard()

    def on_leave(self):
        """Called when leaving game screen"""
        self._keyboard_closed()

    def new_tile(self):
        """Add a new tile based on difficulty level"""
        empty_tiles = []
        for i in range(4):
            for j in range(4):
                if not self.tiles[i][j].text or self.tiles[i][j].text == '0':
                    empty_tiles.append((i, j))
        
        if empty_tiles:
            if self.difficulty == 'easy':
                self._add_tile_easy(empty_tiles)
            elif self.difficulty == 'medium':
                self._add_tile_medium(empty_tiles)
            else:  # hard
                self._add_tile_hard(empty_tiles)

    def _add_tile_easy(self, empty_tiles):
        """Standard 2048 tile generation (90% 2s, 10% 4s)"""
        i, j = choice(empty_tiles)
        value = 2 if randint(0, 9) < 9 else 4
        self._animate_new_tile(i, j, value)

    def _add_tile_medium(self, empty_tiles):
        """Medium difficulty: Analyzes current board state"""
        current_max = max(int(tile.text) if tile.text else 0 for row in self.tiles for tile in row)
        
        # Higher chance of 4s as game progresses
        four_probability = min(0.3, current_max / 2048)
        value = 4 if random() < four_probability else 2
        
        # Try to place tile in most challenging position
        best_pos = self._find_challenging_position(empty_tiles)
        i, j = best_pos or choice(empty_tiles)
        
        self._animate_new_tile(i, j, value)

    def _add_tile_hard(self, empty_tiles):
        """Hard difficulty: Actively tries to create difficult situations"""
        current_max = max(int(tile.text) if tile.text else 0 for row in self.tiles for tile in row)
        
        # Higher chance of 4s and occasional 8s
        rand = random()
        if rand < 0.6:  # 60% chance of 2
            value = 2
        elif rand < 0.9:  # 30% chance of 4
            value = 4
        else:  # 10% chance of 8
            value = 8
        
        # Always try to place tile in worst possible position
        best_pos = self._find_worst_position(empty_tiles)
        i, j = best_pos or choice(empty_tiles)
        
        self._animate_new_tile(i, j, value)

    def _find_challenging_position(self, empty_tiles):
        """Find a position that makes the game more challenging"""
        best_score = -1
        best_pos = None
        
        for i, j in empty_tiles:
            score = 0
            # Check adjacent tiles
            for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < 4 and 0 <= nj < 4:
                    adj_value = int(self.tiles[ni][nj].text) if self.tiles[ni][nj].text else 0
                    if adj_value > 0:
                        score += adj_value
            
            if score > best_score:
                best_score = score
                best_pos = (i, j)
                
        return best_pos

    def _find_worst_position(self, empty_tiles):
        """Find the position that makes the game most difficult"""
        best_score = -1
        best_pos = None
        
        for i, j in empty_tiles:
            score = 0
            # Check all directions
            for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < 4 and 0 <= nj < 4:
                    adj_value = int(self.tiles[ni][nj].text) if self.tiles[ni][nj].text else 0
                    if adj_value > 0:
                        # Prioritize blocking merges
                        if self._would_block_merge(i, j, adj_value):
                            score += adj_value * 2
                        score += adj_value
            
            if score > best_score:
                best_score = score
                best_pos = (i, j)
                
        return best_pos

    def _would_block_merge(self, i, j, value):
        """Check if placing a tile here would block a potential merge"""
        for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
            ni1, nj1 = i + di, j + dj
            ni2, nj2 = i - di, j - dj
            if (0 <= ni1 < 4 and 0 <= nj1 < 4 and
                0 <= ni2 < 4 and 0 <= nj2 < 4):
                val1 = int(self.tiles[ni1][nj1].text) if self.tiles[ni1][nj1].text else 0
                val2 = int(self.tiles[ni2][nj2].text) if self.tiles[ni2][nj2].text else 0
                if val1 == val2 and val1 > 0:
                    return True
        return False

    def _animate_new_tile(self, i, j, value):
        """Animate the appearance of a new tile"""
        self.tiles[i][j].update_value(value)
        self.tiles[i][j].opacity = 0
        anim = Animation(opacity=1, duration=0.2)
        anim.start(self.tiles[i][j])

    def on_keyboard(self, window, key, *args):
        # Process keyboard input only if game is not over
        if self.game_over:
            return False
        
        moved = False
        if key in [273, 82]:  # Up arrow or R
            moved = self.slide_up()
        elif key in [274]:  # Down arrow
            moved = self.slide_down()
        elif key in [276]:  # Left arrow
            moved = self.slide_left()
        elif key in [275]:  # Right arrow
            moved = self.slide_right()
        
        # Generate new tile if move was successful
        if moved:
            Clock.schedule_once(lambda dt: self.new_tile(), 0.2)
            Clock.schedule_once(lambda dt: self.check_game_state(), 0.3)
        elif not self._has_valid_moves():
            self.check_game_state()
        
        return True

    def slide_left(self):
        if self.game_over:
            return False
        
        # Store old positions
        old_positions = {(i, j): self.tiles[i][j].pos[:] for i in range(4) for j in range(4)}
        
        moved = False
        for i in range(4):
            row = [int(self.tiles[i][j].text) if self.tiles[i][j].text else 0 for j in range(4)]
            new_row = self.merge_row(row)
            if new_row != row:
                moved = True
                for j in range(4):
                    if new_row[j] != row[j]:
                        # Animate movement
                        self.tiles[i][j].pos = old_positions[(i, j)]
                        self.tiles[i][j].update_value(new_row[j])
                        
        if moved:
            Clock.schedule_once(lambda dt: self.new_tile(), 0.2)
            Clock.schedule_once(lambda dt: self.check_game_state(), 0.3)
        elif not self._has_valid_moves():
            self.check_game_state()
        return moved

    def slide_right(self):
        if self.game_over:
            return False
        
        # Store old positions
        old_positions = {(i, j): self.tiles[i][j].pos[:] for i in range(4) for j in range(4)}
        
        moved = False
        for i in range(4):
            row = [int(self.tiles[i][j].text) if self.tiles[i][j].text else 0 for j in range(4)]
            row.reverse()
            new_row = self.merge_row(row)
            new_row.reverse()
            if new_row != row[::-1]:
                moved = True
                for j in range(4):
                    if new_row[j] != row[::-1][j]:
                        # Animate movement
                        self.tiles[i][j].pos = old_positions[(i, j)]
                        self.tiles[i][j].update_value(new_row[j])
                        
        if moved:
            Clock.schedule_once(lambda dt: self.new_tile(), 0.2)
            Clock.schedule_once(lambda dt: self.check_game_state(), 0.3)
        elif not self._has_valid_moves():
            self.check_game_state()
        return moved

    def slide_up(self):
        if self.game_over:
            return False
        
        # Store old positions
        old_positions = {(i, j): self.tiles[i][j].pos[:] for i in range(4) for j in range(4)}
        
        moved = False
        for j in range(4):
            column = [int(self.tiles[i][j].text) if self.tiles[i][j].text else 0 for i in range(4)]
            new_column = self.merge_row(column)
            if new_column != column:
                moved = True
                for i in range(4):
                    if new_column[i] != column[i]:
                        # Animate movement
                        self.tiles[i][j].pos = old_positions[(i, j)]
                        self.tiles[i][j].update_value(new_column[i])
                        
        if moved:
            Clock.schedule_once(lambda dt: self.new_tile(), 0.2)
            Clock.schedule_once(lambda dt: self.check_game_state(), 0.3)
        elif not self._has_valid_moves():
            self.check_game_state()
        return moved

    def slide_down(self):
        if self.game_over:
            return False
        
        # Store old positions
        old_positions = {(i, j): self.tiles[i][j].pos[:] for i in range(4) for j in range(4)}
        
        moved = False
        for j in range(4):
            column = [int(self.tiles[i][j].text) if self.tiles[i][j].text else 0 for i in range(4)]
            column.reverse()
            new_column = self.merge_row(column)
            new_column.reverse()
            if new_column != column[::-1]:
                moved = True
                for i in range(4):
                    if new_column[i] != column[::-1][i]:
                        # Animate movement
                        self.tiles[i][j].pos = old_positions[(i, j)]
                        self.tiles[i][j].update_value(new_column[i])
                        
        if moved:
            Clock.schedule_once(lambda dt: self.new_tile(), 0.2)
            Clock.schedule_once(lambda dt: self.check_game_state(), 0.3)
        elif not self._has_valid_moves():
            self.check_game_state()
        return moved

    def merge_row(self, row):
        # Remove zeros
        row = [x for x in row if x != 0]
        # Merge
        points_earned = 0
        for i in range(len(row)-1):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                points_earned += row[i]  # Add points for the merge
                row[i+1] = 0
        
        # Update score immediately
        if points_earned > 0:
            self.update_score(points_earned)
        
        # Remove zeros again
        row = [x for x in row if x != 0]
        # Add zeros at the end
        while len(row) < 4:
            row.append(0)
        return row

    def check_game_state(self):
        """Check if game is over or won"""
        # First check if no more moves are possible
        if not any(self.tiles[i][j].text == '' for i in range(4) for j in range(4)):
            # Board is full, check for possible merges
            if not self._has_valid_moves():
                self.game_over = True
                Clock.schedule_once(lambda dt: self.show_game_over(), 0.1)
                return

        # Check for 2048 tile
        for row in self.tiles:
            for tile in row:
                if tile.text == '2048' and not self.won:
                    self.won = True
                    self.show_win_message()

    def _has_valid_moves(self):
        """Helper method to check if any valid moves remain"""
        # Check horizontal merges
        for i in range(4):
            for j in range(3):
                if self.tiles[i][j].text and self.tiles[i][j].text == self.tiles[i][j+1].text:
                    return True

        # Check vertical merges
        for i in range(3):
            for j in range(4):
                if self.tiles[i][j].text and self.tiles[i][j].text == self.tiles[i+1][j].text:
                    return True

        return False

    def show_win_message(self):
        # Implement win message popup
        pass

    def show_game_over(self):
        """Show game over screen"""
        if self.game_over:
            app = App.get_running_app()
            if app.root:
                app.root.current = 'gameover'

    def on_touch_up(self, touch):
        if abs(touch.dx) > abs(touch.dy):
            if touch.dx > 0:
                self.slide_right()
            else:
                self.slide_left()
        else:
            if touch.dy > 0:
                self.slide_up()
            else:
                self.slide_down()
        self.new_tile()

    def update_score(self, points):
        """Update score with difficulty tracking"""
        self.score += points
        self.scores_by_difficulty[self.difficulty]['score'] = self.score
        if self.score > self.scores_by_difficulty[self.difficulty]['best']:
            self.scores_by_difficulty[self.difficulty]['best'] = self.score
            self.best_score = self.score
            self.save_scores()

    def load_best_score(self):
        best_score_path = os.path.join(BASE_DIR, 'best_score.json')
        try:
            with open(best_score_path, 'r') as f:
                self.best_score = json.load(f)['best_score']
        except:
            self.best_score = 0

    def save_best_score(self):
        best_score_path = os.path.join(BASE_DIR, 'best_score.json')
        try:
            with open(best_score_path, 'w') as f:
                json.dump({'best_score': self.best_score}, f)
        except Exception as e:
            print(f"Error saving best score: {e}")

    def load_best_scores(self):
        """Load best scores for all difficulties"""
        scores_path = os.path.join(BASE_DIR, 'scores.json')
        try:
            with open(scores_path, 'r') as f:
                self.scores_by_difficulty = json.load(f)
        except:
            # Keep default values if file doesn't exist
            pass
        
        # Set current scores based on difficulty
        self.score = self.scores_by_difficulty[self.difficulty]['score']
        self.best_score = self.scores_by_difficulty[self.difficulty]['best']

    def save_scores(self):
        """Save scores for all difficulties"""
        # Update current difficulty scores
        self.scores_by_difficulty[self.difficulty]['score'] = self.score
        if self.score > self.scores_by_difficulty[self.difficulty]['best']:
            self.scores_by_difficulty[self.difficulty]['best'] = self.score
        
        scores_path = os.path.join(BASE_DIR, 'scores.json')
        try:
            with open(scores_path, 'w') as f:
                json.dump(self.scores_by_difficulty, f)
        except Exception as e:
            print(f"Error saving scores: {e}")

    def set_difficulty(self, difficulty):
        """Change difficulty and load appropriate scores"""
        self.difficulty = difficulty
        self.score = self.scores_by_difficulty[difficulty]['score']
        self.best_score = self.scores_by_difficulty[difficulty]['best']
        self.reset_game()

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 0.1)  # Darker background for better contrast
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = (0.2, 0.2, 0.2, 1)
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Draw shadow
            Color(0.15, 0.15, 0.15, 0.2)
            RoundedRectangle(
                pos=(self.x + 2, self.y - 2),
                size=self.size,
                radius=[10]
            )
            # Draw main button
            Color(0.25, 0.25, 0.25, 0.2)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Create screens
        start_screen = StartScreen(name='start')
        game_screen = Screen(name='game')
        game_over_screen = GameOverScreen(name='gameover')
        
        # Create game layout
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header with scores and buttons
        header = BoxLayout(size_hint_y=0.15, spacing=10)
        
        # Score boxes in a layout that takes most of the width
        scores_layout = BoxLayout(size_hint_x=0.8)
        score_box = BoxLayout(orientation='vertical')
        score_label = Label(text='Score', font_size=20, color=(0.2, 0.2, 0.2, 1))
        self.score_value = Label(text='0', font_size=24, color=(0.2, 0.2, 0.2, 1))
        score_box.add_widget(score_label)
        score_box.add_widget(self.score_value)
        
        best_box = BoxLayout(orientation='vertical')
        best_label = Label(text='Best', font_size=20, color=(0.2, 0.2, 0.2, 1))
        self.best_value = Label(text='0', font_size=24, color=(0.2, 0.2, 0.2, 1))
        best_box.add_widget(best_label)
        best_box.add_widget(self.best_value)
        
        scores_layout.add_widget(score_box)
        scores_layout.add_widget(best_box)
        
        # Buttons layout with fixed width and right alignment
        buttons_layout = BoxLayout(
            size_hint_x=None, 
            width=120,  # Fixed width for two 50px buttons + spacing
            spacing=10,
            padding=[0, 0, 10, 0]  # Right padding for edge spacing
        )
        
        # Exit and Restart buttons
        exit_btn = ExitButton()
        restart_btn = RestartButton()
        
        exit_btn.bind(on_release=self.return_to_start)
        restart_btn.bind(on_release=self.restart_game)
        
        buttons_layout.add_widget(exit_btn)
        buttons_layout.add_widget(restart_btn)
        
        # Add layouts to header with proper alignment
        header.add_widget(scores_layout)
        header.add_widget(buttons_layout)
        
        # Game grid
        self.game = Game2048()  # Make game instance accessible to the app
        
        root.add_widget(header)
        root.add_widget(self.game)
        
        # Bind score updates
        self.game.bind(score=self.update_scores)
        self.game.bind(best_score=self.update_scores)
        
        game_screen.add_widget(root)
        
        # Add screens to manager
        sm.add_widget(start_screen)
        sm.add_widget(game_screen)
        sm.add_widget(game_over_screen)
        
        # Store screen manager reference
        self.sm = sm
        return sm

    def return_to_start(self, instance):
        """Improved return to start logic"""
        self.game.save_scores()  # Save current scores
        self.root.current = 'start'

    def restart_game(self, instance):
        """Improved restart logic"""
        self.game.reset_game()
        # Update score displays
        self.update_scores()

    def update_scores(self, *args):
        """Update score displays"""
        self.score_value.text = str(self.game.score)
        self.best_value.text = str(self.game.scores_by_difficulty[self.game.difficulty]['best'])

    def handle_game_over(self):
        """New method to handle game over state"""
        if self.game.game_over:
            # Add slight delay before showing game over screen
            Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'gameover'), 0.5)

    # Add new feature: Save/load game state
    def save_game_state(self):
        """Save current game state"""
        state = {
            'score': self.game.score,
            'best_score': self.game.best_score,
            'difficulty': self.game.difficulty,
            'board': [[tile.text for tile in row] for row in self.game.tiles]
        }
        state_path = os.path.join(BASE_DIR, 'game_state.json')
        try:
            with open(state_path, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            print(f"Error saving game state: {e}")

    def load_game_state(self):
        """Load saved game state"""
        state_path = os.path.join(BASE_DIR, 'game_state.json')
        try:
            with open(state_path, 'r') as f:
                state = json.load(f)
                self.game.score = state['score']
                self.game.best_score = state['best_score']
                self.game.difficulty = state['difficulty']
                for i, row in enumerate(state['board']):
                    for j, value in enumerate(row):
                        self.game.tiles[i][j].update_value(int(value) if value else 0)
        except:
            # Start new game if no saved state
            self.game.reset_game()

    # Add auto-save feature
    def on_stop(self):
        """Save game state when app closes"""
        self.save_game_state()
        self.game.save_scores()

if __name__ == "__main__":
    GameApp().run()
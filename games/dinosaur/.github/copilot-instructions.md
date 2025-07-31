# 🦕 Dinosaur Game - AI Coding Agent Instructions

## Architecture Overview

This is a modular pygame-based dinosaur jumping game with 4 difficulty levels and advanced features. The game follows a **centralized configuration** pattern where all settings are defined in `config/game_config.py` and imported by components.

### Core Components

- **`main.py`**: Entry point with async TTS initialization and Chinese documentation
- **`src/game_engine.py`**: Central game coordinator managing state transitions (MENU → PLAYING → GAME_OVER)
- **`src/menu_system.py`**: Standalone menu with dynamic screen adaptation and difficulty preview
- **`src/dinosaur.py`**: Player character with shield/double-jump abilities and physics scaling
- **`src/obstacles.py`**: Advanced obstacle system with 8+ types (invisible, explosive, splitting)
- **`src/sound_manager.py`**: Dual audio system - procedural "popcat" sounds + YouTube background music
- **`src/text_to_speech.py`**: Async TTS with Windows SAPI fallback to pyttsx3

## Critical Patterns

### Configuration-Driven Design

```python
# All settings centralized in config/game_config.py
from config.game_config import DIFFICULTY_SETTINGS, Physics, SoundSystem
# Components dynamically adjust to difficulty via DIFFICULTY_SETTINGS[difficulty_level]
```

### Dynamic Screen Adaptation

- **Fullscreen toggle**: F11 dynamically recalculates all UI proportions and font sizes
- **Responsive layout**: All positions use percentage-based calculations (`screen_height * 0.3`)
- **Font rescaling**: `setup_fonts()` called after resolution changes

### State Management Pattern

```python
# Three-state game loop in game_engine.py
if self.game_state == GameState.MENU:
    self.menu_system.draw(screen)
elif self.game_state == GameState.PLAYING:
    self.update_gameplay()
# ESC always returns to MENU (never exits directly)
```

### Nightmare Mode Effects

Special difficulty with unique mechanics:

- **Gravity reversal**: `is_gravity_reversed` flag affects physics
- **Screen flicker**: 3 modes (full, edge, stripe) in `apply_screen_flicker()`
- **Control inversion**: Nightmare mode can invert jump controls

## Key Integration Points

### Sound System Architecture

- **Popcat sounds**: Procedural generation using pygame.mixer with frequency/duration configs
- **Background music**: YouTube-dl integration with fallback audio files in `assets/music/`
- **Audio toggle**: F1/F2 keys control separate sound/music systems

### Persistence Layer

- **High scores**: JSON file with versioning (`high_score.json`)
- **Settings**: Game remembers sound preferences and difficulty selection

### TTS Integration

- **Async speech**: Uses ThreadPoolExecutor with priority queue for non-blocking announcements
- **Fallback hierarchy**: Windows SAPI → pyttsx3 → silent mode

## Development Workflows

### Running the Game

```bash
# Install core dependency
pip install pygame

# Optional TTS support
pip install pyttsx3 pywin32  # Windows
```

### Debug Mode Features

- Console logs show menu loading, difficulty selection, and TTS availability
- Physics values print to console during Nightmare mode gravity flips
- Sound system reports initialization status and fallback usage

### Testing Different Difficulties

Navigate menu with ↑↓ keys. Each difficulty has distinct:

- Speed multipliers and obstacle spawn rates (defined in `DIFFICULTY_SETTINGS`)
- Special effects (Nightmare = gravity flip + screen effects)
- Scoring multipliers

## File Structure Conventions

```
src/           # All game logic (no pygame.init in modules)
config/        # Centralized settings (imported by all modules)
assets/music/  # Audio files with fallback naming pattern
main.py        # Only file that calls pygame.init()
```

### Module Import Pattern

```python
# Always add src to path in main.py before imports
sys.path.insert(0, os.path.join(current_dir, "src"))
from game_engine import Game  # Then import game modules
```

## Critical Debugging Notes

- **TTS errors**: Non-blocking; game continues if speech fails
- **Fullscreen issues**: Font re-initialization required after resolution change
- **Nightmare mode**: Effects are intentionally disorienting (not bugs)
- **Sound fallbacks**: Multiple audio file formats for compatibility

## Common Modification Patterns

1. **New difficulty**: Add to `DIFFICULTY_SETTINGS` in config, automatically appears in menu
2. **New obstacle type**: Extend `Obstacle.setup_obstacle()` method with new behavior
3. **UI scaling**: Use percentage-based positioning and call `update_screen_size()` after changes
4. **Audio**: Add new sound types in `SoundSystem` config class, implement in `sound_manager.py`

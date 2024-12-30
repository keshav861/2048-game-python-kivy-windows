# 2048 Game

A modern implementation of the classic 2048 puzzle game built with Python and Kivy framework. Features multiple difficulty levels, smooth animations, and a sleek user interface.

## Features

- 🎮 Three difficulty levels (Easy, Medium, Hard)
- 🎯 Smooth tile animations
- 💾 Auto-save functionality
- 🏆 High score tracking per difficulty
- 🖥️ Cross-platform compatibility
- 📱 Touch and keyboard controls

## ⭐ Star the Project

If you find this project useful or interesting, please consider giving it a star! Your support helps make this project more visible to others who might benefit from it.

```bash
# Click the ⭐ Star button at the top right of the repository page
```

Stars motivate me to:
- 🚀 Add new features
- 🐛 Fix bugs faster
- 📝 Improve documentation
- 🤝 Respond to issues promptly

## Prerequisites

Before running the game, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/keshav861/2048-game-python-kivy-windows.git
cd 2048
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Ensure you're in the game directory and your virtual environment is activated
2. Run the game:
```bash
python src/main.py
```

## How to Play

### Controls
- **Arrow Keys** or **WASD**: Move tiles
- **R**: Restart game
- **ESC**: Return to main menu

### Game Rules
1. Use arrow keys or WASD to move tiles in any direction
2. When two tiles with the same number collide, they merge into one tile with their sum
3. After each move, a new tile appears (2 or 4)
4. Goal: Create a tile with the number 2048

### Difficulty Levels
- **Easy**: Standard 2048 rules
- **Medium**: More challenging tile placement
- **Hard**: Strategic tile placement and higher value tiles

## Project Structure
```
2048/
├── src/
│   └── main.py
├── assets/
│   └── fonts/
├── requirements.txt
├── readme-git.md
├── LICENSE
└── .gitignore
```

## Development

### Setting Up Development Environment
```bash
pip install -r requirements.txt
```

### Code Style
This project follows PEP 8 guidelines. You can format the code using:
```bash
black src/
```

## Troubleshooting

### Common Issues
1. **ModuleNotFoundError: No module named 'kivy'**
   - Ensure you've installed all requirements
   - Verify your virtual environment is activated

2. **Font loading errors**
   - Check that all font files are present in the assets/fonts directory

### Platform-Specific Notes

#### Windows
- If you encounter DLL errors, ensure you have the latest Visual C++ redistributable installed

#### Linux
- Install additional dependencies:
```bash
sudo apt-get install python3-kivy
```

#### MacOS
- Install additional dependencies:
```bash
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/new-feature
```
3. Commit your changes:
```bash
git commit -m 'Add new feature'
```
4. Push to the branch:
```bash
git push origin feature/new-feature
```
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original 2048 game created by Gabriele Cirulli
- Kivy framework developers
- Font Awesome for icons
- 04B_19 font by 04

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Look through existing issues
3. Create a new issue with detailed information about your problem

---
Happy Gaming! 🎮

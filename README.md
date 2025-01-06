# Cryptis - Game Code Documentation

## **main.py**

This file contains the main logic of the game **Cryptis**, including the main menu, game modes, and transition management.

### **Features**:
- **Main Menu**: Allows the user to start a new game, view credits, or quit.
- **Choose Word**: Input a word to encrypt.
- **Difficulty Selection**: Choose between easy or hard game modes.
- **Game Initialization**: Includes background music, assets, and main loop.

---

## **game.py**

Handles the game logic for **easy** and **hard** difficulty modes.

### **Functions**:
1. **extract_numbers**: Converts a string of encrypted text into numerical values.
2. **Victoire**: Displays the victory screen.
3. **game_easy**: Implements the easy game logic with an 8x14 grid.
4. **game_hard**: Implements the hard game logic with an 8x14 grid.

---

## **crypto.py**

Provides cryptographic operations for encoding and encryption in the game.

### **Features**:
- **generate_ternary_table**: Creates a ternary representation for the alphabet.
- **mot_to_ternaire**: Converts words into their ternary representation.
- **apply_noise_to_key**: Adds noise or transforms the encryption key.
- **apply_bayesian_encoding**: Encodes a key using a Bayesian Network.

---

## **config.py**

Stores the configuration variables for the game.

### **Key Configurations**:
- **Screen dimensions**: `SCREEN_WIDTH = 1280`, `SCREEN_HEIGHT = 720`
- **Colors**: `WHITE`, `BLACK`, `LIGHT_BLUE`, `DARK_BLUE`
- **Grid size**: `GRID_WIDTH = 8`, `GRID_HEIGHT = 8`

---

## **ui.py**

Defines UI components, such as buttons and input boxes.

### **Features**:
- **Button**: A clickable button with hover effects.
- **draw_input_box**: Draws and manages input boxes for user interaction.

---

## **Assets and Dependencies**

### **Required Libraries**:
- `pygame`: For game development and rendering.
- `pgmpy`: For Bayesian Network-based encoding.
- `numpy`: For numerical computations.

### **Asset Folders**:
- **Images**: `cryptis/assets/images` (background and sprite images).
- **Sound**: `cryptis/assets/sound` (background music and sound effects).
- **Fonts**: `cryptis/assets/fonts` (custom fonts for the game).

---

## **How to Run**

1. **Install dependencies**: 
   ```bash
   pip install pygame numpy pgmpy

2. **Place all files in the same directory, maintaining the asset folder structure**

3. **Execute the main.py file**

    ```bash
    python main.py

## **Credits**

 **Development**:
  - Anthony BUFFET

**Art and Graphics**:
  - Anthony BUFFET
    
## **Notes**

- This game uses a combination of Bayesian encoding and ternary transformations for its encryption logic.

- The game_easy and game_hard modes are grid-based puzzles with specific win conditions.

- Customize the music, fonts, and visuals by replacing the assets in the respective folders.

- This game is inspired by the Cryptris game projet.

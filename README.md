# Raumschach
a 3d chess game build in python with pygame

<img src="images/screenshot.png">

### Requirements
- Python 3.12
- venv installed
- 
## Installation


```bash
  git clone repogit@github.com:falsanu/raumschach.git
  cd raumschach
  python3.12 -m venv venv
  source venv/bin/activate
  pip install -r ./requirements.txt
```

## Run 
```bash
python3 raumschach.py
```

# Usage
- use mouse to rotate board

## Controls 
  - W - forward
  - A - left
  - S -  down
  - D - right
  - E - level up
  - Q - level down
  - SPACE - Select figure
  - SPACE again - Place figure
  - ESC unselect everything
  - CTRL-Q to quit

## Views
  - TAB - to toggle opponents view
  - 1 - FRONT (0°)
  - 2 - RIGHT (90°)
  - 3 - BACK (180°)
  - 4 - LEFT (270°)
  

# Todo:

Choose wisely:
- [ ] make only possible clickable!
- [ ] show some stats

## Done:

- [x] generate 3d projection
- [x] generate board
- [x] display possible fields
- [x] create figures 
  - [x] Pawn
  - [x] King
  - [x] Queen
  - [x] Bishop
  - [x] Knight
- [x] select single field
- [x] create inital setup
- [x] make moves
- [x] set Default screens
- [x] create Teams
- [x] hit opponents figures

  

 ### Contributions
 very welcome!!!

### 
done @39C3 with Beer + Tschunk and [@jonaspews](https://github.com/jonaspews)

 ### LICENSE 
 MIT 2026
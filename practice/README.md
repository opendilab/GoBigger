## Practice
We offer multiple gameplay modes for players to enjoy, including development, battle (Bot and AI) and spectator mode. Our platform supports both single-player and two-player matches. Welcome to explore and enjoy the experience.

### Download Weight
```bash
wget https://opendilab.net/download/GoBigger/solo_agent.pth.tar
wget https://opendilab.net/download/GoBigger/team.pth.tar
```
### Quick Start

#### Installation
```bash
git clone https://github.com/opendilab/GoBigger.git
pip install -e .
```

#### Usage
```bash
python battle.py --mode single --map farm  # Single-player development
python battle.py --mode single --map vsbot # Single-player vs. Bot
python battle.py --mode single --map vsai  # Single-player vs. Single-AI
python battle.py --mode team   --map farm  # Two-player development
python battle.py --mode team   --map vsbot # Two-player vs. Bot
python battle.py --mode team   --map vsai  # Two-player vs. Team-AI
python battle.py --mode watch              # Spectator mode: Team-AI vs. Team-AI
```

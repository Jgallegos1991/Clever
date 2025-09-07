#!/bin/bash
# Clever Evolution Demo - Shows autonomous learning in action

echo "🌟 Clever AI Evolution Engine Demo"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "🔧 Setting up environment..."
    make setup-full
fi

# Activate virtual environment
source .venv/bin/activate

echo "🧠 Initializing Clever's Evolution Engine..."
python3 -c "
from evolution_engine import get_evolution_engine
from database import db_manager

try:
    # Initialize evolution engine
    engine = get_evolution_engine()
    print('✅ Evolution engine initialized')
    
    # Check initial status
    status = engine.get_evolution_status()
    print(f'📊 Initial Evolution Score: {status[\"evolution_score\"]:.1%}')
    print(f'🔗 Concepts: {status[\"concept_count\"]}')
    print(f'⚡ Connections: {status[\"connection_count\"]}')
    
except Exception as e:
    print(f'❌ Initialization error: {e}')
"

echo ""
echo "🎯 Demo Instructions:"
echo "===================="
echo ""
echo "1. 📂 Drop PDFs into your Google Drive sync folder:"
echo "   ~/GoogleDrive/CLEVER_AI/clever_sync/"
echo ""
echo "2. 💬 Chat with Clever - each interaction teaches her:"
echo "   http://localhost:5000"
echo ""
echo "3. 📈 Watch her evolution in real-time:"
echo "   - Evolution visualizer (bottom-right corner)"
echo "   - make evolution-status (command line)"
echo ""
echo "4. 🧠 Trigger manual learning:"
echo "   - make evolution-learn (process all files)"
echo "   - make trigger-evolution (force cascade)"
echo ""

echo "🚀 Starting Clever AI with Evolution Engine..."
echo "Open http://localhost:5000 to begin the demo!"
echo ""
echo "Watch for these evolution events:"
echo "- 🔮 Concept discovery from your PDFs"
echo "- ⚡ Connection formation between ideas"
echo "- 📈 Capability growth with each interaction"
echo "- ✨ Evolution cascades when learning thresholds are met"
echo ""

# Start the application
make run

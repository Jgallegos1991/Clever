# Clever Memory Management System

## 🧠 Overview

The Clever Memory Management System provides comprehensive memory optimization for development on Chromebook environments with limited RAM. This system ensures stable operation of VS Code, Pylance, Flask, and all Clever components without crashes or extension restarts.

## 🚨 Emergency Situation Resolution

**If VS Code is restarting or crashing:**

```bash
# Immediate emergency optimization
make memory-emergency

# Check current status
make memory-status

# Start continuous monitoring
make memory-monitor
```

## 📊 Memory Thresholds

- **Critical (< 250MB)**: Emergency intervention - aggressive cleanup
- **Warning (250-400MB)**: Preventive optimization - moderate cleanup  
- **Moderate (400-600MB)**: Gentle optimization - minimal cleanup
- **Optimal (> 600MB)**: Normal operation - no intervention needed

## 🛠 Available Commands

### `make memory-status`
Shows current memory situation and optimization history:
```bash
🧠 CLEVER MEMORY MANAGER STATUS
Available Memory: 920MB
Pressure Level: normal
Monitoring Active: False
Total Optimizations: 3
```

### `make memory-optimize` 
Applies appropriate optimization based on current memory pressure:
```bash
🔧 Optimizing Clever memory usage...
💚 Applying gentle memory optimizations...
✅ Optimization complete: 4 actions applied
```

### `make memory-monitor`
Starts continuous background monitoring (checks every 30 seconds):
```bash
🔍 Starting continuous memory monitoring...
💾 920MB available | Pressure: normal
💾 845MB available | Pressure: normal
⚠️  387MB available | Pressure: warning
🟡 Applying preventive memory optimizations...
```

### `make memory-emergency`
Applies aggressive emergency optimization:
```bash
🚨 EMERGENCY: Applying aggressive memory optimization...
🔴 Applying EMERGENCY memory optimizations!
- Pylance restarted
- Non-essential processes killed
- Aggressive system cache clear
✅ Emergency optimization complete: 8 actions applied
```

## 🔧 Optimization Strategies

### Gentle Optimization (600-400MB available)
- Clear Python bytecode cache (`__pycache__` directories)
- Python garbage collection
- VS Code settings optimization
- Clear temporary files

### Preventive Optimization (400-250MB available)  
- All gentle optimizations +
- System page cache clearing
- Chrome renderer restart
- VS Code workspace optimization
- Pylance memory limits

### Emergency Optimization (< 250MB available)
- All preventive optimizations +
- Kill and restart Pylance processes
- Kill non-essential Python processes (preserves Flask)
- Aggressive system cache clearing
- Force VS Code emergency settings

## ⚙️ VS Code Optimization Profiles

The system automatically applies different VS Code settings based on available memory:

### Emergency Profile (< 300MB)
```json
{
  "python.analysis.memory.keepLibraryAst": false,
  "python.analysis.indexing": false,
  "python.analysis.autoImportCompletions": false,
  "editor.minimap.enabled": false,
  "breadcrumbs.enabled": false
}
```

### Conservative Profile (300-500MB)
```json
{
  "python.analysis.memory.keepLibraryAst": false,
  "python.analysis.autoImportCompletions": true,
  "editor.minimap.enabled": true,
  "python.analysis.diagnosticSeverityOverrides": {
    "reportUnusedVariable": "warning"
  }
}
```

### Balanced Profile (> 500MB)
```json
{
  "python.analysis.memory.keepLibraryLocalVariables": true,
  "python.analysis.indexing": true,
  "python.analysis.autoImportCompletions": true,
  "editor.hover.delay": 500
}
```

## 🔍 Monitoring Integration

### Automatic Monitoring
The system can run continuous monitoring that:
- Checks memory every 30 seconds
- Applies optimizations when thresholds are crossed
- Prevents too-frequent optimization cycles (5 minute minimum between optimizations)
- Logs all optimization events for analysis

### Manual Monitoring
```bash
# Check memory anytime
free -m

# Get detailed Clever memory status  
make memory-status

# Run optimization if needed
make memory-optimize
```

## 📁 System Files

- **`clever_memory_manager.py`**: Main memory management system
- **`emergency_memory_stabilizer.py`**: Emergency intervention system  
- **`vscode_memory_optimizer.py`**: VS Code specific optimization
- **`development_environment_optimizer.py`**: Comprehensive dev tool optimization

## 🎯 Integration with Clever

### Database Integration
Memory optimization events are logged to Clever's database for learning and analysis:
```python
{
  'timestamp': '2024-01-15T10:30:00',
  'pressure_level': 'warning',
  'intervention': 'preventive', 
  'actions': ['VS Code optimized', 'Caches cleared'],
  'memory_before': 387,
  'memory_after': 542
}
```

### Cognitive Sovereignty Integration
Clever learns from memory optimization patterns to:
- Predict memory pressure before it occurs
- Optimize development workflows proactively
- Adapt optimization strategies based on usage patterns
- Provide intelligent memory management suggestions

## 🚀 Best Practices

### Development Workflow
1. Start development with `make memory-status`
2. Run `make memory-optimize` if pressure is detected
3. Use `make memory-monitor` during intensive development sessions
4. Keep emergency command ready: `make memory-emergency`

### Prevention Strategies  
- Close unnecessary browser tabs
- Restart VS Code periodically (once per day)
- Use `make memory-optimize` before starting intensive tasks
- Monitor memory during large file operations

### Emergency Response
If VS Code crashes or restarts:
1. **Immediate**: `make memory-emergency`
2. **Verify**: `make memory-status` 
3. **Monitor**: `make memory-monitor` for 5 minutes
4. **Restart VS Code** once memory is stable

## 🔗 Quick Reference

```bash
# Emergency situation
make memory-emergency && make memory-status

# Regular maintenance  
make memory-optimize

# Continuous monitoring
make memory-monitor

# Check current status
make memory-status
```

## 🧠 Technical Details

The memory management system uses several techniques:

1. **Real-time Memory Monitoring**: Continuous tracking of system and process memory usage
2. **Adaptive Thresholds**: Different intervention levels based on memory pressure  
3. **Process-Aware Optimization**: Identifies and optimizes specific development tools
4. **Configuration Management**: Dynamic VS Code and tool configuration based on available memory
5. **Emergency Intervention**: Aggressive cleanup when critical thresholds are reached
6. **Learning Integration**: Feeds optimization events into Clever's learning system

This ensures that Clever's development environment remains stable and performant even on memory-constrained devices like the Chromebook.
#!/usr/bin/env python3
"""
Clever Shape Generation Demo & Test Suite

Why: Demonstrates Clever's mathematical shape generation capabilities and validates
     the complete shape formation system for cognitive enhancement
Where: Standalone demo script showcasing geometric visualization features
How: Generates various mathematical shapes and displays their properties

Connects to:
    - shape_generator.py: Core mathematical shape generation engine
    - app.py: API endpoint testing for shape generation
    - persona.py: Integration with chat-based shape commands
"""

import json
import time
from shape_generator import get_shape_generator

# Try to import requests for API testing
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def test_shape_generator():
    """Test the ShapeGenerator module directly"""
    print("🔮 Testing Clever's Mathematical Shape Generation System")
    print("=" * 60)
    
    shape_gen = get_shape_generator()
    
    # Test basic shapes
    test_shapes = [
        ("triangle", {"sides": 3}),
        ("pentagon", {"sides": 5}),
        ("circle", {"radius": 100}),
        ("spiral", {"type": "fibonacci", "turns": 2.5}),
        ("fractal", {"iterations": 3})
    ]
    
    for shape_name, kwargs in test_shapes:
        print(f"\n📐 Generating {shape_name}...")
        try:
            shape = shape_gen.create_shape(shape_name, **kwargs)
            info = shape_gen.get_shape_info(shape)
            
            print(f"   ✅ {shape.name}")
            print(f"   📊 Points: {len(shape.points)}")
            print(f"   📏 Center: ({shape.center[0]:.1f}, {shape.center[1]:.1f})")
            
            if 'area' in shape.properties:
                print(f"   📐 Area: {shape.properties['area']:.2f}")
            if 'perimeter' in shape.properties:
                print(f"   📏 Perimeter: {shape.properties['perimeter']:.2f}")
            if 'fractal_dimension' in shape.properties:
                print(f"   🌀 Fractal Dimension: {shape.properties['fractal_dimension']:.3f}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_api_endpoints():
    """Test the API endpoints"""
    if not HAS_REQUESTS:
        print("\n⚠️  requests module not available - skipping API tests")
        return
        
    print("\n🌐 Testing Shape Generation API Endpoints")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test available shapes
    print("\n📚 Testing /api/available_shapes...")
    try:
        response = requests.get(f"{base_url}/api/available_shapes")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data['total_shapes']} available shapes")
            for category, shapes in data['categories'].items():
                print(f"   📂 {category}: {list(shapes.keys())}")
        else:
            print(f"   ❌ API Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Test shape generation
    print(f"\n🔮 Testing /api/generate_shape...")
    test_requests = [
        {"shape": "hexagon", "size": 120},
        {"shape": "spiral", "type": "fibonacci", "turns": 3},
        {"shape": "fractal", "iterations": 2}
    ]
    
    for req_data in test_requests:
        try:
            response = requests.post(f"{base_url}/api/generate_shape", json=req_data)
            if response.status_code == 200:
                data = response.json()
                shape = data['shape']
                print(f"   ✅ Generated {shape['name']} with {shape['point_count']} points")
            else:
                print(f"   ❌ API Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")

def showcase_mathematical_beauty():
    """Showcase the mathematical beauty of generated shapes"""
    print("\n✨ Mathematical Beauty Showcase")
    print("=" * 60)
    
    shape_gen = get_shape_generator()
    
    # Golden ratio spiral
    print("\n🌀 Golden Ratio Fibonacci Spiral")
    spiral = shape_gen.create_shape("spiral", type="fibonacci", turns=3, size=150)
    print(f"   Nature's perfect spiral with {len(spiral.points)} calculated points")
    print(f"   Mathematical elegance in {spiral.properties['turns']} turns")
    
    # Perfect hexagon
    print("\n⬡ Perfect Hexagon (Nature's Favorite)")
    hexagon = shape_gen.create_shape("hexagon", size=100)  
    print(f"   Six-fold symmetry with {hexagon.properties['interior_angle']}° angles")
    print(f"   Area: {hexagon.properties['area']:.2f} square units")
    
    # Koch snowflake fractal
    print("\n❄️ Koch Snowflake Fractal")
    fractal = shape_gen.create_shape("fractal", iterations=3, size=80)
    print(f"   Infinite perimeter, finite area paradox")
    print(f"   Fractal dimension: {fractal.properties['fractal_dimension']:.4f}")
    print(f"   Generated with {len(fractal.points)} recursive points")

def main():
    """Run the complete demo"""
    print("🧠 CLEVER'S MATHEMATICAL SHAPE GENERATION DEMO")
    print("Digital Brain Extension - Geometric Cognition System")
    print("=" * 60)
    
    # Test core functionality
    test_shape_generator()
    
    # Test API if available
    try:
        test_api_endpoints()
    except:
        print("\n⚠️  Server not running - skipping API tests")
        print("   Run 'make run' to start Clever and test API endpoints")
    
    # Showcase mathematical beauty
    showcase_mathematical_beauty()
    
    print("\n🎯 Demo Complete!")
    print("\nTry these commands in Clever's chat:")
    print("   • 'form a triangle'")
    print("   • 'create a fibonacci spiral'") 
    print("   • 'show me a fractal'")
    print("   • 'generate a perfect hexagon'")
    print("\nOr use the console functions:")
    print("   • generateShape('pentagon', {size: 150})")
    print("   • getAvailableShapes()")
    
    print(f"\n✨ Clever's cognitive enhancement through mathematical beauty! ✨")

if __name__ == "__main__":
    main()
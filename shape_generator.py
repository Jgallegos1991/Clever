"""
Clever's Mathematical Shape Generation Engine

Why: Provides Clever with advanced geometric and mathematical shape generation capabilities
     as part of her digital brain extension, enabling her to visualize complex mathematical
     concepts and create educational geometric demonstrations.
Where: Integrates with PersonaEngine and HolographicChamber for visual shape manifestation
How: Uses mathematical algorithms to generate coordinate sets for various geometric shapes,
     then interfaces with the particle system for visual representation.

Connects to:
    - persona.py: PersonaEngine calls generate_shape() for shape command responses
    - holographic-chamber.js: Receives coordinate data for particle positioning
    - app.py: Flask routes expose shape generation API endpoints
"""

import math
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass
from debug_config import get_debugger, performance_monitor

# Try to import numpy for enhanced calculations, fallback to math if not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

debugger = get_debugger()

@dataclass
class ShapePoint:
    """Individual point in 3D space for shape generation
    
    Why: Standardized data structure for shape coordinates with metadata
    Where: Used by all shape generation functions as output format
    How: Contains x,y,z coordinates plus optional properties like color, size
    """
    x: float
    y: float 
    z: float = 0.0  # For future 3D expansion
    color: Optional[str] = None
    size: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass 
class Shape:
    """Complete geometric shape definition
    
    Why: Encapsulates shape data with properties for intelligent particle formation
    Where: Returned by all shape generation functions, consumed by visualization layer
    How: Contains points array plus shape metadata for rendering and animation
    """
    name: str
    points: List[ShapePoint]
    center: Tuple[float, float, float]
    bounding_box: Dict[str, float]
    properties: Dict[str, Any]
    animation_data: Optional[Dict[str, Any]] = None

class ShapeGenerator:
    """
    Mathematical Shape Generation Engine for Clever's Cognitive Visualization
    
    Why: Enables Clever to generate and visualize complex geometric shapes as part of
         her digital brain extension capabilities, supporting mathematical education,
         creative visualization, and cognitive enhancement through geometry.
    Where: Core engine called by PersonaEngine when shape commands are detected,
           interfaces with particle system for visual manifestation.
    How: Uses mathematical algorithms and numpy for efficient coordinate calculation,
         supports 2D/3D shapes with animation and morphing capabilities.
    
    Connects to:
        - persona.py: PersonaEngine.generate() → shape detection → ShapeGenerator.create()
        - static/js/engines/holographic-chamber.js: Receives shape data for particle positioning
        - app.py: /api/generate_shape endpoint exposes functionality to frontend
        - evolution_engine.py: Logs shape generation events for learning
    """
    
    def __init__(self):
        """Initialize shape generator with default parameters
        
        Why: Set up mathematical constants and default rendering parameters
        Where: Called once during app initialization from app.py
        How: Initializes mathematical constants and default shape properties
        """
        self.default_size = 200  # Default shape size in pixels
        self.default_point_count = 60  # Default number of particles for shapes
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        debugger.info('shape_generator', 'ShapeGenerator initialized with default parameters')
    
    @performance_monitor('shape_generator.generate_basic_shapes')
    def generate_polygon(self, sides: int, size: float = None, center: Tuple[float, float] = (0, 0)) -> Shape:
        """Generate regular polygon with specified number of sides
        
        Why: Creates mathematically precise regular polygons for geometric education
              and visual demonstrations of mathematical concepts
        Where: Called by create_shape() when polygon shapes are requested
        How: Uses trigonometric functions to calculate vertex positions around circle
        
        Args:
            sides: Number of polygon sides (3+ for valid polygon)  
            size: Radius/size of polygon in pixels
            center: Center point (x, y) for polygon placement
            
        Returns:
            Shape object containing polygon vertex coordinates and metadata
            
        Connects to:
            - create_shape(): Called for 'triangle', 'pentagon', 'hexagon' etc commands
            - HolographicChamber: Points used for particle target positions
        """
        if sides < 3:
            raise ValueError("Polygon must have at least 3 sides")
            
        size = size or self.default_size
        points = []
        
        # Calculate vertex positions using unit circle trigonometry
        for i in range(sides):
            angle = (2 * math.pi * i) / sides
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            points.append(ShapePoint(x, y, color=self._get_vertex_color(i, sides)))
            
        # Add additional points along edges for smoother particle distribution
        edge_points = []
        for i in range(len(points)):
            current = points[i]
            next_point = points[(i + 1) % len(points)]
            
            # Add interpolated points along edge
            segments = max(2, self.default_point_count // (sides * 2))
            for j in range(1, segments):
                t = j / segments
                edge_x = current.x + t * (next_point.x - current.x)
                edge_y = current.y + t * (next_point.y - current.y)
                edge_points.append(ShapePoint(edge_x, edge_y, color=current.color))
        
        all_points = points + edge_points
        
        # Calculate bounding box and properties
        x_coords = [p.x for p in all_points]
        y_coords = [p.y for p in all_points]
        
        shape = Shape(
            name=f"{sides}-sided polygon",
            points=all_points,
            center=(center[0], center[1], 0),
            bounding_box={
                'min_x': min(x_coords), 'max_x': max(x_coords),
                'min_y': min(y_coords), 'max_y': max(y_coords)
            },
            properties={
                'sides': sides,
                'radius': size,
                'perimeter': self._calculate_polygon_perimeter(sides, size),
                'area': self._calculate_polygon_area(sides, size),
                'interior_angle': (sides - 2) * 180 / sides
            }
        )
        
        debugger.info('shape_generator', f'Generated {sides}-sided polygon with {len(all_points)} points')
        return shape
    
    @performance_monitor('shape_generator.generate_circle')  
    def generate_circle(self, radius: float = None, center: Tuple[float, float] = (0, 0), 
                       point_count: int = None) -> Shape:
        """Generate circle with evenly distributed points
        
        Why: Creates perfect circles for geometric demonstrations and smooth particle formations
        Where: Called for 'circle', 'sphere' shape commands in persona responses  
        How: Uses parametric circle equation with evenly spaced angle increments
        
        Args:
            radius: Circle radius in pixels
            center: Center point (x, y) for circle placement  
            point_count: Number of points around circumference
            
        Returns:
            Shape object with circle coordinates and mathematical properties
            
        Connects to:
            - create_shape(): Called for circle/sphere shape requests
            - HolographicChamber.createSphereFormation(): Compatible coordinate format
        """
        radius = radius or self.default_size
        point_count = point_count or self.default_point_count
        points = []
        
        # Generate points around circumference using parametric equations
        for i in range(point_count):
            angle = (2 * math.pi * i) / point_count
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            
            # Add subtle color variation based on position
            hue_shift = (i / point_count) * 360
            points.append(ShapePoint(x, y, metadata={'angle': angle, 'hue_shift': hue_shift}))
        
        shape = Shape(
            name="circle",
            points=points,
            center=(center[0], center[1], 0),
            bounding_box={
                'min_x': center[0] - radius, 'max_x': center[0] + radius,
                'min_y': center[1] - radius, 'max_y': center[1] + radius  
            },
            properties={
                'radius': radius,
                'diameter': 2 * radius,
                'circumference': 2 * math.pi * radius,
                'area': math.pi * radius * radius
            }
        )
        
        debugger.info('shape_generator', f'Generated circle with radius {radius} and {point_count} points')
        return shape
    
    @performance_monitor('shape_generator.generate_spiral')
    def generate_spiral(self, type: str = "archimedean", turns: float = 3, size: float = None, 
                       center: Tuple[float, float] = (0, 0)) -> Shape:
        """Generate mathematical spiral shapes
        
        Why: Creates beautiful spiral patterns demonstrating mathematical growth functions
              and natural phenomena like galaxies, shells, and plant growth patterns
        Where: Called for 'spiral', 'helix', 'fibonacci' shape commands
        How: Uses parametric spiral equations with configurable growth parameters
        
        Args:
            type: Spiral type ('archimedean', 'logarithmic', 'fibonacci')
            turns: Number of complete rotations  
            size: Maximum radius/size in pixels
            center: Center point (x, y) for spiral placement
            
        Returns:
            Shape object with spiral coordinates and mathematical properties
        """
        size = size or self.default_size
        points = []
        point_count = int(self.default_point_count * turns)  # More points for more turns
        
        for i in range(point_count):
            t = (i / point_count) * turns * 2 * math.pi  # Parameter from 0 to turns*2π
            
            if type == "archimedean":
                # r = a * θ (uniform spacing)
                r = (t / (turns * 2 * math.pi)) * size
            elif type == "logarithmic": 
                # r = a * e^(b*θ) (exponential growth)
                r = size * math.exp(t / (turns * 4)) / math.exp(2 * math.pi / 4)
            elif type == "fibonacci":
                # Golden spiral approximation
                r = size * math.sqrt(t) / math.sqrt(turns * 2 * math.pi)
            else:
                r = (t / (turns * 2 * math.pi)) * size  # Default to archimedean
                
            x = center[0] + r * math.cos(t)
            y = center[1] + r * math.sin(t)
            
            points.append(ShapePoint(
                x, y, 
                metadata={
                    'angle': t, 
                    'radius': r, 
                    'turn_progress': t / (turns * 2 * math.pi)
                }
            ))
        
        # Calculate bounding box
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]
        
        shape = Shape(
            name=f"{type} spiral",
            points=points,
            center=(center[0], center[1], 0),
            bounding_box={
                'min_x': min(x_coords), 'max_x': max(x_coords),
                'min_y': min(y_coords), 'max_y': max(y_coords)
            },
            properties={
                'type': type,
                'turns': turns,
                'max_radius': size,
                'length': self._calculate_spiral_length(type, turns, size)
            }
        )
        
        debugger.info('shape_generator', f'Generated {type} spiral with {turns} turns and {len(points)} points')
        return shape
    
    @performance_monitor('shape_generator.generate_fractal')
    def generate_koch_snowflake(self, iterations: int = 3, size: float = None, 
                               center: Tuple[float, float] = (0, 0)) -> Shape:
        """Generate Koch snowflake fractal
        
        Why: Demonstrates mathematical fractals and self-similarity concepts through
              beautiful geometric patterns that exhibit infinite complexity
        Where: Called for 'fractal', 'koch', 'snowflake' shape commands
        How: Recursive generation of Koch curve applied to triangle base
        
        Args:
            iterations: Number of fractal iterations (complexity level)
            size: Base triangle size in pixels  
            center: Center point (x, y) for snowflake placement
            
        Returns:
            Shape object with fractal coordinates and complexity metadata
        """
        size = size or self.default_size
        
        # Start with equilateral triangle
        triangle_points = [
            (center[0] - size, center[1] + size/2),
            (center[0] + size, center[1] + size/2),  
            (center[0], center[1] - size * math.sqrt(3)/2)
        ]
        
        # Generate Koch curve for each side
        all_points = []
        for i in range(3):
            start = triangle_points[i]
            end = triangle_points[(i + 1) % 3]
            koch_points = self._generate_koch_curve(start, end, iterations)
            all_points.extend([ShapePoint(x, y, metadata={'iteration': iterations, 'side': i}) 
                             for x, y in koch_points])
        
        # Calculate bounding box  
        x_coords = [p.x for p in all_points]
        y_coords = [p.y for p in all_points]
        
        shape = Shape(
            name="Koch snowflake",
            points=all_points,
            center=(center[0], center[1], 0),
            bounding_box={
                'min_x': min(x_coords), 'max_x': max(x_coords),
                'min_y': min(y_coords), 'max_y': max(y_coords)
            },
            properties={
                'iterations': iterations,
                'fractal_dimension': math.log(4) / math.log(3),  # ≈ 1.26
                'perimeter_ratio': 4**iterations / 3**(iterations-1),
                'point_count': len(all_points)
            }
        )
        
        debugger.info('shape_generator', f'Generated Koch snowflake with {iterations} iterations and {len(all_points)} points')
        return shape
    
    def _generate_koch_curve(self, start: Tuple[float, float], end: Tuple[float, float], 
                           iterations: int) -> List[Tuple[float, float]]:
        """Recursively generate Koch curve between two points
        
        Why: Core recursive algorithm for Koch snowflake fractal generation
        Where: Called by generate_koch_snowflake() for each triangle side
        How: Divides line into thirds, adds equilateral triangle bump, recurses
        """
        if iterations == 0:
            return [start, end]
        
        # Calculate intermediate points
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # Points dividing line into thirds
        p1 = (start[0] + dx/3, start[1] + dy/3)
        p3 = (start[0] + 2*dx/3, start[1] + 2*dy/3)
        
        # Peak of equilateral triangle 
        peak_x = p1[0] + (dx/6 - dy*math.sqrt(3)/6)
        peak_y = p1[1] + (dy/6 + dx*math.sqrt(3)/6)
        p2 = (peak_x, peak_y)
        
        # Recursively generate Koch curves for each segment
        curve1 = self._generate_koch_curve(start, p1, iterations - 1)
        curve2 = self._generate_koch_curve(p1, p2, iterations - 1)  
        curve3 = self._generate_koch_curve(p2, p3, iterations - 1)
        curve4 = self._generate_koch_curve(p3, end, iterations - 1)
        
        # Combine curves (remove duplicate endpoints)
        result = curve1[:-1] + curve2[:-1] + curve3[:-1] + curve4
        return result
    
    @performance_monitor('shape_generator.create_shape')
    def create_shape(self, shape_name: str, **kwargs) -> Shape:
        """Main entry point for shape creation
        
        Why: Unified interface for all shape generation, handles command parsing
              and parameter normalization for consistent shape creation
        Where: Called by PersonaEngine when shape commands are detected in user input
        How: Dispatches to appropriate generation method based on shape name
        
        Args:
            shape_name: Name/type of shape to generate
            **kwargs: Shape-specific parameters (size, center, etc.)
            
        Returns:
            Shape object ready for particle system visualization
            
        Connects to:
            - persona.py: PersonaEngine calls this when shape commands detected
            - app.py: /api/generate_shape endpoint exposes this functionality
        """
        shape_name = shape_name.lower().strip()
        
        # Normalize common shape aliases
        shape_aliases = {
            'triangle': ('polygon', {'sides': 3}),
            'square': ('polygon', {'sides': 4}),
            'pentagon': ('polygon', {'sides': 5}),
            'hexagon': ('polygon', {'sides': 6}),
            'octagon': ('polygon', {'sides': 8}),
            'sphere': ('circle', {}),
            'ring': ('circle', {'radius': kwargs.get('size', self.default_size) * 0.8}),
            'helix': ('spiral', {'type': 'logarithmic'}),
            'fibonacci': ('spiral', {'type': 'fibonacci'}),
            'fractal': ('koch_snowflake', {}),
            'snowflake': ('koch_snowflake', {})
        }
        
        if shape_name in shape_aliases:
            method_name, extra_kwargs = shape_aliases[shape_name] 
            kwargs.update(extra_kwargs)
            shape_name = method_name
        
        # Dispatch to appropriate generation method
        try:
            if shape_name == 'polygon':
                return self.generate_polygon(**kwargs)
            elif shape_name == 'circle':
                return self.generate_circle(**kwargs)
            elif shape_name == 'spiral':
                return self.generate_spiral(**kwargs)
            elif shape_name == 'koch_snowflake':
                return self.generate_koch_snowflake(**kwargs)
            else:
                # Default to circle for unknown shapes
                debugger.warn('shape_generator', f'Unknown shape "{shape_name}", defaulting to circle')
                return self.generate_circle(**kwargs)
                
        except Exception as e:
            debugger.error('shape_generator', f'Error generating shape "{shape_name}": {str(e)}')
            # Fallback to simple circle
            return self.generate_circle(radius=100, center=(0, 0))
    
    def _get_vertex_color(self, index: int, total: int) -> str:
        """Generate color for polygon vertex based on position
        
        Why: Adds visual variety and mathematical beauty to polygon generation
        Where: Called by generate_polygon() for each vertex
        How: Uses HSL color space with hue based on vertex position
        """
        hue = (index / total) * 360
        return f"hsl({hue}, 70%, 60%)"
    
    def _calculate_polygon_perimeter(self, sides: int, radius: float) -> float:
        """Calculate perimeter of regular polygon inscribed in circle"""
        return sides * 2 * radius * math.sin(math.pi / sides)
    
    def _calculate_polygon_area(self, sides: int, radius: float) -> float:
        """Calculate area of regular polygon inscribed in circle"""  
        return 0.5 * sides * radius * radius * math.sin(2 * math.pi / sides)
    
    def _calculate_spiral_length(self, spiral_type: str, turns: float, size: float) -> float:
        """Calculate approximate arc length of spiral"""
        if spiral_type == "archimedean":
            # Approximation for Archimedean spiral
            a = size / (turns * 2 * math.pi)
            return (math.pi * a * (turns * 2 * math.pi)**2) / 2
        else:
            # Rough approximation for other spirals
            return turns * 2 * math.pi * size * 0.7
    
    def get_shape_info(self, shape: Shape) -> Dict[str, Any]:
        """Get comprehensive information about a generated shape
        
        Why: Provides educational and debugging information about shape properties
        Where: Called by API endpoints and persona responses for shape explanations
        How: Extracts mathematical properties and metadata from Shape object
        
        Args:
            shape: Shape object to analyze
            
        Returns:
            Dictionary containing shape properties, statistics, and educational info
        """
        info = {
            'name': shape.name,
            'point_count': len(shape.points),
            'center': shape.center,
            'bounding_box': shape.bounding_box,
            'properties': shape.properties
        }
        
        # Add calculated statistics
        if shape.points:
            x_coords = [p.x for p in shape.points]
            y_coords = [p.y for p in shape.points]
            
            info['statistics'] = {
                'width': max(x_coords) - min(x_coords),
                'height': max(y_coords) - min(y_coords),
                'average_x': sum(x_coords) / len(x_coords),
                'average_y': sum(y_coords) / len(y_coords)
            }
        
        return info

# Global instance for use throughout application
_shape_generator = None

def get_shape_generator() -> ShapeGenerator:
    """Get global ShapeGenerator instance
    
    Why: Provides singleton access to shape generation capabilities throughout app
    Where: Called by persona.py, app.py, and other modules needing shape generation
    How: Creates instance on first call, returns existing instance on subsequent calls
    
    Connects to:
        - persona.py: PersonaEngine uses this to access shape generation
        - app.py: Flask routes use this for API endpoints
    """
    global _shape_generator
    if _shape_generator is None:
        _shape_generator = ShapeGenerator()
    return _shape_generator
"""
Clever's Mathematical Shape Generation Engine

Why: Provides Clever with advanced         self.default_size = 200  # Default shape size in pixels
        self.default_point_count = 60  # Default number of particles for shapes
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        # Enhanced particle distribution settings (for special shapes only)
        self.dense_point_count = 70  # Modest increase for complex shapes
        self.ultra_dense_count = 80  # Conservative increase for fractalsric and mathematical shape generation capabilities
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
        self.default_point_count = 80  # Default number of particles for shapes - ENHANCED UTILIZATION
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        # Enhanced particle distribution settings
        self.dense_point_count = 80  # For complex shapes requiring more detail
        self.ultra_dense_count = 120  # For fractals and spirals
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
            
        # Add additional points along edges for smoother particle distribution - ENHANCED
        edge_points = []
        remaining_particles = self.default_point_count - len(points)
        segments_per_edge = max(3, remaining_particles // sides)  # More particles per edge
        
        for i in range(len(points)):
            current = points[i]
            next_point = points[(i + 1) % len(points)]
            
            # Add interpolated points along edge with enhanced density
            for j in range(1, segments_per_edge + 1):
                t = j / (segments_per_edge + 1)
                edge_x = current.x + t * (next_point.x - current.x)
                edge_y = current.y + t * (next_point.y - current.y)
                
                # Enhanced color variation for better visual appeal
                hue = ((i + t) / sides) * 360
                saturation = 75 + (t * 15)  # Varying saturation
                lightness = 55 + (t * 20)   # Varying lightness
                
                edge_points.append(ShapePoint(edge_x, edge_y, 
                    color=f"hsl({hue}, {saturation}%, {lightness}%)",
                    metadata={'edge': True, 'segment': j, 'side': i, 'edge_progress': t}))
        
        # Add center fill points for polygons with many particles remaining
        center_points = []
        if len(points) + len(edge_points) < self.default_point_count * 0.8:
            center_x, center_y = center[0], center[1]
            remaining = self.default_point_count - len(points) - len(edge_points)
            
            # Add concentric inner points for visual richness
            for i in range(min(remaining, sides * 2)):
                angle = (2 * math.pi * i) / (sides * 2)
                inner_radius = size * (0.3 + 0.4 * (i % 2))  # Varying inner radii
                x = center_x + inner_radius * math.cos(angle)
                y = center_y + inner_radius * math.sin(angle)
                
                center_points.append(ShapePoint(x, y,
                    color=f"hsl({(i * 360) / (sides * 2)}, 60%, 70%)",
                    metadata={'inner': True, 'ring': i % 2, 'angle': angle}))
        
        all_points = points + edge_points + center_points
        
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
        
        # Generate points around circumference using parametric equations - ENHANCED
        for i in range(point_count):
            angle = (2 * math.pi * i) / point_count
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            
            # Enhanced color variation for better visual appeal
            hue_shift = (i / point_count) * 360
            points.append(ShapePoint(x, y, 
                color=f"hsl({hue_shift}, 75%, 60%)",
                metadata={'angle': angle, 'position': i, 'radius': radius}
            ))
        
        # Add concentric inner circles for richer visualization if particles remain
        if point_count < self.default_point_count:
            remaining = self.default_point_count - point_count
            inner_circles = 2  # Number of inner concentric circles
            
            for ring in range(inner_circles):
                ring_radius = radius * (0.7 - ring * 0.3)  # 70%, 40% of outer radius
                ring_points = min(remaining // (inner_circles - ring), point_count // 2)
                
                for i in range(ring_points):
                    angle = (2 * math.pi * i) / ring_points
                    x = center[0] + ring_radius * math.cos(angle)
                    y = center[1] + ring_radius * math.sin(angle)
                    
                    # Different hue for inner rings
                    hue_shift = ((i / ring_points) * 360 + ring * 60) % 360
                    lightness = 65 + ring * 10  # Lighter for inner rings
                    
                    points.append(ShapePoint(
                        x, y,
                        color=f"hsl({hue_shift}, 70%, {lightness}%)",
                        metadata={'angle': angle, 'ring': ring, 'inner': True}
                    ))
                    
                remaining -= ring_points
                if remaining <= 0:
                    break
        
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

    @performance_monitor('shape_generator.generate_star')
    def generate_star_polygon(self, points: int = 5, size: float = None, center: Tuple[float, float] = (0, 0)) -> Shape:
        """Generate star polygon with specified number of points
        
        Why: Creates beautiful star shapes for mathematical visualization and decoration
        Where: Called for 'star', 'star_5', etc. shape commands
        How: Uses alternating outer and inner radii with trigonometric calculations
        
        Args:
            points: Number of star points (5 for pentagram, 6 for hexagram, etc.)
            size: Outer radius of star in pixels
            center: Center point (x, y) for star placement
            
        Returns:
            Shape object containing star vertex coordinates and metadata
        """
        if points < 3:
            raise ValueError("Star must have at least 3 points")
            
        size = size or self.default_size
        outer_radius = size
        inner_radius = size * 0.4  # Inner points are 40% of outer radius
        
        star_points = []
        vertices_needed = points * 2  # Each star point creates 2 vertices (inner + outer)
        
        # Generate alternating outer and inner vertices
        for i in range(vertices_needed):
            angle = (2 * math.pi * i) / vertices_needed - math.pi / 2  # Start at top
            
            # Alternate between outer and inner radius
            if i % 2 == 0:
                radius = outer_radius  # Outer point
                point_type = 'outer'
            else:
                radius = inner_radius  # Inner point
                point_type = 'inner'
                
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            
            # Enhanced color for star points
            hue = (i / vertices_needed) * 360
            saturation = 85 if point_type == 'outer' else 60
            lightness = 55 if point_type == 'outer' else 70
            
            star_points.append(ShapePoint(
                x, y,
                color=f"hsl({hue}, {saturation}%, {lightness}%)",
                metadata={
                    'point_type': point_type,
                    'star_point_index': i // 2 if point_type == 'outer' else (i - 1) // 2,
                    'angle': angle
                }
            ))
        
        # Add edge interpolation for smoother star edges
        edge_points = []
        remaining = self.default_point_count - len(star_points)
        segments_per_edge = max(2, remaining // vertices_needed)
        
        for i in range(len(star_points)):
            current = star_points[i]
            next_point = star_points[(i + 1) % len(star_points)]
            
            for j in range(1, segments_per_edge + 1):
                t = j / (segments_per_edge + 1)
                edge_x = current.x + t * (next_point.x - current.x)
                edge_y = current.y + t * (next_point.y - current.y)
                
                # Color interpolation for smooth transitions
                hue = ((i + t) / vertices_needed) * 360
                
                edge_points.append(ShapePoint(
                    edge_x, edge_y,
                    color=f"hsl({hue}, 75%, 60%)",
                    metadata={'edge': True, 'progress': t, 'edge_index': i}
                ))
        
        all_points = star_points + edge_points
        
        # Calculate bounding box
        x_coords = [p.x for p in all_points]
        y_coords = [p.y for p in all_points]
        
        shape = Shape(
            name=f"{points}-pointed star",
            points=all_points,
            center=(center[0], center[1], 0),
            bounding_box={
                'min_x': min(x_coords), 'max_x': max(x_coords),
                'min_y': min(y_coords), 'max_y': max(y_coords)
            },
            properties={
                'star_points': points,
                'outer_radius': outer_radius,
                'inner_radius': inner_radius,
                'vertices': vertices_needed,
                'symmetry': f"{points}-fold rotational",
                'mathematical_type': 'star_polygon'
            }
        )
        
        debugger.info('shape_generator', f'Generated {points}-pointed star with {len(all_points)} points')
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
    
    @performance_monitor('shape_generator.generate_3d_shape')  
    def generate_3d_shape(self, shape_type: str = 'cube', size: float = None, 
                         center: Tuple[float, float] = (0, 0)) -> Shape:
        """Generate 3D shape wireframe projection
        
        Why: Creates 3D geometric visualizations by projecting 3D coordinates to 2D
              for stunning mathematical demonstrations of spatial geometry
        Where: Called for 'cube', 'pyramid', 'prism' and other 3D shape commands
        How: Generate 3D vertices, apply perspective projection, create edge connections
        
        Args:
            shape_type: Type of 3D shape ('cube', 'pyramid', 'prism', etc.)
            size: Size of the 3D shape in pixels
            center: Center point (x, y) for shape placement
            
        Returns:
            Shape object with 3D wireframe coordinates and metadata
        """
        size = size or self.default_size
        
        if shape_type == 'cube':
            # Generate cube vertices in 3D space - Y is vertical axis
            half_size = size / 2
            vertices_3d = [
                # Bottom face (y = -half_size)
                (-half_size, -half_size, -half_size),  # 0: back-left-bottom
                ( half_size, -half_size, -half_size),  # 1: back-right-bottom  
                ( half_size, -half_size,  half_size),  # 2: front-right-bottom
                (-half_size, -half_size,  half_size),  # 3: front-left-bottom
                # Top face (y = half_size)
                (-half_size,  half_size, -half_size),  # 4: back-left-top
                ( half_size,  half_size, -half_size),  # 5: back-right-top
                ( half_size,  half_size,  half_size),  # 6: front-right-top
                (-half_size,  half_size,  half_size),  # 7: front-left-top
            ]
            
            # Define cube edges (connect vertices)
            edges = [
                # Bottom face edges
                (0, 1), (1, 2), (2, 3), (3, 0),
                # Top face edges  
                (4, 5), (5, 6), (6, 7), (7, 4),
                # Vertical edges connecting top and bottom
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]
            
        elif shape_type == 'pyramid':
            # Triangular pyramid (tetrahedron) - Y is vertical axis
            half_size = size / 2
            height = size * math.sqrt(2/3)  # Proper tetrahedron height
            vertices_3d = [
                # Base triangle (at y = -height/3)
                (-half_size, -height/3, -half_size/math.sqrt(3)),     # Base vertex 1
                ( half_size, -height/3, -half_size/math.sqrt(3)),     # Base vertex 2  
                (0, -height/3, half_size*math.sqrt(3)/3),             # Base vertex 3
                # Apex
                (0, height*2/3, 0)                                    # Apex (top)
            ]
            
            edges = [
                # Base triangle
                (0, 1), (1, 2), (2, 0),
                # Edges to apex
                (0, 3), (1, 3), (2, 3)
            ]
            
        elif shape_type == 'cone':
            # Cone with circular base - Y is vertical axis
            half_size = size / 2
            height = size * 0.8  # Cone height
            base_radius = half_size
            num_base_points = 12  # Circular base resolution
            
            vertices_3d = []
            
            # Generate circular base points (at y = -height/2)
            for i in range(num_base_points):
                angle = (2 * math.pi * i) / num_base_points
                x = base_radius * math.cos(angle)
                z = base_radius * math.sin(angle)
                vertices_3d.append((x, -height/2, z))
            
            # Add apex point (at y = height/2)
            vertices_3d.append((0, height/2, 0))
            
            # Define edges
            edges = []
            # Base circle edges
            for i in range(num_base_points):
                edges.append((i, (i + 1) % num_base_points))
            # Edges from base to apex
            apex_idx = num_base_points
            for i in range(num_base_points):
                edges.append((i, apex_idx))
                
        elif shape_type == 'cylinder':
            # Cylinder with circular top and bottom - Y is vertical axis
            half_size = size / 2
            height = size * 0.8
            radius = half_size * 0.6
            num_circle_points = 10  # Circle resolution
            
            vertices_3d = []
            
            # Bottom circle (at y = -height/2)
            for i in range(num_circle_points):
                angle = (2 * math.pi * i) / num_circle_points
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                vertices_3d.append((x, -height/2, z))
            
            # Top circle (at y = height/2)
            for i in range(num_circle_points):
                angle = (2 * math.pi * i) / num_circle_points
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                vertices_3d.append((x, height/2, z))
            
            # Define edges
            edges = []
            # Bottom circle edges
            for i in range(num_circle_points):
                edges.append((i, (i + 1) % num_circle_points))
            # Top circle edges  
            for i in range(num_circle_points):
                top_i = i + num_circle_points
                edges.append((top_i, ((i + 1) % num_circle_points) + num_circle_points))
            # Vertical edges connecting bottom to top
            for i in range(num_circle_points):
                edges.append((i, i + num_circle_points))
                
        elif shape_type == 'sphere':
            # Wireframe sphere using latitude/longitude lines - Y is vertical axis
            half_size = size / 2
            radius = half_size
            lat_segments = 6  # Latitude lines
            lon_segments = 8  # Longitude lines
            
            vertices_3d = []
            
            # Generate sphere vertices using spherical coordinates
            for lat in range(lat_segments + 1):
                theta = (lat / lat_segments) * math.pi  # 0 to π (latitude)
                for lon in range(lon_segments):
                    phi = (lon / lon_segments) * 2 * math.pi  # 0 to 2π (longitude)
                    
                    x = radius * math.sin(theta) * math.cos(phi)
                    y = radius * math.cos(theta)  # Y is vertical
                    z = radius * math.sin(theta) * math.sin(phi)
                    vertices_3d.append((x, y, z))
            
            # Define edges for wireframe
            edges = []
            # Latitude lines (horizontal circles)
            for lat in range(lat_segments + 1):
                for lon in range(lon_segments):
                    current = lat * lon_segments + lon
                    next_lon = lat * lon_segments + ((lon + 1) % lon_segments)
                    if current < len(vertices_3d) and next_lon < len(vertices_3d):
                        edges.append((current, next_lon))
            
            # Longitude lines (vertical semicircles)
            for lon in range(lon_segments):
                for lat in range(lat_segments):
                    current = lat * lon_segments + lon
                    next_lat = (lat + 1) * lon_segments + lon
                    if current < len(vertices_3d) and next_lat < len(vertices_3d):
                        edges.append((current, next_lat))
            
        elif shape_type == 'star' or shape_type == 'star_3d':
            # 3D Star - extrude 2D star with depth layers for true 3D visualization
            half_size = size / 2
            depth = size * 0.3  # 3D extrusion depth
            star_points = 5  # 5-pointed star
            outer_radius = half_size
            inner_radius = half_size * 0.4
            
            vertices_3d = []
            
            # Generate front face star vertices (z = depth/2)
            for i in range(star_points * 2):  # Alternating outer/inner points
                angle = (i * math.pi) / star_points
                if i % 2 == 0:  # Outer points
                    radius = outer_radius
                else:  # Inner points
                    radius = inner_radius
                
                x = radius * math.cos(angle - math.pi/2)  # Start from top
                y = radius * math.sin(angle - math.pi/2)
                vertices_3d.append((x, y, depth/2))
            
            # Generate back face star vertices (z = -depth/2)
            for i in range(star_points * 2):
                angle = (i * math.pi) / star_points
                if i % 2 == 0:  # Outer points
                    radius = outer_radius
                else:  # Inner points
                    radius = inner_radius
                
                x = radius * math.cos(angle - math.pi/2)
                y = radius * math.sin(angle - math.pi/2)
                vertices_3d.append((x, y, -depth/2))
            
            # Define edges for 3D star wireframe
            edges = []
            num_star_points = star_points * 2
            
            # Front face star edges
            for i in range(num_star_points):
                edges.append((i, (i + 1) % num_star_points))
            
            # Back face star edges
            for i in range(num_star_points):
                back_i = i + num_star_points
                back_next = ((i + 1) % num_star_points) + num_star_points
                edges.append((back_i, back_next))
            
            # Connecting edges between front and back faces
            for i in range(num_star_points):
                edges.append((i, i + num_star_points))
                
        elif shape_type in ['triangle_3d', 'pentagon_3d', 'hexagon_3d', 'octagon_3d']:
            # 3D extruded polygons - create front and back faces with connecting edges
            half_size = size / 2
            depth = size * 0.25  # 3D extrusion depth
            
            # Determine number of sides
            sides_map = {
                'triangle_3d': 3,
                'pentagon_3d': 5, 
                'hexagon_3d': 6,
                'octagon_3d': 8
            }
            sides = sides_map.get(shape_type, 6)
            
            vertices_3d = []
            
            # Generate front face polygon vertices (z = depth/2)
            for i in range(sides):
                angle = (2 * math.pi * i) / sides - math.pi/2  # Start from top
                x = half_size * math.cos(angle)
                y = half_size * math.sin(angle)
                vertices_3d.append((x, y, depth/2))
            
            # Generate back face polygon vertices (z = -depth/2)
            for i in range(sides):
                angle = (2 * math.pi * i) / sides - math.pi/2
                x = half_size * math.cos(angle)
                y = half_size * math.sin(angle)
                vertices_3d.append((x, y, -depth/2))
            
            # Define edges for 3D polygon wireframe
            edges = []
            
            # Front face edges
            for i in range(sides):
                edges.append((i, (i + 1) % sides))
            
            # Back face edges
            for i in range(sides):
                back_i = i + sides
                back_next = ((i + 1) % sides) + sides
                edges.append((back_i, back_next))
            
            # Connecting edges between front and back faces
            for i in range(sides):
                edges.append((i, i + sides))
                
        elif shape_type == 'torus':
            # 3D Torus (donut shape) - wireframe representation
            half_size = size / 2
            major_radius = half_size * 0.7  # Main torus radius
            minor_radius = half_size * 0.2  # Tube radius
            major_segments = 8  # Around the main circle
            minor_segments = 6  # Around the tube
            
            vertices_3d = []
            
            # Generate torus vertices using parametric equations
            for i in range(major_segments):
                theta = (2 * math.pi * i) / major_segments  # Major angle
                for j in range(minor_segments):
                    phi = (2 * math.pi * j) / minor_segments  # Minor angle
                    
                    # Torus parametric equations
                    x = (major_radius + minor_radius * math.cos(phi)) * math.cos(theta)
                    y = minor_radius * math.sin(phi)  # Y is vertical
                    z = (major_radius + minor_radius * math.cos(phi)) * math.sin(theta)
                    vertices_3d.append((x, y, z))
            
            # Define edges for torus wireframe
            edges = []
            
            # Major circle edges (around the torus)
            for i in range(major_segments):
                for j in range(minor_segments):
                    current = i * minor_segments + j
                    next_major = ((i + 1) % major_segments) * minor_segments + j
                    edges.append((current, next_major))
            
            # Minor circle edges (around the tube)
            for i in range(major_segments):
                for j in range(minor_segments):
                    current = i * minor_segments + j
                    next_minor = i * minor_segments + ((j + 1) % minor_segments)
                    edges.append((current, next_minor))
                
        else:
            # Default to cube for unknown 3D shapes
            return self.generate_3d_shape('cube', size, center)
        
        # Apply simple perspective projection (3D to 2D)
        points = []
        perspective_factor = 300  # Distance from viewer
        
        for vertex in vertices_3d:
            x, y, z = vertex
            
            # Simple perspective projection
            if perspective_factor + z != 0:
                projected_x = (x * perspective_factor) / (perspective_factor + z)
                projected_y = (y * perspective_factor) / (perspective_factor + z)
            else:
                projected_x, projected_y = x, y
                
            # Translate to center position
            final_x = center[0] + projected_x
            final_y = center[1] + projected_y
            
            points.append((final_x, final_y))
        
        # Create edge-based point list for wireframe rendering
        edge_points = []
        for edge in edges:
            start_idx, end_idx = edge
            start_point = points[start_idx]  
            end_point = points[end_idx]
            
            # Interpolate points along each edge for smooth wireframe
            num_interpolated = 5
            for i in range(num_interpolated + 1):
                t = i / num_interpolated
                interpolated_x = start_point[0] + t * (end_point[0] - start_point[0])
                interpolated_y = start_point[1] + t * (end_point[1] - start_point[1])
                edge_points.append((interpolated_x, interpolated_y))
        
        # Convert edge_points to ShapePoint objects
        shape_points = []
        for i, (x, y) in enumerate(edge_points):
            shape_points.append(ShapePoint(
                x=x, y=y, z=0.0,
                color=f"hsl({(i * 30) % 360}, 70%, 60%)",
                metadata={'index': i, 'edge_point': True}
            ))
        
        # Calculate bounding box
        if shape_points:
            xs = [p.x for p in shape_points]
            ys = [p.y for p in shape_points] 
            bounding_box = {
                'min_x': min(xs), 'max_x': max(xs),
                'min_y': min(ys), 'max_y': max(ys)
            }
        else:
            bounding_box = {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0}
        
        # Create shape with proper parameters
        shape = Shape(
            name=shape_type,
            points=shape_points,
            center=(center[0], center[1], 0.0),
            bounding_box=bounding_box,
            properties={
                'type': '3d_wireframe',
                'shape_type': shape_type,
                'vertex_count': len(vertices_3d),
                'edge_count': len(edges),
                'perspective_projection': True,
                'mathematical_complexity': 0.8,
                'size': size
            }
        )
        
        debugger.info('shape_generator', f'Generated 3D {shape_type} wireframe with {len(vertices_3d)} vertices and {len(edge_points)} edge points')
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
        
        # Normalize common shape aliases (3D by default for immersive experience)
        shape_aliases = {
            'triangle': ('3d_shape', {'shape_type': 'triangle_3d'}),
            'square': ('3d_shape', {'shape_type': 'cube'}),  # 3D square is a cube
            'pentagon': ('3d_shape', {'shape_type': 'pentagon_3d'}),
            'hexagon': ('3d_shape', {'shape_type': 'hexagon_3d'}),
            'octagon': ('3d_shape', {'shape_type': 'octagon_3d'}),
            # 2D polygon shapes (explicit)
            'triangle_2d': ('polygon', {'sides': 3}),
            'square_2d': ('polygon', {'sides': 4}),
            'pentagon_2d': ('polygon', {'sides': 5}),
            'hexagon_2d': ('polygon', {'sides': 6}),
            'octagon_2d': ('polygon', {'sides': 8}),
            'sphere': ('3d_shape', {'shape_type': 'sphere'}),
            'circle': ('3d_shape', {'shape_type': 'sphere'}),  # 3D circle is a sphere
            'ring': ('3d_shape', {'shape_type': 'torus'}),
            # 2D circle shapes (explicit)
            'circle_2d': ('circle', {}),
            'ring_2d': ('circle', {'radius': kwargs.get('size', self.default_size) * 0.8}),
            'helix': ('spiral', {'type': 'logarithmic'}),
            'fibonacci': ('spiral', {'type': 'fibonacci'}),
            'fractal': ('koch_snowflake', {}),
            'snowflake': ('koch_snowflake', {}),
            # DNA and biological shapes
            'dna': ('dna_helix', {}),
            'double_helix': ('dna_helix', {}),
            'genetic': ('dna_helix', {}),
            # Star shapes (3D by default for immersive experience)
            'star': ('3d_shape', {'shape_type': 'star'}),
            'star_3d': ('3d_shape', {'shape_type': 'star'}),
            'pentagram': ('3d_shape', {'shape_type': 'star'}),
            'hexagram': ('3d_shape', {'shape_type': 'star'}),
            # 2D star shapes (explicit)
            'star_2d': ('star_polygon', {'points': 5}),
            'star_5': ('star_polygon', {'points': 5}),
            'star_6': ('star_polygon', {'points': 6}),
            'star_8': ('star_polygon', {'points': 8}),
            # 3D shapes
            'cube': ('3d_shape', {'shape_type': 'cube'}),
            'box': ('3d_shape', {'shape_type': 'cube'}),
            'pyramid': ('3d_shape', {'shape_type': 'pyramid'}),
            'tetrahedron': ('3d_shape', {'shape_type': 'pyramid'}),
            'cone': ('3d_shape', {'shape_type': 'cone'}),
            'cylinder': ('3d_shape', {'shape_type': 'cylinder'}),
            'tube': ('3d_shape', {'shape_type': 'cylinder'}),
            'sphere_3d': ('3d_shape', {'shape_type': 'sphere'}),
            'ball': ('3d_shape', {'shape_type': 'sphere'})
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
            elif shape_name == 'star_polygon':
                return self.generate_star_polygon(**kwargs)
            elif shape_name == 'dna_helix':
                return self.generate_dna_helix(**kwargs)
            elif shape_name == 'koch_snowflake':
                return self.generate_koch_snowflake(**kwargs)
            elif shape_name == '3d_shape':
                return self.generate_3d_shape(**kwargs)
            else:
                # Default to circle for unknown shapes
                debugger.warning('shape_generator', f'Unknown shape "{shape_name}", defaulting to circle')
                return self.generate_circle(**kwargs)
                
        except Exception:
            debugger.error('shape_generator', f'Error generating shape "{shape_name}": {str(e)}')
            # Fallback to simple circle
            return self.generate_circle(radius=100, center=(0, 0))
    
    @performance_monitor('shape_generator.generate_dna')
    def generate_dna_helix(self, size: float = None, turns: float = 2.5, 
                          center: Tuple[float, float, float] = (0, 0, 0)) -> Shape:
        """Generate DNA double helix structure
        
        Why: Creates beautiful 3D double helix demonstrating biological structures 
              and advanced mathematical visualization of intertwined spirals
        Where: Called for 'dna', 'double helix', 'genetic' shape commands
        How: Generates two counter-rotating helixes with connecting base pairs
        
        Args:
            size: Helix radius in pixels
            turns: Number of complete rotations
            center: Center point (x, y) for helix placement
            
        Returns:
            Shape object with DNA helix coordinates and biological properties
        """
        size = size or self.default_size * 0.8  # Larger radius for DNA prominence
        points = []
        point_count = int(self.default_point_count * turns * 1.5)  # Dense points for smooth helix
        helix_height = size * 1.2  # Taller height for better vertical presence
        
        for i in range(point_count):
            t = (i / point_count) * turns * 2 * math.pi  # Parameter from 0 to turns*2π
            y_progress = (i / point_count) - 0.5  # -0.5 to 0.5 for vertical positioning
            
            # First helix (backbone 1) - Y is vertical axis, X/Z form horizontal circle
            x1 = center[0] + size * math.cos(t)  # X is circular motion (horizontal)
            y1 = center[1] + y_progress * helix_height  # Y is vertical axis (screen vertical)
            z1 = center[2] + size * math.sin(t)  # Z is circular motion (depth)
            
            # Second helix (backbone 2) - 180° phase shift
            x2 = center[0] + size * math.cos(t + math.pi)  # X is circular motion (horizontal)
            y2 = center[1] + y_progress * helix_height  # Y is vertical axis (screen vertical)
            z2 = center[2] + size * math.sin(t + math.pi)  # Z is circular motion (depth)
            
            # Add backbone points
            points.extend([
                ShapePoint(x1, y1, z1, metadata={
                    'helix': 'backbone1', 'angle': t, 'z_depth': z1,
                    'turn_progress': t / (turns * 2 * math.pi),
                    'vertical_position': y_progress
                }),
                ShapePoint(x2, y2, z2, metadata={
                    'helix': 'backbone2', 'angle': t + math.pi, 'z_depth': z2,
                    'turn_progress': t / (turns * 2 * math.pi),
                    'vertical_position': y_progress
                })
            ])
            
            # Add base pair connections (every 10th point for clarity)
            if i % 10 == 0:
                # Create connecting base pair lines
                for step in range(5):  # 5 intermediate points
                    step_progress = step / 4  # 0 to 1
                    base_x = x1 + step_progress * (x2 - x1)
                    base_y = y1 + step_progress * (y2 - y1)
                    base_z = z1 + step_progress * (z2 - z1)
                    
                    points.append(ShapePoint(base_x, base_y, base_z, metadata={
                        'helix': 'base_pair', 'angle': t, 'z_depth': base_z,
                        'base_progress': step_progress
                    }))
        
        # Calculate 3D bounding box
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]
        z_coords = [p.z for p in points]
        
        shape = Shape(
            name="dna double helix",
            points=points,
            center=center,
            bounding_box={
                'min_x': min(x_coords), 'max_x': max(x_coords),
                'min_y': min(y_coords), 'max_y': max(y_coords),
                'min_z': min(z_coords), 'max_z': max(z_coords)
            },
            properties={
                'type': 'dna_helix',
                'turns': turns,
                'helix_radius': size,
                'height': helix_height,
                'base_pairs': point_count // 10,
                'complexity': 0.95  # Very high complexity
            }
        )
        
        debugger.info('shape_generator', f'Generated DNA helix with {turns} turns and {len(points)} points')
        return shape

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
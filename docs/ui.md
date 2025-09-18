# Clever UI Vision & Conventions

## UI Philosophy
Clever's interface prioritizes the **particle stage** as the main focus, with minimal, floating UI elements that don't distract from her expressive particle formations.

## Core Design Principles

### 1. **Stage-First Design**
- The particle engine is the primary visual element
- UI components are secondary and should not compete for attention
- Clever's title remains centered and prominent
- All interactions should enhance, not obstruct, the particle experience

### 2. **Floating & Ephemeral Elements**
- **Chat bubbles**: Float in/out with smooth animations, auto-fade after 4 seconds
- **No persistent boxes**: Remove static chat containers that block the stage
- **Minimal footprint**: UI elements appear only when needed

### 3. **Input Bar Design**
- **Centered positioning**: Bottom-center of screen
- **Subtle glow**: Gentle border glow on focus
- **Minimal styling**: Transparent background with subtle blur
- **Responsive feedback**: Hover and focus states with smooth transitions

## Visual Specifications

### Color Palette
- **Primary**: `#69EACB` (Clever teal)
- **Secondary**: `#33CCFF` (Response blue) 
- **Accent**: `#FF6BFF` (Thinking pink)
- **Background**: Dark cosmic gradient
- **Text**: `#e9f1fb` (Light blue-white)

### Animation Standards
- **Ease curves**: `cubic-bezier(0.34, 1.56, 0.64, 1)` for playful bounces
- **Duration**: 0.3-0.5s for interactions, 0.8s for fade transitions
- **Bubble lifecycle**: Fade in (0.5s) → Display (4s) → Fade out (0.8s)

### Typography
- **Font**: Inter (system fallbacks)
- **Title**: 3rem, weight 300, with glow effect
- **Bubbles**: 1rem, weight 300
- **Input**: 1rem, weight 300

## Component Behaviors

### Chat Bubbles
```css
/* User bubbles: Right-aligned, teal gradient */
.chat-bubble.user {
    background: linear-gradient(135deg, rgba(105, 234, 203, 0.15), rgba(105, 234, 203, 0.05));
    border: 1px solid rgba(105, 234, 203, 0.3);
    margin-left: auto;
    margin-right: 1rem;
}

/* AI bubbles: Left-aligned, blue gradient */
.chat-bubble.ai {
    background: linear-gradient(135deg, rgba(51, 204, 255, 0.15), rgba(51, 204, 255, 0.05));
    border: 1px solid rgba(51, 204, 255, 0.3);
    margin-left: 1rem;
    margin-right: auto;
}
```

### Input Bar States
- **Default**: Subtle border, minimal presence
- **Focus**: Enhanced glow, slight upward movement
- **Send button**: Hover scale effect with glow

## Interaction Patterns

### Message Flow
1. User types → Input bar glows
2. Send → User bubble fades in (right side)
3. Particles shift to "thinking" spiral
4. AI responds → AI bubble fades in (left side)  
5. Particles shift to "responding" sphere
6. Both bubbles auto-fade after 4 seconds
7. Return to natural particle swarm

### Particle Integration
- **Thinking**: Spiral formation, pink title glow
- **Responding**: Sphere formation, blue title glow  
- **Idle**: Natural swarm movement, teal title
- **Manual cycling**: Click canvas or 8-second auto-cycle

## Code Conventions

### Modern CSS Features
- Use `backdrop-filter: blur()` for glass effects
- Employ CSS custom properties for consistent theming
- Leverage `transform` and `opacity` for smooth animations
- Prefer `flex` layouts for responsive positioning

### JavaScript Patterns  
- **Modular functions**: Single responsibility principle
- **Event-driven**: Particle system responds to chat events
- **Clean DOM**: Auto-remove old bubbles to prevent memory leaks
- **Smooth transitions**: Coordinate animations with CSS

### File Organization
- **Self-contained templates**: Embed CSS/JS to avoid conflicts
- **Particle system**: Separate concerns (shapes, animations, interactions)
- **Responsive design**: Mobile-first approach with flexible layouts

## Accessibility Considerations
- Maintain sufficient color contrast for text readability
- Provide `aria-label` attributes for interactive elements  
- Ensure keyboard navigation works for input and send button
- Consider motion preferences for animation-sensitive users

---

*This UI vision emphasizes Clever's unique personality through her particle expressions while maintaining clean, unobtrusive chat functionality.*
/**
 * Clever AI - TypeScript Declarations
 * 
 * Why: Provides type definitions for dynamically added window properties
 * and global objects to eliminate TypeScript compilation warnings while
 * maintaining type safety and IDE intellisense support.
 * 
 * Where: Loaded by TypeScript compiler and VS Code language service
 * to understand Clever's runtime JavaScript environment and global APIs.
 * 
 * How: Extends the global Window interface with custom properties added
 * by Clever's JavaScript modules (holographic chamber, UI foundation, etc.)
 */

// Extend the global Window interface with Clever-specific properties
declare global {
  interface Window {
    // Holographic Chamber particle system
    holographicChamber?: {
      morphToFormation: (formation: string) => void;
      morphToFormationWithHold?: (formation: string, opts?: { holdMs?: number; postDriftMs?: number }) => void;
      summon: () => void;
      idle: () => void;
      dialogue: () => void;
      particles?: any[];
      currentFormation?: string;
      triggerPulse?: (intensity: number) => void;
      explode?: (intensity?: number) => void;
      implode?: (intensity?: number) => void;
      createVortex?: (x: number, y: number, strength?: number, duration?: number) => void;
      morphToText?: (text: string, fontSize?: number) => void;
      danceParty?: (duration?: number) => void;
      createLightning?: (fromIndex: number, toIndex: number) => void;
      toggleTrailMode?: () => void;
      addMagneticField?: (x: number, y: number, strength?: number, radius?: number, polarity?: number) => void;
      createEnergyWave?: (x: number, y: number, maxRadius?: number, speed?: number, intensity?: number) => void;
    };
    startHolographicChamber?: (canvas: HTMLCanvasElement) => any;
    cleverIntent?: string;
  morphToText?: (text: string) => void;

    // Particle effects functions
    explodeParticles?: (intensity: number) => void;
    implodeParticles?: (intensity: number) => void;
    createVortex?: () => void;
    createEnergyWave?: () => void;
    createLightning?: () => void;
    startDanceParty?: (duration: number) => void;
    toggleTrails?: () => void;
    addMagneticField?: () => void;
    triggerPulse?: (intensity: number) => void;
    updateFieldMode?: (mode: string) => void;

    // UI Foundation System
    CleverUIFoundation?: new () => {
      createComponent: (type: string, id: string, options: any) => any;
      removeComponent: (id: string) => void;
      getComponent: (id: string) => any;
      componentCount: number;
    };
    uiFoundation?: {
      createComponent: (type: string, id: string, options: any) => any;
      removeComponent: (id: string) => void;
      getComponent: (id: string) => any;
      componentCount: number;
    };

    // Chat and UI components
    CleverUIComponents?: any;
    
    // UI Component Classes
    FloatingPanel?: new (options: any) => any;
    AnalysisDisplay?: new (options: any) => any;
    ChatBubble?: new (options: any) => any;
    StatusIndicator?: new (options: any) => any;
    
    // Simple Browser compatibility
    SimpleBrowserEffects?: new () => any;
  }
}

// Particle system interfaces
interface ParticleSystem {
  morphToFormation: (formation: string) => void;
  summon: () => void;
}

interface UIComponent {
  id: string;
  type: string;
  element: HTMLElement;
  remove: () => void;
}

interface UIFoundation {
  createComponent: (type: string, id: string, options: any) => UIComponent;
  removeComponent: (id: string) => void;
  getComponent: (id: string) => UIComponent | null;
  componentCount: number;
}

// Export empty object to make this a module
export { };

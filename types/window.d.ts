/**
 * TypeScript declarations for custom window properties
 * This file extends the Window interface to include custom properties used in the Clever application
 */

declare global {
  interface Window {
    // Particle system functions
    startParticles?: (canvas: HTMLCanvasElement, options?: {count?: number}) => any;
    triggerPulse?: (intensity?: number) => void;

    // Holographic Chamber system
    HolographicChamber: any;
    holographicChamber?: any;
    startHolographicChamber?: (canvas: HTMLCanvasElement) => any;
    morphForIntent?: (intent: string) => void;
    dissolveToSwarm?: () => void;
    updateFieldMode?: (mode: string) => void;
    testHolographicChamber?: () => void;
    updateFieldMode?: (mode: string) => void;
    morphForIntent?: (intent: any) => void;

    // Nanobot swarm particle system
    nanobotSwarm?: {
      setColor?: (color: string, opacity: number) => void;
      sparkle?: (intensity: number) => void;
      pulse?: (intensity: number) => void;
      breathe?: (intensity: number) => void;
      pulseParticles?: (color: string, intensity: number) => void;
      burstParticles?: (color: string, intensity: number) => void;
    };

    // Scene particle system
    scene?: {
      particles?: {
        setColor?: (color: string, opacity: number) => void;
        sparkle?: (intensity: number) => void;
        pulse?: (intensity: number) => void;
        breathe?: (intensity: number) => void;
      };
    };

    // Particle field system
    particleField?: {
      setColor?: (color: string, opacity: number) => void;
      sparkle?: (intensity: number) => void;
      pulse?: (intensity: number) => void;
      breathe?: (intensity: number) => void;
      pulseParticles?: (color: string, intensity: number) => void;
      burstParticles?: (color: string, intensity: number) => void;
    };

    // Clever personality enhancer instances
    cleverPersonalityEnhancer?: any;
    cleverInvisiblePersonality?: any;
  }
}

// This export is needed to make this file a module and avoid conflicts
export { };

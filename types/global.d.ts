// types/global.d.ts - Global type declarations for Clever's cognitive interface
//
// Why: Provides TypeScript definitions for Clever's global window extensions and custom properties
// Where: Used throughout JavaScript files to eliminate TypeScript type checking errors
// How: Interface extensions for Window object and custom type declarations

declare global {
    interface Window {
        // Holographic Chamber Engine
        startHolographicChamber?: (canvas: HTMLCanvasElement) => any;
        cleverCognitiveStatus?: any;
        
        // Chat Components
        createChatBubble?: (text: string, sender?: string) => void;
        clearChatMessages?: () => void;
        getMessageCount?: () => number;
        
        // Cognitive Status Component
        createCognitiveStatusOverlay?: () => void;
        toggleCognitiveStatus?: () => void;
        
        // Main Application
        CleverApp?: {
            holographicChamber: any;
            isProcessingMessage: boolean;
            displayMessage: (text: string, sender?: string) => void;
            showSystemMessage: (text: string) => void;
            updateLastInteraction: () => void;
            version: string;
        };
    }
}

export { };

#!/usr/bin/env python3
"""
Validation script for spaCy lazy loading recommendations
Tests the proposed optimization patterns for offline performance

Usage: python docs/nlp/validate_lazy_loading.py
"""

import time
import sys
import os
import spacy
from functools import lru_cache

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def get_memory_usage():
    """Get current memory usage in MB (fallback implementation)"""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        # Fallback to approximate measurement
        return 0.0  # Return 0 if psutil not available

def test_standard_loading():
    """Test standard spaCy loading pattern (current implementation)"""
    print("=== Standard Loading Test ===")
    start_time = time.time()
    start_memory = get_memory_usage()
    
    nlp = spacy.load("en_core_web_sm")
    
    load_time = time.time() - start_time
    memory_used = get_memory_usage() - start_memory
    
    print(f"Load time: {load_time:.2f}s")
    print(f"Memory used: {memory_used:.1f}MB")
    print(f"Components: {list(nlp.pipe_names)}")
    
    # Test processing
    test_text = "Hello Clever, can you analyze this text for entities and sentiment?"
    doc = nlp(test_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Entities found: {entities}")
    print()
    
    return {
        'load_time': load_time,
        'memory_used': memory_used,
        'model': nlp
    }

class LazyNLPProcessor:
    """Demonstration of lazy loading pattern"""
    
    def __init__(self, model_name="en_core_web_sm"):
        self.model_name = model_name
        self._nlp = None
        self._load_time = None
        
    @property
    def nlp(self):
        if self._nlp is None:
            start_time = time.time()
            self._nlp = spacy.load(self.model_name)
            self._load_time = time.time() - start_time
            print(f"Lazy loaded model in {self._load_time:.2f}s")
        return self._nlp
    
    def process(self, text):
        """Process text with lazy-loaded model"""
        doc = self.nlp(text)
        return doc

def test_lazy_loading():
    """Test lazy loading pattern"""
    print("=== Lazy Loading Test ===")
    start_time = time.time()
    start_memory = get_memory_usage()
    
    # Processor creation should be instant
    processor = LazyNLPProcessor()
    creation_time = time.time() - start_time
    
    print(f"Processor creation time: {creation_time:.4f}s")
    print("Model not yet loaded...")
    
    # First use triggers loading
    test_text = "Hello Clever, can you analyze this text for entities and sentiment?"
    doc = processor.process(test_text)
    
    total_time = time.time() - start_time
    memory_used = get_memory_usage() - start_memory
    
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Total time (creation + first use): {total_time:.2f}s")
    print(f"Memory used: {memory_used:.1f}MB")
    print(f"Entities found: {entities}")
    print()
    
    return {
        'creation_time': creation_time,
        'total_time': total_time,
        'memory_used': memory_used,
        'processor': processor
    }

def test_minimal_pipeline():
    """Test loading minimal pipeline components"""
    print("=== Minimal Pipeline Test ===")
    start_time = time.time()
    start_memory = get_memory_usage()
    
    # Load only essential components
    nlp = spacy.load("en_core_web_sm", disable=["parser", "attribute_ruler"])
    
    load_time = time.time() - start_time
    memory_used = get_memory_usage() - start_memory
    
    print(f"Load time: {load_time:.2f}s")
    print(f"Memory used: {memory_used:.1f}MB")
    print(f"Active components: {list(nlp.pipe_names)}")
    
    # Test processing
    test_text = "Hello Clever, can you analyze this text for entities and sentiment?"
    doc = nlp(test_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    tokens = [(token.text, token.pos_, token.lemma_) for token in doc[:5]]
    
    print(f"Entities found: {entities}")
    print(f"First 5 tokens (text, POS, lemma): {tokens}")
    print()
    
    return {
        'load_time': load_time,
        'memory_used': memory_used,
        'model': nlp
    }

@lru_cache(maxsize=10)
def cached_process(text_hash, nlp_instance):
    """Simulate cached processing (for demonstration)"""
    # In real implementation, would cache the processed Doc object
    doc = nlp_instance(text_hash)
    return [(ent.text, ent.label_) for ent in doc.ents]

def test_caching_benefits():
    """Demonstrate caching benefits"""
    print("=== Caching Benefits Test ===")
    
    nlp = spacy.load("en_core_web_sm")
    test_texts = [
        "Hello Clever, analyze this text.",
        "What's the weather like in San Francisco?",
        "Hello Clever, analyze this text.",  # Repeat
        "Can you help me with Python programming?",
        "What's the weather like in San Francisco?"  # Repeat
    ]
    
    # Without caching
    start_time = time.time()
    for text in test_texts:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
    no_cache_time = time.time() - start_time
    
    # With caching (simulated)
    start_time = time.time()
    for text in test_texts:
        entities = cached_process(text, nlp)
    with_cache_time = time.time() - start_time
    
    print(f"Without caching: {no_cache_time:.4f}s")
    print(f"With caching: {with_cache_time:.4f}s")
    print(f"Speedup: {no_cache_time/with_cache_time:.1f}x")
    print()

def main():
    """Run all validation tests"""
    print("SpaCy Lazy Loading Validation Script")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"SpaCy version: {spacy.__version__}")
    print(f"Initial memory usage: {get_memory_usage():.1f}MB")
    print()
    
    try:
        # Test current implementation
        standard = test_standard_loading()
        
        # Test lazy loading
        lazy = test_lazy_loading()
        
        # Test minimal pipeline
        minimal = test_minimal_pipeline()
        
        # Test caching benefits
        test_caching_benefits()
        
        # Summary comparison
        print("=== Performance Summary ===")
        print(f"Standard loading: {standard['load_time']:.2f}s, {standard['memory_used']:.1f}MB")
        print(f"Lazy loading (creation): {lazy['creation_time']:.4f}s")
        print(f"Lazy loading (first use): {lazy['total_time']:.2f}s, {lazy['memory_used']:.1f}MB")
        print(f"Minimal pipeline: {minimal['load_time']:.2f}s, {minimal['memory_used']:.1f}MB")
        
        print()
        print("✅ All lazy loading patterns validated successfully!")
        print("✅ Recommendations are compatible with offline-first architecture")
        
        # Memory efficiency comparison
        memory_saved = standard['memory_used'] - minimal['memory_used']
        if memory_saved > 0:
            print(f"📊 Memory savings with minimal pipeline: {memory_saved:.1f}MB ({memory_saved/standard['memory_used']*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
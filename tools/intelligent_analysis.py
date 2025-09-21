#!/usr/bin/env python3
"""
Intelligent Code Analysis CLI Tool

Why: Provide developers with a powerful command-line interface to analyze
code quality, detect problems, and get actionable recommendations using
the enhanced Why/Where/How graph system. This makes the intelligent
analysis accessible outside the web interface.

Where: Run from project root as `python tools/intelligent_analysis.py`
or `python -m tools.intelligent_analysis`. Connects to intelligent_analyzer.py
and can output results in multiple formats for different use cases.

How: Uses argparse for CLI interface, calls intelligent analysis engine,
and formats results for terminal display with color coding, filtering,
and detailed recommendations. Supports multiple output formats.

Connects to:
    - intelligent_analyzer.py: Core analysis engine
    - introspection.py: Runtime state integration
    - app.py: Flask application analysis (when available)
"""
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from intelligent_analyzer import (
        get_intelligent_analysis, 
        analyze_single_component,
        get_fix_recommendations, 
        AnalysisResult
    )
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Intelligent analysis not available: {e}")
    ANALYSIS_AVAILABLE = False

# Terminal color codes
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

SEVERITY_COLORS = {
    'CRITICAL': Colors.RED + Colors.BOLD,
    'HIGH': Colors.RED,
    'MEDIUM': Colors.YELLOW,
    'LOW': Colors.CYAN
}

CATEGORY_COLORS = {
    'ARCHITECTURAL': Colors.RED,
    'PERFORMANCE': Colors.YELLOW,
    'DOCUMENTATION': Colors.CYAN,
    'SECURITY': Colors.MAGENTA + Colors.BOLD,
    'COUPLING': Colors.YELLOW,
    'COMPLEXITY': Colors.BLUE,
    'OPTIMIZATION': Colors.GREEN
}

def print_header(text: str, char: str = '='):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{char * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{char * 60}{Colors.END}")

def format_severity(severity: str) -> str:
    """Format severity with color."""
    color = SEVERITY_COLORS.get(severity, Colors.WHITE)
    return f"{color}{severity}{Colors.END}"

def format_category(category: str) -> str:
    """Format category with color.""" 
    color = CATEGORY_COLORS.get(category, Colors.WHITE)
    return f"{color}{category}{Colors.END}"

def print_analysis_result(result: AnalysisResult, show_details: bool = True):
    """Print a single analysis result with formatting."""
    print(f"\n{Colors.BOLD}📍 {result.title}{Colors.END}")
    print(f"   {format_category(result.category)} | {format_severity(result.severity)} | "
          f"Confidence: {result.confidence:.0%}")
    print(f"   📄 {Colors.BLUE}{result.node_id}{Colors.END}")
    
    if show_details:
        print(f"   💬 {result.description}")
        
        if result.fix_suggestions:
            print(f"   {Colors.GREEN}💡 Fix Suggestions:{Colors.END}")
            for i, suggestion in enumerate(result.fix_suggestions, 1):
                print(f"      {i}. {suggestion}")
        
        if result.performance_impact:
            print(f"   {Colors.YELLOW}⚡ Performance Impact:{Colors.END} {result.performance_impact}")
        
        if result.related_nodes:
            print(f"   {Colors.CYAN}🔗 Related Components:{Colors.END} {', '.join(result.related_nodes)}")

def print_quality_summary(analysis: Dict):
    """Print overall quality summary."""
    score = analysis.get('quality_score', 0)
    score_color = Colors.GREEN if score >= 80 else Colors.YELLOW if score >= 60 else Colors.RED
    
    print(f"\n{Colors.BOLD}📊 Code Quality Score: {score_color}{score:.1f}%{Colors.END}")
    
    # Problem counts by severity
    results = analysis.get('analysis_results', [])
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    category_counts = {}
    
    for result in results:
        severity_counts[result.severity] = severity_counts.get(result.severity, 0) + 1
        category_counts[result.category] = category_counts.get(result.category, 0) + 1
    
    print(f"\n{Colors.BOLD}🚨 Issues by Severity:{Colors.END}")
    for severity, count in severity_counts.items():
        if count > 0:
            print(f"   {format_severity(severity)}: {count}")
    
    print(f"\n{Colors.BOLD}📋 Issues by Category:{Colors.END}")
    for category, count in sorted(category_counts.items()):
        print(f"   {format_category(category)}: {count}")

def print_architectural_insights(insights: List):
    """Print architectural insights."""
    if not insights:
        return
        
    print_header("🏗️  ARCHITECTURAL INSIGHTS")
    
    for insight in insights:
        urgency_color = SEVERITY_COLORS.get(insight.urgency, Colors.WHITE)
        print(f"\n{Colors.BOLD}{insight.pattern_name}{Colors.END}")
        print(f"   {urgency_color}Urgency: {insight.urgency}{Colors.END} | "
              f"Effort: {insight.estimated_effort}")
        print(f"   {insight.description}")
        print(f"   {Colors.GREEN}📈 Business Impact:{Colors.END} {insight.business_impact}")
        
        if insight.recommended_actions:
            print(f"   {Colors.CYAN}🔧 Recommended Actions:{Colors.END}")
            for action in insight.recommended_actions:
                print(f"      • {action}")

def print_performance_recommendations(recommendations: List):
    """Print performance recommendations."""
    if not recommendations:
        return
        
    print_header("⚡ PERFORMANCE RECOMMENDATIONS")
    
    for rec in recommendations:
        print_analysis_result(rec)

def print_trend_analysis(trend_data: Dict):
    """Print trend analysis."""
    if not trend_data or trend_data.get('message'):
        print(f"\n{Colors.YELLOW}📈 Trend Analysis: {trend_data.get('message', 'No data available')}{Colors.END}")
        return
        
    print_header("📈 TREND ANALYSIS")
    
    trend = trend_data.get('quality_trend', 'stable')
    trend_symbol = {'improving': '↗️', 'declining': '↘️', 'stable': '→'}.get(trend, '→')
    trend_color = {'improving': Colors.GREEN, 'declining': Colors.RED, 'stable': Colors.YELLOW}.get(trend, Colors.WHITE)
    
    print(f"Quality Trend: {trend_color}{trend_symbol} {trend.title()}{Colors.END}")
    print(f"Current Score: {trend_data.get('current_quality_score', 0):.1f}%")
    print(f"Total Analyses: {trend_data.get('total_analyses', 0)}")
    print(f"Avg Issues/Analysis: {trend_data.get('average_issues_per_analysis', 0):.1f}")

def analyze_command(args):
    """Run comprehensive codebase analysis."""
    if not ANALYSIS_AVAILABLE:
        print(f"{Colors.RED}Error: Intelligent analysis not available{Colors.END}")
        return 1
        
    print_header("🧠 INTELLIGENT CODE ANALYSIS")
    print(f"Analyzing codebase... {Colors.CYAN}(this may take a moment){Colors.END}")
    
    start_time = time.time()
    analysis = get_intelligent_analysis(args.files)
    duration = time.time() - start_time
    
    if analysis.get('error'):
        print(f"{Colors.RED}Analysis failed: {analysis['error']}{Colors.END}")
        return 1
    
    print(f"Analysis completed in {duration:.2f}s")
    
    # Print quality summary
    print_quality_summary(analysis)
    
    # Filter results by severity if requested
    results = analysis.get('analysis_results', [])
    if args.severity:
        results = [r for r in results if r.severity.lower() == args.severity.lower()]
    
    # Filter by category if requested  
    if args.category:
        results = [r for r in results if r.category.lower() == args.category.lower()]
    
    # Sort by severity and confidence
    severity_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    results.sort(key=lambda r: (severity_order.get(r.severity, 0), r.confidence), reverse=True)
    
    # Print issues
    if results:
        print_header("🔍 IDENTIFIED ISSUES")
        for i, result in enumerate(results[:args.limit], 1):
            print(f"\n{Colors.BOLD}[{i}/{len(results)}]{Colors.END}")
            print_analysis_result(result, show_details=not args.summary)
    else:
        print(f"\n{Colors.GREEN}✅ No issues found matching the criteria!{Colors.END}")
    
    # Print additional sections
    if not args.summary:
        print_architectural_insights(analysis.get('architectural_insights', []))
        print_performance_recommendations(analysis.get('performance_recommendations', []))
        print_trend_analysis(analysis.get('trend_analysis', {}))
    
    # Output to file if requested
    if args.output:
        output_path = Path(args.output)
        if args.format == 'json':
            with open(output_path, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
        else:
            # TODO: Implement other formats
            print(f"{Colors.YELLOW}Warning: Only JSON output format is currently supported{Colors.END}")
        
        print(f"\n{Colors.GREEN}Results saved to: {output_path}{Colors.END}")
    
    return 0

def component_command(args):
    """Analyze a specific component."""
    if not ANALYSIS_AVAILABLE:
        print(f"{Colors.RED}Error: Intelligent analysis not available{Colors.END}")
        return 1
        
    component_path = args.component
    print_header(f"🔍 COMPONENT ANALYSIS: {component_path}")
    
    results = analyze_single_component(component_path)
    if not results:
        print(f"{Colors.GREEN}✅ No issues found in {component_path}{Colors.END}")
        return 0
    
    for result in results:
        print_analysis_result(result)
    
    return 0

def recommend_command(args):
    """Get fix recommendations for a specific issue."""
    if not ANALYSIS_AVAILABLE:
        print(f"{Colors.RED}Error: Intelligent analysis not available{Colors.END}")
        return 1
        
    recommendations = get_fix_recommendations(args.node_id, args.category)
    
    print_header(f"💡 FIX RECOMMENDATIONS")
    print(f"Node: {Colors.BLUE}{args.node_id}{Colors.END}")
    print(f"Category: {format_category(args.category)}")
    
    rec_data = recommendations.get('recommendations', {})
    if not rec_data:
        print(f"{Colors.YELLOW}No specific recommendations found for this category{Colors.END}")
        return 0
    
    for issue_type, fixes in rec_data.items():
        print(f"\n{Colors.BOLD}{issue_type.replace('_', ' ').title()}:{Colors.END}")
        for fix in fixes:
            print(f"  • {fix}")
    
    return 0

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Intelligent Code Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze                           # Full codebase analysis
  %(prog)s analyze --severity HIGH          # Only high severity issues
  %(prog)s analyze --category SECURITY      # Only security issues
  %(prog)s analyze --summary                # Brief summary only
  %(prog)s component app.py                 # Analyze specific file
  %(prog)s recommend app.py PERFORMANCE     # Fix recommendations
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze entire codebase')
    analyze_parser.add_argument('--files', nargs='*', help='Specific files to analyze')
    analyze_parser.add_argument('--severity', choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                               help='Filter by severity level')
    analyze_parser.add_argument('--category', 
                               choices=['ARCHITECTURAL', 'PERFORMANCE', 'DOCUMENTATION', 
                                       'SECURITY', 'COUPLING', 'COMPLEXITY', 'OPTIMIZATION'],
                               help='Filter by issue category')
    analyze_parser.add_argument('--limit', type=int, default=50, help='Maximum issues to show')
    analyze_parser.add_argument('--summary', action='store_true', help='Show summary only')
    analyze_parser.add_argument('--output', help='Output file path')
    analyze_parser.add_argument('--format', choices=['json', 'yaml', 'html'], default='json',
                               help='Output format')
    
    # Component command  
    component_parser = subparsers.add_parser('component', help='Analyze specific component')
    component_parser.add_argument('component', help='Path to component to analyze')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Get fix recommendations')
    recommend_parser.add_argument('node_id', help='Node ID (file or component path)')
    recommend_parser.add_argument('category', help='Issue category')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'analyze':
            return analyze_command(args)
        elif args.command == 'component':
            return component_command(args)
        elif args.command == 'recommend':
            return recommend_command(args)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Analysis interrupted by user{Colors.END}")
        return 130
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
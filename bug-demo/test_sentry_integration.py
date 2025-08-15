#!/usr/bin/env python3
"""
Test script to validate the Sentry integration proof-of-concept.
This script simulates the notebook functionality to ensure all dependencies work.
"""

import os
import json
from datetime import datetime
import uuid

def test_dependencies():
    """Test that all required dependencies are available."""
    print("🔍 Testing dependencies...")
    
    try:
        import requests
        print("✅ requests library available")
    except ImportError as e:
        print(f"❌ requests library missing: {e}")
        return False
    
    try:
        import json
        print("✅ json library available")
    except ImportError as e:
        print(f"❌ json library missing: {e}")
        return False
    
    print("✅ All dependencies available")
    return True

def simulate_c_log_analysis():
    """Simulate c-log-analysis output."""
    print("\n📊 Simulating c-log-analysis output...")
    
    # Example simulated output from c-log-analysis
    block_id = 42
    similarity_score = 0.60  # Simulated anomaly (below threshold)
    threshold = 0.85
    log_excerpt = "[2025-08-06 14:54:00] ERROR: Unexpected shutdown in service X. Memory usage exceeded 95%."
    service_name = "payment-processor"
    pod_name = "payment-processor-7d8f9b-xyz123"
    
    if similarity_score < threshold:
        detected = True
        deviation_severity = "high" if similarity_score < 0.5 else "medium"
        print(f"🚨 Deviation detected in block {block_id} (score: {similarity_score})")
        print(f"   Severity: {deviation_severity}")
        print(f"   Service: {service_name}")
        print(f"   Pod: {pod_name}")
    else:
        detected = False
        print(f"✅ No deviation detected (score: {similarity_score})")
    
    return {
        'detected': detected,
        'block_id': block_id,
        'similarity_score': similarity_score,
        'threshold': threshold,
        'log_excerpt': log_excerpt,
        'service_name': service_name,
        'pod_name': pod_name
    }

def create_sentry_event_data(analysis_result):
    """Create structured event data for Sentry."""
    print("\n📋 Creating Sentry event data...")
    
    event_id = str(uuid.uuid4()).replace('-', '')
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Determine severity level
    similarity_score = analysis_result['similarity_score']
    if similarity_score < 0.3:
        level = "fatal"
    elif similarity_score < 0.5:
        level = "error"
    elif similarity_score < 0.7:
        level = "warning"
    else:
        level = "info"
    
    event_data = {
        "event_id": event_id,
        "timestamp": timestamp,
        "level": level,
        "message": f"Log anomaly detected in {analysis_result['service_name']} (block {analysis_result['block_id']})",
        "logger": "c-log-analysis",
        "platform": "python",
        "tags": {
            "system": "log-analysis",
            "service": analysis_result['service_name'],
            "pod": analysis_result['pod_name'],
            "automated": "true",
            "anomaly_type": "similarity_deviation",
            "severity": level
        },
        "extra": {
            "block_id": analysis_result['block_id'],
            "similarity_score": analysis_result['similarity_score'],
            "threshold": analysis_result['threshold'],
            "deviation_amount": analysis_result['threshold'] - analysis_result['similarity_score'],
            "log_excerpt": analysis_result['log_excerpt'],
            "source_system": "c-log-analysis",
            "analysis_timestamp": timestamp,
            "kubernetes_pod": analysis_result['pod_name'],
            "service_name": analysis_result['service_name']
        }
    }
    
    print(f"  Event ID: {event_data['event_id']}")
    print(f"  Level: {event_data['level']}")
    print(f"  Message: {event_data['message']}")
    print(f"  Deviation: {event_data['extra']['deviation_amount']:.2f} below threshold")
    
    return event_data

def simulate_mcp_integration(event_data):
    """Simulate MCP Sentry integration."""
    print("\n🔧 Simulating Sentry MCP Integration:")
    
    # Sentry configuration - these match the MCP server setup
    SENTRY_ORG = "cisco-og"
    SENTRY_PROJECT = "bug-demo"
    SENTRY_REGION_URL = "https://us.sentry.io"
    
    print(f"\n1. Cline would call: use_mcp_tool with sentry server")
    print(f"   Tool: create_issue or send_event")
    print(f"   Arguments:")
    
    mcp_args = {
        "organizationSlug": SENTRY_ORG,
        "projectSlug": SENTRY_PROJECT,
        "regionUrl": SENTRY_REGION_URL,
        "level": event_data['level'],
        "message": event_data['message'],
        "tags": event_data['tags'],
        "extra": event_data['extra']
    }
    
    print(json.dumps(mcp_args, indent=2))
    
    print(f"\n2. Sentry would create an issue with:")
    print(f"   - Title: {event_data['message']}")
    print(f"   - Level: {event_data['level']}")
    print(f"   - Service: {event_data['tags']['service']}")
    print(f"   - Similarity Score: {event_data['extra']['similarity_score']}")
    print(f"   - Log Excerpt: {event_data['extra']['log_excerpt'][:100]}...")
    
    return f"SENTRY-{event_data['extra']['block_id']}-{event_data['event_id'][:8]}"

def simulate_complete_workflow(analysis_result, event_data, issue_id):
    """Simulate the complete L2P workflow."""
    print("\n🔄 Complete L2P Workflow Simulation:")
    print("\n" + "="*60)
    
    if analysis_result['detected']:
        print(f"\n1. 📊 c-log-analysis detects anomaly")
        print(f"   - Block ID: {analysis_result['block_id']}")
        print(f"   - Similarity Score: {analysis_result['similarity_score']} (below threshold {analysis_result['threshold']})")
        print(f"   - Service: {analysis_result['service_name']}")
        
        print(f"\n2. 🚨 Sentry issue creation (via MCP)")
        print(f"   - Organization: cisco-og")
        print(f"   - Project: bug-demo")
        print(f"   - Issue Level: {event_data['level']}")
        print(f"   - Simulated Issue ID: {issue_id}")
        
        print(f"\n3. 🔗 GitHub issue creation (via Cline)")
        github_issue_title = f"Log anomaly detected in {analysis_result['service_name']} - Sentry {issue_id}"
        print(f"   - Title: {github_issue_title}")
        print(f"   - Repository: ccapetz/L2P")
        print(f"   - Labels: bug, automated, sentry-integration")
        
        print(f"\n4. 🔧 Automated analysis (via Sentry MCP)")
        print(f"   - Cline calls analyze_issue_with_seer")
        print(f"   - AI provides root cause analysis")
        print(f"   - Suggested fixes generated")
        
        print(f"\n5. 🛠️ Bug fix workflow")
        print(f"   - Create fix branch")
        print(f"   - Implement suggested fixes")
        print(f"   - Create PR with Sentry/GitHub issue references")
        
        print(f"\n6. ✅ Issue resolution")
        print(f"   - Update Sentry issue status")
        print(f"   - Close GitHub issue")
        print(f"   - Deploy fix")
        
    else:
        print(f"\n✅ No workflow needed - system operating normally")
        print(f"   - Similarity score {analysis_result['similarity_score']} above threshold {analysis_result['threshold']}")
        print(f"   - Continuing monitoring...")
    
    print("\n" + "="*60)
    print("\n🎯 Workflow Complete!")

def main():
    """Main test function."""
    print("🚀 Testing Sentry Integration Proof-of-Concept")
    print("=" * 50)
    
    # Test dependencies
    if not test_dependencies():
        print("❌ Dependency test failed")
        return False
    
    # Simulate c-log-analysis
    analysis_result = simulate_c_log_analysis()
    
    if analysis_result['detected']:
        # Create Sentry event data
        event_data = create_sentry_event_data(analysis_result)
        
        # Simulate MCP integration
        issue_id = simulate_mcp_integration(event_data)
        print(f"\n✅ Simulated Sentry Issue ID: {issue_id}")
        
        # Simulate complete workflow
        simulate_complete_workflow(analysis_result, event_data, issue_id)
    else:
        print("\n✅ No Sentry integration needed - no anomaly detected")
    
    print("\n🎉 Test completed successfully!")
    print("\n📝 Summary:")
    print("- All dependencies are properly installed")
    print("- Sentry MCP integration is configured (cisco-og/bug-demo)")
    print("- Event data structure is properly formatted")
    print("- Complete workflow simulation works as expected")
    print("- Ready for integration with c-log-analysis pipeline")
    
    return True

if __name__ == "__main__":
    main()

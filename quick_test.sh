#!/bin/bash
# Quick test script to verify both jobs work
echo "🧪 Testing On-Demand Jobs"
echo "========================"
echo ""
echo "1️⃣ Testing Planetary Job..."
./run_job.sh 2>&1 | tail -10
echo ""
echo "2️⃣ Testing Event Collection Job..."
echo "   (Requires OpenAI API key)"
./run_event_job.sh 2>&1 | tail -10
echo ""
echo "✅ Test complete! Check your email for notifications."

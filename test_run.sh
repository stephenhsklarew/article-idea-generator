#!/bin/bash
# Test script to run DocIdeaGenerator with specific email and local output

echo "Running DocIdeaGenerator test..."
echo "Email filter: Prashant/Stephen"
echo "Output: Local markdown files"
echo "Model: qwen2.5:32b (Qwen - Local, Free)"
echo ""

# Use default test mode (Qwen 2.5 32B) and pipe 'y' to confirm save
echo "y" | python3 cli.py --email "Prashant/Stephen" --save-local

echo ""
echo "Test completed. Check current directory for generated .md files."

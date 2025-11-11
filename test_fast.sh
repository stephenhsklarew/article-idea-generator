#!/bin/bash
# Test script to run DocIdeaGenerator with fast mode (Gemini 2.5 Flash)

echo "Running DocIdeaGenerator test with --fast mode..."
echo "Email filter: Prashant/Stephen"
echo "Output: Local markdown files"
echo "Model: gemini-2.5-flash (Google - 300+ tok/s)"
echo ""

# Use fast mode and pipe 'y' to confirm save
echo "y" | python3 cli.py --email "Prashant/Stephen" --save-local --fast

echo ""
echo "Test completed. Check current directory for generated .md files."

#!/bin/bash

# Clean up any existing category directories and previous extractions to ensure a clean run
rm -rf archives café configs data documentation münchen naïve-bayes notes reports resources résumé scripts templates 日本語 docs project

# Step 1: Extract the ZIP file
# The zip file is located at ../files_to_reorganize.zip
unzip -o ../files_to_reorganize.zip

# Step 2: Move and rename files based on category
# We use find with -print0 and read -d '' to properly handle spaces and special characters in paths
find . -type f -name "*.txt" -print0 | while IFS= read -r -d '' file; do
  # Extract category from the first line starting with "category:"
  # We use tr -d '\r' to strip Windows line endings
  category=$(grep -m 1 "^category:" "$file" | cut -d' ' -f2- | tr -d '\r')
  
  if [ -n "$category" ]; then
    # Create directory for the category if it doesn't exist
    mkdir -p "$category"
    
    # Get relative path (removing leading ./)
    relpath="${file#./}"
    
    # Convert slashes to dashes
    newname=$(echo "$relpath" | tr '/' '-')
    
    # Move the file
    mv "$file" "$category/$newname"
  fi
done

# Step 3: Clean up empty directories
find . -type d -empty -delete

# Step 4: Generate and display hash
# Run this hash command on the clean directory (excluding reorganize.sh)
echo "Reorganization complete."

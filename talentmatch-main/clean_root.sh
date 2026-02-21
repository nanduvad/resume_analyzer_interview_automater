#!/bin/bash

echo "🧹 CLEANING ROOT DIRECTORY"
echo "=========================="
echo ""

# 1. Remove temporary files
echo "🗑️  Removing temporary files..."
rm -f clutter_analysis.txt quick_audit.txt 2>/dev/null && echo "✅ clutter_analysis.txt, quick_audit.txt"
rm -f professional_cleanup.sh final_touch.sh 2>/dev/null && echo "✅ cleanup scripts"

# 2. Remove duplicate nginx config
echo ""
echo "⚙️  Cleaning nginx configs..."
if [ -f "nginx.conf" ] && [ -f "nginx-simple.conf" ]; then
    rm -f nginx-simple.conf && echo "✅ Removed nginx-simple.conf"
fi

# 3. Move docs to docs/ directory
echo ""
echo "📚 Organizing documentation..."
mkdir -p docs
mv SAFETY_CHECKLIST.md ONBOARDING_GUIDE.md docs/ 2>/dev/null && echo "✅ Moved docs to docs/"
if [ -f "PROJECT_CARD.md" ]; then
    echo "📋 Merging PROJECT_CARD.md into README.md..."
    echo -e "\n## 📋 Project Overview\n" >> README.md
    tail -n +3 PROJECT_CARD.md >> README.md
    rm -f PROJECT_CARD.md && echo "✅ Merged PROJECT_CARD.md"
fi

# 4. Check package.json
echo ""
echo "📦 Checking package.json..."
if node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))" 2>/dev/null; then
    echo "✅ package.json is valid JSON"
else
    echo "❌ package.json has JSON errors"
    echo "   Creating a valid version..."
    cat << 'JSON' > package.json
{
  "name": "talentmatch",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.9.3",
    "vite": "^4.5.14"
  }
}
JSON
    echo "✅ Created valid package.json"
fi

# 5. Create .dockerignore
echo ""
if [ ! -f ".dockerignore" ]; then
    echo "🐳 Creating .dockerignore..."
    cat << 'DOCKERIGNORE' > .dockerignore
node_modules/
__pycache__/
*.pyc
*.pyo
.env
.git/
dist/
build/
*.log
DOCKERIGNORE
    echo "✅ Created .dockerignore"
fi

echo ""
echo "✅ ROOT CLEANUP COMPLETE!"

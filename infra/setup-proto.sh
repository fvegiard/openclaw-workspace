#!/bin/bash
# Proto + modern tool setup for OpenClaw agents
export PATH="$HOME/.proto/shims:$HOME/.proto/bin:$PATH"

echo "=== Proto Managed Environment ==="
echo "Node: $(node --version)"
echo "Python: $(python --version)"
python -c "import sys; print('No-GIL:', getattr(sys, '_is_gil_enabled', lambda: 'N/A')())"
echo "uv: $(uv --version)"

echo ""
echo "Pinned versions in .prototools:"
cat /home/fvegiard/.openclaw/workspace/.prototools

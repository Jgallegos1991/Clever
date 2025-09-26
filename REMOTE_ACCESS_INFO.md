# Clever Remote Access via Tailscale

## 🧠 Access Your Digital Brain Extension Remotely

### Primary Access URL:
**http://100.124.203.114:5000**

### From Your Other Devices:
- **Chromebook**: Open browser → http://100.124.203.114:5000
- **Samsung Phone**: Browser → http://100.124.203.114:5000  
- **Any Tailscale Device**: http://100.124.203.114:5000

### API Endpoints for Advanced Usage:
- **Chat**: POST http://100.124.203.114:5000/api/chat
- **Document Analysis**: POST http://100.124.203.114:5000/api/query_documents
- **Cognitive Sovereignty**: GET http://100.124.203.114:5000/api/cognitive_sovereignty/status

### Connected Devices in Your Network:
- **penguin**: 100.124.203.114 (linux) - -
- **chromeos-google-dedede**: 100.98.119.50 (android) - offline
- **samsung-sm-a125u**: 100.72.156.1 (android) - offline


### Security Notes:
- ✅ **Private Network**: Only accessible within your Tailscale network
- ✅ **Encrypted**: All traffic encrypted via WireGuard
- ✅ **No External Access**: Complete digital sovereignty maintained
- ✅ **Gmail Account**: Authenticated via lapirfta@gmail.com

### Quick Commands:
```bash
# Check Clever is running
curl http://100.124.203.114:5000

# Quick chat test  
curl -X POST http://100.124.203.114:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Clever!"}' 

# Check cognitive sovereignty status
curl http://100.124.203.114:5000/api/cognitive_sovereignty/status
```

### Mobile Bookmarks:
Create these bookmarks on your phone/tablet for instant Clever access:
- **Clever Home**: http://100.124.203.114:5000
- **Clever Chat**: http://100.124.203.114:5000 (same interface)

---
*Generated: 1758897945.1022882*
*Tailscale IP: 100.124.203.114*
*Network Status: Connected*

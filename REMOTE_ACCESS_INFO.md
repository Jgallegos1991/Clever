# Clever Remote Access via Tailscale

## 🧠 Access Your Digital Brain Extension Remotely

### Primary Access URL:
**http://100.124.203.114:5001**

### From Your Other Devices:
- **Chromebook**: Open browser → http://100.124.203.114:5001
- **Samsung Phone**: Browser → http://100.124.203.114:5001  
- **Any Tailscale Device**: http://100.124.203.114:5001

### API Endpoints for Advanced Usage:
- **Chat**: POST http://100.124.203.114:5001/api/chat
- **Document Analysis**: POST http://100.124.203.114:5001/api/query_documents
- **Cognitive Sovereignty**: GET http://100.124.203.114:5001/api/cognitive_sovereignty/status
- **Network Status**: GET http://100.124.203.114:5001/api/network-status

### Connected Devices in Your Network:
- **penguin**: 100.124.203.114 (linux) - -
- **chromeos-google-dedede**: 100.98.119.50 (android) - offline
- **samsung-sm-a125u**: 100.72.156.1 (android) - idle,


### Security Notes:
- ✅ **Private Network**: Only accessible within your Tailscale network
- ✅ **Encrypted**: All traffic encrypted via WireGuard
- ✅ **No External Access**: Complete digital sovereignty maintained
- ✅ **Gmail Account**: Authenticated via lapirfta@gmail.com

### Quick Commands:
```bash
# Check Clever is running
curl http://{tailscale_ip}:5001

# Quick chat test  
curl -X POST http://{tailscale_ip}:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{{"message": "Hello Clever!"}}' 

# Check network status
curl http://{tailscale_ip}:5001/api/network-status
```

### Mobile Bookmarks:
Create these bookmarks on your phone/tablet for instant Clever access:
- **Clever Home**: http://{tailscale_ip}:5001
- **Clever Chat**: http://{tailscale_ip}:5001 (same interface)

---
*Generated: {Path(__file__).stat().st_mtime if Path(__file__).exists() else 'now'}*
*Tailscale IP: {tailscale_ip}*
*Network Status: {'Connected' if status['connected'] else 'Disconnected'}*

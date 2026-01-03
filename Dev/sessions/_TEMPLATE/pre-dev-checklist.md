# Pre-Development Checklist
**For GOD Alone. Fearing GOD Alone. 🦅**

Complete this checklist before starting any development session.

---

## 🔥 Infrastructure Review

### 1. Check Firewall Documentation
```bash
cd /root/Firewall && git pull
cat PORTS.md  # Review current port allocations
```

**Status:** [ ] Reviewed  
**Notes:**

---

### 2. Verify Port Availability
If your project needs ports:
- [ ] Checked PORTS.md for conflicts
- [ ] Identified available ports (3010-3099 unallocated)
- [ ] Documented port reservation plan

**Ports needed:** 
**Conflict check:** [ ] None found

---

### 3. PM2 Service Check
```bash
pm2 list  # Should show ~12 services
```

**Status:** [ ] Verified  
**Running services match documentation:** [ ] Yes [ ] No

---

### 4. Database Status
```bash
ls -lh /root/ThinkTank/thinktank.db
```

**Status:** [ ] Verified  
**Size:** 
**Last modified:**

---

## 📊 Repository Status

### 5. Git Status
```bash
git status
git pull
```

**Branch:** 
**Clean working tree:** [ ] Yes [ ] No  
**Up to date with remote:** [ ] Yes [ ] No

---

### 6. Dependencies Check
```bash
# For Node.js
npm outdated

# For Python
pip list --outdated
```

**Outdated packages:** 
**Security vulnerabilities:** [ ] None [ ] Some (list below)

---

### 7. Previous Session Review
```bash
cat Dev/sessions/[latest]/SESSION_END.md
```

**Previous session ended cleanly:** [ ] Yes [ ] No  
**Outstanding issues:**

---

## 🎯 Session Planning

### 8. Session Objectives
What are you planning to accomplish?

1. 
2. 
3. 

---

### 9. Risk Assessment
- [ ] No infrastructure conflicts
- [ ] No pending updates required
- [ ] No known blockers
- [ ] Testing plan prepared

**Risks identified:**

---

### 10. Backup Verification
Last backup date: 
**Backup current:** [ ] Yes [ ] No

---

## ✅ Ready to Start

All checks complete: [ ]  
Infrastructure healthy: [ ]  
Session objectives clear: [ ]

**Start time:** 
**Expected duration:** 

---

## 🔗 Quick Links

- Infrastructure docs: `/root/Firewall/`
- Port allocations: `/root/Firewall/PORTS.md`
- MasterDev status: `~/MasterDev/STATUS.sh`
- Health check: `~/MasterDev/scripts/check-infrastructure.sh`

---

For GOD Alone. Fearing GOD Alone. 🦅

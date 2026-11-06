# Hosting readiness checklist

- [ ] Secrets changed; .env not committed
- [ ] VPS OS patched and SSH hardened
- [ ] Domain DNS points to VPS
- [ ] HTTPS reverse proxy and automatic certificates
- [ ] Only 80/443 publicly exposed; database internal only
- [ ] Backup schedule and restore test
- [ ] Upload storage quota/retention set
- [ ] API key rotation procedure
- [ ] Dashboard auth (accounts/roles) implemented before multi-user use
- [ ] Test screenshots per supported chart theme, asset and timeframe
- [ ] Analyze latency and false alerts on held-out data

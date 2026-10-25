# Security

* ensure ssh key is installed and then harden ssh
* block cockpit port
* configure fail2ban

## fail2ban

`fail2ban` bans IPs on all ports when they fail to authenticate with sshd.
Other roles add their own jails (e.g. authelia), which use the defaults below.

Configuration options:

* `security_fail2ban_ignoreip` (**required**): IP (`192.168.1.5`), IP range
  (`192.168.1.0/24`) or list of IPs to exempt from banning (in addition to
  default loopback addresses); these should be your IPs so you do not
  accidentally ban yourself.
* `security_fail2ban_sshd_jail` (optional, default `true`): `true` to enable
  or `false` to disable sshd jail
* `security_fail2ban_maxretry` (optional, default `3`): number of failed
  authentication attempts until banned
* `security_fail2ban_findtime` (optional, default `1h`): timeframe for repeated
  failed authentication attempts
* `security_fail2ban_bantime` (optional, default `1d`): how long an IP is banned
  (increases for repeat offenders)
* `security_fail2ban_bantime_maxtime` (optional, default `4w`): max ban time
  for repeat offenders
* `security_fail2ban_dbpurgeage` (optional, default `30d`): after what time to
  forget offenders

Manage fail2ban:

* `sudo fail2ban-client banned`: list banned IPs
* `sudo fail2ban-client unban <IP>`: unban an IP
* `sudo fail2ban-client set sshd banip <IP>`: ban an IP in the sshd jail

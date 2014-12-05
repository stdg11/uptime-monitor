uptime-monitor
==============

## Rotate Log Files

To rotate the log file place the following in /etc/logrotate.d/uptime-monitor

/usr/share/nginx/uptime-monitor/*.log {
        daily
        missingok
        rotate 7
        compress
        notifempty
        nocreate
    }

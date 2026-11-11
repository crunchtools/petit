Nov 09 16:59:59 host01.example.net systemd[1]: systemd-localed.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-localed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd-logind[663]: System is rebooting.
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=70 op=UNLOAD
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=69 op=UNLOAD
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=68 op=UNLOAD
Nov 09 16:59:59 host01.example.net systemd-logind[663]: The system will reboot now!
Nov 09 16:59:59 host01.example.net systemd[1]: Removed slice system-modprobe.slice - Slice /system/modprobe.
Nov 09 16:59:59 host01.example.net systemd[1]: Removed slice system-sshd\x2dkeygen.slice - Slice /system/sshd-keygen.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target cloud-init.target - Cloud-init target.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target nss-lookup.target - Host and Network Name Lookups.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target remote-cryptsetup.target - Remote Encrypted Volumes.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target remote-veritysetup.target - Remote Verity Protected Volumes.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target timers.target - Timer Units.
Nov 09 16:59:59 host01.example.net systemd[1]: dnf-makecache.timer: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped dnf-makecache.timer - dnf5 makecache.
Nov 09 16:59:59 host01.example.net systemd[1]: fstrim.timer: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped fstrim.timer - Discard unused filesystem blocks once a week.
Nov 09 16:59:59 host01.example.net systemd[1]: logrotate.timer: Deactivated successfully.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-final comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-config comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-load-credentials comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net sshd[788]: Received signal 15; terminating.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped logrotate.timer - Daily rotation of log files.
Nov 09 16:59:59 host01.example.net chronyd[649]: chronyd exiting
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-tmpfiles-clean.timer: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-tmpfiles-clean.timer - Daily Cleanup of Temporary Directories.
Nov 09 16:59:59 host01.example.net systemd[1]: unbound-anchor.timer: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped unbound-anchor.timer - daily update of the root trust anchor for DNSSEC.
Nov 09 16:59:59 host01.example.net systemd[1]: lvm2-lvmpolld.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed lvm2-lvmpolld.socket - LVM2 poll daemon socket.
Nov 09 16:59:59 host01.example.net systemd[1]: cloud-final.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped cloud-final.service - Cloud-init: Final Stage.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target multi-user.target - Multi-User System.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target getty.target - Login Prompts.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping chronyd.service - NTP client/server...
Nov 09 16:59:59 host01.example.net systemd[1]: cloud-config.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped cloud-config.service - Cloud-init: Config Stage.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target cloud-config.target - Cloud-config availability.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target network-online.target - Network is Online.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping dracut-shutdown.service - Restore /run/initramfs on shutdown...
Nov 09 16:59:59 host01.example.net systemd[1]: grub2-systemd-integration.service - Grub2 systemctl reboot --boot-loader-menu=... support skipped, unmet condition check ConditionPathExists=/run/systemd/reboot-to-boot-loader-menu
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping kmsconvt@tty1.service - KMS System Console on tty1...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping serial-getty@ttyS0.service - Serial Getty on ttyS0...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping sshd.service - OpenSSH server daemon...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-logind.service - User Login Management...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-oomd.service - Userspace Out-Of-Memory (OOM) Killer...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-random-seed.service - Load/Save OS Random Seed...
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-udev-load-credentials.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-udev-load-credentials.service - Load udev Rules from Credentials.
Nov 09 16:59:59 host01.example.net systemd[1]: chronyd.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped chronyd.service - NTP client/server.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=chronyd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-oomd.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-oomd.service - Userspace Out-Of-Memory (OOM) Killer.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-oomd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-logind.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-logind.service - User Login Management.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-logind comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: sshd.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped sshd.service - OpenSSH server daemon.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=sshd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: serial-getty@ttyS0.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped serial-getty@ttyS0.service - Serial Getty on ttyS0.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=serial-getty@ttyS0 comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: kmsconvt@tty1.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped kmsconvt@tty1.service - KMS System Console on tty1.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=kmsconvt@tty1 comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: dracut-shutdown.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped dracut-shutdown.service - Restore /run/initramfs on shutdown.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=dracut-shutdown comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-random-seed.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-random-seed.service - Load/Save OS Random Seed.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-random-seed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=58 op=UNLOAD
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=60 op=UNLOAD
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=54 op=UNLOAD
Nov 09 16:59:59 host01.example.net systemd[1]: Removed slice system-kmsconvt.slice - Slice /system/kmsconvt.
Nov 09 16:59:59 host01.example.net systemd[1]: Removed slice system-serial\x2dgetty.slice - Slice /system/serial-getty.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target sshd-keygen.target.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-user-sessions.service - Permit User Sessions...
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-user-sessions.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-user-sessions.service - Permit User Sessions.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-user-sessions comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target network.target - Network.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target nss-user-lookup.target - User and Group Name Lookups.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target remote-fs.target - Remote File Systems.
Nov 09 16:59:59 host01.example.net systemd[1]: authselect-apply-changes.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped authselect-apply-changes.service - Apply authselect changes.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=authselect-apply-changes comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: cloud-init-network.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped cloud-init-network.service - Cloud-init: Network Stage.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-init-network comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: NetworkManager-wait-online.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped NetworkManager-wait-online.service - Network Manager Wait Online.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=NetworkManager-wait-online comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping NetworkManager.service - Network Manager...
Nov 09 16:59:59 host01.example.net NetworkManager[676]: <info>  [1794243599.7181] caught SIGTERM, shutting down normally.
Nov 09 16:59:59 host01.example.net NetworkManager[676]: <info>  [1794243599.7210] dhcp4 (enp0s4): canceled DHCP transaction
Nov 09 16:59:59 host01.example.net NetworkManager[676]: <info>  [1794243599.7212] dhcp4 (enp0s4): activation: beginning transaction (timeout in 45 seconds)
Nov 09 16:59:59 host01.example.net NetworkManager[676]: <info>  [1794243599.7212] dhcp4 (enp0s4): state changed no lease
Nov 09 16:59:59 host01.example.net NetworkManager[676]: <info>  [1794243599.7215] manager: NetworkManager state is now CONNECTED_SITE
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-homed-activate.service - Home Area Activation...
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-userdb-load-credentials.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-userdb-load-credentials.service - Load JSON user/group Records from Credentials.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-userdb-load-credentials comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net NetworkManager[676]: <info>  [1794243599.7329] exiting (success)
Nov 09 16:59:59 host01.example.net dbus-broker-launch[645]: Activation request for 'org.freedesktop.nm_dispatcher' failed.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-homed-activate.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-homed-activate.service - Home Area Activation.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-homed-activate comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-homed.service - Home Area Manager...
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=67 op=UNLOAD
Nov 09 16:59:59 host01.example.net systemd[1]: NetworkManager.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped NetworkManager.service - Network Manager.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=NetworkManager comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-homed.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-homed.service - Home Area Manager.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-homed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target basic.target - Basic System.
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=59 op=UNLOAD
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target network-pre.target - Preparation for Network.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target paths.target - Path Units.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target slices.target - Slice Units.
Nov 09 16:59:59 host01.example.net systemd[1]: Removed slice user.slice - User and Session Slice.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target sockets.target - Socket Units.
Nov 09 16:59:59 host01.example.net systemd[1]: sshd-unix-local.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed sshd-unix-local.socket - OpenSSH Server Socket (systemd-ssh-generator, AF_UNIX Local).
Nov 09 16:59:59 host01.example.net systemd[1]: sssd-kcm.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed sssd-kcm.socket - SSSD Kerberos Cache Manager responder socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-hostnamed.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-hostnamed.socket - Hostname Service Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-logind-varlink.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-logind-varlink.socket - User Login Management Varlink Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-mute-console.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-mute-console.socket - Console Output Muting Service Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-oomd.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-oomd.socket - Userspace Out-Of-Memory (OOM) Killer Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-repart.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-repart.socket - Disk Repartitioning Service Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-report-cgroup.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-report-cgroup.socket - CGroup Report Varlink Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-report-files.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-report-files.socket - Report Files Metrics Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-report-sign-plain.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-report-sign-plain.socket - Report Signing Socket (Local Software Key).
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-storage-fs.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-storage-fs.socket - Simple File System Backed Storage Provider.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-sysinstall.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-sysinstall.socket - System Install Tool.
Nov 09 16:59:59 host01.example.net systemd[1]: cloud-init-local.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped cloud-init-local.service - Cloud-init: Local Stage (pre-network).
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-init-local comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net dbus-broker[646]: Dispatched 1445 messages @ 4(±14)μs / message.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping dbus-broker.service - D-Bus System Message Bus...
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-network-generator.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-network-generator.service - Generate Network Units from Kernel Command Line.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-network-generator comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: dbus-broker.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped dbus-broker.service - D-Bus System Message Bus.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=dbus-broker comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: dbus.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed dbus.socket - D-Bus System Message Bus Socket.
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=57 op=UNLOAD
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target sysinit.target - System Initialization.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target clonesetup.target - Local dm-clone Devices.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target cryptsetup.target - Local Encrypted Volumes.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-ask-password-console.path: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-ask-password-console.path - Dispatch Password Requests to Console Directory Watch.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-ask-password-wall.path: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-ask-password-wall.path - Forward Password Requests to Wall Directory Watch.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target imports.target - Image Downloads.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target integritysetup.target - Local Integrity Protected Volumes.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target veritysetup.target - Local Verity Protected Volumes.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-binfmt.service - Set Up Additional Binary Formats...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-resolved.service - Network Name Resolution...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-update-utmp.service - Record System Boot/Shutdown in UTMP...
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-resolved.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-resolved.service - Network Name Resolution.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-resolved comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-binfmt.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-binfmt.service - Set Up Additional Binary Formats.
Nov 09 16:59:59 host01.example.net audit[849]: SYSTEM_SHUTDOWN pid=849 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg=' comm="update-utmp" exe="/usr/lib/systemd/systemd-update-utmp" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-binfmt comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-update-utmp.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-update-utmp.service - Record System Boot/Shutdown in UTMP.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-update-utmp comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net audit: BPF prog-id=48 op=UNLOAD
Nov 09 16:59:59 host01.example.net systemd[1]: proc-sys-fs-binfmt_misc.automount: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Unset automount proc-sys-fs-binfmt_misc.automount - Arbitrary Executable File Formats File System Automount Point.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-resolved-monitor.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-resolved-monitor.socket - Resolve Monitor Varlink Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-resolved-varlink.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-resolved-varlink.socket - Resolve Service Varlink Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping auditd.service - Security Audit Logging Service...
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-sysctl.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-sysctl.service - Apply Kernel Variables.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-sysctl comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-coredump.socket: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Closed systemd-coredump.socket - Process Core Dump Socket.
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-modules-load.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-modules-load.service - Load Kernel Modules.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-modules-load comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: proc-sys-fs-binfmt_misc.mount: Deactivated successfully.
Nov 09 16:59:59 host01.example.net auditd[603]: The audit daemon is exiting.
Nov 09 16:59:59 host01.example.net audit: CONFIG_CHANGE op=set audit_pid=0 old=603 auid=4294967295 ses=4294967295 subj=system_u:system_r:auditd_t:s0 res=1
Nov 09 16:59:59 host01.example.net kernel: kauditd_printk_skb: 27 callbacks suppressed
Nov 09 16:59:59 host01.example.net kernel: audit: type=1305 audit(1794243599.877:128): op=set audit_pid=0 old=603 auid=4294967295 ses=4294967295 subj=system_u:system_r:auditd_t:s0 res=1
Nov 09 16:59:59 host01.example.net systemd[1]: auditd.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped auditd.service - Security Audit Logging Service.
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=auditd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: systemd-tmpfiles-setup.service: Deactivated successfully.
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped systemd-tmpfiles-setup.service - Create System Files and Directories.
Nov 09 16:59:59 host01.example.net kernel: audit: type=1131 audit(1794243599.883:129): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=auditd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-tmpfiles-setup comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: Stopped target local-fs.target - Local File Systems.
Nov 09 16:59:59 host01.example.net kernel: audit: type=1131 audit(1794243599.889:130): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-tmpfiles-setup comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 16:59:59 host01.example.net systemd[1]: Unmounting boot-efi.mount - /boot/efi...
Nov 09 16:59:59 host01.example.net systemd[1]: Unmounting home.mount - /home...
Nov 09 16:59:59 host01.example.net systemd[1]: Unmounting tmp.mount - Temporary Directory /tmp...
Nov 09 16:59:59 host01.example.net systemd[1]: Stopping systemd-journal-flush.service - Flush Journal to Persistent Storage...
Nov 09 17:00:06 localhost kernel: Linux version 7.2.11-300.fc45.x86_64 (mockbuild@00000000000000000000000000000000) (gcc (GCC) 16.2.1 20260819 (Red Hat 16.2.1-2), GNU ld version 2.47.20260726) #1 SMP PREEMPT_DYNAMIC Thu Oct 15 17:29:26 UTC 2026
Nov 09 17:00:06 localhost kernel: Command line: BOOT_IMAGE=(hd0,gpt3)/boot/vmlinuz-7.2.11-300.fc45.x86_64 no_timer_check console=tty1 console=ttyS0,115200n8 systemd.firstboot=off root=UUID=00000000-0000-0000-0000-000000000000 rootflags=subvol=root
Nov 09 17:00:06 localhost kernel: BIOS-provided physical RAM map:
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff]  System RAM
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [gap 0x00000000000a0000-0x00000000000effff]
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x0000000000100000-0x000000007ffd5fff]  System RAM
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x000000007ffd6000-0x000000007fffffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [gap 0x0000000080000000-0x00000000afffffff]
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x00000000b0000000-0x00000000bfffffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [gap 0x00000000c0000000-0x00000000fed1bfff]
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x00000000fed1c000-0x00000000fed1ffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [gap 0x00000000fed20000-0x00000000feffbfff]
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x00000000feffc000-0x00000000feffffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [gap 0x00000000ff000000-0x00000000fffbffff]
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff]  device reserved
Nov 09 17:00:06 localhost kernel: BIOS-e820: [gap 0x0000000100000000-0x000000fcffffffff]
Nov 09 17:00:06 localhost kernel: BIOS-e820: [mem 0x000000fd00000000-0x000000ffffffffff]  device reserved
Nov 09 17:00:06 localhost kernel: NX (Execute Disable) protection: active
Nov 09 17:00:06 localhost kernel: APIC: Static calls initialized
Nov 09 17:00:06 localhost kernel: DMI: SMBIOS 3.0.0 present.
Nov 09 17:00:06 localhost kernel: DMI: QEMU Standard PC (Q35 + ICH9, 2009), BIOS 1.16.3-debian-1.16.3-2 04/01/2014
Nov 09 17:00:06 localhost kernel: DMI: Memory slots populated: 1/1
Nov 09 17:00:06 localhost kernel: Hypervisor detected: KVM
Nov 09 17:00:06 localhost kernel: last_pfn = 0x7ffd6 max_arch_pfn = 0x400000000
Nov 09 17:00:06 localhost kernel: kvm-clock: Using msrs 4b564d01 and 4b564d00
Nov 09 17:00:06 localhost kernel: kvm-clock: using sched offset of 83122386984 cycles
Nov 09 17:00:06 localhost kernel: clocksource: kvm-clock: mask: 0xffffffffffffffff max_cycles: 0x1cd42e4dffb, max_idle_ns: 881590591483 ns
Nov 09 17:00:06 localhost kernel: tsc: Detected 2596.132 MHz processor
Nov 09 17:00:06 localhost kernel: e820: update [mem 0x00000000-0x00000fff] System RAM ==> device reserved
Nov 09 17:00:06 localhost kernel: e820: remove [mem 0x000a0000-0x000fffff] System RAM
Nov 09 17:00:06 localhost kernel: last_pfn = 0x7ffd6 max_arch_pfn = 0x400000000
Nov 09 17:00:06 localhost kernel: MTRR map: 4 entries (3 fixed + 1 variable; max 19), built from 8 variable MTRRs
Nov 09 17:00:06 localhost kernel: x86/PAT: Configuration [0-7]: WB  WC  UC- UC  WB  WP  UC- WT  
Nov 09 17:00:06 localhost kernel: found SMP MP-table at [mem 0x000f5460-0x000f546f]
Nov 09 17:00:06 localhost kernel: Using GB pages for direct mapping
Nov 09 17:00:06 localhost kernel: RAMDISK: [mem 0x327ed000-0x353eefff]
Nov 09 17:00:06 localhost kernel: ACPI: Early table checksum verification disabled
Nov 09 17:00:06 localhost kernel: ACPI: RSDP 0x00000000000F52A0 000014 (v00 BOCHS )
Nov 09 17:00:06 localhost kernel: ACPI: RSDT 0x000000007FFE239C 000038 (v01 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: FACP 0x000000007FFE218C 0000F4 (v03 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: DSDT 0x000000007FFE0040 00214C (v01 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: FACS 0x000000007FFE0000 000040
Nov 09 17:00:06 localhost kernel: ACPI: APIC 0x000000007FFE2280 000080 (v03 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: HPET 0x000000007FFE2300 000038 (v01 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: MCFG 0x000000007FFE2338 00003C (v01 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: WAET 0x000000007FFE2374 000028 (v01 BOCHS  BXPC     00000001 BXPC 00000001)
Nov 09 17:00:06 localhost kernel: ACPI: Reserving FACP table memory at [mem 0x7ffe218c-0x7ffe227f]
Nov 09 17:00:06 localhost kernel: ACPI: Reserving DSDT table memory at [mem 0x7ffe0040-0x7ffe218b]
Nov 09 17:00:06 localhost kernel: ACPI: Reserving FACS table memory at [mem 0x7ffe0000-0x7ffe003f]
Nov 09 17:00:06 localhost kernel: ACPI: Reserving APIC table memory at [mem 0x7ffe2280-0x7ffe22ff]
Nov 09 17:00:06 localhost kernel: ACPI: Reserving HPET table memory at [mem 0x7ffe2300-0x7ffe2337]
Nov 09 17:00:06 localhost kernel: ACPI: Reserving MCFG table memory at [mem 0x7ffe2338-0x7ffe2373]
Nov 09 17:00:06 localhost kernel: ACPI: Reserving WAET table memory at [mem 0x7ffe2374-0x7ffe239b]
Nov 09 17:00:06 localhost kernel: No NUMA configuration found
Nov 09 17:00:06 localhost kernel: Faking a node at [mem 0x0000000000000000-0x000000007ffd5fff]
Nov 09 17:00:06 localhost kernel: NODE_DATA(0) allocated [mem 0x7ffaaf80-0x7ffd5fff]
Nov 09 17:00:06 localhost kernel: ACPI: PM-Timer IO Port: 0x608
Nov 09 17:00:06 localhost kernel: ACPI: LAPIC_NMI (acpi_id[0xff] dfl dfl lint[0x1])
Nov 09 17:00:06 localhost kernel: IOAPIC[0]: apic_id 0, version 17, address 0xfec00000, GSI 0-23
Nov 09 17:00:06 localhost kernel: ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
Nov 09 17:00:06 localhost kernel: ACPI: INT_SRC_OVR (bus 0 bus_irq 5 global_irq 5 high level)
Nov 09 17:00:06 localhost kernel: ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
Nov 09 17:00:06 localhost kernel: ACPI: INT_SRC_OVR (bus 0 bus_irq 10 global_irq 10 high level)
Nov 09 17:00:06 localhost kernel: ACPI: INT_SRC_OVR (bus 0 bus_irq 11 global_irq 11 high level)
Nov 09 17:00:06 localhost kernel: ACPI: Using ACPI (MADT) for SMP configuration information
Nov 09 17:00:06 localhost kernel: ACPI: HPET id: 0x8086a201 base: 0xfed00000
Nov 09 17:00:06 localhost kernel: TSC deadline timer available
Nov 09 17:00:06 localhost kernel: CPU topo: Max. logical packages:   1
Nov 09 17:00:06 localhost kernel: CPU topo: Max. logical nodes:      1
Nov 09 17:00:06 localhost kernel: CPU topo: Num. nodes per package:  1
Nov 09 17:00:06 localhost kernel: CPU topo: Max. logical dies:       1
Nov 09 17:00:06 localhost kernel: CPU topo: Max. dies per package:   1
Nov 09 17:00:06 localhost kernel: CPU topo: Max. threads per core:   1
Nov 09 17:00:06 localhost kernel: CPU topo: Num. cores per package:     2
Nov 09 17:00:06 localhost kernel: CPU topo: Num. threads per package:   2
Nov 09 17:00:06 localhost kernel: CPU topo: Allowing 2 present CPUs plus 0 hotplug CPUs
Nov 09 17:00:06 localhost kernel: kvm-guest: APIC: eoi() replaced with kvm_guest_apic_eoi_write()
Nov 09 17:00:06 localhost kernel: kvm-guest: KVM setup pv remote TLB flush
Nov 09 17:00:06 localhost kernel: kvm-guest: setup PV sched yield
Nov 09 17:00:06 localhost kernel: PM: hibernation: Registered nosave memory: [mem 0x00000000-0x00000fff]
Nov 09 17:00:06 localhost kernel: PM: hibernation: Registered nosave memory: [mem 0x0009f000-0x000fffff]
Nov 09 17:00:06 localhost kernel: [gap 0xc0000000-0xfed1bfff] available for PCI devices
Nov 09 17:00:06 localhost kernel: Booting paravirtualized kernel on KVM
Nov 09 17:00:06 localhost kernel: clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1910969940391419 ns
Nov 09 17:00:06 localhost kernel: Zone ranges:
Nov 09 17:00:06 localhost kernel:   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
Nov 09 17:00:06 localhost kernel:   DMA32    [mem 0x0000000001000000-0x000000007ffd5fff]
Nov 09 17:00:06 localhost kernel:   Normal   empty
Nov 09 17:00:06 localhost kernel:   Device   empty
Nov 09 17:00:06 localhost kernel: Movable zone start for each node
Nov 09 17:00:06 localhost kernel: Early memory node ranges
Nov 09 17:00:06 localhost kernel:   node   0: [mem 0x0000000000001000-0x000000000009efff]
Nov 09 17:00:06 localhost kernel:   node   0: [mem 0x0000000000100000-0x000000007ffd5fff]
Nov 09 17:00:06 localhost kernel: Initmem setup node 0 [mem 0x0000000000001000-0x000000007ffd5fff]
Nov 09 17:00:06 localhost kernel: On node 0, zone DMA: 1 pages in unavailable ranges
Nov 09 17:00:06 localhost kernel: On node 0, zone DMA: 97 pages in unavailable ranges
Nov 09 17:00:06 localhost kernel: On node 0, zone DMA32: 42 pages in unavailable ranges
Nov 09 17:00:06 localhost kernel: setup_percpu: NR_CPUS:8192 nr_cpumask_bits:2 nr_cpu_ids:2 nr_node_ids:1
Nov 09 17:00:06 localhost kernel: percpu: Embedded 85 pages/cpu s225280 r8192 d114688 u1048576
Nov 09 17:00:06 localhost kernel: pcpu-alloc: s225280 r8192 d114688 u1048576 alloc=1*2097152
Nov 09 17:00:06 localhost kernel: pcpu-alloc: [0] 0 1 
Nov 09 17:00:06 localhost kernel: kvm-guest: PV spinlocks enabled
Nov 09 17:00:06 localhost kernel: PV qspinlock hash table entries: 256 (order: 0, 4096 bytes, linear)
Nov 09 17:00:06 localhost kernel: Kernel command line: BOOT_IMAGE=(hd0,gpt3)/boot/vmlinuz-7.2.11-300.fc45.x86_64 no_timer_check console=tty1 console=ttyS0,115200n8 systemd.firstboot=off root=UUID=00000000-0000-0000-0000-000000000000 rootflags=subvol=root
Nov 09 17:00:06 localhost kernel: random: crng init done
Nov 09 17:00:06 localhost kernel: printk: log buffer data + meta data: 262144 + 1114112 = 1376256 bytes
Nov 09 17:00:06 localhost kernel: Dentry cache hash table entries: 262144 (order: 9, 2097152 bytes, linear)
Nov 09 17:00:06 localhost kernel: Inode-cache hash table entries: 131072 (order: 8, 1048576 bytes, linear)
Nov 09 17:00:06 localhost kernel: Fallback order for Node 0: 0 
Nov 09 17:00:06 localhost kernel: Built 1 zonelists, mobility grouping on.  Total pages: 524148
Nov 09 17:00:06 localhost kernel: Policy zone: DMA32
Nov 09 17:00:06 localhost kernel: mem auto-init: stack:all(zero), heap alloc:on, heap free:off
Nov 09 17:00:06 localhost kernel: SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=2, Nodes=1
Nov 09 17:00:06 localhost kernel: ftrace: allocating 64797 entries in 256 pages
Nov 09 17:00:06 localhost kernel: ftrace: allocated 256 pages with 1 groups
Nov 09 17:00:06 localhost kernel: Dynamic Preempt: lazy
Nov 09 17:00:06 localhost kernel: rcu: Preemptible hierarchical RCU implementation.
Nov 09 17:00:06 localhost kernel: rcu:         RCU event tracing is enabled.
Nov 09 17:00:06 localhost kernel: rcu:         RCU restricting CPUs from NR_CPUS=8192 to nr_cpu_ids=2.
Nov 09 17:00:06 localhost kernel:         Trampoline variant of Tasks RCU enabled.
Nov 09 17:00:06 localhost kernel:         Rude variant of Tasks RCU enabled.
Nov 09 17:00:06 localhost kernel:         Tracing variant of Tasks RCU enabled.
Nov 09 17:00:06 localhost kernel: rcu: RCU calculated value of scheduler-enlistment delay is 100 jiffies.
Nov 09 17:00:06 localhost kernel: rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=2
Nov 09 17:00:06 localhost kernel: RCU Tasks: Setting shift to 1 and lim to 1 rcu_task_cb_adjust=1 rcu_task_cpu_ids=2.
Nov 09 17:00:06 localhost kernel: RCU Tasks Rude: Setting shift to 1 and lim to 1 rcu_task_cb_adjust=1 rcu_task_cpu_ids=2.
Nov 09 17:00:06 localhost kernel: NR_IRQS: 524544, nr_irqs: 440, preallocated irqs: 16
Nov 09 17:00:06 localhost kernel: rcu: srcu_init: Setting srcu_struct sizes based on contention.
Nov 09 17:00:06 localhost kernel: clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275000 ns
Nov 09 17:00:06 localhost kernel: kfence: initialized - using 2097152 bytes for 255 objects at 0x(____ptrval____)-0x(____ptrval____)
Nov 09 17:00:06 localhost kernel: Console: colour VGA+ 80x25
Nov 09 17:00:06 localhost kernel: printk: legacy console [tty1] enabled
Nov 09 17:00:06 localhost kernel: printk: legacy console [ttyS0] enabled
Nov 09 17:00:06 localhost kernel: ACPI: Core revision 20260408
Nov 09 17:00:06 localhost kernel: clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604467 ns
Nov 09 17:00:06 localhost kernel: APIC: Switch to symmetric I/O mode setup
Nov 09 17:00:06 localhost kernel: x2apic enabled
Nov 09 17:00:06 localhost kernel: APIC: Switched APIC routing to: physical x2apic
Nov 09 17:00:06 localhost kernel: kvm-guest: APIC: send_IPI_mask() replaced with kvm_send_ipi_mask()
Nov 09 17:00:06 localhost kernel: kvm-guest: APIC: send_IPI_mask_allbutself() replaced with kvm_send_ipi_mask_allbutself()
Nov 09 17:00:06 localhost kernel: kvm-guest: setup PV IPIs
Nov 09 17:00:06 localhost kernel: ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
Nov 09 17:00:06 localhost kernel: clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x256bf670eee, max_idle_ns: 440795311217 ns
Nov 09 17:00:06 localhost kernel: Calibrating delay loop (skipped) preset value.. 5192.26 BogoMIPS (lpj=2596132)
Nov 09 17:00:06 localhost kernel: x86/cpu: User Mode Instruction Prevention (UMIP) activated
Nov 09 17:00:06 localhost kernel: Last level iTLB entries: 4KB 512, 2MB 255, 4MB 127
Nov 09 17:00:06 localhost kernel: Last level dTLB entries: 4KB 512, 2MB 255, 4MB 127, 1GB 0
Nov 09 17:00:06 localhost kernel: mitigations: Enabled attack vectors: user_kernel, user_user, guest_host, guest_guest, SMT mitigations: auto
Nov 09 17:00:06 localhost kernel: Speculative Store Bypass: Vulnerable
Nov 09 17:00:06 localhost kernel: Speculative Return Stack Overflow: IBPB-extending microcode not applied!
Nov 09 17:00:06 localhost kernel: Speculative Return Stack Overflow: WARNING: See https://kernel.org/doc/html/latest/admin-guide/hw-vuln/srso.html for mitigation options.
Nov 09 17:00:06 localhost kernel: Transient Scheduler Attacks: Vulnerable: No microcode
Nov 09 17:00:06 localhost kernel: Spectre V2 : Mitigation: Retpolines
Nov 09 17:00:06 localhost kernel: Speculative Return Stack Overflow: Vulnerable: Safe RET, no microcode
Nov 09 17:00:06 localhost kernel: Spectre V1 : Mitigation: usercopy/swapgs barriers and __user pointer sanitization
Nov 09 17:00:06 localhost kernel: Spectre V2 : Spectre v2 / SpectreRSB: Filling RSB on context switch and VMEXIT
Nov 09 17:00:06 localhost kernel: active return thunk: srso_alias_return_thunk
Nov 09 17:00:06 localhost kernel: x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
Nov 09 17:00:06 localhost kernel: x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
Nov 09 17:00:06 localhost kernel: x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
Nov 09 17:00:06 localhost kernel: x86/fpu: Supporting XSAVE feature 0x020: 'AVX-512 opmask'
Nov 09 17:00:06 localhost kernel: x86/fpu: Supporting XSAVE feature 0x040: 'AVX-512 Hi256'
Nov 09 17:00:06 localhost kernel: x86/fpu: Supporting XSAVE feature 0x080: 'AVX-512 ZMM_Hi256'
Nov 09 17:00:06 localhost kernel: x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
Nov 09 17:00:06 localhost kernel: x86/fpu: xstate_offset[5]:  832, xstate_sizes[5]:   64
Nov 09 17:00:06 localhost kernel: x86/fpu: xstate_offset[6]:  896, xstate_sizes[6]:  512
Nov 09 17:00:06 localhost kernel: x86/fpu: xstate_offset[7]: 1408, xstate_sizes[7]: 1024
Nov 09 17:00:06 localhost kernel: x86/fpu: Enabled xstate features 0xe7, context size is 2432 bytes, using 'compacted' format.
Nov 09 17:00:06 localhost kernel: pid_max: default: 32768 minimum: 301
Nov 09 17:00:06 localhost kernel: Yama: becoming mindful.
Nov 09 17:00:06 localhost kernel: SELinux:  Initializing.
Nov 09 17:00:06 localhost kernel: LSM support for eBPF active
Nov 09 17:00:06 localhost kernel: landlock: Up and running.
Nov 09 17:00:06 localhost kernel: Mount-cache hash table entries: 4096 (order: 3, 32768 bytes, linear)
Nov 09 17:00:06 localhost kernel: Mountpoint-cache hash table entries: 4096 (order: 3, 32768 bytes, linear)
Nov 09 17:00:06 localhost kernel: VFS: Finished mounting rootfs on nullfs
Nov 09 17:00:06 localhost kernel: smpboot: CPU0: AMD EPYC 9V74 80-Core Processor (family: 0x19, model: 0x11, stepping: 0x1)
Nov 09 17:00:06 localhost kernel: Performance Events: PMU not available due to virtualization, using software events only.
Nov 09 17:00:06 localhost kernel: signal: max sigframe size: 3376
Nov 09 17:00:06 localhost kernel: rcu: Hierarchical SRCU implementation.
Nov 09 17:00:06 localhost kernel: rcu:         Max phase no-delay instances is 400.
Nov 09 17:00:06 localhost kernel: Timer migration: 1 hierarchy levels; 8 children per group; 1 crossnode level
Nov 09 17:00:06 localhost kernel: NMI watchdog: Perf NMI watchdog permanently disabled
Nov 09 17:00:06 localhost kernel: smp: Bringing up secondary CPUs ...
Nov 09 17:00:06 localhost kernel: smpboot: x86: Booting SMP configuration:
Nov 09 17:00:06 localhost kernel: .... node  #0, CPUs:      #1
Nov 09 17:00:06 localhost kernel: smp: Brought up 1 node, 2 CPUs
Nov 09 17:00:06 localhost kernel: smpboot: Total of 2 processors activated (10384.52 BogoMIPS)
Nov 09 17:00:06 localhost kernel: Memory: 1938652K/2096592K available (24463K kernel code, 4815K rwdata, 18656K rodata, 5324K init, 4212K bss, 150416K reserved, 0K cma-reserved)
Nov 09 17:00:06 localhost kernel: devtmpfs: initialized
Nov 09 17:00:06 localhost kernel: x86/mm: Memory block size: 128MB
Nov 09 17:00:06 localhost kernel: posixtimers hash table entries: 1024 (order: 2, 16384 bytes, linear)
Nov 09 17:00:06 localhost kernel: futex hash table entries: 512 (32768 bytes on 1 NUMA nodes, total 32 KiB, linear).
Nov 09 17:00:06 localhost kernel: xor: automatically using best checksumming function   avx       
Nov 09 17:00:06 localhost kernel: PM: RTC time: 17:00:03, date: 2026-11-09
Nov 09 17:00:06 localhost kernel: NET: Registered PF_NETLINK/PF_ROUTE protocol family
Nov 09 17:00:06 localhost kernel: DMA: preallocated 256 KiB GFP_KERNEL|GFP_DMA pool for atomic allocations
Nov 09 17:00:06 localhost kernel: DMA: preallocated 256 KiB GFP_KERNEL|GFP_DMA32 pool for atomic allocations
Nov 09 17:00:06 localhost kernel: audit: initializing netlink subsys (disabled)
Nov 09 17:00:06 localhost kernel: audit: type=2000 audit(1794243603.090:1): state=initialized audit_enabled=0 res=1
Nov 09 17:00:06 localhost kernel: thermal_sys: Registered thermal governor 'fair_share'
Nov 09 17:00:06 localhost kernel: thermal_sys: Registered thermal governor 'bang_bang'
Nov 09 17:00:06 localhost kernel: thermal_sys: Registered thermal governor 'step_wise'
Nov 09 17:00:06 localhost kernel: thermal_sys: Registered thermal governor 'user_space'
Nov 09 17:00:06 localhost kernel: cpuidle: using governor menu
Nov 09 17:00:06 localhost kernel: Freeing SMP alternatives memory: 60K
Nov 09 17:00:06 localhost kernel: acpiphp: ACPI Hot Plug PCI Controller Driver version: 0.5
Nov 09 17:00:06 localhost kernel: PCI: ECAM [mem 0xb0000000-0xbfffffff] (base 0xb0000000) for domain 0000 [bus 00-ff]
Nov 09 17:00:06 localhost kernel: PCI: ECAM [mem 0xb0000000-0xbfffffff] reserved as E820 entry
Nov 09 17:00:06 localhost kernel: PCI: Using configuration type 1 for base access
Nov 09 17:00:06 localhost kernel: virt/tdx: TDX not supported by the host platform
Nov 09 17:00:06 localhost kernel: kprobes: kprobe jump-optimization is enabled. All kprobes are optimized if possible.
Nov 09 17:00:06 localhost kernel: HugeTLB: registered 1.00 GiB page size, pre-allocated 0 pages
Nov 09 17:00:06 localhost kernel: HugeTLB: 16380 KiB vmemmap can be freed for a 1.00 GiB page
Nov 09 17:00:06 localhost kernel: HugeTLB: registered 2.00 MiB page size, pre-allocated 0 pages
Nov 09 17:00:06 localhost kernel: HugeTLB: 28 KiB vmemmap can be freed for a 2.00 MiB page
Nov 09 17:00:06 localhost kernel: raid6: using avx512x2 recovery algorithm
Nov 09 17:00:06 localhost kernel: raid6: skipped pq benchmark and selected avx512x4
Nov 09 17:00:06 localhost kernel: ACPI: Added _OSI(Module Device)
Nov 09 17:00:06 localhost kernel: ACPI: Added _OSI(Processor Device)
Nov 09 17:00:06 localhost kernel: ACPI: Added _OSI(Processor Aggregator Device)
Nov 09 17:00:06 localhost kernel: ACPI: 1 ACPI AML tables successfully acquired and loaded
Nov 09 17:00:06 localhost kernel: ACPI: \_SB_: platform _OSC: OS support mask [006e7eff]
Nov 09 17:00:06 localhost kernel: ACPI: Interpreter enabled
Nov 09 17:00:06 localhost kernel: ACPI: PM: (supports S0 S3 S4 S5)
Nov 09 17:00:06 localhost kernel: ACPI: Using IOAPIC for interrupt routing
Nov 09 17:00:06 localhost kernel: PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
Nov 09 17:00:06 localhost kernel: PCI: Using E820 reservations for host bridge windows
Nov 09 17:00:06 localhost kernel: ACPI: Enabled 2 GPEs in block 00 to 3F
Nov 09 17:00:06 localhost kernel: ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
Nov 09 17:00:06 localhost kernel: acpi PNP0A08:00: _OSC: OS supports [ExtendedConfig ASPM ClockPM Segments MSI EDR HPX-Type3]
Nov 09 17:00:06 localhost kernel: acpi PNP0A08:00: _OSC: platform does not support [PCIeHotplug LTR DPC]
Nov 09 17:00:06 localhost kernel: acpi PNP0A08:00: _OSC: OS now controls [SHPCHotplug PME AER PCIeCapability]
Nov 09 17:00:06 localhost kernel: PCI host bridge to bus 0000:00
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [mem 0x80000000-0xafffffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [mem 0xc0000000-0xfebfffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [mem 0x100000000-0x8ffffffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: root bus resource [bus 00-ff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:00.0: [8086:29c0] type 00 class 0x060000 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: [1234:1111] type 00 class 0x030000 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: BAR 0 [mem 0xfd000000-0xfdffffff pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: BAR 2 [mem 0xfeb90000-0xfeb90fff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: ROM [mem 0xfeb80000-0xfeb8ffff pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:02.0: [1af4:1001] type 00 class 0x010000 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:02.0: BAR 0 [io  0xc000-0xc07f]
Nov 09 17:00:06 localhost kernel: pci 0000:00:02.0: BAR 1 [mem 0xfeb91000-0xfeb91fff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:02.0: BAR 4 [mem 0xfe000000-0xfe003fff 64bit pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:03.0: [1af4:1001] type 00 class 0x010000 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:03.0: BAR 0 [io  0xc080-0xc0ff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:03.0: BAR 1 [mem 0xfeb92000-0xfeb92fff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:03.0: BAR 4 [mem 0xfe004000-0xfe007fff 64bit pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:04.0: [1af4:1000] type 00 class 0x020000 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:04.0: BAR 0 [io  0xc1c0-0xc1df]
Nov 09 17:00:06 localhost kernel: pci 0000:00:04.0: BAR 1 [mem 0xfeb93000-0xfeb93fff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:04.0: BAR 4 [mem 0xfe008000-0xfe00bfff 64bit pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:04.0: ROM [mem 0xfeb00000-0xfeb7ffff pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:05.0: [1af4:1001] type 00 class 0x010000 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:05.0: BAR 0 [io  0xc100-0xc17f]
Nov 09 17:00:06 localhost kernel: pci 0000:00:05.0: BAR 1 [mem 0xfeb94000-0xfeb94fff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:05.0: BAR 4 [mem 0xfe00c000-0xfe00ffff 64bit pref]
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.0: [8086:2918] type 00 class 0x060100 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.0: quirk: [io  0x0600-0x067f] claimed by ICH6 ACPI/GPIO/TCO
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.2: [8086:2922] type 00 class 0x010601 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.2: BAR 4 [io  0xc1e0-0xc1ff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.2: BAR 5 [mem 0xfeb95000-0xfeb95fff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.3: [8086:2930] type 00 class 0x0c0500 conventional PCI endpoint
Nov 09 17:00:06 localhost kernel: pci 0000:00:1f.3: BAR 4 [io  0x0700-0x073f]
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKA configured for IRQ 10
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKB configured for IRQ 10
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKC configured for IRQ 11
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKD configured for IRQ 11
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKE configured for IRQ 10
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKF configured for IRQ 10
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKG configured for IRQ 11
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link LNKH configured for IRQ 11
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIA configured for IRQ 16
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIB configured for IRQ 17
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIC configured for IRQ 18
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSID configured for IRQ 19
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIE configured for IRQ 20
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIF configured for IRQ 21
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIG configured for IRQ 22
Nov 09 17:00:06 localhost kernel: ACPI: PCI: Interrupt link GSIH configured for IRQ 23
Nov 09 17:00:06 localhost kernel: iommu: Default domain type: Translated
Nov 09 17:00:06 localhost kernel: iommu: DMA domain TLB invalidation policy: lazy mode
Nov 09 17:00:06 localhost kernel: SCSI subsystem initialized
Nov 09 17:00:06 localhost kernel: libata version 3.00 loaded.
Nov 09 17:00:06 localhost kernel: ACPI: bus type USB registered
Nov 09 17:00:06 localhost kernel: usbcore: registered new interface driver usbfs
Nov 09 17:00:06 localhost kernel: usbcore: registered new interface driver hub
Nov 09 17:00:06 localhost kernel: usbcore: registered new device driver usb
Nov 09 17:00:06 localhost kernel: pps_core: LinuxPPS API ver. 1 registered
Nov 09 17:00:06 localhost kernel: pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
Nov 09 17:00:06 localhost kernel: PTP clock support registered
Nov 09 17:00:06 localhost kernel: EDAC MC: Ver: 3.0.0
Nov 09 17:00:06 localhost kernel: NetLabel: Initializing
Nov 09 17:00:06 localhost kernel: NetLabel:  domain hash size = 128
Nov 09 17:00:06 localhost kernel: NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
Nov 09 17:00:06 localhost kernel: NetLabel:  unlabeled traffic allowed by default
Nov 09 17:00:06 localhost kernel: mctp: management component transport protocol core
Nov 09 17:00:06 localhost kernel: NET: Registered PF_MCTP protocol family
Nov 09 17:00:06 localhost kernel: PCI: Using ACPI for IRQ routing
Nov 09 17:00:06 localhost kernel: PCI: pci_cache_line_size set to 64 bytes
Nov 09 17:00:06 localhost kernel: e820: register RAM buffer resource [mem 0x0009fc00-0x0009ffff]
Nov 09 17:00:06 localhost kernel: e820: register RAM buffer resource [mem 0x7ffd6000-0x7fffffff]
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: vgaarb: setting as boot VGA device
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: vgaarb: bridge control possible
Nov 09 17:00:06 localhost kernel: pci 0000:00:01.0: vgaarb: VGA device added: decodes=io+mem,owns=io+mem,locks=none
Nov 09 17:00:06 localhost kernel: vgaarb: loaded
Nov 09 17:00:06 localhost kernel: hpet0: at MMIO 0xfed00000, IRQs 2, 8, 0
Nov 09 17:00:06 localhost kernel: hpet0: 3 comparators, 64-bit 100.000000 MHz counter
Nov 09 17:00:06 localhost kernel: clocksource: Switched to clocksource kvm-clock
Nov 09 17:00:06 localhost kernel: VFS: Disk quotas dquot_6.6.0
Nov 09 17:00:06 localhost kernel: VFS: Dquot-cache hash table entries: 512 (4096 bytes)
Nov 09 17:00:06 localhost kernel: acpi PNP0C01:00: Reserved [mem 0xb0000000-0xbfffffff]
Nov 09 17:00:06 localhost kernel: pnp: PnP ACPI init
Nov 09 17:00:06 localhost kernel: pnp: PnP ACPI: found 4 devices
Nov 09 17:00:06 localhost kernel: clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
Nov 09 17:00:06 localhost kernel: NET: Registered PF_INET protocol family
Nov 09 17:00:06 localhost kernel: IP idents hash table entries: 32768 (order: 6, 262144 bytes, linear)
Nov 09 17:00:06 localhost kernel: tcp_listen_portaddr_hash hash table entries: 1024 (order: 2, 16384 bytes, linear)
Nov 09 17:00:06 localhost kernel: Table-perturb hash table entries: 65536 (order: 6, 262144 bytes, linear)
Nov 09 17:00:06 localhost kernel: TCP established hash table entries: 16384 (order: 5, 131072 bytes, linear)
Nov 09 17:00:06 localhost kernel: TCP bind hash table entries: 16384 (order: 7, 524288 bytes, linear)
Nov 09 17:00:06 localhost kernel: TCP: Hash tables configured (established 16384 bind 16384)
Nov 09 17:00:06 localhost kernel: MPTCP token hash table entries: 2048 (order: 4, 49152 bytes, linear)
Nov 09 17:00:06 localhost kernel: UDP hash table entries: 1024 (order: 4, 65536 bytes, linear)
Nov 09 17:00:06 localhost kernel: NET: Registered PF_UNIX/PF_LOCAL protocol family
Nov 09 17:00:06 localhost kernel: NET: Registered PF_XDP protocol family
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7 window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: resource 5 [io  0x0d00-0xffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000bffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: resource 7 [mem 0x80000000-0xafffffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: resource 8 [mem 0xc0000000-0xfebfffff window]
Nov 09 17:00:06 localhost kernel: pci_bus 0000:00: resource 9 [mem 0x100000000-0x8ffffffff window]
Nov 09 17:00:06 localhost kernel: PCI: CLS 0 bytes, default 64
Nov 09 17:00:06 localhost kernel: Trying to unpack rootfs image as initramfs...
Nov 09 17:00:06 localhost kernel: clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x256bf670eee, max_idle_ns: 440795311217 ns
Nov 09 17:00:06 localhost kernel: Initialise system trusted keyrings
Nov 09 17:00:06 localhost kernel: Key type blacklist registered
Nov 09 17:00:06 localhost kernel: workingset: timestamp_bits=36 (anon: 31) max_order=19 bucket_order=0 (anon: 0)
Nov 09 17:00:06 localhost kernel: integrity: Platform Keyring initialized
Nov 09 17:00:06 localhost kernel: integrity: Machine keyring initialized
Nov 09 17:00:06 localhost kernel: cryptd: max_cpu_qlen set to 1000
Nov 09 17:00:06 localhost kernel: NET: Registered PF_ALG protocol family
Nov 09 17:00:06 localhost kernel: Key type asymmetric registered
Nov 09 17:00:06 localhost kernel: Asymmetric key parser 'x509' registered
Nov 09 17:00:06 localhost kernel: Block layer SCSI generic (bsg) driver version 0.4 loaded (major 244)
Nov 09 17:00:06 localhost kernel: io scheduler mq-deadline registered
Nov 09 17:00:06 localhost kernel: io scheduler kyber registered
Nov 09 17:00:06 localhost kernel: io scheduler bfq registered
Nov 09 17:00:06 localhost kernel: atomic64_test: passed for x86-64 platform with CX8 and with SSE
Nov 09 17:00:06 localhost kernel: input: Power Button as /devices/platform/LNXPWRBN:00/input/input0
Nov 09 17:00:06 localhost kernel: ACPI: button: Power Button [PWRF]
Nov 09 17:00:06 localhost kernel: ACPI: \_SB_.GSIG: Enabled at IRQ 22
Nov 09 17:00:06 localhost kernel: ACPI: \_SB_.GSIH: Enabled at IRQ 23
Nov 09 17:00:06 localhost kernel: ACPI: \_SB_.GSIE: Enabled at IRQ 20
Nov 09 17:00:06 localhost kernel: ACPI: \_SB_.GSIF: Enabled at IRQ 21
Nov 09 17:00:06 localhost kernel: Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
Nov 09 17:00:06 localhost kernel: 00:03: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
Nov 09 17:00:06 localhost kernel: Non-volatile memory driver v1.3
Nov 09 17:00:06 localhost kernel: ACPI: bus type drm_connector registered
Nov 09 17:00:06 localhost kernel: virtio_blk virtio0: 2/0/0 default/read/poll queues
Nov 09 17:00:06 localhost kernel: virtio_blk virtio0: [vda] 41943040 512-byte logical blocks (21.5 GB/20.0 GiB)
Nov 09 17:00:06 localhost kernel:  vda: vda1 vda2 vda3
Nov 09 17:00:06 localhost kernel: virtio_blk virtio1: 2/0/0 default/read/poll queues
Nov 09 17:00:06 localhost kernel: virtio_blk virtio1: [vdb] 131072 512-byte logical blocks (67.1 MB/64.0 MiB)
Nov 09 17:00:06 localhost kernel: virtio_blk virtio3: 2/0/0 default/read/poll queues
Nov 09 17:00:06 localhost kernel: virtio_blk virtio3: [vdc] 736 512-byte logical blocks (377 kB/368 KiB)
Nov 09 17:00:06 localhost kernel: ACPI: \_SB_.GSIA: Enabled at IRQ 16
Nov 09 17:00:06 localhost kernel: ahci 0000:00:1f.2: AHCI vers 0001.0000, 32 command slots, 1.5 Gbps, SATA mode
Nov 09 17:00:06 localhost kernel: ahci 0000:00:1f.2: 6/6 ports implemented (port mask 0x3f)
Nov 09 17:00:06 localhost kernel: ahci 0000:00:1f.2: flags: 64bit ncq only 
Nov 09 17:00:06 localhost kernel: scsi host0: ahci
Nov 09 17:00:06 localhost kernel: scsi host1: ahci
Nov 09 17:00:06 localhost kernel: scsi host2: ahci
Nov 09 17:00:06 localhost kernel: scsi host3: ahci
Nov 09 17:00:06 localhost kernel: scsi host4: ahci
Nov 09 17:00:06 localhost kernel: scsi host5: ahci
Nov 09 17:00:06 localhost kernel: ata1: SATA max UDMA/133 abar m4096@0xfeb95000 port 0xfeb95100 irq 33 lpm-pol 1
Nov 09 17:00:06 localhost kernel: ata2: SATA max UDMA/133 abar m4096@0xfeb95000 port 0xfeb95180 irq 33 lpm-pol 1
Nov 09 17:00:06 localhost kernel: ata3: SATA max UDMA/133 abar m4096@0xfeb95000 port 0xfeb95200 irq 33 lpm-pol 1
Nov 09 17:00:06 localhost kernel: ata4: SATA max UDMA/133 abar m4096@0xfeb95000 port 0xfeb95280 irq 33 lpm-pol 1
Nov 09 17:00:06 localhost kernel: ata5: SATA max UDMA/133 abar m4096@0xfeb95000 port 0xfeb95300 irq 33 lpm-pol 1
Nov 09 17:00:06 localhost kernel: ata6: SATA max UDMA/133 abar m4096@0xfeb95000 port 0xfeb95380 irq 33 lpm-pol 1
Nov 09 17:00:06 localhost kernel: CAN device driver interface
Nov 09 17:00:06 localhost kernel: usbcore: registered new interface driver usbserial_generic
Nov 09 17:00:06 localhost kernel: usbserial: USB Serial support registered for generic
Nov 09 17:00:06 localhost kernel: i8042: PNP: PS/2 Controller [PNP0303:KBD,PNP0f13:MOU] at 0x60,0x64 irq 1,12
Nov 09 17:00:06 localhost kernel: Freeing initrd memory: 45064K
Nov 09 17:00:06 localhost kernel: serio: i8042 KBD port at 0x60,0x64 irq 1
Nov 09 17:00:06 localhost kernel: serio: i8042 AUX port at 0x60,0x64 irq 12
Nov 09 17:00:06 localhost kernel: mousedev: PS/2 mouse device common for all mice
Nov 09 17:00:06 localhost kernel: rtc_cmos PNP0B00:00: RTC can wake from S4
Nov 09 17:00:06 localhost kernel: input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input1
Nov 09 17:00:06 localhost kernel: rtc_cmos PNP0B00:00: registered as rtc0
Nov 09 17:00:06 localhost kernel: rtc_cmos PNP0B00:00: setting system clock to 2026-11-09T17:00:04 UTC (1794243604)
Nov 09 17:00:06 localhost kernel: rtc_cmos PNP0B00:00: alarms up to one day, y3k, 242 bytes nvram, hpet irqs
Nov 09 17:00:06 localhost kernel: device-mapper: core: CONFIG_IMA_DISABLE_HTABLE is disabled. Duplicate IMA measurements will not be recorded in the IMA log.
Nov 09 17:00:06 localhost kernel: device-mapper: uevent: version 1.0.3
Nov 09 17:00:06 localhost kernel: input: VirtualPS/2 VMware VMMouse as /devices/platform/i8042/serio1/input/input4
Nov 09 17:00:06 localhost kernel: device-mapper: ioctl: 4.50.0-ioctl (2025-04-28) initialised: dm-devel@lists.linux.dev
Nov 09 17:00:06 localhost kernel: input: VirtualPS/2 VMware VMMouse as /devices/platform/i8042/serio1/input/input3
Nov 09 17:00:06 localhost kernel: hid: raw HID events driver (C) Jiri Kosina
Nov 09 17:00:06 localhost kernel: usbcore: registered new interface driver usbhid
Nov 09 17:00:06 localhost kernel: usbhid: USB HID core driver
Nov 09 17:00:06 localhost kernel: drop_monitor: Initializing network drop monitor service
Nov 09 17:00:06 localhost kernel: Initializing XFRM netlink socket
Nov 09 17:00:06 localhost kernel: NET: Registered PF_INET6 protocol family
Nov 09 17:00:06 localhost kernel: Segment Routing with IPv6
Nov 09 17:00:06 localhost kernel: RPL Segment Routing with IPv6
Nov 09 17:00:06 localhost kernel: In-situ OAM (IOAM) with IPv6
Nov 09 17:00:06 localhost kernel: mip6: Mobile IPv6
Nov 09 17:00:06 localhost kernel: NET: Registered PF_PACKET protocol family
Nov 09 17:00:06 localhost kernel: can: controller area network core
Nov 09 17:00:06 localhost kernel: NET: Registered PF_CAN protocol family
Nov 09 17:00:06 localhost kernel: IPI shorthand broadcast: enabled
Nov 09 17:00:06 localhost kernel: sched_clock: Marking stable (1026010455, 322388458)->(1414778176, -66379263)
Nov 09 17:00:06 localhost kernel: registered taskstats version 1
Nov 09 17:00:06 localhost kernel: Loading compiled-in X.509 certificates
Nov 09 17:00:06 localhost kernel: Loaded X.509 cert 'Fedora kernel signing key: 925079f85d8cf849b2cfc1ccc8e5eb56d336c8f3'
Nov 09 17:00:06 localhost kernel: Loaded X.509 cert 'Fedora IMA CA: a8a00c31663f853f9c6ff2564872e378af026b28'
Nov 09 17:00:06 localhost kernel: Demotion targets for Node 0: null
Nov 09 17:00:06 localhost kernel: page_owner is disabled
Nov 09 17:00:06 localhost kernel: Key type .fscrypt registered
Nov 09 17:00:06 localhost kernel: Key type fscrypt-provisioning registered
Nov 09 17:00:06 localhost kernel: Btrfs loaded, zoned=yes, fsverity=yes
Nov 09 17:00:06 localhost kernel: Key type big_key registered
Nov 09 17:00:06 localhost kernel: Key type encrypted registered
Nov 09 17:00:06 localhost kernel: ima: No TPM chip found, activating TPM-bypass!
Nov 09 17:00:06 localhost kernel: Loading compiled-in module X.509 certificates
Nov 09 17:00:06 localhost kernel: Loaded X.509 cert 'Fedora kernel signing key: 925079f85d8cf849b2cfc1ccc8e5eb56d336c8f3'
Nov 09 17:00:06 localhost kernel: ima: Allocated hash algorithm: sha256
Nov 09 17:00:06 localhost kernel: ima: No architecture policies found
Nov 09 17:00:06 localhost kernel: evm: Initialising EVM extended attributes:
Nov 09 17:00:06 localhost kernel: evm: security.selinux
Nov 09 17:00:06 localhost kernel: evm: security.SMACK64 (disabled)
Nov 09 17:00:06 localhost kernel: evm: security.SMACK64EXEC (disabled)
Nov 09 17:00:06 localhost kernel: evm: security.SMACK64TRANSMUTE (disabled)
Nov 09 17:00:06 localhost kernel: evm: security.SMACK64MMAP (disabled)
Nov 09 17:00:06 localhost kernel: evm: security.apparmor (disabled)
Nov 09 17:00:06 localhost kernel: evm: security.ima
Nov 09 17:00:06 localhost kernel: evm: security.capability
Nov 09 17:00:06 localhost kernel: evm: HMAC attrs: 0x1
Nov 09 17:00:06 localhost kernel: alg: No test for 842 (842-scomp)
Nov 09 17:00:06 localhost kernel: alg: No test for mldsa87 (mldsa87-lib)
Nov 09 17:00:06 localhost kernel: alg: No test for mldsa65 (mldsa65-lib)
Nov 09 17:00:06 localhost kernel: alg: No test for mldsa44 (mldsa44-lib)
Nov 09 17:00:06 localhost kernel: PM:   Magic number: 2:472:36
Nov 09 17:00:06 localhost kernel: RAS: Correctable Errors collector initialized.
Nov 09 17:00:06 localhost kernel: clk: Disabling unused clocks
Nov 09 17:00:06 localhost kernel: PM: genpd: Disabling unused power domains
Nov 09 17:00:06 localhost kernel: ata1: SATA link down (SStatus 0 SControl 300)
Nov 09 17:00:06 localhost kernel: ata3: SATA link up 1.5 Gbps (SStatus 113 SControl 300)
Nov 09 17:00:06 localhost kernel: ata3.00: ATAPI: QEMU DVD-ROM, 2.5+, max UDMA/100
Nov 09 17:00:06 localhost kernel: ata3.00: applying bridge limits
Nov 09 17:00:06 localhost kernel: ata4: SATA link down (SStatus 0 SControl 300)
Nov 09 17:00:06 localhost kernel: ata5: SATA link down (SStatus 0 SControl 300)
Nov 09 17:00:06 localhost kernel: ata6: SATA link down (SStatus 0 SControl 300)
Nov 09 17:00:06 localhost kernel: ata2: SATA link down (SStatus 0 SControl 300)
Nov 09 17:00:06 localhost kernel: ata3.00: configured for UDMA/100
Nov 09 17:00:06 localhost kernel: scsi 2001:db8::1 CD-ROM            QEMU     QEMU DVD-ROM     2.5+ PQ: 0 ANSI: 5
Nov 09 17:00:06 localhost kernel: sr 2001:db8::1 [sr0] scsi3-mmc drive: 4x/4x cd/rw xa/form2 tray
Nov 09 17:00:06 localhost kernel: cdrom: Uniform CD-ROM driver Revision: 3.20
Nov 09 17:00:06 localhost kernel: sr 2001:db8::1 Attached scsi CD-ROM sr0
Nov 09 17:00:06 localhost kernel: sr 2001:db8::1 Attached scsi generic sg0 type 5
Nov 09 17:00:06 localhost kernel: Freeing unused decrypted memory: 2028K
Nov 09 17:00:06 localhost kernel: Freeing unused kernel image (initmem) memory: 5324K
Nov 09 17:00:06 localhost kernel: Write protecting the kernel read-only data: 45056k
Nov 09 17:00:06 localhost kernel: Freeing unused kernel image (text/rodata gap) memory: 112K
Nov 09 17:00:06 localhost kernel: Freeing unused kernel image (rodata/data gap) memory: 1824K
Nov 09 17:00:06 localhost kernel: x86/mm: Checked W+X mappings: passed, no W+X pages found.
Nov 09 17:00:06 localhost kernel: Run /init as init process
Nov 09 17:00:06 localhost kernel:   with arguments:
Nov 09 17:00:06 localhost kernel:     /init
Nov 09 17:00:06 localhost kernel:   with environment:
Nov 09 17:00:06 localhost kernel:     HOME=/
Nov 09 17:00:06 localhost kernel:     TERM=linux
Nov 09 17:00:06 localhost kernel: fuse: init (API version 7.45)
Nov 09 17:00:06 localhost systemd[1]: Successfully made /usr/ read-only.
Nov 09 17:00:06 localhost systemd[1]: systemd 262-3.fc45 running in system mode (+PAM +AUDIT +SELINUX -APPARMOR +IMA +IPE +SMACK +SECCOMP +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 +KMOD +LIBCRYPTSETUP +LIBCRYPTSETUP_PLUGINS +LIBFDISK +PCRE2 +PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD +BPF_FRAMEWORK +BTF +XKBCOMMON +UTMP +LIBARCHIVE)
Nov 09 17:00:06 localhost systemd[1]: Detected virtualization kvm.
Nov 09 17:00:06 localhost systemd[1]: Detected architecture x86-64.
Nov 09 17:00:06 localhost systemd[1]: Running in initrd.
Nov 09 17:00:06 localhost systemd[1]: Initializing machine ID from random generator.
Nov 09 17:00:06 localhost systemd[1]: No hostname configured, using default hostname.
Nov 09 17:00:06 localhost systemd[1]: Hostname set to <localhost>.
Nov 09 17:00:06 localhost systemd[1]: bpf-restrict-fs: LSM BPF program attached
Nov 09 17:00:06 localhost (gene[163]: '/usr/lib/systemd/system-generators/dracut-crypt-generator' failed with exit status 2.
Nov 09 17:00:06 localhost systemd[1]: Queued start job for default target initrd.target.
Nov 09 17:00:06 localhost systemd[1]: Started systemd-ask-password-console.path - Dispatch Password Requests to Console Directory Watch.
Nov 09 17:00:06 localhost systemd[1]: Expecting device dev-disk-by\x2duuid-89f8a76e\x2dbfd7\x2d4e60\x2d89f8\x2db1769a33429a.device - /dev/disk/by-uuid/00000000-0000-0000-0000-000000000000...
Nov 09 17:00:06 localhost systemd[1]: Reached target initrd-usr-fs.target - Initrd /usr File System.
Nov 09 17:00:06 localhost systemd[1]: Reached target paths.target - Path Units.
Nov 09 17:00:06 localhost systemd[1]: Reached target slices.target - Slice Units.
Nov 09 17:00:06 localhost systemd[1]: Reached target swap.target - Swaps.
Nov 09 17:00:06 localhost systemd[1]: Reached target timers.target - Timer Units.
Nov 09 17:00:06 localhost systemd[1]: Listening on systemd-journald-dev-log.socket - Journal Socket (/dev/log).
Nov 09 17:00:06 localhost systemd[1]: Listening on systemd-journald.socket - Journal Sockets.
Nov 09 17:00:06 localhost systemd[1]: Listening on systemd-udevd-kernel.socket - udev Kernel Socket.
Nov 09 17:00:06 localhost systemd[1]: Listening on systemd-udevd-varlink.socket - udev Varlink Socket.
Nov 09 17:00:06 localhost systemd[1]: Reached target sockets.target - Socket Units.
Nov 09 17:00:06 localhost systemd[1]: Starting kmod-static-nodes.service - Create List of Static Device Nodes...
Nov 09 17:00:06 localhost systemd[1]: memstrack.service - Memstrack Anylazing Service skipped, no trigger condition checks were met.
Nov 09 17:00:06 localhost systemd[1]: systemd-battery-check.service - Early Battery Level Check skipped, unmet condition check ConditionDirectoryNotEmpty=/sys/class/power_supply
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-journald.service - Journal Service...
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-modules-load.service - Load Kernel Modules...
Nov 09 17:00:06 localhost systemd[1]: systemd-pcrphase-initrd.service - TPM PCR Barrier (initrd) skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:06 localhost systemd[1]: Reached target cryptsetup.target - Local Encrypted Volumes.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-vconsole-setup.service - Virtual Console Setup...
Nov 09 17:00:06 localhost systemd-journald[217]: Collecting audit messages is disabled.
Nov 09 17:00:06 localhost systemd[1]: Finished kmod-static-nodes.service - Create List of Static Device Nodes.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-modules-load.service - Load Kernel Modules.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-sysctl.service - Apply Kernel Variables...
Nov 09 17:00:06 localhost systemd-journald[217]: Journal started
Nov 09 17:00:06 localhost systemd-journald[217]: Runtime Journal (/run/log/journal/00000000000000000000000000000000) is 4.8M, max 39M, 34.1M free.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully...
Nov 09 17:00:06 localhost systemd[1]: Started systemd-journald.service - Journal Service.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-sysctl.service - Apply Kernel Variables.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev...
Nov 09 17:00:06 localhost systemd-vconsole-setup[220]: Configuration of first virtual console was skipped, ignoring remaining ones.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-vconsole-setup.service - Virtual Console Setup.
Nov 09 17:00:06 localhost systemd[1]: dracut-cmdline-ask.service - dracut ask for additional cmdline parameters skipped, no trigger condition checks were met.
Nov 09 17:00:06 localhost systemd[1]: Starting dracut-cmdline.service - dracut cmdline hook...
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev.
Nov 09 17:00:06 localhost systemd[1]: Reached target local-fs-pre.target - Preparation for Local File Systems.
Nov 09 17:00:06 localhost systemd[1]: Reached target local-fs.target - Local File Systems.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-tmpfiles-setup.service - Create System Files and Directories...
Nov 09 17:00:06 localhost dracut-cmdline[231]: dracut-111-4.fc45
Nov 09 17:00:06 localhost dracut-cmdline[231]: Using kernel command line parameters:    BOOT_IMAGE=(hd0,gpt3)/boot/vmlinuz-7.2.11-300.fc45.x86_64 no_timer_check console=tty1 console=ttyS0,115200n8 systemd.firstboot=off root=UUID=00000000-0000-0000-0000-000000000000 rootflags=subvol=root
Nov 09 17:00:06 localhost systemd-tmpfiles[237]: /usr/lib/tmpfiles.d/systemd.conf:36: Duplicate line for path "/var/lib/systemd", ignoring.
Nov 09 17:00:06 localhost systemd-tmpfiles[237]: /usr/lib/tmpfiles.d/var.conf:14: Duplicate line for path "/var/log", ignoring.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-tmpfiles-setup.service - Create System Files and Directories.
Nov 09 17:00:06 localhost systemd[1]: Finished dracut-cmdline.service - dracut cmdline hook.
Nov 09 17:00:06 localhost systemd[1]: Starting dracut-pre-udev.service - dracut pre-udev hook...
Nov 09 17:00:06 localhost systemd[1]: Finished dracut-pre-udev.service - dracut pre-udev hook.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-udevd.service - Rule-based Manager for Device Events and Files...
Nov 09 17:00:06 localhost systemd-udevd[337]: Using default interface naming scheme 'v261'.
Nov 09 17:00:06 localhost systemd[1]: Started systemd-udevd.service - Rule-based Manager for Device Events and Files.
Nov 09 17:00:06 localhost systemd[1]: dracut-pre-trigger.service - dracut pre-trigger hook skipped, no trigger condition checks were met.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-udev-trigger.service - Coldplug All udev Devices...
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-udev-trigger.service - Coldplug All udev Devices.
Nov 09 17:00:06 localhost systemd[1]: Reached target sysinit.target - System Initialization.
Nov 09 17:00:06 localhost systemd[1]: Reached target basic.target - Basic System.
Nov 09 17:00:06 localhost systemd[1]: Starting dracut-initqueue.service - dracut initqueue hook...
Nov 09 17:00:06 localhost systemd[1]: Created slice system-modprobe.slice - Slice /system/modprobe.
Nov 09 17:00:06 localhost systemd[1]: modprobe@configfs.service - Load Kernel Module configfs skipped, unmet condition check ConditionKernelModuleLoaded=!configfs
Nov 09 17:00:06 localhost systemd[1]: Found device dev-disk-by\x2duuid-89f8a76e\x2dbfd7\x2d4e60\x2d89f8\x2db1769a33429a.device - /dev/disk/by-uuid/00000000-0000-0000-0000-000000000000.
Nov 09 17:00:06 localhost systemd[1]: Reached target initrd-root-device.target - Initrd Root Device.
Nov 09 17:00:06 localhost systemd[1]: systemd-vconsole-setup.service: Deactivated successfully.
Nov 09 17:00:06 localhost systemd[1]: Stopped systemd-vconsole-setup.service - Virtual Console Setup.
Nov 09 17:00:06 localhost systemd[1]: Stopping systemd-vconsole-setup.service - Virtual Console Setup...
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-vconsole-setup.service - Virtual Console Setup...
Nov 09 17:00:06 localhost systemd[1]: Finished dracut-initqueue.service - dracut initqueue hook.
Nov 09 17:00:06 localhost systemd[1]: Reached target remote-fs-pre.target - Preparation for Remote File Systems.
Nov 09 17:00:06 localhost systemd[1]: Reached target remote-cryptsetup.target - Remote Encrypted Volumes.
Nov 09 17:00:06 localhost systemd[1]: Reached target remote-fs.target - Remote File Systems.
Nov 09 17:00:06 localhost systemd[1]: Starting dracut-pre-mount.service - dracut pre-mount hook...
Nov 09 17:00:06 localhost systemd[1]: Finished dracut-pre-mount.service - dracut pre-mount hook.
Nov 09 17:00:06 localhost systemd[1]: Starting systemd-fsck-root.service - File System Check on /dev/disk/by-uuid/00000000-0000-0000-0000-000000000000...
Nov 09 17:00:06 localhost systemd-vconsole-setup[371]: Configuration of first virtual console was skipped, ignoring remaining ones.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-vconsole-setup.service - Virtual Console Setup.
Nov 09 17:00:06 localhost systemd[1]: Finished systemd-fsck-root.service - File System Check on /dev/disk/by-uuid/00000000-0000-0000-0000-000000000000.
Nov 09 17:00:07 localhost systemd[1]: Mounting sys-kernel-config.mount - Kernel Configuration File System...
Nov 09 17:00:07 localhost systemd[1]: Mounting sysroot.mount - /sysroot...
Nov 09 17:00:07 localhost systemd[1]: Mounted sys-kernel-config.mount - Kernel Configuration File System.
Nov 09 17:00:07 localhost kernel: BTRFS: device label fedora devid 1 transid 35 /dev/vda3 (253:3) scanned by mount (391)
Nov 09 17:00:07 localhost kernel: BTRFS info (device vda3): first mount of filesystem 00000000-0000-0000-0000-000000000000
Nov 09 17:00:07 localhost kernel: BTRFS info (device vda3): using crc32c checksum algorithm
Nov 09 17:00:07 localhost kernel: BTRFS info (device vda3): turning on async discard
Nov 09 17:00:07 localhost kernel: BTRFS info (device vda3): enabling free space tree
Nov 09 17:00:07 localhost systemd[1]: Mounted sysroot.mount - /sysroot.
Nov 09 17:00:07 localhost systemd[1]: Reached target initrd-root-fs.target - Initrd Root File System.
Nov 09 17:00:07 localhost systemd[1]: Starting initrd-parse-etc.service - Mountpoints Configured in the Real Root...
Nov 09 17:00:07 localhost systemd[1]: initrd-parse-etc.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Finished initrd-parse-etc.service - Mountpoints Configured in the Real Root.
Nov 09 17:00:07 localhost systemd[1]: initrd-parse-etc.service: Triggering OnSuccess= dependencies.
Nov 09 17:00:07 localhost systemd[1]: Reached target initrd-fs.target - Initrd File Systems.
Nov 09 17:00:07 localhost systemd[1]: Reached target initrd.target - Initrd Default Target.
Nov 09 17:00:07 localhost systemd[1]: Starting dracut-mount.service - dracut mount hook...
Nov 09 17:00:07 localhost systemd[1]: Finished dracut-mount.service - dracut mount hook.
Nov 09 17:00:07 localhost systemd[1]: Starting dracut-pre-pivot.service - dracut pre-pivot and cleanup hook...
Nov 09 17:00:07 localhost systemd[1]: Finished dracut-pre-pivot.service - dracut pre-pivot and cleanup hook.
Nov 09 17:00:07 localhost systemd[1]: Starting initrd-cleanup.service - Cleaning Up and Shutting Down Daemons...
Nov 09 17:00:07 localhost systemd[1]: Stopped target remote-cryptsetup.target - Remote Encrypted Volumes.
Nov 09 17:00:07 localhost systemd[1]: Stopped target timers.target - Timer Units.
Nov 09 17:00:07 localhost systemd[1]: dracut-pre-pivot.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped dracut-pre-pivot.service - dracut pre-pivot and cleanup hook.
Nov 09 17:00:07 localhost systemd[1]: Stopped target initrd.target - Initrd Default Target.
Nov 09 17:00:07 localhost systemd[1]: Stopped target basic.target - Basic System.
Nov 09 17:00:07 localhost systemd[1]: Stopped target initrd-root-device.target - Initrd Root Device.
Nov 09 17:00:07 localhost systemd[1]: Stopped target initrd-usr-fs.target - Initrd /usr File System.
Nov 09 17:00:07 localhost systemd[1]: Stopped target paths.target - Path Units.
Nov 09 17:00:07 localhost systemd[1]: Stopped target remote-fs.target - Remote File Systems.
Nov 09 17:00:07 localhost systemd[1]: Stopped target remote-fs-pre.target - Preparation for Remote File Systems.
Nov 09 17:00:07 localhost systemd[1]: Stopped target slices.target - Slice Units.
Nov 09 17:00:07 localhost systemd[1]: Stopped target sockets.target - Socket Units.
Nov 09 17:00:07 localhost systemd[1]: Stopped target sysinit.target - System Initialization.
Nov 09 17:00:07 localhost systemd[1]: Stopped target swap.target - Swaps.
Nov 09 17:00:07 localhost systemd[1]: dracut-mount.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped dracut-mount.service - dracut mount hook.
Nov 09 17:00:07 localhost systemd[1]: dracut-pre-mount.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped dracut-pre-mount.service - dracut pre-mount hook.
Nov 09 17:00:07 localhost systemd[1]: Stopped target cryptsetup.target - Local Encrypted Volumes.
Nov 09 17:00:07 localhost systemd[1]: systemd-ask-password-console.path: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-ask-password-console.path - Dispatch Password Requests to Console Directory Watch.
Nov 09 17:00:07 localhost systemd[1]: dracut-initqueue.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped dracut-initqueue.service - dracut initqueue hook.
Nov 09 17:00:07 localhost systemd[1]: systemd-sysctl.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-sysctl.service - Apply Kernel Variables.
Nov 09 17:00:07 localhost systemd[1]: systemd-modules-load.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-modules-load.service - Load Kernel Modules.
Nov 09 17:00:07 localhost systemd[1]: systemd-tmpfiles-setup.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-tmpfiles-setup.service - Create System Files and Directories.
Nov 09 17:00:07 localhost systemd[1]: Stopped target local-fs.target - Local File Systems.
Nov 09 17:00:07 localhost systemd[1]: Stopped target local-fs-pre.target - Preparation for Local File Systems.
Nov 09 17:00:07 localhost systemd[1]: systemd-udev-trigger.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-udev-trigger.service - Coldplug All udev Devices.
Nov 09 17:00:07 localhost systemd[1]: Stopping systemd-udevd.service - Rule-based Manager for Device Events and Files...
Nov 09 17:00:07 localhost systemd[1]: systemd-vconsole-setup.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-vconsole-setup.service - Virtual Console Setup.
Nov 09 17:00:07 localhost systemd[1]: initrd-cleanup.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Finished initrd-cleanup.service - Cleaning Up and Shutting Down Daemons.
Nov 09 17:00:07 localhost systemd[1]: systemd-udevd.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-udevd.service - Rule-based Manager for Device Events and Files.
Nov 09 17:00:07 localhost systemd[1]: systemd-udevd-varlink.socket: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Closed systemd-udevd-varlink.socket - udev Varlink Socket.
Nov 09 17:00:07 localhost systemd[1]: dracut-pre-udev.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped dracut-pre-udev.service - dracut pre-udev hook.
Nov 09 17:00:07 localhost systemd[1]: dracut-cmdline.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped dracut-cmdline.service - dracut cmdline hook.
Nov 09 17:00:07 localhost systemd[1]: Starting initrd-udevadm-cleanup-db.service - Cleanup udev Database...
Nov 09 17:00:07 localhost systemd[1]: systemd-tmpfiles-setup-dev.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev.
Nov 09 17:00:07 localhost systemd[1]: systemd-tmpfiles-setup-dev-early.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully.
Nov 09 17:00:07 localhost systemd[1]: kmod-static-nodes.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Stopped kmod-static-nodes.service - Create List of Static Device Nodes.
Nov 09 17:00:07 localhost systemd[1]: initrd-udevadm-cleanup-db.service: Deactivated successfully.
Nov 09 17:00:07 localhost systemd[1]: Finished initrd-udevadm-cleanup-db.service - Cleanup udev Database.
Nov 09 17:00:07 localhost systemd[1]: Reached target initrd-switch-root.target - Switch Root.
Nov 09 17:00:07 localhost systemd[1]: Starting initrd-switch-root.service - Switch Root...
Nov 09 17:00:07 localhost systemd[1]: Switching root.
Nov 09 17:00:07 localhost systemd-journald[217]: Journal stopped
Nov 09 17:00:09 host01.example.net systemd-journald[217]: Received SIGTERM from PID 1 (systemd).
Nov 09 17:00:09 host01.example.net kernel: audit: type=1404 audit(1794243607.589:2): enforcing=1 old_enforcing=0 auid=4294967295 ses=4294967295 enabled=1 old-enabled=1 lsm=selinux res=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission firmware_load in class system not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission kexec_image_load in class system not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission kexec_initramfs_load in class system not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission policy_load in class system not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission x509_certificate_load in class system not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission map_create_as in class bpf not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission prog_load_as in class bpf not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Permission allowed in class io_uring not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux:  Class memfd_file not defined in policy.
Nov 09 17:00:09 host01.example.net kernel: SELinux: the above unknown classes and permissions will be allowed
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability network_peer_controls=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability open_perms=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability extended_socket_class=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability always_check_network=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability cgroup_seclabel=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability nnp_nosuid_transition=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability genfs_seclabel_symlinks=1
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability ioctl_skip_cloexec=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability userspace_initial_context=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability netlink_xperm=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability netif_wildcard=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability genfs_seclabel_wildcard=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability functionfs_seclabel=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability memfd_class=0
Nov 09 17:00:09 host01.example.net kernel: SELinux:  policy capability bpf_token_perms=0
Nov 09 17:00:09 host01.example.net kernel: audit: type=1403 audit(1794243607.713:3): auid=4294967295 ses=4294967295 lsm=selinux res=1
Nov 09 17:00:09 host01.example.net systemd[1]: Successfully loaded SELinux policy in 128.003ms.
Nov 09 17:00:09 host01.example.net kernel: NET: Registered PF_VSOCK protocol family
Nov 09 17:00:09 host01.example.net systemd[1]: Relabeled /dev/, /dev/shm/, /run/ in 12.489ms.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd 262-3.fc45 running in system mode (+PAM +AUDIT +SELINUX -APPARMOR +IMA +IPE +SMACK +SECCOMP +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 +KMOD +LIBCRYPTSETUP +LIBCRYPTSETUP_PLUGINS +LIBFDISK +PCRE2 +PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD +BPF_FRAMEWORK +BTF +XKBCOMMON +UTMP +LIBARCHIVE)
Nov 09 17:00:09 host01.example.net systemd[1]: Detected virtualization kvm.
Nov 09 17:00:09 host01.example.net systemd[1]: Detected architecture x86-64.
Nov 09 17:00:09 host01.example.net systemd[1]: Hostname set to <host01.example.net>.
Nov 09 17:00:09 host01.example.net systemd[1]: bpf-restrict-fs: LSM BPF program attached
Nov 09 17:00:09 host01.example.net kernel: zram: Added device: zram0
Nov 09 17:00:09 host01.example.net systemd[1]: initrd-switch-root.service: Deactivated successfully.
Nov 09 17:00:09 host01.example.net systemd[1]: Stopped initrd-switch-root.service - Switch Root.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-journald.service: Scheduled restart job, restart counter is at 1.
Nov 09 17:00:09 host01.example.net systemd[1]: Created slice system-kmsconvt.slice - Slice /system/kmsconvt.
Nov 09 17:00:09 host01.example.net systemd[1]: Created slice system-serial\x2dgetty.slice - Slice /system/serial-getty.
Nov 09 17:00:09 host01.example.net systemd[1]: Created slice system-sshd\x2dkeygen.slice - Slice /system/sshd-keygen.
Nov 09 17:00:09 host01.example.net systemd[1]: Created slice system-systemd\x2dzram\x2dsetup.slice - Slice /system/systemd-zram-setup.
Nov 09 17:00:09 host01.example.net systemd[1]: Created slice user.slice - User and Session Slice.
Nov 09 17:00:09 host01.example.net systemd[1]: Started systemd-ask-password-console.path - Dispatch Password Requests to Console Directory Watch.
Nov 09 17:00:09 host01.example.net systemd[1]: Started systemd-ask-password-wall.path - Forward Password Requests to Wall Directory Watch.
Nov 09 17:00:09 host01.example.net systemd[1]: Set up automount proc-sys-fs-binfmt_misc.automount - Arbitrary Executable File Formats File System Automount Point.
Nov 09 17:00:09 host01.example.net systemd[1]: Expecting device dev-disk-by\x2duuid-89f8a76e\x2dbfd7\x2d4e60\x2d89f8\x2db1769a33429a.device - /dev/disk/by-uuid/00000000-0000-0000-0000-000000000000...
Nov 09 17:00:09 host01.example.net systemd[1]: Expecting device dev-disk-by\x2duuid-9767\x2d0BCD.device - /dev/disk/by-uuid/9767-0BCD...
Nov 09 17:00:09 host01.example.net systemd[1]: Expecting device dev-ttyS0.device - /dev/ttyS0...
Nov 09 17:00:09 host01.example.net systemd[1]: Expecting device dev-zram0.device - /dev/zram0...
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target clonesetup.target - Local dm-clone Devices.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target imports.target - Image Downloads.
Nov 09 17:00:09 host01.example.net systemd[1]: Stopped target initrd-switch-root.target - Switch Root.
Nov 09 17:00:09 host01.example.net systemd[1]: Stopped target initrd-fs.target - Initrd File Systems.
Nov 09 17:00:09 host01.example.net systemd[1]: Stopped target initrd-root-fs.target - Initrd Root File System.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target integritysetup.target - Local Integrity Protected Volumes.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target paths.target - Path Units.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target remote-cryptsetup.target - Remote Encrypted Volumes.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target remote-fs.target - Remote File Systems.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target remote-veritysetup.target - Remote Verity Protected Volumes.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target slices.target - Slice Units.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target veritysetup.target - Local Verity Protected Volumes.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on dm-event.socket - Device-mapper event daemon FIFOs.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on lvm2-lvmpolld.socket - LVM2 poll daemon socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-ask-password.socket - Query the User Interactively for a Password.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-coredump.socket - Process Core Dump Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-creds.socket - Credential Encryption/Decryption.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-cryptenroll.socket - Disk Encryption Enrollment Service Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-factory-reset.socket - Factory Reset Management.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-hostnamed.socket - Hostname Service Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-journald-audit.socket - Journal Audit Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-mute-console.socket - Console Output Muting Service Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-oomd.socket - Userspace Out-Of-Memory (OOM) Killer Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-pcrextend.socket - TPM PCR Measurements skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-pcrlock.socket - Make TPM PCR Policy skipped, unmet condition check ConditionSecurity=measured-uki
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-repart.socket - Disk Repartitioning Service Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-report-basic.socket - Report System Basic Metrics Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-report-cgroup.socket - CGroup Report Varlink Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-report-files.socket - Report Files Metrics Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-report-sign-tsm.socket - Report Signing Socket (configfs-tsm) skipped, unmet condition check ConditionSecurity=cvm
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-report.socket - System Report Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-resolved-monitor.socket - Resolve Monitor Varlink Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-resolved-varlink.socket - Resolve Service Varlink Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-storage-block.socket - Simple Block Device Backed Storage Provider.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-sysinstall.socket - System Install Tool.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-sysupdate.socket - System Updates.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-udevd-varlink.socket - udev Varlink Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-userdbd.socket - User Database Manager Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Mounting dev-hugepages.mount - Huge Pages File System...
Nov 09 17:00:09 host01.example.net systemd[1]: Mounting dev-mqueue.mount - POSIX Message Queue File System...
Nov 09 17:00:09 host01.example.net systemd[1]: Mounting sys-kernel-debug.mount - Kernel Debug File System...
Nov 09 17:00:09 host01.example.net systemd[1]: Mounting sys-kernel-tracing.mount - Kernel Trace File System...
Nov 09 17:00:09 host01.example.net systemd[1]: fips-crypto-policy-overlay.service - Bind-mount FIPS crypto-policy in FIPS mode skipped, unmet condition check ConditionKernelCommandLine=fips=1
Nov 09 17:00:09 host01.example.net systemd[1]: Starting kmod-static-nodes.service - Create List of Static Device Nodes...
Nov 09 17:00:09 host01.example.net systemd[1]: Starting lvm2-monitor.service - Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling...
Nov 09 17:00:09 host01.example.net systemd[1]: modprobe@configfs.service - Load Kernel Module configfs skipped, unmet condition check ConditionKernelModuleLoaded=!configfs
Nov 09 17:00:09 host01.example.net systemd[1]: modprobe@drm.service - Load Kernel Module drm skipped, unmet condition check ConditionKernelModuleLoaded=!drm
Nov 09 17:00:09 host01.example.net systemd[1]: modprobe@efi_pstore.service - Load Kernel Module efi_pstore skipped, unmet condition check ConditionKernelModuleLoaded=!efi_pstore
Nov 09 17:00:09 host01.example.net systemd[1]: modprobe@fuse.service - Load Kernel Module fuse skipped, unmet condition check ConditionKernelModuleLoaded=!fuse
Nov 09 17:00:09 host01.example.net systemd[1]: Mounting sys-fs-fuse-connections.mount - FUSE Control File System...
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-boot-clear-sysfail.service - Clear SysFail Entry If The Boot Is Successful skipped, unmet condition check ConditionPathExists=/sys/firmware/efi/efivars/LoaderEntrySysFail-00000000-0000-0000-0000-000000000000
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-hibernate-clear.service - Clear Stale Hibernate Storage Info skipped, unmet condition check ConditionPathExists=/sys/firmware/efi/efivars/HibernateLocation-00000000-0000-0000-0000-000000000000
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-journald.service - Journal Service...
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-modules-load.service - Load Kernel Modules...
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-network-generator.service - Generate Network Units from Kernel Command Line...
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-pcrmachine.service - TPM PCR Machine ID Measurement skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-pcrosseparator.service - TPM PCR OS Separator skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-remount-fs.service - Remount Root and Kernel File Systems...
Nov 09 17:00:09 host01.example.net systemd-journald[501]: Collecting audit messages is enabled.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-tpm2-setup-early.service - Early TPM SRK Setup skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-pcrnvdone.service - TPM PCR NvPCR Initialization Separator skipped, unmet condition check ConditionPathExists=/etc/initrd-release
Nov 09 17:00:09 host01.example.net systemd-journald[501]: Journal started
Nov 09 17:00:09 host01.example.net systemd-journald[501]: Runtime Journal (/run/log/journal/00000000000000000000000000000000) is 4.8M, max 39M, 34.1M free.
Nov 09 17:00:09 host01.example.net systemd[1]: Queued start job for default target multi-user.target.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-journald.service: Deactivated successfully.
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target cryptsetup.target - Local Encrypted Volumes.
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-udev-load-credentials.service - Load udev Rules from Credentials...
Nov 09 17:00:09 host01.example.net kernel: BTRFS info (device vda3 state M): use zstd compression, level 1
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-udev-trigger.service - Coldplug All udev Devices...
Nov 09 17:00:09 host01.example.net systemd[1]: Started systemd-journald.service - Journal Service.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-journald comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Mounted dev-hugepages.mount - Huge Pages File System.
Nov 09 17:00:09 host01.example.net systemd[1]: Mounted dev-mqueue.mount - POSIX Message Queue File System.
Nov 09 17:00:09 host01.example.net systemd[1]: Mounted sys-kernel-debug.mount - Kernel Debug File System.
Nov 09 17:00:09 host01.example.net systemd[1]: Mounted sys-kernel-tracing.mount - Kernel Trace File System.
Nov 09 17:00:09 host01.example.net systemd[1]: Finished kmod-static-nodes.service - Create List of Static Device Nodes.
Nov 09 17:00:09 host01.example.net systemd[1]: Finished lvm2-monitor.service - Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling.
Nov 09 17:00:09 host01.example.net systemd[1]: Mounted sys-fs-fuse-connections.mount - FUSE Control File System.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=kmod-static-nodes comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.667:4): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-journald comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.684:5): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=kmod-static-nodes comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-modules-load.service - Load Kernel Modules.
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-network-generator.service - Generate Network Units from Kernel Command Line.
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-remount-fs.service - Remount Root and Kernel File Systems.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=lvm2-monitor comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.686:6): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=lvm2-monitor comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-udev-load-credentials.service - Load udev Rules from Credentials.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-modules-load comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.697:7): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-modules-load comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-network-generator comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.700:8): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-network-generator comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-hwdb-update.service - Rebuild Hardware Database skipped, unmet condition check ConditionNeedsUpdate=/etc
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-remount-fs comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-sysctl.service - Apply Kernel Variables...
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-load-credentials comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.703:9): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-remount-fs comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.712:10): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-load-credentials comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully...
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-sysctl.service - Apply Kernel Variables.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-sysctl comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.769:11): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-sysctl comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-tmpfiles-setup-dev-early comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-sysusers.service - Create System Users skipped, no trigger condition checks were met.
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-journalctl-metrics.socket - Journal Metrics Report Socket...
Nov 09 17:00:09 host01.example.net kernel: audit: type=1130 audit(1794243609.791:12): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-tmpfiles-setup-dev-early comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-journalctl.socket - Journal Log Access Socket...
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=48 op=LOAD
Nov 09 17:00:09 host01.example.net kernel: audit: type=1334 audit(1794243609.810:13): prog-id=48 op=LOAD
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-resolved.service - Network Name Resolution...
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev...
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-udev-trigger.service - Coldplug All udev Devices.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-trigger comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-journalctl-metrics.socket - Journal Metrics Report Socket.
Nov 09 17:00:09 host01.example.net systemd[1]: Listening on systemd-journalctl.socket - Journal Log Access Socket.
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=49 op=LOAD
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=50 op=LOAD
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=51 op=LOAD
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-userdbd.service - User Database Manager...
Nov 09 17:00:09 host01.example.net systemd[1]: Finished systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-tmpfiles-setup-dev comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target local-fs-pre.target - Preparation for Local File Systems.
Nov 09 17:00:09 host01.example.net systemd[1]: systemd-repart.service - Repartition Root Disk skipped, no trigger condition checks were met.
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=23 op=UNLOAD
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=22 op=UNLOAD
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=52 op=LOAD
Nov 09 17:00:09 host01.example.net audit: BPF prog-id=53 op=LOAD
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-udevd.service - Rule-based Manager for Device Events and Files...
Nov 09 17:00:09 host01.example.net systemd[1]: Started systemd-userdbd.service - User Database Manager.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-userdbd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd-udevd[531]: Using default interface naming scheme 'v261'.
Nov 09 17:00:09 host01.example.net systemd[1]: Started systemd-udevd.service - Rule-based Manager for Device Events and Files.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udevd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd-resolved[526]: Positive Trust Anchors:
Nov 09 17:00:09 host01.example.net systemd-resolved[526]: . IN DS 20326 8 2 e06d44b80b8f1d39a95c0b0d7c65d08458e880409bbc683457104237c7f8ec8d
Nov 09 17:00:09 host01.example.net systemd-resolved[526]: . IN DS 38696 8 2 683d2d0acb8c9b712a1948b27f741219298d0a450d612c483af444a4c0fb2b16
Nov 09 17:00:09 host01.example.net systemd-resolved[526]: Negative trust anchors: home.arpa 10.in-addr.arpa 16.172.in-addr.arpa 17.172.in-addr.arpa 18.172.in-addr.arpa 19.172.in-addr.arpa 20.172.in-addr.arpa 21.172.in-addr.arpa 22.172.in-addr.arpa 23.172.in-addr.arpa 24.172.in-addr.arpa 25.172.in-addr.arpa 26.172.in-addr.arpa 27.172.in-addr.arpa 28.172.in-addr.arpa 29.172.in-addr.arpa 30.172.in-addr.arpa 31.172.in-addr.arpa 170.0.0.192.in-addr.arpa 171.0.0.192.in-addr.arpa 168.192.in-addr.arpa d.f.ip6.arpa ipv4only.arpa resolver.arpa corp home internal intranet lan local private test
Nov 09 17:00:09 host01.example.net systemd-resolved[526]: Using system hostname 'host01.example.net'.
Nov 09 17:00:09 host01.example.net systemd[1]: Started systemd-resolved.service - Network Name Resolution.
Nov 09 17:00:09 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-resolved comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:09 host01.example.net systemd[1]: Reached target nss-lookup.target - Host and Network Name Lookups.
Nov 09 17:00:09 host01.example.net systemd[1]: Found device dev-zram0.device - /dev/zram0.
Nov 09 17:00:09 host01.example.net systemd[1]: modprobe@configfs.service - Load Kernel Module configfs skipped, unmet condition check ConditionKernelModuleLoaded=!configfs
Nov 09 17:00:09 host01.example.net systemd[1]: Starting systemd-zram-setup@zram0.service - Create swap on /dev/zram0...
Nov 09 17:00:09 host01.example.net systemd[1]: modprobe@fuse.service - Load Kernel Module fuse skipped, unmet condition check ConditionKernelModuleLoaded=!fuse
Nov 09 17:00:10 host01.example.net kernel: zram0: detected capacity change from 0 to 3999744
Nov 09 17:00:10 host01.example.net systemd-makefs[553]: Formatting /dev/zram0 as swap
Nov 09 17:00:10 host01.example.net systemd-makefs[553]: /dev/zram0 successfully formatted as swap (label "zram0", uuid 00000000-0000-0000-0000-000000000000)
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-zram-setup@zram0.service - Create swap on /dev/zram0.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-zram-setup@zram0 comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Activating swap dev-zram0.swap - Compressed Swap on /dev/zram0...
Nov 09 17:00:10 host01.example.net kernel: Adding 1999868k swap on /dev/zram0.  Priority:100 extents:1 across:1999868k SSDsc
Nov 09 17:00:10 host01.example.net kernel: clocksource: Watchdog remote CPU 1 read timed out
Nov 09 17:00:10 host01.example.net systemd[1]: Activated swap dev-zram0.swap - Compressed Swap on /dev/zram0.
Nov 09 17:00:10 host01.example.net systemd[1]: Reached target swap.target - Swaps.
Nov 09 17:00:10 host01.example.net audit: BPF prog-id=54 op=LOAD
Nov 09 17:00:10 host01.example.net audit: BPF prog-id=55 op=LOAD
Nov 09 17:00:10 host01.example.net audit: BPF prog-id=56 op=LOAD
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-oomd.service - Userspace Out-Of-Memory (OOM) Killer...
Nov 09 17:00:10 host01.example.net systemd[1]: Condition check resulted in dev-ttyS0.device - /dev/ttyS0 being skipped.
Nov 09 17:00:10 host01.example.net systemd[1]: Started systemd-oomd.service - Userspace Out-Of-Memory (OOM) Killer.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-oomd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Mounting tmp.mount - Temporary Directory /tmp...
Nov 09 17:00:10 host01.example.net systemd[1]: Mounted tmp.mount - Temporary Directory /tmp.
Nov 09 17:00:10 host01.example.net kernel: bochs-drm 0000:00:01.0: vgaarb: deactivate vga console
Nov 09 17:00:10 host01.example.net kernel: Console: switching to colour dummy device 80x25
Nov 09 17:00:10 host01.example.net systemd[1]: Found device dev-disk-by\x2duuid-89f8a76e\x2dbfd7\x2d4e60\x2d89f8\x2db1769a33429a.device - /dev/disk/by-uuid/00000000-0000-0000-0000-000000000000.
Nov 09 17:00:10 host01.example.net kernel: [drm] Found bochs VGA, ID 0xb0c5.
Nov 09 17:00:10 host01.example.net kernel: [drm] Framebuffer size 16384 kB @ 0xfd000000, mmio @ 0xfeb90000.
Nov 09 17:00:10 host01.example.net systemd[1]: Condition check resulted in dev-disk-by\x2duuid-9767\x2d0BCD.device - /dev/disk/by-uuid/9767-0BCD being skipped.
Nov 09 17:00:10 host01.example.net systemd[1]: boot.mount: Directory /boot to mount over is not empty, mounting anyway.
Nov 09 17:00:10 host01.example.net kernel: bochs-drm 0000:00:01.0: [drm] Registered 1 planes with drm panic
Nov 09 17:00:10 host01.example.net systemd[1]: Mounting boot.mount - /boot...
Nov 09 17:00:10 host01.example.net kernel: [drm] Initialized bochs-drm 1.0.0 for 0000:00:01.0 on minor 0
Nov 09 17:00:10 host01.example.net systemd[1]: Mounting home.mount - /home...
Nov 09 17:00:10 host01.example.net systemd[1]: Mounting var.mount - /var...
Nov 09 17:00:10 host01.example.net systemd[1]: Mounted home.mount - /home.
Nov 09 17:00:10 host01.example.net kernel: parport_pc 00:02: reported by Plug and Play ACPI
Nov 09 17:00:10 host01.example.net kernel: parport0: PC-style at 0x378, irq 7 [PCSPP,TRISTATE]
Nov 09 17:00:10 host01.example.net systemd[1]: Mounted boot.mount - /boot.
Nov 09 17:00:10 host01.example.net kernel: i801_smbus 0000:00:1f.3: SMBus using PCI interrupt
Nov 09 17:00:10 host01.example.net kernel: i2c i2c-0: Memory type 0x07 not supported yet, not instantiating SPD
Nov 09 17:00:10 host01.example.net kernel: Console: switching to colour frame buffer device 160x50
Nov 09 17:00:10 host01.example.net kernel: virtio_net virtio2 enp0s4: renamed from eth0
Nov 09 17:00:10 host01.example.net kernel: bochs-drm 0000:00:01.0: [drm] fb0: bochs-drmdrmfb frame buffer device
Nov 09 17:00:10 host01.example.net systemd[1]: Mounted var.mount - /var.
Nov 09 17:00:10 host01.example.net systemd[1]: Listening on systemd-report-sign-plain.socket - Report Signing Socket (Local Software Key).
Nov 09 17:00:10 host01.example.net systemd[1]: Listening on systemd-storage-fs.socket - Simple File System Backed Storage Provider.
Nov 09 17:00:10 host01.example.net systemd[1]: Mounting boot-efi.mount - /boot/efi...
Nov 09 17:00:10 host01.example.net systemd[1]: Starting cloud-init-main.service - Cloud-init: Single Process...
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-journal-flush.service - Flush Journal to Persistent Storage...
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-pcrproduct.service - TPM NvPCR Product ID Measurement skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-pstore.service - Platform Persistent Storage Archival skipped, unmet condition check ConditionDirectoryNotEmpty=/sys/fs/pstore
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-random-seed.service - Load/Save OS Random Seed...
Nov 09 17:00:10 host01.example.net systemd-journald[501]: Time spent on flushing to /var/log/journal/00000000000000000000000000000000 is 26.075ms for 897 entries.
Nov 09 17:00:10 host01.example.net systemd-journald[501]: System Journal (/var/log/journal/00000000000000000000000000000000) is 8M, max 1.9G, 1.9G free.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-random-seed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd-journald[501]: Received client request to flush runtime journal.
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-tpm2-setup.service - TPM SRK Setup skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:10 host01.example.net kernel: ppdev: user-space parallel port driver
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-random-seed.service - Load/Save OS Random Seed.
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-vconsole-setup.service - Virtual Console Setup...
Nov 09 17:00:10 host01.example.net systemd[1]: Mounted boot-efi.mount - /boot/efi.
Nov 09 17:00:10 host01.example.net systemd[1]: Reached target local-fs.target - Local File Systems.
Nov 09 17:00:10 host01.example.net systemd[1]: Listening on systemd-bootctl.socket - Boot Loader Control Service Socket.
Nov 09 17:00:10 host01.example.net systemd[1]: Listening on systemd-sysext.socket - System Extension Image Management.
Nov 09 17:00:10 host01.example.net systemd[1]: selinux-autorelabel-mark.service - Mark the need to relabel after reboot skipped, unmet condition check ConditionSecurity=!selinux
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-binfmt.service - Set Up Additional Binary Formats...
Nov 09 17:00:10 host01.example.net kernel: kvm_amd: TSC scaling supported
Nov 09 17:00:10 host01.example.net kernel: kvm_amd: Nested Virtualization enabled
Nov 09 17:00:10 host01.example.net kernel: kvm_amd: Nested Paging enabled
Nov 09 17:00:10 host01.example.net kernel: kvm_amd: Virtual VMLOAD VMSAVE supported
Nov 09 17:00:10 host01.example.net kernel: kvm_amd: PMU virtualization is disabled
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-boot-random-seed.service - Update Boot Loader Random Seed skipped, no trigger condition checks were met.
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-confext.service - Merge System Configuration Images into /etc/ skipped, no trigger condition checks were met.
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-sysext.service - Merge System Extension Images into /usr/ and /opt/ skipped, no trigger condition checks were met.
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-userdb-load-credentials.service - Load JSON user/group Records from Credentials...
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-journal-flush.service - Flush Journal to Persistent Storage.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-journal-flush comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: proc-sys-fs-binfmt_misc.automount: Got automount request for /proc/sys/fs/binfmt_misc, triggered by 592 (systemd-binfmt)
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-userdb-load-credentials.service - Load JSON user/group Records from Credentials.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-userdb-load-credentials comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-tmpfiles-setup.service - Create System Files and Directories...
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-vconsole-setup.service: Deactivated successfully.
Nov 09 17:00:10 host01.example.net systemd[1]: Stopped systemd-vconsole-setup.service - Virtual Console Setup.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-vconsole-setup comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-vconsole-setup comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-vconsole-setup.service - Virtual Console Setup...
Nov 09 17:00:10 host01.example.net systemd-vconsole-setup[599]: Configuration of first virtual console was skipped, ignoring remaining ones.
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-vconsole-setup.service - Virtual Console Setup.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-vconsole-setup comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-tmpfiles-setup.service - Create System Files and Directories.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-tmpfiles-setup comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Starting auditd.service - Security Audit Logging Service...
Nov 09 17:00:10 host01.example.net systemd[1]: ldconfig.service - Rebuild Dynamic Linker Cache skipped, no trigger condition checks were met.
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-firstboot.service - Initial Setup skipped, unmet condition check ConditionFirstBoot=yes
Nov 09 17:00:10 host01.example.net systemd[1]: first-boot-complete.target - First Boot Complete skipped, unmet condition check ConditionFirstBoot=yes
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-journal-catalog-update.service - Rebuild Journal Catalog skipped, unmet condition check ConditionNeedsUpdate=/var
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-machine-id-commit.service - Save Transient machine-id to Disk skipped, unmet condition check ConditionPathIsMountPoint=/etc/machine-id
Nov 09 17:00:10 host01.example.net systemd[1]: systemd-update-done.service - Update is Completed skipped, no trigger condition checks were met.
Nov 09 17:00:10 host01.example.net auditd[605]: No plugins found, not dispatching events
Nov 09 17:00:10 host01.example.net audit: CONFIG_CHANGE op=set audit_enabled=1 old=1 auid=4294967295 ses=4294967295 subj=system_u:system_r:auditd_t:s0 res=1
Nov 09 17:00:10 host01.example.net audit[605]: SYSCALL arch=c000003e syscall=44 success=yes exit=60 a0=3 a1=7ffe451c7af0 a2=3c a3=0 items=0 ppid=604 pid=605 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="auditd" exe="/usr/bin/auditd" subj=system_u:system_r:auditd_t:s0 key=(null)
Nov 09 17:00:10 host01.example.net audit: PROCTITLE proctitle="/usr/bin/auditd"
Nov 09 17:00:10 host01.example.net audit: CONFIG_CHANGE op=set audit_pid=605 old=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:auditd_t:s0 res=1
Nov 09 17:00:10 host01.example.net audit[605]: SYSCALL arch=c000003e syscall=44 success=yes exit=60 a0=3 a1=7ffe451c57b0 a2=3c a3=0 items=0 ppid=604 pid=605 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="auditd" exe="/usr/bin/auditd" subj=system_u:system_r:auditd_t:s0 key=(null)
Nov 09 17:00:10 host01.example.net audit: PROCTITLE proctitle="/usr/bin/auditd"
Nov 09 17:00:10 host01.example.net auditd[605]: Init complete, auditd 4.2.1 listening for events (startup state enable)
Nov 09 17:00:10 host01.example.net systemd[1]: Started auditd.service - Security Audit Logging Service.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=auditd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Starting audit-rules.service - Load Audit Rules...
Nov 09 17:00:10 host01.example.net systemd[1]: Starting systemd-update-utmp.service - Record System Boot/Shutdown in UTMP...
Nov 09 17:00:10 host01.example.net audit[610]: SYSTEM_BOOT pid=610 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg=' comm="update-utmp" exe="/usr/lib/systemd/systemd-update-utmp" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net systemd[1]: Finished systemd-update-utmp.service - Record System Boot/Shutdown in UTMP.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-update-utmp comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net augenrules[609]: /usr/bin/augenrules: No change
Nov 09 17:00:10 host01.example.net audit: CONFIG_CHANGE auid=4294967295 ses=4294967295 subj=system_u:system_r:unconfined_service_t:s0 op=add_rule key=(null) list=1 res=1
Nov 09 17:00:10 host01.example.net audit[625]: SYSCALL arch=c000003e syscall=44 success=yes exit=1056 a0=3 a1=7ffe7d40bd00 a2=420 a3=0 items=0 ppid=609 pid=625 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="auditctl" exe="/usr/bin/auditctl" subj=system_u:system_r:unconfined_service_t:s0 key=(null)
Nov 09 17:00:10 host01.example.net audit: PROCTITLE proctitle=2F7573722F62696E2F617564697463746C002D52002F6574632F61756469742F61756469742E72756C6573
Nov 09 17:00:10 host01.example.net augenrules[625]: No rules
Nov 09 17:00:10 host01.example.net systemd[1]: audit-rules.service: Deactivated successfully.
Nov 09 17:00:10 host01.example.net systemd[1]: Finished audit-rules.service - Load Audit Rules.
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=audit-rules comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:10 host01.example.net audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=audit-rules comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Started cloud-init-main.service - Cloud-init: Single Process.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-init-main comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Starting cloud-init-local.service - Cloud-init: Local Stage (pre-network)...
Nov 09 17:00:11 host01.example.net systemd[1]: Mounting proc-sys-fs-binfmt_misc.mount - Arbitrary Executable File Formats File System...
Nov 09 17:00:11 host01.example.net systemd[1]: Mounted proc-sys-fs-binfmt_misc.mount - Arbitrary Executable File Formats File System.
Nov 09 17:00:11 host01.example.net systemd[1]: Finished systemd-binfmt.service - Set Up Additional Binary Formats.
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target sysinit.target - System Initialization.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-binfmt comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Started dnf-makecache.timer - dnf5 makecache.
Nov 09 17:00:11 host01.example.net systemd[1]: Started fstrim.timer - Discard unused filesystem blocks once a week.
Nov 09 17:00:11 host01.example.net systemd[1]: Started logrotate.timer - Daily rotation of log files.
Nov 09 17:00:11 host01.example.net systemd[1]: Started systemd-tmpfiles-clean.timer - Daily Cleanup of Temporary Directories.
Nov 09 17:00:11 host01.example.net cloud-init[642]: Cloud-init v. 26.2 running 'init-local' at Mon, 09 Nov 2026 17:00:11 +0000. Up 7.68 seconds.
Nov 09 17:00:11 host01.example.net systemd[1]: Started unbound-anchor.timer - daily update of the root trust anchor for DNSSEC.
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target timers.target - Timer Units.
Nov 09 17:00:11 host01.example.net systemd[1]: Listening on dbus.socket - D-Bus System Message Bus Socket.
Nov 09 17:00:11 host01.example.net systemd[1]: Listening on sshd-unix-local.socket - OpenSSH Server Socket (systemd-ssh-generator, AF_UNIX Local).
Nov 09 17:00:11 host01.example.net systemd[1]: Listening on sssd-kcm.socket - SSSD Kerberos Cache Manager responder socket.
Nov 09 17:00:11 host01.example.net systemd[1]: Listening on systemd-logind-varlink.socket - User Login Management Varlink Socket.
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target sockets.target - Socket Units.
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=57 op=LOAD
Nov 09 17:00:11 host01.example.net systemd[1]: Starting dbus-broker.service - D-Bus System Message Bus...
Nov 09 17:00:11 host01.example.net systemd[1]: rpmdb-rebuild.service - RPM database rebuild skipped, unmet condition check ConditionPathExists=/usr/lib/sysimage/rpm/.rebuilddb
Nov 09 17:00:11 host01.example.net systemd[1]: systemd-pcrphase-sysinit.service - TPM PCR Barrier (Initialization) skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:11 host01.example.net systemd[1]: Started dbus-broker.service - D-Bus System Message Bus.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=dbus-broker comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target basic.target - Basic System.
Nov 09 17:00:11 host01.example.net systemd[1]: Starting authselect-apply-changes.service - Apply authselect changes...
Nov 09 17:00:11 host01.example.net dbus-broker-launch[643]: Ready
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=58 op=LOAD
Nov 09 17:00:11 host01.example.net systemd[1]: Starting chronyd.service - NTP client/server...
Nov 09 17:00:11 host01.example.net systemd[1]: Starting dracut-shutdown.service - Restore /run/initramfs on shutdown...
Nov 09 17:00:11 host01.example.net authselect[646]: Installed profiles did not change. No action is needed.
Nov 09 17:00:11 host01.example.net systemd[1]: ssh-host-keys-migration.service - Update OpenSSH host key permissions skipped, unmet condition check ConditionPathExists=!/var/lib/.ssh-host-keys-migration
Nov 09 17:00:11 host01.example.net systemd[1]: sshd-keygen@ecdsa.service - OpenSSH ecdsa Server Key Generation skipped, unmet condition check ConditionPathExists=!/run/systemd/generator.early/multi-user.target.wants/cloud-init.target
Nov 09 17:00:11 host01.example.net systemd[1]: sshd-keygen@ed25519.service - OpenSSH ed25519 Server Key Generation skipped, unmet condition check ConditionPathExists=!/run/systemd/generator.early/multi-user.target.wants/cloud-init.target
Nov 09 17:00:11 host01.example.net systemd[1]: sshd-keygen@rsa.service - OpenSSH rsa Server Key Generation skipped, unmet condition check ConditionPathExists=!/run/systemd/generator.early/multi-user.target.wants/cloud-init.target
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target sshd-keygen.target.
Nov 09 17:00:11 host01.example.net systemd[1]: sssd.service - System Security Services Daemon skipped, no trigger condition checks were met.
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=59 op=LOAD
Nov 09 17:00:11 host01.example.net systemd[1]: Starting systemd-homed.service - Home Area Manager...
Nov 09 17:00:11 host01.example.net systemd[1]: systemd-pcrphase.service - TPM PCR Barrier (User) skipped, unmet condition check ConditionSecurity=measured-os
Nov 09 17:00:11 host01.example.net systemd[1]: Finished authselect-apply-changes.service - Apply authselect changes.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=authselect-apply-changes comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Finished dracut-shutdown.service - Restore /run/initramfs on shutdown.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=dracut-shutdown comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target nss-user-lookup.target - User and Group Name Lookups.
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=60 op=LOAD
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=61 op=LOAD
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=62 op=LOAD
Nov 09 17:00:11 host01.example.net systemd[1]: Starting systemd-logind.service - User Login Management...
Nov 09 17:00:11 host01.example.net systemd-homed[650]: Watching /home.
Nov 09 17:00:11 host01.example.net systemd[1]: Started systemd-homed.service - Home Area Manager.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-homed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Finished systemd-homed-activate.service - Home Area Activation.
Nov 09 17:00:11 host01.example.net chronyd[647]: chronyd version 4.9 starting (+CMDMON +REFCLOCK +RTC +PRIVDROP +SCFILTER +SIGND +NTS +SECHASH +IPV6 +DEBUG)
Nov 09 17:00:11 host01.example.net chronyd[647]: Using leap second list /usr/share/zoneinfo/leap-seconds.list
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-homed-activate comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net chronyd[647]: Frequency 6.971 +/- 833.745 ppm read from /var/lib/chrony/drift
Nov 09 17:00:11 host01.example.net chronyd[647]: Loaded seccomp filter (level 2)
Nov 09 17:00:11 host01.example.net systemd[1]: Started chronyd.service - NTP client/server.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=chronyd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd-logind[660]: New seat seat0.
Nov 09 17:00:11 host01.example.net systemd-logind[660]: Watching system buttons on /dev/input/event0 (Power Button)
Nov 09 17:00:11 host01.example.net systemd-logind[660]: Watching system buttons on /dev/input/event1 (AT Translated Set 2 keyboard)
Nov 09 17:00:11 host01.example.net systemd[1]: Started systemd-logind.service - User Login Management.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-logind comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net kernel: ISO 9660 Extensions: Microsoft Joliet Level 3
Nov 09 17:00:11 host01.example.net kernel: ISO 9660 Extensions: RRIP_1991A
Nov 09 17:00:11 host01.example.net systemd[1]: run-cloud\x2dinit-tmp-tmpqwzgi8ry.mount: Deactivated successfully.
Nov 09 17:00:11 host01.example.net systemd[1]: Finished cloud-init-local.service - Cloud-init: Local Stage (pre-network).
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-init-local comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target network-pre.target - Preparation for Network.
Nov 09 17:00:11 host01.example.net systemd[1]: Starting NetworkManager.service - Network Manager...
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.6498] NetworkManager (version 1.58.1-3.fc45) is starting... (boot:00000000-0000-0000-0000-000000000000)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.6500] Read config: /etc/NetworkManager/NetworkManager.conf, /usr/lib/NetworkManager/conf.d/{22-wifi-mac-addr.conf,24-clat-auto.conf}, /etc/NetworkManager/conf.d/30-cloud-init-ip6-addr-gen-mode.conf
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.6548] manager[0x55ddd35f5950]: monitoring kernel firmware directory '/lib/firmware'.
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=63 op=LOAD
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=64 op=LOAD
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=65 op=LOAD
Nov 09 17:00:11 host01.example.net systemd[1]: Starting systemd-hostnamed.service - Hostname Service...
Nov 09 17:00:11 host01.example.net systemd[1]: Started systemd-hostnamed.service - Hostname Service.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-hostnamed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7165] hostname: hostname: using hostnamed
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7166] hostname: static hostname changed from (none) to "host01.example.net"
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7168] dns-mgr: init: dns=systemd-resolved rc-manager=unmanaged (auto), plugin=systemd-resolved
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7188] manager: rfkill: Wi-Fi enabled by radio killswitch; enabled by state file
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7189] manager: rfkill: WWAN enabled by radio killswitch; enabled by state file
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7189] manager: Networking is enabled by state file
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7191] settings: Loaded settings plugin: keyfile (internal)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7202] dhcp: init: Using DHCP client 'internal'
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7203] manager: (lo): new Loopback device (/org/freedesktop/NetworkManager/Devices/1)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7209] device (lo): state change: unmanaged -> unavailable (reason 'connection-assumed', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7211] device (lo): state change: unavailable -> disconnected (reason 'connection-assumed', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7214] device (lo): Activation: starting connection 'lo' (00000000-0000-0000-0000-000000000000)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7220] manager: (enp0s4): new Ethernet device (/org/freedesktop/NetworkManager/Devices/2)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7221] device (enp0s4): state change: unmanaged -> unavailable (reason 'managed', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7239] bus-manager: acquired D-Bus service "org.freedesktop.NetworkManager"
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7241] device (lo): state change: disconnected -> prepare (reason 'none', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7241] device (lo): state change: prepare -> config (reason 'none', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7242] device (lo): state change: config -> ip-config (reason 'none', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7242] device (enp0s4): carrier: link connected
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7243] device (lo): state change: ip-config -> ip-check (reason 'none', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7245] device (enp0s4): state change: unavailable -> disconnected (reason 'carrier-changed', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7250] policy: auto-activating connection 'cloud-init enp0s4' (00000000-0000-0000-0000-000000000000)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7252] device (enp0s4): Activation: starting connection 'cloud-init enp0s4' (00000000-0000-0000-0000-000000000000)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7252] device (enp0s4): state change: disconnected -> prepare (reason 'none', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7253] manager: NetworkManager state is now CONNECTING
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7253] device (enp0s4): state change: prepare -> config (reason 'none', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7258] device (enp0s4): state change: config -> ip-config (reason 'none', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7262] dhcp4 (enp0s4): activation: beginning transaction (timeout in 45 seconds)
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7268] dhcp4 (enp0s4): state changed new lease, address=192.0.2.2, acd pending
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=66 op=LOAD
Nov 09 17:00:11 host01.example.net systemd[1]: Started NetworkManager.service - Network Manager.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=NetworkManager comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Reached target network.target - Network.
Nov 09 17:00:11 host01.example.net systemd[1]: Starting NetworkManager-dispatcher.service - Network Manager Script Dispatcher Service...
Nov 09 17:00:11 host01.example.net systemd[1]: Starting NetworkManager-wait-online.service - Network Manager Wait Online...
Nov 09 17:00:11 host01.example.net systemd[1]: Started NetworkManager-dispatcher.service - Network Manager Script Dispatcher Service.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=NetworkManager-dispatcher comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7597] device (lo): state change: ip-check -> secondaries (reason 'none', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7602] device (lo): state change: secondaries -> activated (reason 'none', managed-type: 'external')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.7614] device (lo): Activation: successful, device activated.
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8758] dhcp4 (enp0s4): state changed new lease, address=192.0.2.2
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=67 op=LOAD
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8773] policy: set 'cloud-init enp0s4' (enp0s4) as default for IPv4 routing and DNS
Nov 09 17:00:11 host01.example.net systemd-resolved[526]: enp0s4: Bus client set default route setting: yes
Nov 09 17:00:11 host01.example.net audit: BPF prog-id=66 op=UNLOAD
Nov 09 17:00:11 host01.example.net systemd-resolved[526]: enp0s4: Bus client set DNS server list to: 192.0.2.3
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8833] device (enp0s4): state change: ip-config -> ip-check (reason 'none', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8849] device (enp0s4): state change: ip-check -> secondaries (reason 'none', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8850] device (enp0s4): state change: secondaries -> activated (reason 'none', managed-type: 'full')
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8851] manager: NetworkManager state is now CONNECTED_SITE
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8861] device (enp0s4): Activation: successful, device activated.
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8870] manager: NetworkManager state is now CONNECTED_GLOBAL
Nov 09 17:00:11 host01.example.net NetworkManager[678]: <info>  [1794243611.8871] manager: startup complete
Nov 09 17:00:11 host01.example.net systemd[1]: Finished NetworkManager-wait-online.service - Network Manager Wait Online.
Nov 09 17:00:11 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=NetworkManager-wait-online comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:11 host01.example.net systemd[1]: Starting cloud-init-network.service - Cloud-init: Network Stage...
Nov 09 17:00:11 host01.example.net cloud-init[642]: Cloud-init v. 26.2 running 'init' at Mon, 09 Nov 2026 17:00:11 +0000. Up 8.39 seconds.
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: ++++++++++++++++++++++++++++++++++++Net device info+++++++++++++++++++++++++++++++++++++
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +--------+------+-------------------------+---------------+--------+-------------------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: | Device |  Up  |         Address         |      Mask     | Scope  |     Hw-Address    |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +--------+------+-------------------------+---------------+--------+-------------------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: | enp0s4 | True |        192.0.2.2        | 255.255.255.0 | global | 00:00:5e:00:53:04 |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: | enp0s4 | True | 2001:db8::5/64 |       .       |  link  | 00:00:5e:00:53:04 |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: |   lo   | True |        127.0.0.1        |   255.0.0.0   |  host  |         .         |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: |   lo   | True |         ::1/128         |       .       |  host  |         .         |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +--------+------+-------------------------+---------------+--------+-------------------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +++++++++++++++++++++++++++Route IPv4 info++++++++++++++++++++++++++++
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +-------+-------------+----------+---------------+-----------+-------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: | Route | Destination | Gateway  |    Genmask    | Interface | Flags |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +-------+-------------+----------+---------------+-----------+-------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: |   0   |   0.0.0.0   | 192.0.2.6 |    0.0.0.0    |   enp0s4  |   UG  |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: |   1   |   192.0.2.7  | 0.0.0.0  | 255.255.255.0 |   enp0s4  |   U   |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +-------+-------------+----------+---------------+-----------+-------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +++++++++++++++++++Route IPv6 info+++++++++++++++++++
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +-------+-------------+---------+-----------+-------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: | Route | Destination | Gateway | Interface | Flags |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +-------+-------------+---------+-----------+-------+
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: |   0   |  2001:db8::8/64  |    2001:db8::9   |   enp0s4  |   U   |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: |   2   |  multicast  |    2001:db8::9   |   enp0s4  |   U   |
Nov 09 17:00:11 host01.example.net cloud-init[642]: ci-info: +-------+-------------+---------+-----------+-------+
Nov 09 17:00:12 host01.example.net systemd[1]: Finished cloud-init-network.service - Cloud-init: Network Stage.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-init-network comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net systemd[1]: Reached target cloud-config.target - Cloud-config availability.
Nov 09 17:00:12 host01.example.net systemd[1]: Reached target network-online.target - Network is Online.
Nov 09 17:00:12 host01.example.net systemd[1]: Starting cloud-config.service - Cloud-init: Config Stage...
Nov 09 17:00:12 host01.example.net systemd[1]: Starting sshd.service - OpenSSH server daemon...
Nov 09 17:00:12 host01.example.net systemd[1]: Starting systemd-user-sessions.service - Permit User Sessions...
Nov 09 17:00:12 host01.example.net sshd[790]: Server listening on 0.0.0.0 port 22.
Nov 09 17:00:12 host01.example.net systemd[1]: Finished systemd-user-sessions.service - Permit User Sessions.
Nov 09 17:00:12 host01.example.net sshd[790]: Server listening on 2001:db8::9 port 22.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-user-sessions comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net systemd[1]: Started sshd.service - OpenSSH server daemon.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=sshd comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net systemd[1]: Started kmsconvt@tty1.service - KMS System Console on tty1.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=kmsconvt@tty1 comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net cloud-init[642]: Cloud-init v. 26.2 running 'modules:config' at Mon, 09 Nov 2026 17:00:12 +0000. Up 8.59 seconds.
Nov 09 17:00:12 host01.example.net systemd[1]: Started serial-getty@ttyS0.service - Serial Getty on ttyS0.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=serial-getty@ttyS0 comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net systemd[1]: Reached target getty.target - Login Prompts.
Nov 09 17:00:12 host01.example.net systemd[1]: Reached target multi-user.target - Multi-User System.
Nov 09 17:00:12 host01.example.net systemd[1]: Finished cloud-config.service - Cloud-init: Config Stage.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-config comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net systemd[1]: Starting cloud-final.service - Cloud-init: Final Stage...
Nov 09 17:00:12 host01.example.net kmscon[796]: log: kmscon Revision v10.0.4 Oct  9 2026 00:00:00
Nov 09 17:00:12 host01.example.net audit: BPF prog-id=68 op=LOAD
Nov 09 17:00:12 host01.example.net audit: BPF prog-id=69 op=LOAD
Nov 09 17:00:12 host01.example.net audit: BPF prog-id=70 op=LOAD
Nov 09 17:00:12 host01.example.net systemd[1]: Starting systemd-localed.service - Locale Service...
Nov 09 17:00:12 host01.example.net cloud-init[642]: Cloud-init v. 26.2 running 'modules:final' at Mon, 09 Nov 2026 17:00:12 +0000. Up 8.67 seconds.
Nov 09 17:00:12 host01.example.net cloud-init[642]: Cloud-init v. 26.2 finished at Mon, 09 Nov 2026 17:00:12 +0000. Datasource DataSourceNoCloud [seed=/dev/vdc].  Up 8.71 seconds
Nov 09 17:00:12 host01.example.net systemd[1]: Finished cloud-final.service - Cloud-init: Final Stage.
Nov 09 17:00:12 host01.example.net audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=cloud-final comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
Nov 09 17:00:12 host01.example.net systemd[1]: Reached target cloud-init.target - Cloud-init target.
Nov 09 17:00:12 host01.example.net systemd[1]: Started systemd-localed.service - Locale Service.
Nov 09 17:00:12 host01.example.net systemd[1]: Startup finished in 1.391s (kernel) + 2.662s (initrd) + 4.707s (userspace) = 8.761s.

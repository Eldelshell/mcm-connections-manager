# mcm-connections-manager
MCM is made to ease the management of connections (SSH, VNC, FTP, Telnet & RDP) to several servers either from the CLI or from the GUI. It's aimed at network or system administrators who need to connect every day to different servers by different means and have a lousy memory for passwords.

## NOTE

This project was started on 2009 on [Google Code](https://code.google.com/archive/p/mcm-connections-manager/) and I've decided to save move it to GitHub. It's *not being actively maintained since July 2012*. Some time on the future I might retake this, but not currently. Check the alternatives section below.

I've tested this an it runs on pretty much any Ubuntu distribution.

## Supported protocols:

* SSH
* VNC
* RDP (Windows Remote Desktop)
* FTP
* Telnet
* SSH Tunnels (Using SSH options) (example)

## Features:

* GTK GUI
* Use different options for each connection.
* Tabs navigation. (Alt+1, Alt+2...Alt+N)
* Import from CSV
* Export to CSV, ODF and HTML the list of connections (useful for sharing with team members)
* Clustered SSH/FTP/Telnet/Local Connections
* Themes for terminals.
* Search google using selected text on the console (useful for error hunting).
* Optional field for storing a connection's password. (optional!)
* Install SSH public key on a connected server easily.
* Share your connections data to other team members using the encrypted .mcm file format.

## Terminal

MCM Connections Manager is designed to ease the management of connections to several types of servers from any command line in any Linux server with Python installed.

```
$ mcm
$ mcm -a 
$ mcm -l 
$ mcm -s my_ftp_server 
$ mcm -d delete_me_server
```

## Graphical Interface

The GTK2 version of MCM Connections Manager works as a replacement of the default terminal enhancing it. You've got tabs, different themes and the ability to connect to all your servers with one click.


![MCM GTK with MCM ncurse inside](https://a.fsdn.com/fm/screenshots/6a/84/6a84d7ff6fc5b256ce16b7b48dce418a_medium.png)

## License

MCM Connections Manager is Free Software released under the GPLv3. I've been using it daily for the past four years and there always things that can improve and others can be removed. It's a work in progress project and your help, requests and bugs are welcome.

## Dependencies

MCM depends on several client applications to connect to the different servers. Most of this clients come bundled by default with Xubuntu (main target of development) and other Linux distributions. Some of this applications are:

* OpenSSH client
* xvnc4viewer or embedded python-gtk-vnc
* rdesktop
* lftp
* telnet

I didn't want to reinvent the wheel, that's why I use of-the-shelve clients which work and get patched more frequently.

Also, the MCM depends on several libraries for Python: 

* PyGTK 
* Python Glade Bindings (python-glade) 
* Python VteTerminal Bindings (python-vte) 
* Python GTK VNC Bindings (python-gtk-vnc)

This also come pre-installed with any modern distro which uses GNOME or XFCE.

## SSH Tunnel

You can use MCM to create a SSH Tunnel by simply using the right options. Simply use the appropriate options in the options field when adding a new SSH connection. For example:

* Alias: Google-SSH-Tunnel 
* Type: SSH
* Group: <<ANY>> 
* Username: foo
* Server: my-ssh-server (or the IP address)
* Options: -N -L 55555:www.google.com:80

Here we're creating a secure HTTP connection with google.com using my-ssh-server as the tunnel creator.

More info: http://www.revsys.com/writings/quicktips/ssh-tunnel.html http://www.ssh.com/support/documentation/online/ssh/winhelp/32/Tunneling_Explained.html

## Development

As stated above, MCM is a personal project without any support or any guarantee of active development, but it's open source, you might clone this repository and start hacking it to fit your needs. I believe the code is pretty easy to understand and it shouldn't take more than an hour start up. Also, since it's written in Python and Glade (XML) you can directly hack stuff in the installation directory at `/usr/share/apps/mcm-connections-manager/`.

## Files

A thing I find annoying of many projects, is the lack of a list of files they install or generate in my filesystem. Here's the list of files which MCM uses:

* In `/usr/share/apps/mcm-connections-manager/` is the application
* `${HOME}/.local/share/mcm/mcm.json` your connections
* `${HOME}/.local/share/mcm/tips.json` tips file (currently not used)
* `${HOME}/.config/mcm/mcm.conf` your preferences
* `/usr/share/pixmaps/internet-network-preferences-tools-icone-5174.ico`
* `/usr/share/applications/mcm.desktop`

## Alternatives

Once again, MCM is a personal project born of the need for something that met my needs. If MCM is not for you, I might give you different alternatives which I believe are very good, but don't quite fit with what I wanted (yet):

Gnome Connection Manager is pretty good, but it doesn't support tab navigation, which was a kill for me. Also, that big "donate" button is a little too much.

remmina is also very good, with support for NX and lots more, but missing FTP and no localhost console wasn't either very good. I didn't want to jump around SSH sessions and local ones in different windows.

Summary:	XShipWars - Multiplayer space gaming system
Summary(pl):	XShipWars - System gry kosmicznej dla wielu graczy
Name:		xsw
Version:	1.34.0
Release:	2
License:	GPL-like
Group:		Applications/Games
Source0:	ftp://gd.tuwien.ac.at/games/wolfpack/%{name}-%{version}.tar.bz2
# Source0-md5:	09a3109f8588af9940d71522c713007c
Source1:	%{name}.desktop
Source2:	monitor.desktop
Source3:	unvedit.desktop
Source4:	swserv.init
Source5:	swserv.sysconfig
Patch0:		%{name}-paths.patch
URL:		http://wolfpack.twu.net/ShipWars/XShipWars/
BuildRequires:	XFree86-devel
BuildRequires:	esound-devel
BuildRequires:	libjsw-devel
BuildRequires:	yiff-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xprefix	/usr/X11R6
%define		_xbindir	/usr/X11R6/bin
%define		_xmandir	/usr/X11R6/man
%define		_xdatadir	/usr/X11R6/share

%description
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.

%description -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet.

%package client
Summary:	XShipWars client
Summary(pl):	Klient XShipWars
Group:		Applications/Games
Requires:	%{name}-sounds
Requires:	%{name}-images
Requires:	%{name}-data

%description client
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet. This
package contains game client.

%description client -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet. Ten pakiet zawiera klienta.

%package server
Summary:	XShipWars server
Summary(pl):	Serwer XShipWars
Group:		Applications/Games
Prereq:		/sbin/chkconfig

%description server
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet. This
package contains game server.

%description server -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet. Ten pakiet zawiera serwer.

%package monitor
Summary:	XShipWars monitor
Summary(pl):	Monitor XShipWars
Group:		Applications/Games

%description monitor
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet. This
package contains game monitor.

%description monitor -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet. Ten pakiet zawiera monitor gry.

%package unvedit
Summary:	XShipWars universe editor
Summary(pl):	Edytor wszech�wiata XShipWars
Group:		Applications/Games

%description unvedit
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet. This
package contains universe editor for the game.

%description unvedit -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet. Ten pakiet zawiera edytor
wszech�wiata do gry.

%prep
%setup -qn %{name}%{version}
%patch0 -p1

%build
%configure
%{__make} client_linux
%{__make} server_linux
%{__make} monitor_linux
%{__make} unvedit_linux

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_xdatadir}/xshipwars/{images,sounds}
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Games,/etc/sysconfig,/etc/rc.d/init.d}

%{__make} client_install_unix \
	GAMES_DIR=$RPM_BUILD_ROOT%{_xbindir} \
	XSW_DIR=$RPM_BUILD_ROOT%{_xdatadir}/xshipwars \
	XSW_ETC_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/xshipwars

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/xshipwars/universes # comes with data

%{__make} server_install_unix \
	SWSERV_BASE_DIR=$RPM_BUILD_ROOT/home/services/swserv \
	SWSERV_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	SWSERV_ETC_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/swserv

%{__make} monitor_install_unix \
	DIR_SWSERV=$RPM_BUILD_ROOT%{_xprefix} \
	GAMES_DIR=$RPM_BUILD_ROOT%{_xbindir} \
	PROG_DATA_DIR=$RPM_BUILD_ROOT%{_xdatadir}/xshipwars

%{__make} unvedit_install_unix \
	GAMES_BIN=$RPM_BUILD_ROOT%{_xbindir} \
	PROG_DATA_DIR=$RPM_BUILD_ROOT%{_xdatadir}/xshipwars

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE3} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/swserv
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/swserv

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
grep -q swserv /etc/group || (
	/usr/sbin/groupadd -g 91 -r -f swserv 1>&2 || :
)
grep -q swserv /etc/passwd || (
	/usr/sbin/useradd -M -o -r -u 91 \
		-g swserv -c "XShipWars server" -d /home/services/swserv swserv 1>&2 || :
)

%post server
if [ "$1" = "1" ]; then
	/sbin/chkconfig --add swserv
	echo "Run \"/etc/rc.d/init.d/swserv start\" to start swserv." >&2
else
	if [ -f /var/lock/subsys/swserv ]; then
		/etc/rc.d/init.d/swserv restart >&2
	fi
fi

%preun server
if [ "$1" = 0 ]; then
	if [ -f /var/lock/sybsys/swserv ]; then
		/etc/rc.d/init.d/swserv stop >&2
	fi
	/sbin/chkconfig --del swserv
	rm -f %{_datadir}/swserv/errors
fi

%files client
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE*
%dir %{_sysconfdir}/xshipwars
%config %verify(not size mtime md5) %{_sysconfdir}/xshipwars/*
%attr(755,root,root) %{_xbindir}/xsw
%{_xdatadir}/xshipwars/images
%{_xdatadir}/xshipwars/sounds
%{_applnkdir}/Games/xsw.desktop

%files server
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE*
%dir %attr(751,root,swserv) /home/services/swserv
%attr(775,root,swserv) /home/services/swserv/db
%attr(775,root,swserv) /home/services/swserv/logs
%attr(775,root,swserv) /home/services/swserv/public_html
%attr(775,root,swserv) /home/services/swserv/tmp
%attr(774,root,swserv) /home/services/swserv/restart
%attr(754,root,swserv) %{_bindir}/swserv
%dir %{_sysconfdir}/swserv
%config %verify(not size mtime md5) %{_sysconfdir}/swserv/*
%config %verify(not size mtime md5) /etc/sysconfig/swserv
%attr(754,root,root) /etc/rc.d/init.d/swserv

%files monitor
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE*
%attr(755,root,root) %{_xbindir}/monitor
%{_xdatadir}/xshipwars/images/monitor
%{_applnkdir}/Games/monitor.desktop

%files unvedit
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE*
%attr(755,root,root) %{_xbindir}/unvedit
%{_xdatadir}/xshipwars/images/unvedit
%{_applnkdir}/Games/unvedit.desktop

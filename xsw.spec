Summary:	XShipWars - Multiplayer space gaming system
Summary(pl):	XShipWars - System gry kosmicznej dla wielu graczy
Name:		xsw
Version:	1.34.0
Release:	3
License:	GPL-like
Group:		X11/Applications/Games
Source0:	ftp://gd.tuwien.ac.at/games/wolfpack/%{name}-%{version}.tar.bz2
# Source0-md5:	09a3109f8588af9940d71522c713007c
Source1:	%{name}.desktop
Source2:	monitor.desktop
Source3:	unvedit.desktop
Source4:	swserv.init
Source5:	swserv.sysconfig
Patch0:		%{name}-paths.patch
Patch1:		%{name}-fix.patch
URL:		http://wolfpack.twu.net/ShipWars/XShipWars/
BuildRequires:	XFree86-devel
BuildRequires:	esound-devel
BuildRequires:	libjsw-devel
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	yiff-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.

%description -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet.

%package client
Summary:	XShipWars client
Summary(pl):	Klient XShipWars
Group:		X11/Applications/Games
Requires:	xsw-sounds
Requires:	xsw-images
Requires:	xsw-data

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
Group:		X11/Applications/Games
PreReq:		rc-scripts
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/groupmod
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(swserv)
Provides:	user(swserv)

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
Group:		X11/Applications/Games
Requires:	%{name}-client

%description monitor
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet. This
package contains game monitor.

%description monitor -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet. Ten pakiet zawiera monitor gry.

%package unvedit
Summary:	XShipWars universe editor
Summary(pl):	Edytor wszech¶wiata XShipWars
Group:		X11/Applications/Games
Requires:	%{name}-client

%description unvedit
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet. This
package contains universe editor for the game.

%description unvedit -l pl
XShipWars jest wysoko konfigurowalnym systemem gry kosmicznej dla
wielu graczy do grania przez Internet. Ten pakiet zawiera edytor
wszech¶wiata do gry.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# not autoconf-generated configure
./configure.client Linux \
	--prefix=%{_prefix} \
	--CFLAGS="%{rpmcflags}"
%{__make} -f Makefile.client

./configure.server Linux \
	--prefix=%{_prefix} \
	--CFLAGS="%{rpmcflags}"
%{__make} -f Makefile.server

./configure.monitor Linux \
	--prefix=%{_prefix} \
	--CFLAGS="%{rpmcflags}"
%{__make} -f Makefile.monitor

./configure.unvedit Linux \
	--prefix=%{_prefix} \
	--CFLAGS="%{rpmcflags}"
%{__make} -f Makefile.unvedit

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/xshipwars/{images,sounds}
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Games,/etc/sysconfig,/etc/rc.d/init.d}

%{__make} -f Makefile.client install \
	GAMES_DIR=$RPM_BUILD_ROOT%{_bindir} \
	XSW_DIR=$RPM_BUILD_ROOT%{_datadir}/xshipwars \
	XSW_ETC_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/xshipwars

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/xshipwars/universes # comes with data

%{__make} -f Makefile.server install \
	SWSERV_BASE_DIR=$RPM_BUILD_ROOT/home/services/swserv \
	SWSERV_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	SWSERV_ETC_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/swserv

%{__make} -f Makefile.monitor install \
	GAMES_DIR=$RPM_BUILD_ROOT%{_bindir} \
	XSW_DIR=$RPM_BUILD_ROOT%{_datadir}/xshipwars

%{__make} -f Makefile.unvedit install \
	GAMES_BIN=$RPM_BUILD_ROOT%{_bindir} \
	XSW_DATA_DIR=$RPM_BUILD_ROOT%{_datadir}/xshipwars

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE3} $RPM_BUILD_ROOT%{_applnkdir}/Games
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/swserv
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/swserv

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
# trigger would had been better place for this
if [ "$1" = 1 -a "`/usr/bin/getgid swserv`" = "91" ]; then
	/usr/sbin/groupmod -g 96 swserv
fi
%groupadd -P %{name}-server -g 96 -r -f swserv

# trigger would had been better place for this
if [ -n "`/bin/id -u swserv 2>/dev/null`" ] && [ "$1" = 1 -a "`/bin/id -u swserv`" = "91" ]; then
	/usr/sbin/usermod -u 96 swserv 
fi
%useradd -P %{name}-server -M -o -r -u 96 -g swserv -c "XShipWars server" -d /home/services/swserv -s /bin/sh swserv

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
if [ "$1" = "0" ]; then
	if [ -f /var/lock/sybsys/swserv ]; then
		/etc/rc.d/init.d/swserv stop >&2
	fi
	/sbin/chkconfig --del swserv
	rm -f %{_datadir}/swserv/errors
fi

%postun server
if [ "$1" = "0" ]; then
	%userremove swserv
	%groupremove swserv
fi

%files client
%defattr(644,root,root,755)
%doc CREDITS LICENSE README TODO
%dir %{_sysconfdir}/xshipwars
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/xshipwars/*
%attr(755,root,root) %{_bindir}/xsw
%dir %{_datadir}/xshipwars
%{_datadir}/xshipwars/images
%{_datadir}/xshipwars/sounds
%{_applnkdir}/Games/xsw.desktop

%files server
%defattr(644,root,root,755)
%doc CREDITS LICENSE README TODO
%attr(751,root,swserv) %dir /home/services/swserv
%attr(775,root,swserv) /home/services/swserv/db
%attr(775,root,swserv) /home/services/swserv/logs
%attr(775,root,swserv) /home/services/swserv/public_html
%attr(775,root,swserv) /home/services/swserv/tmp
%attr(774,root,swserv) /home/services/swserv/restart
%attr(754,root,swserv) %{_bindir}/swserv
%dir %{_sysconfdir}/swserv
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/swserv/*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/swserv
%attr(754,root,root) /etc/rc.d/init.d/swserv

%files monitor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/monitor
%{_datadir}/xshipwars/images/monitor
%{_applnkdir}/Games/monitor.desktop

%files unvedit
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/unvedit
%{_datadir}/xshipwars/images/unvedit
%{_applnkdir}/Games/unvedit.desktop

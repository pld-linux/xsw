Summary:	XShipWars - Multiplayer space gaming system
Name:		xsw
Version:	1.33h
Release:	1
License:	Modified GPL
Group:		Applications/Games
Group(de):	Applikationen/Spiele
Group(pl):	Aplikacje/Gry
Source0:	ftp://fox.mit.edu/pub/%{name}/%{name}%{version}.tgz
Patch0:		%{name}-paths.patch
URL:		http://wolfpack.tfu.net/ShipWars/XShipWars/
BuildRequires:	XFree86-devel
BuildRequires:	esound-devel
BuildRequires:	yiff-devel
BuildRequires:	libjsw-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xprefix	/usr/X11R6
%define		_xbindir	/usr/X11R6/bin
%define		_xmandir	/usr/X11R6/man
%define		_xdatadir	/usr/X11R6/share

%description 
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.

%package client
Summary:	XShipWars client
Group:		Applications/Games
Requires:	%{name}-sounds
Requires:	%{name}-images
Requires:	%{name}-data

%description client
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.
This package contains game client.

%package server
Summary:	XShipWars server
Group:		Applications/Games

%description server
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.
This package contains game server.

%package monitor
Summary:	XShipWars monitor
Group:		Applications/Games

%description monitor
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.
This package contains game monitor.

%package unvedit
Summary:	XShipWars universe editor
Group:		Applications/Games

%description unvedit
XShipWars is a highly customizable and massivly multiplayer space
gamming system designed for play entirly over the Internet.
This package contains universe editor for the game.

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
install -d $RPM_BUILD_ROOT/%{_xdatadir}/xshipwars/{images,sounds}

%{__make} client_install_unix \
	GAMES_DIR=$RPM_BUILD_ROOT/%{_xbindir} \
	XSW_DIR=$RPM_BUILD_ROOT/%{_xdatadir}/xshipwars \
	XSW_ETC_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/xshipwars

%{__make} server_install_unix \
	SWSERV_BASE_DIR=$RPM_BUILD_ROOT/home/swserv \
	SWSERV_BIN_DIR=$RPM_BUILD_ROOT/%{_bindir}/swserv \
	SWSERV_ETC_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/swserv

%{__make} monitor_install_unix \
	DIR_SWSERV=$RPM_BUILD_ROOT/%{_xprefix} \
	GAMES_DIR=$RPM_BUILD_ROOT/%{_xbindir} \
	PROG_DATA_DIR=$RPM_BUILD_ROOT/%{_xdatadir}/xshipwars

%{__make} unvedit_install_unix \
	GAMES_BIN=$RPM_BUILD_ROOT/%{_xbindir} \
	PROG_DATA_DIR=$RPM_BUILD_ROOT/%{_xdatadir}/xshipwars

%clean
rm -rf $RPM_BUILD_ROOT

%files client
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE* 
%config %verify(not size mtime md5) %{_sysconfdir}/xshipwars/*
%attr(755,root,root) %{_xbindir}/xsw
%{_xdatadir}/xshipwars/images
%{_xdatadir}/xshipwars/sounds

%files server
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE* 
%dir %attr(644,root,swserv) /home/swserv
%attr(664,root,swserv) /home/swserv/db
%attr(664,root,swserv) /home/swserv/logs
%attr(664,root,swserv) /home/swserv/public_html
%attr(664,root,swserv) /home/swserv/tmp
%attr(754,root,swserv) /home/swserv/restart
%attr(754,root,swserv) %{_bindir}/swserv

%files monitor
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE* 
%attr(755,root,root) %{_xbindir}/monitor
%{_xdatadir}/xshipwars/images/monitor

%files unvedit
%defattr(644,root,root,755)
%doc LICENSE* DOCS_NOW_ONLINE* 
%attr(755,root,root) %{_xbindir}/unvedit
%{_xdatadir}/xshipwars/images/unvedit

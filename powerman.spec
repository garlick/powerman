Name: 
Version: 
Release: 
Summary: PowerMan - centralized power control for clusters
License: GPL
Group: Applications/System
Url: http://sourceforge.net/projects/powerman
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: tcp_wrappers, flex, bison, curl-devel

%description
PowerMan is a tool for manipulating remote power control (RPC) devices from a 
central location. Several RPC varieties are supported natively by PowerMan and 
Expect-like configurability simplifies the addition of new devices.

%prep
%setup

%build
make clean
make VERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} sbindir=%{_sbindir} bindir=%{_bindir} initrddir=%{_initrddir} make -e install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/stonith/plugins/external
cp scripts/stonith-powerman $RPM_BUILD_ROOT%{_libdir}/stonith/plugins/external/powerman

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x %{_initrddir}/powerman ]; then
  if %{_initrddir}/powerman status | grep running >/dev/null 2>&1; then
    %{_initrddir}/powerman stop
    WASRUNNING=1
  fi
  [ -x /sbin/chkconfig ] && /sbin/chkconfig --del powerman
  [ -x /sbin/chkconfig ] && /sbin/chkconfig --add powerman
  if test x$WASRUNNING = x1; then
    %{_initrddir}/powerman start
  fi
fi

%preun
if [ "$1" = 0 ]; then
  if [ -x %{_initrddir}/powerman ]; then
    [ -x /sbin/chkconfig ] && /sbin/chkconfig --del powerman
    if %{_initrddir}/powerman status | grep running >/dev/null 2>&1; then
      %{_initrddir}/powerman stop
    fi
  fi
fi

%files
%defattr(-,root,root,-)
%doc ChangeLog 
%doc DISCLAIMER 
%doc COPYING
%doc NEWS
%doc TODO
%doc examples/powerman.conf-mcr
%doc examples/powerman.conf-small
%doc examples/powerman.conf-thunder
%{_bindir}/powerman
%{_bindir}/pm
%{_sbindir}/powermand
%{_sbindir}/httppower
%dir %config %{_sysconfdir}/powerman
%{_sysconfdir}/powerman/*.dev
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_initrddir}/powerman
%{_libdir}/stonith/plugins/external/powerman

%changelog

* Tue Feb 14 2006 Ben Woodard <woodard@redhat.com> 1.0.22-3
- Changed /usr/bin to bindir
- Changed /usr/sbin to sbindir
- Added COPYING to list of docs.
- Changed /etc/rc.d/init.d/ to initrddir
- Changed /usr/man to mandir
- Added a fully qualified path to the source file.
- Fixed buildroot
- Added a patch which should fix a fc4 build problem.

* Thu Feb 09 2006 Ben Woodard <woodard@redhat.com> 1.0.22-2
- changed the buildroot to match fedora guidlines
- changed permissions of spec and src files.
- added changelog to spec file

%define name dnotify 
%define version 0.18.0
%define release 10

Summary: Execute command when directory changes
Name: %{name}
Version: %{version}
Release: %{release}
# Not working anymore ??
# URL: http://oskarsapps.mine.nu/dnotify.html
Source0: http://oskarsapps.mine.nu/src/%{name}-%{version}.tar.bz2
Source1: %{name}.init
Source2: %{name}.sysconfig
Source3: %{name}.d.README
Patch0: dnotify-include-stat_h.patch
License: GPL
Group: File tools
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
Dnotify is a simple program that makes it possible
to execute a command every time the contents of a
specific directory change in Linux. It is run from
the command line and takes two arguments: one or
more directories to monitor and a command to
execute whenever a directory has changed. Options
control what events to trigger on: when a file was
read in the directory, when one was created/deleted,
etc.

%prep
%setup -q
%patch0 -p0 -b .stat_h

%build
%configure
%make

%install
%makeinstall
%{__install} -m755 -d %{buildroot}%{_sysconfdir}/sysconfig/%{name}.d
%{__install} -m755 -d %{buildroot}%{_initrddir}
%{__install} -m700 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -m600 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}.d/README

%find_lang %name

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %name.lang
%{_bindir}/dnotify
%{_mandir}/*/*
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_sysconfdir}/sysconfig/%{name}.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}.d/README
%doc README NEWS AUTHORS COPYING INSTALL

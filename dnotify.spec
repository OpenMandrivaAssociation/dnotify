%define name dnotify 
%define version 0.18.0
%define release %mkrel 4

Summary: Execute command when directory changes
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://oskarsapps.mine.nu/dnotify.html
Source0: http://oskarsapps.mine.nu/src/%{name}-%{version}.tar.bz2
Source1: %{name}.init.bz2
Source2: %{name}.sysconfig.bz2
Source3: %{name}.d.README.bz2
License: GPL
Group: File tools
BuildRoot: %{_tmppath}/%{name}-buildroot
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

%build
%configure
%make

%install
%{__rm} -rf $RPM_BUILD_ROOT

%makeinstall
%{__install} -m755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}.d
%{__install} -m755 -d $RPM_BUILD_ROOT%{_initrddir}
%{__bzip2} -dc %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/%{name}
%{__bzip2} -dc %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%{__bzip2} -dc %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}.d/README
%{__chmod} 700 $RPM_BUILD_ROOT%{_initrddir}/%{name}
%{__chmod} 600 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%{__chmod} 644 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}.d/README

%find_lang %name

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %name.lang
%defattr(-,root,root)
%{_bindir}/dnotify
%{_mandir}/*/*
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_sysconfdir}/sysconfig/%{name}.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}.d/README
%doc README NEWS AUTHORS COPYING INSTALL


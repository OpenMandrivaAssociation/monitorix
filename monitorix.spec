%define name    monitorix
%define version 1.2.0
%define rel     3
%define release %mkrel %{rel}

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary: Monitorix is a free, open source, lightweight system monitoring tool
License: GPLv2
Group: Monitoring
URL: http://www.monitorix.org
Source0: http://www.monitorix.org/%{name}-%{version}.tar.gz
Source1: %{name}.initscript
Requires: rrdtool, xinetd, apache, perl-CGI
Requires: iptables
Requires(post):   rpm-helper
Requires(preun):   rpm-helper
%if %mdkversion < 201010
Requires(postun):   rpm-helper
%endif
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
Monitorix is a free, open source, lightweight system monitoring tool
designed to monitorize as many services as it can. At this time it
monitors from the CPU load and temperatures to the users using the
system. Network devices activity, network services demand and even
the devices' interrupt activity are also monitored. The current
status of any corporate Linux server with Monitorix installed can be
accessed via a web browser.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_sbindir}
install -m 755 monitorix.pl %{buildroot}%{_sbindir}

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 monitorix.conf %{buildroot}%{_sysconfdir}

install -d -m 755 %{buildroot}%{_localstatedir}/lib/monitorix
cp -r reports %{buildroot}%{_localstatedir}/lib/monitorix

install -d -m 755 %{buildroot}%{_localstatedir}/www/monitorix
install -m 644 monitorixico.png envelope.png logo_bot_black.png logo_bot_white.png logo_top.jpg %{buildroot}%{_localstatedir}/www/monitorix
install -m 755 monitorix.cgi %{buildroot}%{_localstatedir}/www/monitorix

# install initscript provided with this package
install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%name

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
Alias /%{name} /var/www/%{name}
<Directory /var/www/%{name}>
	Order allow,deny
	Allow from all
</Location>
EOF

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}
%if %mdkversion < 201010
%_post_webapp
%endif

%preun
%_preun_service %{name}

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root, root)
%doc Changes Configuration.help COPYING monitorix-apache.conf monitorix.spec README
%{_initrddir}/%name
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_sbindir}/%{name}.pl
%{_localstatedir}/www/%{name}
%{_localstatedir}/lib/%{name}

Name:              monitorix
Version:	3.15.0
Release:	1
Summary:           A free, open source, lightweight system monitoring tool
License:           GPLv2+
Group:             Monitoring
URL:               http://www.monitorix.org
Source0:           http://www.monitorix.org/%{name}-%{version}.tar.gz
BuildArch:         noarch
BuildRequires:     perl
BuildRequires:     systemd
Requires:          logrotate
Requires:          perl(CGI)
Requires:          perl(Config::General)
Requires:          perl(DBD::mysql)
Requires:          perl(DBI)
Requires:          perl(HTTP::Server::Simple::CGI)
Requires:          perl(XML::Simple)
Requires:          perl(IO::Socket::SSL)
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
Monitorix is a free, open source, lightweight system monitoring tool designed
to monitor as many services and system resources as possible. It has been
created to be used under production Linux/UNIX servers, but due to its
simplicity and small size may also be used on embedded devices as well.

%prep
%setup -q
sed -i 's|#!/usr/bin/env perl|#!/usr/bin/perl|' %{name}
sed -i 's|#!/usr/bin/env perl|#!/usr/bin/perl|' %{name}.cgi

%build
# Nothing to build.

%install
install -pDm644 docs/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/conf.d
install -pDm644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -pDm755 %{name} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}/usr/lib/%{name}
install -pDm644 lib/*.pm %{buildroot}/usr/lib/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/www
install -pDm644 logo_top.png %{buildroot}%{_localstatedir}/lib/%{name}/www
install -pDm644 logo_bot.png %{buildroot}%{_localstatedir}/lib/%{name}/www
install -pDm644 %{name}ico.png %{buildroot}%{_localstatedir}/lib/%{name}/www
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/www/imgs
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/www/cgi
install -pDm755 %{name}.cgi %{buildroot}%{_localstatedir}/lib/%{name}/www/cgi
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/reports
install -pDm644 reports/*.html %{buildroot}%{_localstatedir}/lib/%{name}/reports
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/usage
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
install -pDm644 man/man5/%{name}.conf.5 %{buildroot}%{_mandir}/man5
install -pDm644 man/man8/%{name}.8 %{buildroot}%{_mandir}/man8
install -pDm644 docs/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pDm644 docs/%{name}.service %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{buildroot}%{_unitdir}/%{name}.service

%preun
%systemd_preun %{buildroot}%{_unitdir}/%{name}.service

%postun
%systemd_postun_with_restart %{buildroot}%{_unitdir}/%{name}.service

%files
%doc Changes COPYING README README.nginx
%doc docs/%{name}-alert.sh docs/%{name}-apache.conf docs/%{name}-lighttpd.conf
%doc docs/htpasswd.pl
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_localstatedir}/lib/%{name}/
%dir %{_localstatedir}/lib/%{name}/www
%dir %{_localstatedir}/lib/%{name}/www/cgi
%dir %{_localstatedir}/lib/%{name}/reports
%{_localstatedir}/lib/%{name}/reports/*.html
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}.8*
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%{_prefix}/lib/%{name}/
%{_localstatedir}/lib/%{name}/www/logo_top.png
%{_localstatedir}/lib/%{name}/www/logo_bot.png
%{_localstatedir}/lib/%{name}/www/%{name}ico.png
%{_localstatedir}/lib/%{name}/www/cgi/%{name}.cgi
%attr(755,apache,apache) %{_localstatedir}//lib/%{name}/www/imgs
%attr(755,root,root) %{_localstatedir}/lib/%{name}/usage
